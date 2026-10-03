# Hyperemergence

**Study the coherence that becomes possible across recursive levels while it
is still emerging.** A coherent outcome can retain several incompatible
explanations. A projection can erase their difference. A named stable
presentation can preserve a result while losing the route that formed it.
Hyperemergence investigates those transitions and supplies an executable
laboratory for inspecting them.

The sourced starting point is
[Hyperstratum's definition](https://github.com/TimeLordRaps/hyperstratum/blob/c4ffe2c7ff42c747d74ef5236d3bef631dd5f08e/specs/canonical-definitions.md):
newly emerging cross-level coherence before stabilization into a named
hyperrelation, graph, or hyperform. This repository develops an
assistant-proposed **[FRAME]** of witnessed finite presentations. The native
formation and adequacy questions remain **[OPEN]**.

## What you can actually do

- Reconstruct a route from typed nodes and labelled arcs, retaining each
  intermediate node, semantic role, level and trace tag.
- Compose routes with checked boundaries and compare shared outcomes with
  retained level/role/trace observations and full ordered path reproduction.
- Check cross-level coherence obligations and obtain concrete witnesses,
  counterexamples or missing-evidence reports.
- Transport a presentation through a checked structure map and see which
  intermediate nodes, arcs, roles or trace distinctions were discarded.
- Compare an incomplete baseline with an extended presentation and identify
  which specified coherence obligations acquired witnesses in the same
  typed context. Identifier churn is reported as an unknown comparison.
- Enumerate continuations through a finite horizon, including cycles, with
  explicit evidence loss when the path budget is exhausted.
- Bind a coherent finite presentation to a named stabilization handoff and
  reject reuse after a source, obligation, role, level or target mutation.

These are working mechanisms. Their results are relative to the supplied
presentation and obligations; `COHERENT` does not mean a native
hyperemergent has been established.

## Run it

Python 3.12 or later; the runtime uses only the standard library.

```console
python -B -m hyperemergence demo
python -B -m hyperemergence check examples/coherent.json
python -B -m hyperemergence check examples/partial.json
python -B -m hyperemergence walks examples/coherent.json seed --depth 2
python -B -u validate.py
```

The demo computes a cross-level diamond. Both routes reach `joined`, so the
endpoint obligation is satisfied. Their intermediate nodes and arc roles
differ, so exact path reproduction is obstructed. Together the two
obligations yield `PARTIAL`. A coarse map merges the two routes into one
summary route; the output retains both original witnesses and reports the
loss. Adding the missing branch acquires an endpoint witness relative to an
explicit baseline. The endpoint-only presentation can be handed to a named
graph, and removing an arc invalidates that handoff.

`check` exits 0 only for a nonempty, fully coherent obligation set; partial,
obstructed and undetermined checks exit 1. Invalid input exits 2. `walks`
exits 1 when its budget truncates the selected horizon. The validation
runner streams named tests under a 20-second overall deadline, with no
per-test process isolation.

Install from the checkout to obtain the `hyperemergence` command:

```console
python -m pip install .
hyperemergence demo
```

## Read and develop the field

[THEORY.md](THEORY.md) develops the objects, coherence hierarchy, transport
laws, worked counterexamples, stabilization boundary and research program.
[FIELD_SPEC.md](FIELD_SPEC.md) binds those ideas to the actual executable
contract. [PROVENANCE.md](PROVENANCE.md) separates sourced senses,
user-stated questions and proposed constructions.

Hypermath distinguishes continuation overlap (`~~`), matching outcomes
with paths discarded (`=~`), and mutual path reproduction (`==`). The finite
laboratory keeps those distinctions visible without identifying its Python
records with native Hypermath Forms. Cross-level coherence also does not
establish Hyperorder's convergence of divergences or Hyperchaos's convergence
toward divergence; those fields own their respective mechanisms.

The earlier declaration API remains available: `assess(Candidate(...))`
returns `REFUTED` or `UNKNOWN`. The richer checker preserves that native
uncertainty while providing actual finite evidence.

[FIELD.json](FIELD.json) lists the integration surface.
[TECHNICAL_DEBT.md](TECHNICAL_DEBT.md) records unresolved obligations;
[AGENT_HANDOFF.md](AGENT_HANDOFF.md) records the next research and review
gates. No Verifier Standard (VSTD) certificate is asserted.
