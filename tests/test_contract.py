"""Independent finite counterexamples for the proposed Hyperemergence frame."""

import dataclasses
import unittest

import hyperemergence
from hyperemergence import (FIELDS_ASKED, FROM_HYPERPHYSICS, NOVELTIES, SENSES,
                            STATEMENTS, Candidate, Stabilization, Target, Verdict,
                            assess, resolve_sense)


class SenseTests(unittest.TestCase):
    def test_hyperemergent_resolves_to_hyperstratums_definition(self):
        sense = resolve_sense("hyperemergent")
        self.assertIn("before it stabilizes", sense.gloss)
        self.assertIn("canonical-definitions.md line 90", sense.source)

    def test_the_field_name_is_a_declared_term_of_the_same_sense(self):
        self.assertIs(resolve_sense("hyperemergence"), resolve_sense("hyperemergent"))
        self.assertIn("hyperemergence", resolve_sense("hyperemergence").terms)

    def test_every_sense_names_its_source_and_terms(self):
        for sense in SENSES:
            self.assertTrue(sense.gloss and sense.source and sense.terms, sense.name)

    def test_plain_emergence_is_not_hyperemergence(self):
        for term in ("emergence", "emergent", "Hyperemergence", "hyper-emergence", ""):
            with self.assertRaises(KeyError, msg=repr(term)):
                resolve_sense(term)

    def test_tylers_statements_are_recorded_open_and_name_no_sense(self):
        self.assertEqual(STATEMENTS, (FIELDS_ASKED, FROM_HYPERPHYSICS, NOVELTIES))
        names = {s.name for s in SENSES}
        for statement in STATEMENTS:
            self.assertEqual(statement.status, "OPEN")
            self.assertTrue(statement.said and statement.source)
            self.assertFalse(names & set(statement.relates))
        self.assertTrue(FROM_HYPERPHYSICS.said.endswith("?"))

    def test_no_closure_flag_confirmation_grounding_or_clock_is_exported(self):
        for forbidden in ("closed", "closure", "is_hyperemergent", "confirm", "certify",
                          "detect", "ground", "grounds", "time", "clock", "index",
                          "duration", "step"):
            self.assertFalse(hasattr(hyperemergence, forbidden), forbidden)


def site(*levels, stabilization=None):
    return Candidate("site", levels, stabilization)


class FrameTests(unittest.TestCase):
    def test_the_targets_are_the_three_the_definition_names(self):
        self.assertEqual({t.value for t in Target}, {"hyperrelation", "graph", "hyperform"})

    def test_a_single_level_candidate_is_refuted(self):
        reading = assess(site("chemistry"))
        self.assertIs(reading.verdict, Verdict.REFUTED)
        self.assertTrue(any("cross-level" in r for r in reading.reasons))

    def test_a_declared_stabilization_refutes(self):
        reading = assess(site("a", "b", stabilization=Stabilization(Target.HYPERFORM, "f")))
        self.assertIs(reading.verdict, Verdict.REFUTED)
        self.assertTrue(any("hyperform 'f'" in r for r in reading.reasons))

    def test_both_refutations_are_reported(self):
        reading = assess(site("a", stabilization=Stabilization(Target.GRAPH, "g")))
        self.assertIs(reading.verdict, Verdict.REFUTED)
        self.assertEqual(len(reading.reasons), 2)

    def test_a_cross_level_unstabilized_candidate_is_unknown_never_confirmed(self):
        reading = assess(site("a", "b", "c"))
        self.assertIs(reading.verdict, Verdict.UNKNOWN)
        for condition in ("coherence", "newness", "stabilization"):
            self.assertTrue(any(r.startswith(condition) for r in reading.reasons), condition)

    def test_there_is_no_confirming_verdict(self):
        self.assertEqual({v.name for v in Verdict}, {"REFUTED", "UNKNOWN"})

    def test_stabilization_requires_a_named_target(self):
        with self.assertRaises(ValueError):
            Stabilization(Target.GRAPH, "")
        with self.assertRaises(ValueError):
            Stabilization("hyperobject", "o")
        with self.assertRaises(ValueError):
            Stabilization(Target.HYPERRELATION, 3)

    def test_levels_are_names_never_numbers(self):
        for bad in ((1, 2), (True, "a"), ("a", 2.0), ("",)):
            with self.assertRaises(ValueError, msg=repr(bad)):
                Candidate("site", bad)

    def test_malformed_candidates_are_refused(self):
        with self.assertRaises(ValueError):
            Candidate("site", ("a", "a"))
        with self.assertRaises(ValueError):
            Candidate("", ("a", "b"))
        with self.assertRaises(ValueError):
            Candidate("site", ["a", "b"])
        with self.assertRaises(ValueError):
            Candidate("site", ())
        with self.assertRaises(ValueError):
            Candidate("site", ("a", "b"), Target.GRAPH)
        with self.assertRaises(TypeError):
            assess(("a", "b"))

    def test_a_candidate_has_no_closure_flag(self):
        self.assertEqual([f.name for f in dataclasses.fields(Candidate)],
                         ["name", "levels", "stabilization"])

    def test_the_frame_is_finite(self):
        with self.assertRaises(ValueError):
            Candidate("site", tuple(f"l{i}" for i in range(65)))


if __name__ == "__main__":
    unittest.main()
