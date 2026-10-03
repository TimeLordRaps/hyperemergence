"""The off-branch abstraction spelling survives without becoming an L1 grade."""

from dataclasses import replace
import json
from pathlib import Path as FilePath
import subprocess
import sys
import tempfile
import unittest

from coherence import (Arc, CheckStatus, CoherenceStatus, Criterion, Node,
                       Obligation, Path, Presentation, StructureMap, TraceLevel,
                       check, compose, map_report, realize, relabel,
                       presentation_digest, stabilize, transport,
                       verify_stabilization)
from coherence_cli import load_case
from hyperemergence import Stabilization, Target


class FiltrationTagTests(unittest.TestCase):
    root = FilePath(__file__).resolve().parents[1]

    def abstraction_case(self):
        return load_case(self.root / "examples" / "abstraction-path.json")

    def test_all_four_spellings_are_retained_independently(self):
        self.assertEqual({tag.value for tag in TraceLevel}, {"~~", "=~", "~=", "=="})
        self.assertIsNot(TraceLevel("~="), TraceLevel("=~"))

    def test_actual_abstraction_path_is_coherent_and_roundtrips_with_its_witness(self):
        graph, obligations = self.abstraction_case()
        report = check(graph, obligations)
        self.assertEqual(report.status, CoherenceStatus.COHERENT)
        self.assertEqual(report.checks[0].status, CheckStatus.SATISFIED)
        self.assertEqual(report.native_hyperemergence, "UNKNOWN")
        path = compose(graph, Path("seed", ("abstract",)), Path("schema", ("compose",)))
        witness = realize(graph, path)
        target, mapping = relabel(graph, {"seed": "start", "schema": "middle", "claim": "finish"},
                                  {"abstract": "renamed-abstract", "compose": "renamed-compose"})
        image = transport(graph, target, mapping, path)
        self.assertEqual(tuple(tag.value for tag in image.image.traces), ("~=", "~="))
        inverse = StructureMap(tuple((v, k) for k, v in mapping.node_images),
                               tuple((v[0], (k,)) for k, v in mapping.arc_images))
        recovered = transport(target, graph, inverse, image.image.path)
        self.assertEqual(recovered.image, witness)
        self.assertFalse(image.path_information_lost)
        self.assertFalse(recovered.path_information_lost)

    def test_abstraction_annotation_has_no_l1_floor(self):
        graph, obligations = self.abstraction_case()
        witness = realize(graph, obligations[0].left)
        self.assertIsNone(witness.trace_floor)
        self.assertEqual(witness.trace_floor_status, "OFF_BRANCH_UNKNOWN")

    def test_mixed_path_does_not_insert_abstraction_into_a_linear_rank(self):
        graph, obligations = self.abstraction_case()
        for tag in (TraceLevel.OVERLAP, TraceLevel.OUTCOME, TraceLevel.SIMULATION):
            mixed = replace(graph, arcs=(graph.arcs[0], replace(graph.arcs[1], trace=tag)))
            witness = realize(mixed, obligations[0].left)
            self.assertIsNone(witness.trace_floor)
            self.assertEqual(witness.trace_floor_status, "OFF_BRANCH_UNKNOWN")
            self.assertEqual(witness.traces, (TraceLevel("~="), tag))

    def test_l1_floor_and_empty_path_semantics_are_preserved(self):
        graph, obligations = self.abstraction_case()
        for a, b, expected in (("==", "=~", "=~"), ("=~", "~~", "~~"), ("==", "==", "==")):
            ordinary = replace(graph, arcs=(replace(graph.arcs[0], trace=TraceLevel(a)),
                                           replace(graph.arcs[1], trace=TraceLevel(b))))
            witness = realize(ordinary, obligations[0].left)
            self.assertEqual(witness.trace_floor.value, expected)
            self.assertEqual(witness.trace_floor_status, "L1_DECLARED_FLOOR")
        empty = realize(graph, Path("seed", ()))
        self.assertIsNone(empty.trace_floor)
        self.assertEqual(empty.trace_floor_status, "EMPTY")

    def test_transport_reports_off_branch_comparison_without_weaker_grade(self):
        graph, obligations = self.abstraction_case()
        ordinary = replace(graph, arcs=tuple(replace(a, trace=TraceLevel.OUTCOME) for a in graph.arcs))
        mapping = StructureMap(tuple((n.name, n.name) for n in graph.nodes),
                               tuple((a.name, (a.name,)) for a in graph.arcs))
        report = map_report(graph, ordinary, mapping)
        self.assertEqual(report.trace_weakenings, ())
        self.assertEqual(report.trace_incomparabilities, ("abstract", "compose"))
        self.assertTrue(transport(graph, ordinary, mapping, obligations[0].left).path_information_lost)
        retained = map_report(graph, graph, mapping)
        self.assertEqual(retained.trace_weakenings, ())
        self.assertEqual(retained.trace_incomparabilities, ("abstract", "compose"))

    def test_abstraction_and_outcome_tags_are_not_normalized_in_bindings(self):
        graph, obligations = self.abstraction_case()
        receipt = stabilize(graph, obligations, Stabilization(Target.GRAPH, "schema-v1"))
        changed = replace(graph, arcs=tuple(replace(a, trace=TraceLevel.OUTCOME) for a in graph.arcs))
        self.assertNotEqual(presentation_digest(graph), presentation_digest(changed))
        self.assertFalse(verify_stabilization(changed, obligations, receipt))
        self.assertEqual(receipt.native_hyperemergence, "UNKNOWN")

    def test_cli_retains_abstraction_in_full_path_evidence(self):
        result = subprocess.run([sys.executable, "-B", "-m", "hyperemergence", "check",
                                 "examples/abstraction-path.json"], cwd=self.root, text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["checks"][0]["left"]["traces"], ["~=", "~="])
        self.assertIsNone(data["checks"][0]["left"]["trace_floor"])
        self.assertEqual(data["checks"][0]["left"]["trace_floor_status"], "OFF_BRANCH_UNKNOWN")
        self.assertEqual(data["native_hyperemergence"], "UNKNOWN")

    def test_duplicate_trace_member_cannot_silently_erase_abstraction(self):
        original = (self.root / "examples" / "abstraction-path.json").read_text()
        ambiguous = original.replace('"trace": "~="', '"trace": "~=", "trace": "=~"', 1)
        self.assertNotEqual(ambiguous, original)
        with tempfile.TemporaryDirectory(prefix=".trace-input-", dir=self.root) as directory:
            case = FilePath(directory) / "duplicate-trace.json"
            case.write_text(ambiguous, encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-m", "hyperemergence", "check", str(case)],
                                    cwd=self.root, text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("duplicate JSON key: trace", result.stderr)


if __name__ == "__main__":
    unittest.main()
