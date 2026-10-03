"""Finite counterexamples, independent path enumeration, and transport laws."""

from dataclasses import replace
import itertools
import json
from pathlib import Path as FilePath
import random
import subprocess
import sys
import unittest

from coherence import (Arc, CheckStatus, CoherenceStatus, Criterion, MissingEvidence,
                       Node, Obligation, Path, Presentation, StructureMap, TraceLevel,
                       check, compare_development, compose, continuation_profile,
                       map_report, presentation_digest, realize, relabel, stabilize,
                       transport, verify_stabilization)
from hyperemergence import Candidate, Stabilization, Target, Verdict, assess


def diamond():
    return Presentation(
        "two explanations", ("base", "meta", "whole"),
        (Node("seed", "base"), Node("left", "meta"), Node("right", "meta"),
         Node("joined", "whole")),
        (Arc("a", "seed", "left", "open-left"),
         Arc("b", "left", "joined", "join-left"),
         Arc("c", "seed", "right", "open-right"),
         Arc("d", "right", "joined", "join-right")))


LEFT = Path("seed", ("a", "b"))
RIGHT = Path("seed", ("c", "d"))
ENDPOINT = Obligation("joined outcome", LEFT, RIGHT, Criterion.ENDPOINT)
EXACT = Obligation("reproduced explanation", LEFT, RIGHT, Criterion.PATH)


class WitnessTests(unittest.TestCase):
    def test_composition_retains_intermediate_nodes_and_labels(self):
        graph = diamond()
        joined = compose(graph, Path("seed", ("a",)), Path("left", ("b",)))
        self.assertEqual(joined, LEFT)
        witness = realize(graph, joined)
        self.assertEqual(witness.nodes, ("seed", "left", "joined"))
        self.assertEqual(witness.roles, ("open-left", "join-left"))
        self.assertEqual(witness.levels, ("base", "meta", "whole"))

    def test_identity_and_associativity_are_path_preserving(self):
        graph = diamond()
        p, q = Path("seed", ("a",)), Path("left", ("b",))
        identity = Path("joined", ())
        self.assertEqual(compose(graph, compose(graph, p, q), identity),
                         compose(graph, p, compose(graph, q, identity)))
        self.assertEqual(compose(graph, Path("seed", ()), LEFT), LEFT)

    def test_two_paths_share_an_outcome_without_sharing_a_path(self):
        report = check(diamond(), (ENDPOINT, EXACT))
        self.assertEqual(report.status, CoherenceStatus.PARTIAL)
        self.assertEqual(tuple(item.status for item in report.checks),
                         (CheckStatus.SATISFIED, CheckStatus.OBSTRUCTED))
        self.assertEqual(report.checks[1].left.nodes, ("seed", "left", "joined"))
        self.assertEqual(report.checks[1].right.nodes, ("seed", "right", "joined"))

    def test_distinct_paths_can_preserve_the_same_role_level_trace_observations(self):
        graph = diamond()
        roles = ("open", "join", "open", "join")
        graph = replace(graph, arcs=tuple(replace(a, role=role) for a, role in zip(graph.arcs, roles)))
        observation = replace(ENDPOINT, criterion=Criterion.OBSERVATION)
        report = check(graph, (observation, EXACT))
        self.assertEqual(report.checks[0].status, CheckStatus.SATISFIED)
        self.assertEqual(report.checks[1].status, CheckStatus.OBSTRUCTED)

    def test_same_observation_claim_fails_on_role_or_trace_mutation(self):
        graph = diamond()
        observation = replace(ENDPOINT, criterion=Criterion.OBSERVATION)
        self.assertEqual(check(graph, (observation,)).status, CoherenceStatus.OBSTRUCTED)
        graph = replace(graph, arcs=tuple(replace(a, role="common") for a in graph.arcs))
        changed = replace(graph, arcs=(replace(graph.arcs[0], trace=TraceLevel.SIMULATION),) + graph.arcs[1:])
        self.assertEqual(check(graph, (observation,)).status, CoherenceStatus.COHERENT)
        self.assertEqual(check(changed, (observation,)).status, CoherenceStatus.OBSTRUCTED)

    def test_composition_rejects_unmatched_boundary(self):
        with self.assertRaisesRegex(ValueError, "boundary"):
            compose(diamond(), Path("seed", ("a",)), Path("right", ("d",)))

    def test_missing_arc_is_missing_evidence_not_a_confirmed_path(self):
        graph = replace(diamond(), arcs=diamond().arcs[:-1])
        self.assertEqual(check(graph, (ENDPOINT,)).checks[0].status, CheckStatus.UNKNOWN)
        self.assertEqual(check(graph, (ENDPOINT,)).status, CoherenceStatus.UNDETERMINED)
        with self.assertRaises(MissingEvidence):
            realize(graph, RIGHT)

    def test_discontinuous_declared_path_supplies_an_obstruction(self):
        obligation = replace(ENDPOINT, left=Path("seed", ("a", "d")))
        report = check(diamond(), (obligation,))
        self.assertEqual(report.status, CoherenceStatus.OBSTRUCTED)
        self.assertIn("discontinuous", report.checks[0].reason)

    def test_level_labels_do_not_make_same_level_paths_cross_level(self):
        graph = replace(diamond(), nodes=tuple(Node(n.name, "base") for n in diamond().nodes))
        report = check(graph, (ENDPOINT,))
        self.assertEqual(report.status, CoherenceStatus.OBSTRUCTED)
        self.assertIn("cross-level", report.checks[0].reason)

    def test_unused_declared_levels_do_not_supply_a_cross_level_witness(self):
        graph = Presentation("unused level", ("base", "meta"),
                             (Node("x", "base"),), (Arc("loop", "x", "x", "repeat"),))
        path = Path("x", ("loop",))
        self.assertEqual(check(graph, (Obligation("loop", path, path),)).status,
                         CoherenceStatus.OBSTRUCTED)

    def test_empty_obligation_set_does_not_pass_vacuously(self):
        self.assertEqual(check(diamond(), ()).status, CoherenceStatus.UNDETERMINED)

    def test_distinct_origins_do_not_pass_on_a_shared_destination(self):
        obligation = Obligation("different origins", Path("left", ("b",)),
                                Path("right", ("d",)))
        self.assertEqual(check(diamond(), (obligation,)).status, CoherenceStatus.OBSTRUCTED)

    def test_trace_strength_is_explicit_and_never_native_evidence(self):
        graph = diamond()
        arcs = (replace(graph.arcs[0], trace=TraceLevel.SIMULATION),) + graph.arcs[1:]
        witness = realize(replace(graph, arcs=arcs), LEFT)
        self.assertEqual(witness.trace_floor, TraceLevel.OVERLAP)
        self.assertEqual(assess(Candidate("tested site", ("base", "meta"))).verdict,
                         Verdict.UNKNOWN)

    def test_inputs_reject_duplicate_ids_dangling_edges_and_wrong_types(self):
        graph = diamond()
        for kwargs in ({"nodes": graph.nodes + (graph.nodes[0],)},
                       {"arcs": graph.arcs + (graph.arcs[0],)},
                       {"nodes": (Node("x", "undeclared"),)},
                       {"arcs": (Arc("x", "missing", "joined", "fake"),)},
                       {"levels": ["base", "meta"]}):
            with self.assertRaises((ValueError, TypeError), msg=repr(kwargs)):
                replace(graph, **kwargs)
        with self.assertRaises(ValueError):
            Arc("x", "seed", "joined", "fake", "==")


