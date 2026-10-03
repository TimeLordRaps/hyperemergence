"""Hyperemergence: sourced declarations and a witnessed finite coherence laboratory.

This module does not detect hyperemergence. It records Hyperstratum's definition with its
source, keeps Tyler's statements open, and reads a declared candidate against the two
conditions the definition makes checkable: the coherence is cross-level, and it has not
stabilized into a named hyperrelation, graph, or hyperform. The definition gives no
criterion that establishes coherence or newness, so a candidate can be refuted, never
confirmed. The companion coherence module constructs and checks finite paths,
transport and stabilization handoffs without promoting them to native instances.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

HYPERSTRATUM = "hyperstratum c4ffe2c7ff42c747d74ef5236d3bef631dd5f08e"
MAX_LEVELS = 64


@dataclass(frozen=True)
class Sense:
    name: str
    terms: tuple[str, ...]
    gloss: str
    source: str


SENSES = (
    Sense("pre-stabilization-coherence",
          ("hyperemergent", "hyperemergence"),
          "newly emerging cross-level coherence before it stabilizes into a named "
          "hyperrelation, graph, or hyperform",
          f"{HYPERSTRATUM} specs/canonical-definitions.md line 90"),
)


def resolve_sense(term: str) -> Sense:
    """The declared sense of a term; KeyError for anything not declared verbatim.

    Each sense lists its exact terms. There is no alias table: "emergence" is not
    "hyperemergence".
    """
    for sense in SENSES:
        if term in sense.terms:
            return sense
    raise KeyError(term)


@dataclass(frozen=True)
class Statement:
    said: str
    source: str
    relates: tuple[str, ...]
    status: str


FIELDS_ASKED = Statement(
    said=("So for hyperemergence what are we doing with hyperstructure, hyperdynamics, "
          "hypergrammar, hypermath and hyperlogic, o yeah check hyperchemistry against "
          "hypermath and definitely hyperlogic."),
    source="Tyler Roost, 2026-09-27, USER-STATED in a working session",
    relates=("hyperemergence", "hyperstructure", "hyperdynamics", "hypergrammar",
             "hypermath", "hyperlogic", "hyperchemistry"),
    status="OPEN",
)

FROM_HYPERPHYSICS = Statement(
    said=("So Hyperchemistry cannot be defined as a hyperemergence from hyperphysics? "
          "Not yet at least?"),
    source="Tyler Roost, 2026-09-27, USER-STATED in a working session",
    relates=("hyperchemistry", "hyperemergence", "hyperphysics"),
    status="OPEN",
)

NOVELTIES = Statement(
    said=("I believe the realities loop and close themselves, with the hypergeometric "
          "reality, abstract reality, possibility reality, surreal reality, and base reality "
          "we can then say that consciousness links the realities, from hyperethics we then "
          "can show that consciousness emerges novelties from hyperobjects, which are "
          "instantiations of hyperforms, which need to be formed from forms."),
    source="Tyler Roost, 2026-09-27, USER-STATED in a working session",
    relates=("realities", "consciousness", "hyperethics", "novelties", "hyperobjects",
             "hyperforms", "forms"),
    status="OPEN",
)

STATEMENTS = (FIELDS_ASKED, FROM_HYPERPHYSICS, NOVELTIES)


class Target(Enum):
    """The three things the definition names a hyperemergent stabilizing into."""

    HYPERRELATION = "hyperrelation"
    GRAPH = "graph"
    HYPERFORM = "hyperform"


def _is_name(x: object) -> bool:
    return isinstance(x, str) and bool(x)


@dataclass(frozen=True)
class Stabilization:
    """Declares that a coherence has stabilized into a named target."""

    into: Target
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.into, Target):
            raise ValueError("stabilization is into a hyperrelation, graph, or hyperform")
        if not _is_name(self.name):
            raise ValueError("stabilization is into a named target")


@dataclass(frozen=True)
class Candidate:
    """A declared site of coherence across named levels. Declaring it establishes nothing."""

    name: str
    levels: tuple[str, ...]
    stabilization: Stabilization | None = None

    def __post_init__(self) -> None:
        if not _is_name(self.name):
            raise ValueError("a candidate is a non-empty name")
        if not isinstance(self.levels, tuple) or not 1 <= len(self.levels) <= MAX_LEVELS:
            raise ValueError(f"finite candidate requires 1-{MAX_LEVELS} levels")
        if not all(_is_name(level) for level in self.levels):
            raise ValueError("levels are non-empty names, never numbers")
        if len(set(self.levels)) != len(self.levels):
            raise ValueError("duplicate level")
        if self.stabilization is not None and not isinstance(self.stabilization, Stabilization):
            raise ValueError("invalid stabilization declaration")


class Verdict(Enum):
    REFUTED = "REFUTED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Reading:
    verdict: Verdict
    reasons: tuple[str, ...]


UNESTABLISHED = (
    "coherence: the definition states no criterion that establishes it",
    "newness: the definition states no criterion that establishes it",
    "stabilization: none declared, which is not evidence that none occurred",
)


def assess(candidate: Candidate) -> Reading:
    """REFUTED when a declaration contradicts the definition; otherwise UNKNOWN, never confirmed."""
    if not isinstance(candidate, Candidate):
        raise TypeError("assess reads a declared Candidate")
    reasons = []
    if len(candidate.levels) < 2:
        reasons.append("single level: the definition requires cross-level coherence")
    if candidate.stabilization is not None:
        s = candidate.stabilization
        reasons.append(f"stabilized into the {s.into.value} {s.name!r}: "
                       "the definition reads before it stabilizes")
    if reasons:
        return Reading(Verdict.REFUTED, tuple(reasons))
    return Reading(Verdict.UNKNOWN, UNESTABLISHED)


from coherence import (Arc, CheckStatus, CoherenceStatus, Criterion, Development,
                       Handoff, MapReport, MissingEvidence, Node, Obligation, Path,
                       Presentation, StructureMap, TraceLevel, Transport, Witness,
                       check, compare_development, compose, continuation_profile,
                       map_report, presentation_digest, realize, relabel, stabilize,
                       transport, verify_stabilization)


if __name__ == "__main__":
    from coherence_cli import main
    raise SystemExit(main())
