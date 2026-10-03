"""[FRAME] Witnessed finite cross-level coherence, transport, and development.

Every result is relative to supplied presentations and listed obligations. Trace
tags preserve a distinction borrowed from Hypermath, but are not proof of native
~~, =~, or ==. No result confirms that an instance is a native hyperemergent.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json

MAX_NODES = 256
MAX_ARCS = 1024
MAX_PATH_LENGTH = 64
MAX_OBLIGATIONS = 1024
MAX_WALKS = 100_000


def _name(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _tuple(value: object, kind: type, limit: int, label: str) -> None:
    if not isinstance(value, tuple) or len(value) > limit:
        raise ValueError(f"{label} must be a tuple with at most {limit} entries")
    if not all(isinstance(item, kind) for item in value):
        raise TypeError(f"invalid {label} entry")


class TraceLevel(Enum):
    OVERLAP = "~~"
    OUTCOME = "=~"
    SIMULATION = "=="


_STRENGTH = {TraceLevel.OVERLAP: 0, TraceLevel.OUTCOME: 1, TraceLevel.SIMULATION: 2}


@dataclass(frozen=True)
class Node:
    name: str
    level: str

    def __post_init__(self):
        if not _name(self.name) or not _name(self.level):
            raise ValueError("node and level require nonempty names")


@dataclass(frozen=True)
class Arc:
    name: str
    source: str
    target: str
    role: str
    trace: TraceLevel = TraceLevel.OVERLAP

    def __post_init__(self):
        if not all(_name(value) for value in (self.name, self.source, self.target, self.role)):
            raise ValueError("arc identifiers, endpoints, and role require names")
        if not isinstance(self.trace, TraceLevel):
            raise ValueError("trace is an explicit TraceLevel tag, not native evidence")


@dataclass(frozen=True)
class Presentation:
    name: str
    levels: tuple[str, ...]
    nodes: tuple[Node, ...]
    arcs: tuple[Arc, ...]

    def __post_init__(self):
        if not _name(self.name):
            raise ValueError("presentation requires a name")
        _tuple(self.levels, str, 64, "levels")
        _tuple(self.nodes, Node, MAX_NODES, "nodes")
        _tuple(self.arcs, Arc, MAX_ARCS, "arcs")
        if not self.levels or not self.nodes or not all(_name(x) for x in self.levels):
            raise ValueError("presentation requires named levels and nodes")
        for items in (self.levels, tuple(n.name for n in self.nodes), tuple(a.name for a in self.arcs)):
            if len(items) != len(set(items)):
                raise ValueError("duplicate identifier")
        if any(node.level not in self.levels for node in self.nodes):
            raise ValueError("node level is undeclared")
        names = {node.name for node in self.nodes}
        if any(arc.source not in names or arc.target not in names for arc in self.arcs):
            raise ValueError("dangling arc endpoint")


@dataclass(frozen=True)
class Path:
    start: str
    arcs: tuple[str, ...]

    def __post_init__(self):
        if not _name(self.start):
            raise ValueError("path requires a named starting point")
        _tuple(self.arcs, str, MAX_PATH_LENGTH, "path arcs")
        if not all(_name(arc) for arc in self.arcs):
            raise ValueError("path arc identifiers require names")


class MissingEvidence(ValueError):
    """A declared path requires a node or arc absent from this presentation."""


@dataclass(frozen=True)
class Witness:
    path: Path
    nodes: tuple[str, ...]
    levels: tuple[str, ...]
    roles: tuple[str, ...]
    traces: tuple[TraceLevel, ...]

    @property
    def trace_floor(self) -> TraceLevel | None:
        return min(self.traces, key=_STRENGTH.get) if self.traces else None

    @property
    def endpoint(self) -> str:
        return self.nodes[-1]


def realize(presentation: Presentation, path: Path) -> Witness:
    """Reconstruct a path from actual arcs, retaining every intermediate node."""
    if not isinstance(presentation, Presentation) or not isinstance(path, Path):
        raise TypeError("realize requires a Presentation and Path")
    nodes = {node.name: node for node in presentation.nodes}
    arcs = {arc.name: arc for arc in presentation.arcs}
    if path.start not in nodes:
        raise MissingEvidence(f"starting node {path.start!r} is absent")
    visited, roles, traces = [path.start], [], []
    for name in path.arcs:
        if name not in arcs:
            raise MissingEvidence(f"arc {name!r} is absent")
        arc = arcs[name]
        if arc.source != visited[-1]:
            raise ValueError(f"discontinuous path at arc {name!r}: {visited[-1]!r} != {arc.source!r}")
        visited.append(arc.target)
        roles.append(arc.role)
        traces.append(arc.trace)
    return Witness(path, tuple(visited), tuple(nodes[n].level for n in visited),
                   tuple(roles), tuple(traces))


def compose(presentation: Presentation, first: Path, second: Path) -> Path:
    left, right = realize(presentation, first), realize(presentation, second)
    if left.endpoint != second.start:
        raise ValueError("path composition has an unmatched boundary")
    return Path(first.start, first.arcs + second.arcs)


class Criterion(Enum):
    ENDPOINT = "endpoint"
    OBSERVATION = "observation"
    PATH = "path"


@dataclass(frozen=True)
class Obligation:
    name: str
    left: Path
    right: Path
    criterion: Criterion = Criterion.ENDPOINT

    def __post_init__(self):
        if not _name(self.name) or not isinstance(self.left, Path) or not isinstance(self.right, Path):
            raise ValueError("obligation requires a name and two Paths")
        if not isinstance(self.criterion, Criterion):
            raise ValueError("criterion requires an explicit Criterion")


class CheckStatus(Enum):
    SATISFIED = "SATISFIED"
    OBSTRUCTED = "OBSTRUCTED"
    UNKNOWN = "UNKNOWN"


class CoherenceStatus(Enum):
    COHERENT = "COHERENT"
    PARTIAL = "PARTIAL"
    OBSTRUCTED = "OBSTRUCTED"
    UNDETERMINED = "UNDETERMINED"


@dataclass(frozen=True)
class Check:
    name: str
    criterion: Criterion
    status: CheckStatus
    reason: str
    left: Witness | None = None
    right: Witness | None = None


@dataclass(frozen=True)
class CoherenceReport:
    status: CoherenceStatus
    checks: tuple[Check, ...]
    native_hyperemergence: str = "UNKNOWN"


def _obligations(obligations: tuple[Obligation, ...]) -> None:
    _tuple(obligations, Obligation, MAX_OBLIGATIONS, "obligations")
    if len({item.name for item in obligations}) != len(obligations):
        raise ValueError("duplicate obligation name")


def check(presentation: Presentation, obligations: tuple[Obligation, ...]) -> CoherenceReport:
    """Evaluate explicit coherence obligations against reconstructed evidence."""
    if not isinstance(presentation, Presentation):
        raise TypeError("check requires a Presentation")
    _obligations(obligations)
    results = []
    for obligation in obligations:
        left = right = None
        try:
            left = realize(presentation, obligation.left)
            right = realize(presentation, obligation.right)
        except MissingEvidence as exc:
            status, reason = CheckStatus.UNKNOWN, str(exc)
        except ValueError as exc:
            status, reason = CheckStatus.OBSTRUCTED, str(exc)
        else:
            if len(set(left.levels + right.levels)) < 2:
                status, reason = CheckStatus.OBSTRUCTED, "witness is not cross-level"
            elif left.path.start != right.path.start or left.endpoint != right.endpoint:
                status, reason = CheckStatus.OBSTRUCTED, "boundary endpoints disagree"
            elif obligation.criterion is Criterion.OBSERVATION and (left.levels, left.roles, left.traces) != (right.levels, right.roles, right.traces):
                status, reason = CheckStatus.OBSTRUCTED, "ordered level, role, or trace observations disagree"
            elif obligation.criterion is Criterion.PATH and left != right:
                status, reason = CheckStatus.OBSTRUCTED, "shared outcome does not reproduce the ordered path"
            else:
                status = CheckStatus.SATISFIED
                reason = {Criterion.ENDPOINT: "same boundary endpoints",
                          Criterion.OBSERVATION: "same ordered level, role, and trace observations",
                          Criterion.PATH: "same full ordered witness"}[obligation.criterion]
        results.append(Check(obligation.name, obligation.criterion, status, reason, left, right))
    counts = Counter(result.status for result in results)
    if results and counts[CheckStatus.SATISFIED] == len(results):
        status = CoherenceStatus.COHERENT
    elif counts[CheckStatus.SATISFIED]:
        status = CoherenceStatus.PARTIAL
    elif counts[CheckStatus.OBSTRUCTED]:
        status = CoherenceStatus.OBSTRUCTED
    else:
        status = CoherenceStatus.UNDETERMINED
    return CoherenceReport(status, tuple(results))


@dataclass(frozen=True)
class StructureMap:
    node_images: tuple[tuple[str, str], ...]
    arc_images: tuple[tuple[str, tuple[str, ...]], ...]


@dataclass(frozen=True)
class MapReport:
    injective: bool
    node_collisions: tuple[tuple[str, tuple[str, ...]], ...]
    contracted_arcs: tuple[str, ...]
    expanded_arcs: tuple[str, ...]
    role_changes: tuple[str, ...]
    level_changes: tuple[str, ...]
    trace_weakenings: tuple[str, ...]


def _map_dict(items: tuple, expected: set[str], label: str) -> dict:
    if not isinstance(items, tuple) or any(not isinstance(item, tuple) or len(item) != 2 for item in items):
        raise ValueError(f"malformed {label} map")
    result = dict(items)
    if len(result) != len(items) or set(result) != expected:
        raise ValueError(f"{label} map must assign each source identifier exactly once")
    return result


def map_report(source: Presentation, target: Presentation, mapping: StructureMap) -> MapReport:
    """Check endpoint-compatible arc images; report coarsening rather than hide it."""
    if not all(isinstance(p, Presentation) for p in (source, target)) or not isinstance(mapping, StructureMap):
        raise TypeError("map requires source, target, and StructureMap")
    nodes = _map_dict(mapping.node_images, {n.name for n in source.nodes}, "node")
    arcs = _map_dict(mapping.arc_images, {a.name for a in source.arcs}, "arc")
    target_nodes = {n.name: n for n in target.nodes}
    if not all(_name(image) and image in target_nodes for image in nodes.values()):
        raise ValueError("node map has an absent target")
    inverses = {image: tuple(sorted(name for name, value in nodes.items() if value == image))
                for image in set(nodes.values())}
    collisions = tuple(sorted((image, names) for image, names in inverses.items() if len(names) > 1))
    contracted, expanded, roles, weakened = [], [], [], []
    for arc in source.arcs:
        witness = realize(target, Path(nodes[arc.source], arcs[arc.name]))
        if witness.endpoint != nodes[arc.target]:
            raise ValueError(f"mapped boundary fails at source arc {arc.name!r}")
        if not witness.path.arcs:
            contracted.append(arc.name)
        elif len(witness.path.arcs) > 1:
            expanded.append(arc.name)
        if witness.roles != (arc.role,):
            roles.append(arc.name)
        if witness.trace_floor is None or _STRENGTH[witness.trace_floor] < _STRENGTH[arc.trace]:
            weakened.append(arc.name)
    level_changes = tuple(sorted(n.name for n in source.nodes if n.level != target_nodes[nodes[n.name]].level))
    one_for_one = all(len(image) == 1 for image in arcs.values())
    distinct_arc_images = len({image for image in arcs.values()}) == len(arcs)
    return MapReport(not collisions and one_for_one and distinct_arc_images, collisions,
                     tuple(sorted(contracted)), tuple(sorted(expanded)), tuple(sorted(roles)),
                     level_changes, tuple(sorted(weakened)))


@dataclass(frozen=True)
class Transport:
    source: Witness
    image: Witness
    path_information_lost: bool


def transport(source: Presentation, target: Presentation, mapping: StructureMap, path: Path) -> Transport:
    report = map_report(source, target, mapping)
    original = realize(source, path)
    nodes, arcs = dict(mapping.node_images), dict(mapping.arc_images)
    projected = Path(nodes[path.start], tuple(e for name in path.arcs for e in arcs[name]))
    image = realize(target, projected)
    used_nodes = set(original.nodes)
    lost = (len({nodes[n] for n in used_nodes}) != len(used_nodes)
            or any(len(arcs[a]) != 1 for a in path.arcs)
            or len({arcs[a] for a in set(path.arcs)}) != len(set(path.arcs))
            or original.roles != image.roles or original.traces != image.traces
            or bool(used_nodes & set(report.level_changes)))
    return Transport(original, image, lost)


def relabel(presentation: Presentation, node_names: dict[str, str], arc_names: dict[str, str]):
    if set(node_names) != {n.name for n in presentation.nodes} or set(arc_names) != {a.name for a in presentation.arcs}:
        raise ValueError("renaming must cover every identifier")
    if len(set(node_names.values())) != len(node_names) or len(set(arc_names.values())) != len(arc_names):
        raise ValueError("renaming must be bijective onto its images")
    result = Presentation(presentation.name, presentation.levels,
                          tuple(Node(node_names[n.name], n.level) for n in presentation.nodes),
                          tuple(Arc(arc_names[a.name], node_names[a.source], node_names[a.target],
                                    a.role, a.trace) for a in presentation.arcs))
    mapping = StructureMap(tuple(node_names.items()), tuple((a, (image,)) for a, image in arc_names.items()))
    return result, mapping


@dataclass(frozen=True)
class ContinuationProfile:
    horizon: int
    paths: tuple[Path, ...]
    endpoints: tuple[str, ...]
    complete_within_horizon: bool
    stop_reason: str | None


def continuation_profile(presentation: Presentation, start: str, horizon: int, *, max_paths: int = 4096) -> ContinuationProfile:
    """Enumerate positive-length walks through a declared finite horizon, cycles included."""
    if type(horizon) is not int or not 0 <= horizon <= MAX_PATH_LENGTH:
        raise ValueError(f"horizon must be an integer between 0 and {MAX_PATH_LENGTH}")
    if type(max_paths) is not int or not 1 <= max_paths <= MAX_WALKS:
        raise ValueError(f"path budget must be an integer between 1 and {MAX_WALKS}")
    realize(presentation, Path(start, ()))
    outgoing = {n.name: tuple(sorted((a for a in presentation.arcs if a.source == n.name), key=lambda a: a.name))
                for n in presentation.nodes}
    pending = deque([(Path(start, ()), start)])
    paths, ends = [], set()
    while pending:
        path, endpoint = pending.popleft()
        if len(path.arcs) >= horizon:
            continue
        for arc in outgoing[endpoint]:
            if len(paths) == max_paths:
                return ContinuationProfile(horizon, tuple(paths), tuple(sorted(ends)), False, "path budget reached")
            child = Path(start, path.arcs + (arc.name,))
            paths.append(child)
            ends.add(arc.target)
            pending.append((child, arc.target))
    return ContinuationProfile(horizon, tuple(paths), tuple(sorted(ends)), True, None)


@dataclass(frozen=True)
class Development:
    before: CoherenceReport
    after: CoherenceReport
    newly_witnessed: tuple[str, ...]
    lost: tuple[str, ...]
    correspondence_status: str
    context_reasons: tuple[str, ...]
    native_hyperemergence: str = "UNKNOWN"


def compare_development(before: Presentation, after: Presentation, obligations: tuple[Obligation, ...]) -> Development:
    first, second = check(before, obligations), check(after, obligations)
    reasons = []
    if set(before.levels) != set(after.levels) or {n.name: n.level for n in before.nodes} != {n.name: n.level for n in after.nodes}:
        reasons.append("fixed typed node/level correspondence is not established")
    original_arcs, resulting_arcs = {a.name: a for a in before.arcs}, {a.name: a for a in after.arcs}
    if any(original_arcs[name] != resulting_arcs[name] for name in original_arcs.keys() & resulting_arcs.keys()):
        reasons.append("shared arc identifiers changed endpoints, roles, or trace tags")
    if reasons:
        return Development(first, second, (), (), "UNKNOWN_CONTEXT", tuple(reasons))
    newly = tuple(b.name for a, b in zip(first.checks, second.checks)
                  if a.status is not CheckStatus.SATISFIED and b.status is CheckStatus.SATISFIED)
    lost = tuple(b.name for a, b in zip(first.checks, second.checks)
                 if a.status is CheckStatus.SATISFIED and b.status is not CheckStatus.SATISFIED)
    return Development(first, second, newly, lost, "FIXED_TYPED_CONTEXT", ())


def _plain(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def json_data(value):
    """JSON-compatible data without dropping ordered paths or evidence status."""
    return _plain(asdict(value))


def _presentation_data(presentation: Presentation) -> dict:
    result = json_data(presentation)
    result["nodes"] = sorted(result["nodes"], key=lambda node: node["name"])
    result["arcs"] = sorted(result["arcs"], key=lambda arc: arc["name"])
    result["levels"] = sorted(result["levels"])
    return result


def _digest(data: object) -> str:
    content = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def presentation_digest(presentation: Presentation) -> str:
    return _digest(_presentation_data(presentation))


@dataclass(frozen=True)
class Handoff:
    target: object
    digest: str
    native_hyperemergence: str = "UNKNOWN"


def _handoff_digest(presentation, obligations, target):
    return _digest({"presentation": _presentation_data(presentation),
                    "obligations": sorted((json_data(o) for o in obligations), key=lambda o: o["name"]),
                    "target": json_data(target), "mechanism": "finite-coherence-v1"})


def stabilize(presentation: Presentation, obligations: tuple[Obligation, ...], target) -> Handoff:
    """Bind a named finite presentation handoff; this does not prove a native Hyperform."""
    from hyperemergence import Stabilization
    if not isinstance(target, Stabilization):
        raise ValueError("handoff requires an explicit named Stabilization target")
    report = check(presentation, obligations)
    if report.status is not CoherenceStatus.COHERENT:
        raise ValueError("finite handoff requires COHERENT nonempty obligations")
    return Handoff(target, _handoff_digest(presentation, obligations, target))


def verify_stabilization(presentation: Presentation, obligations: tuple[Obligation, ...], receipt: Handoff) -> bool:
    if not isinstance(receipt, Handoff) or receipt.native_hyperemergence != "UNKNOWN":
        return False
    try:
        current = stabilize(presentation, obligations, receipt.target)
    except (ValueError, TypeError):
        return False
    return current == receipt