class ProjectionTests(unittest.TestCase):
    def coarse(self):
        target = Presentation("coarse", ("base", "whole"),
                              (Node("origin", "base"), Node("result", "whole")),
                              (Arc("joined", "origin", "result", "summary"),))
        mapping = StructureMap(
            (("seed", "origin"), ("left", "origin"), ("right", "origin"),
             ("joined", "result")),
            (("a", ()), ("b", ("joined",)), ("c", ()), ("d", ("joined",))))
        return target, mapping

    def test_projection_preserves_outcome_and_loses_two_explanations(self):
        graph = diamond()
        target, mapping = self.coarse()
        left = transport(graph, target, mapping, LEFT)
        right = transport(graph, target, mapping, RIGHT)
        self.assertEqual(left.image, right.image)
        self.assertNotEqual(left.source, right.source)
        self.assertEqual(left.source.nodes, ("seed", "left", "joined"))
        self.assertEqual(left.image.nodes, ("origin", "result"))
        self.assertTrue(left.path_information_lost)
        self.assertTrue(map_report(graph, target, mapping).contracted_arcs)

    def test_projection_image_cannot_be_silently_reversed(self):
        target, mapping = self.coarse()
        report = map_report(diamond(), target, mapping)
        self.assertEqual(report.node_collisions,
                         (("origin", ("left", "right", "seed")),))
        self.assertFalse(report.injective)

    def test_endpoint_preserving_map_must_actually_realize_its_edge_images(self):
        target, mapping = self.coarse()
        broken = replace(mapping, arc_images=(("a", ("joined",)),) + mapping.arc_images[1:])
        with self.assertRaisesRegex(ValueError, "mapped boundary"):
            transport(diamond(), target, broken, LEFT)

    def test_missing_or_extra_map_assignments_are_rejected(self):
        target, mapping = self.coarse()
        for broken in (replace(mapping, node_images=mapping.node_images[:-1]),
                       replace(mapping, arc_images=mapping.arc_images + (("extra", ()),))):
            with self.assertRaises(ValueError):
                map_report(diamond(), target, broken)

    def test_pure_bijective_renaming_preserves_obstructions_and_witnesses(self):
        graph = diamond()
        nodes = {name: "node-" + name for name in (n.name for n in graph.nodes)}
        arcs = {arc.name: "arc-" + arc.name for arc in graph.arcs}
        target, mapping = relabel(graph, nodes, arcs)
        projected = tuple(Obligation(item.name,
                                    Path(nodes[item.left.start], tuple(arcs[e] for e in item.left.arcs)),
                                    Path(nodes[item.right.start], tuple(arcs[e] for e in item.right.arcs)),
                                    item.criterion) for item in (ENDPOINT, EXACT))
        self.assertEqual(check(graph, (ENDPOINT, EXACT)).status, check(target, projected).status)
        self.assertFalse(transport(graph, target, mapping, LEFT).path_information_lost)
        self.assertTrue(map_report(graph, target, mapping).injective)

    def test_role_and_trace_changes_are_reported_even_with_bijective_ids(self):
        graph = diamond()
        changed = replace(graph, arcs=(replace(graph.arcs[0], role="different",
                                              trace=TraceLevel.SIMULATION),) + graph.arcs[1:])
        mapping = StructureMap(tuple((n.name, n.name) for n in graph.nodes),
                               tuple((a.name, (a.name,)) for a in graph.arcs))
        report = map_report(changed, graph, mapping)
        self.assertEqual(report.role_changes, ("a",))
        self.assertEqual(report.trace_weakenings, ("a",))
        self.assertTrue(transport(changed, graph, mapping, LEFT).path_information_lost)


