"""Command-line interface (CLI) for the finite coherence laboratory."""

from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path as FilePath

from coherence import (Arc, CoherenceStatus, Criterion, Node, Obligation, Path,
                       Presentation, StructureMap, TraceLevel, check,
                       compare_development, continuation_profile, json_data,
                       map_report, stabilize, transport, verify_stabilization)


def load_case(path: FilePath):
    if path.stat().st_size > 1_048_576:
        raise ValueError("case file exceeds the one-mebibyte input limit")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"presentation", "obligations"}:
        raise ValueError("case requires exactly presentation and obligations")
    p = data["presentation"]
    if not isinstance(p, dict) or set(p) != {"name", "levels", "nodes", "arcs"}:
        raise ValueError("presentation requires name, levels, nodes, and arcs")
    if not all(isinstance(p[key], list) for key in ("levels", "nodes", "arcs")):
        raise ValueError("levels, nodes, and arcs require arrays")
    if not isinstance(data["obligations"], list):
        raise ValueError("obligations require an array")
    nodes = tuple(Node(**node) for node in p["nodes"])
    arcs = tuple(Arc(**{**arc, "trace": TraceLevel(arc.get("trace", "~~"))}) for arc in p["arcs"])
    presentation = Presentation(p["name"], tuple(p["levels"]), nodes, arcs)
    obligations = []
    for item in data["obligations"]:
        if not isinstance(item, dict) or set(item) != {"name", "left", "right", "criterion"}:
            raise ValueError("each obligation requires name, left, right, and criterion")
        paths = []
        for key in ("left", "right"):
            raw = item[key]
            if not isinstance(raw, dict) or set(raw) != {"start", "arcs"} or not isinstance(raw["arcs"], list):
                raise ValueError("each path requires start and an arcs array")
            paths.append(Path(raw["start"], tuple(raw["arcs"])))
        obligations.append(Obligation(item["name"], *paths, Criterion(item["criterion"])))
    return presentation, tuple(obligations)


def demo() -> dict:
    graph = Presentation(
        "cross-level explanations", ("base", "meta", "whole"),
        (Node("seed", "base"), Node("left", "meta"), Node("right", "meta"), Node("joined", "whole")),
        (Arc("a", "seed", "left", "open-left"), Arc("b", "left", "joined", "join-left"),
         Arc("c", "seed", "right", "open-right"), Arc("d", "right", "joined", "join-right")))
    left, right = Path("seed", ("a", "b")), Path("seed", ("c", "d"))
    endpoint = Obligation("joined outcome", left, right, Criterion.ENDPOINT)
    exact = Obligation("reproduced explanation", left, right, Criterion.PATH)
    partial = check(graph, (endpoint, exact))
    coarse = Presentation("projected outcome", ("base", "whole"),
                          (Node("origin", "base"), Node("result", "whole")),
                          (Arc("summary", "origin", "result", "summary"),))
    mapping = StructureMap((("seed", "origin"), ("left", "origin"), ("right", "origin"), ("joined", "result")),
                           (("a", ()), ("b", ("summary",)), ("c", ()), ("d", ("summary",))))
    image_left, image_right = transport(graph, coarse, mapping, left), transport(graph, coarse, mapping, right)
    baseline = replace(graph, arcs=graph.arcs[:-1])
    development = compare_development(baseline, graph, (endpoint, exact))
    from hyperemergence import Stabilization, Target
    handoff = stabilize(graph, (endpoint,), Stabilization(Target.GRAPH, "joined-outcome-v1"))
    return {
        "classification": "FRAME",
        "partial_coherence": partial.status.value,
        "obligations": json_data(partial),
        "development": json_data(development),
        "projection": {
            "two_paths_collapse": image_left.image == image_right.image,
            "source_witnesses_are_distinct": image_left.source != image_right.source,
            "left": json_data(image_left), "right": json_data(image_right),
            "map": json_data(map_report(graph, coarse, mapping)),
        },
        "continuations": json_data(continuation_profile(graph, "seed", 2)),
        "stabilization_handoff": json_data(handoff),
        "mutation_reuses_handoff": verify_stabilization(baseline, (endpoint,), handoff),
        "native_hyperemergence": "UNKNOWN",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Witnessed finite cross-level coherence; native adequacy remains OPEN.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo", help="compute development, obstruction, projection, and invalidation examples")
    checking = commands.add_parser("check", help="check a JSON case; incomplete or obstructed coherence exits 1")
    checking.add_argument("case", type=FilePath)
    walking = commands.add_parser("walks", help="enumerate actual continuations to a finite horizon")
    walking.add_argument("case", type=FilePath)
    walking.add_argument("start")
    walking.add_argument("--depth", type=int, required=True)
    walking.add_argument("--max-paths", type=int, default=4096)
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result, code = demo(), 0
        else:
            presentation, obligations = load_case(args.case)
            if args.command == "check":
                report = check(presentation, obligations)
                result, code = json_data(report), 0 if report.status is CoherenceStatus.COHERENT else 1
            else:
                profile = continuation_profile(presentation, args.start, args.depth, max_paths=args.max_paths)
                result, code = json_data(profile), 0 if profile.complete_within_horizon else 1
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