class DevelopmentTests(unittest.TestCase):
    def test_new_coherence_is_measured_against_an_explicit_baseline(self):
        after = diamond()
        before = replace(after, arcs=after.arcs[:-1])
        report = compare_development(before, after, (ENDPOINT, EXACT))
        self.assertEqual(report.newly_witnessed, ("joined outcome",))
        self.assertEqual(report.correspondence_status, "FIXED_TYPED_CONTEXT")
        self.assertEqual(report.after.status, CoherenceStatus.PARTIAL)
        self.assertEqual(report.native_hyperemergence, "UNKNOWN")

    def test_relabelling_alone_creates_no_new_coherence(self):
        graph = diamond()
        self.assertEqual(compare_development(graph, graph, (ENDPOINT,)).newly_witnessed, ())

    def test_actual_renaming_requires_source_correspondence_before_newness(self):
        before = Presentation("one route", ("base", "whole"),
                              (Node("a", "base"), Node("b", "whole")),
                              (Arc("move", "a", "b", "advance"),))
        after, mapping = relabel(before, {"a": "renamed-a", "b": "renamed-b"},
                                {"move": "renamed-move"})
        path = Path("renamed-a", ("renamed-move",))
        obligation = Obligation("same continuation", path, path)
        report = compare_development(before, after, (obligation,))
        self.assertEqual(report.newly_witnessed, ())
        self.assertEqual(report.correspondence_status, "UNKNOWN_CONTEXT")
        self.assertEqual(report.native_hyperemergence, "UNKNOWN")
        self.assertFalse(transport(before, after, mapping, Path("a", ("move",))).path_information_lost)

    def test_shared_identifier_with_changed_role_is_context_drift(self):
        before = diamond()
        after = replace(before, arcs=(replace(before.arcs[0], role="other-role"),) + before.arcs[1:])
        report = compare_development(before, after, (ENDPOINT,))
        self.assertEqual(report.correspondence_status, "UNKNOWN_CONTEXT")
        self.assertEqual(report.newly_witnessed, ())

    def test_stabilization_handoff_binds_source_obligations_and_named_target(self):
        graph = diamond()
        target = Stabilization(Target.GRAPH, "explanations-v1")
        receipt = stabilize(graph, (ENDPOINT,), target)
        self.assertEqual(receipt.target, target)
        self.assertEqual(receipt.native_hyperemergence, "UNKNOWN")
        self.assertTrue(verify_stabilization(graph, (ENDPOINT,), receipt))
        self.assertEqual(assess(Candidate("site", graph.levels, target)).verdict, Verdict.REFUTED)

    def test_partial_coherence_cannot_be_stabilized_as_complete(self):
        with self.assertRaisesRegex(ValueError, "COHERENT"):
            stabilize(diamond(), (ENDPOINT, EXACT), Stabilization(Target.HYPERFORM, "all"))

    def test_invalidating_mutations_cannot_reuse_a_stabilization_receipt(self):
        graph = diamond()
        receipt = stabilize(graph, (ENDPOINT,), Stabilization(Target.HYPERRELATION, "r"))
        for changed in (replace(graph, arcs=graph.arcs[:-1]),
                        replace(graph, arcs=(replace(graph.arcs[0], role="new-role"),) + graph.arcs[1:]),
                        replace(graph, nodes=(replace(graph.nodes[0], level="meta"),) + graph.nodes[1:])):
            self.assertFalse(verify_stabilization(changed, (ENDPOINT,), receipt))
        self.assertFalse(verify_stabilization(graph, (EXACT,), receipt))

    def test_descriptor_order_changes_do_not_invalidate_semantic_digest(self):
        graph = diamond()
        reordered = replace(graph, nodes=graph.nodes[::-1], arcs=graph.arcs[::-1])
        self.assertEqual(presentation_digest(graph), presentation_digest(reordered))

    def test_stabilization_receipt_tampering_is_rejected(self):
        graph = diamond()
        receipt = stabilize(graph, (ENDPOINT,), Stabilization(Target.GRAPH, "g"))
        self.assertFalse(verify_stabilization(graph, (ENDPOINT,), replace(receipt, digest="0" * 64)))


class ContinuationTests(unittest.TestCase):
    def test_horizon_contains_all_walks_but_never_claims_unbounded_closure(self):
        profile = continuation_profile(diamond(), "seed", 2)
        self.assertEqual(set(profile.endpoints), {"left", "right", "joined"})
        self.assertEqual({p.arcs for p in profile.paths}, {("a",), ("c",), ("a", "b"), ("c", "d")})
        self.assertTrue(profile.complete_within_horizon)
        self.assertEqual(profile.horizon, 2)

    def test_cycles_are_finite_walks_with_an_explicit_horizon(self):
        graph = Presentation("cycle", ("base",), (Node("x", "base"),),
                             (Arc("again", "x", "x", "repeat"),))
        profile = continuation_profile(graph, "x", 3)
        self.assertEqual(tuple(len(p.arcs) for p in profile.paths), (1, 2, 3))
        self.assertTrue(profile.complete_within_horizon)

    def test_resource_stop_reports_incomplete_evidence(self):
        profile = continuation_profile(diamond(), "seed", 2, max_paths=2)
        self.assertFalse(profile.complete_within_horizon)
        self.assertEqual(profile.stop_reason, "path budget reached")

    def test_bad_horizons_and_budgets_are_refused(self):
        for bad in (True, -1, 65, 1.5):
            with self.assertRaises(ValueError):
                continuation_profile(diamond(), "seed", bad)
        with self.assertRaises(ValueError):
            continuation_profile(diamond(), "seed", 2, max_paths=0)

    def test_enumerator_agrees_with_independent_edge_product_oracle(self):
        rng = random.Random(73)
        for sample in range(20):
            node_names = ("n0", "n1", "n2")
            arcs = tuple(Arc(f"e{i}", x, y, "relation")
                         for i, (x, y) in enumerate(itertools.product(node_names, repeat=2))
                         if rng.randrange(3) == 0)
            graph = Presentation(f"sample{sample}", ("base",),
                                 tuple(Node(n, "base") for n in node_names), arcs)
            expected = set()
            for length in range(1, 4):
                for sequence in itertools.product(arcs, repeat=length):
                    if sequence[0].source == "n0" and all(
                            x.target == y.source for x, y in zip(sequence, sequence[1:])):
                        expected.add(tuple(e.name for e in sequence))
            observed = continuation_profile(graph, "n0", 3)
            self.assertEqual({p.arcs for p in observed.paths}, expected)
            self.assertTrue(observed.complete_within_horizon)


class CommandTests(unittest.TestCase):
    root = FilePath(__file__).resolve().parents[1]

    def invoke(self, *args):
        return subprocess.run([sys.executable, "-B", "-m", "hyperemergence", *args],
                              cwd=self.root, capture_output=True, text=True, timeout=5)

    def test_demo_computes_partial_projection_handoff_and_mutation_cases(self):
        result = self.invoke("demo")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["partial_coherence"], "PARTIAL")
        self.assertTrue(data["projection"]["two_paths_collapse"])
        self.assertFalse(data["mutation_reuses_handoff"])
        self.assertEqual(data["native_hyperemergence"], "UNKNOWN")

    def test_input_file_drives_actual_checks_and_exit_status(self):
        good = self.invoke("check", "examples/coherent.json")
        bad = self.invoke("check", "examples/partial.json")
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertEqual(json.loads(good.stdout)["status"], "COHERENT")
        self.assertEqual(json.loads(bad.stdout)["status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
