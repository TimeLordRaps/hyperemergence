# Hyperemergence field contract

Version 0.2.0, 2026-10-03. The defining source is Hyperstratum's
[pinned canonical text](https://github.com/TimeLordRaps/hyperstratum/blob/c4ffe2c7ff42c747d74ef5236d3bef631dd5f08e/specs/canonical-definitions.md).
It locates a hyperemergent as newly emerging cross-level coherence before
stabilization into a named hyperrelation, graph or hyperform.

Classification: **[HYPER]** sourced ontological sense or proposal;
**[FRAME]** finite mathematical/executable construction;
**[FORM within this FRAME]** a derived structural proposition under the
explicit finite assumptions; **[OPEN]** an unresolved native correspondence
or research obligation. Host-level proofs are not native L0/L1/L2/L3 closes.

## Objects and reconstructed evidence [FRAME]

`Presentation(name, levels, nodes, arcs)` has distinct named levels, nodes
and arcs. A `Node` has one declared level. An `Arc` has distinct identifier,
source and target node identifiers, a semantic role and an explicit
`TraceLevel` tag. A role is not merely an edge's name. Node levels and arc
endpoints must be declared. Duplicate identifiers, malformed types and
dangling endpoints are refused. A presentation permits partial evidence:
omission of a named arc does not assert that no such arc exists in reality.

`Path(start, arcs)` is an ordered sequence of arc identifiers from a given
starting node. `realize` looks up every actual arc and checks continuity. It
returns a `Witness` containing the ordered nodes, node levels, roles and
trace tags. A missing referenced node or arc raises `MissingEvidence`; a
discontinuous path supplies a structural contradiction. Empty paths retain
their starting point and act as identity routes.

`compose` validates the first route's ending node against the second
route's starting node before concatenating their arc records. It preserves
intermediate structure. It does not substitute an endpoint pair for a path.

Finite bounds: at most 64 levels, 256 nodes, 1,024 arcs, 64 arcs per path,
1,024 obligations, 100,000 enumerated walks and a one-mebibyte CLI input.
These are explicit resource bounds, not physical capacities or ordinal
claims. Bounds fail explicitly; they do not clamp a record into validity.

## Coherence obligations and obstructions [FRAME]

An `Obligation` supplies a name, two paths and a `Criterion`:

| Criterion | What is checked |
|---|---|
| `ENDPOINT` | Same starting and ending nodes after both routes are reconstructed. |
| `OBSERVATION` | Same boundaries and ordered levels, roles and trace tags; intermediate node and arc identities may differ. |
| `PATH` | Same entire reconstructed ordered witness, including route identifiers, intermediate nodes, levels, roles and trace tags. |

Every satisfied obligation additionally requires actual cross-level
participation: at least two node levels occur in its reconstructed routes.
Two unused level declarations do not discharge that requirement.

`check` reconstructs evidence and returns an item for every obligation:
`SATISFIED`, `OBSTRUCTED`, or `UNKNOWN`. An obstruction includes its reason
and any successfully reconstructed witness. Missing referenced material is
`UNKNOWN`, with the exact missing reference. It is not coerced to agreement.

| Aggregate status | Meaning within the supplied obligation set |
|---|---|
| `COHERENT` | Nonempty set; every obligation satisfied. |
| `PARTIAL` | At least one satisfied obligation and at least one unknown or obstructed obligation. |
| `OBSTRUCTED` | None satisfied; at least one concrete obstruction. |
| `UNDETERMINED` | Empty set, or every obligation unknown. |

The report always retains `native_hyperemergence="UNKNOWN"`. It checks no
unlisted obligation and makes no claim that its declaration of levels,
roles or arcs is externally authenticated.

## Structure maps and witness retention [FRAME]

`StructureMap` assigns every source node exactly one target node, and every
source arc a target path, including a possible empty path. `map_report`
reconstructs each arc image and checks both mapped boundaries. Missing or
extra assignments, duplicate keys, absent target nodes and incompatible
boundaries are refused.

The report lists node collisions, contracted or expanded arcs, role
changes, level changes and weakened trace floors. `injective` is the
specific one-for-one criterion: distinct source nodes remain distinct and
each distinct source arc has a distinct one-arc image. It does not decide
decodability for expanded encodings.

`transport` returns the original full witness and its image; the original
is preserved for inspection. `path_information_lost` records failure to
retain the original's observations one for one in that image: node
identification, arc contraction/expansion/identification, changed ordered
roles or tags, or changed levels. An expanded route might be recoverable
with an additional decoder; this flag does not establish irrecoverability
under every possible encoding. The demo supplies a stronger concrete
obstruction: two distinct source paths have exactly the same image, so the
image alone cannot choose the original.

`relabel` constructs and checks a bijective node/arc renaming. It retains
levels, roles and tags. Relabeling preserves coherence and path
observations; it supplies no new coherence.

## Development and stabilization [FRAME]

`compare_development` runs the same obligations against an explicit baseline
and resulting presentation. Acquired/lost witness reports require a fixed
typed carrier: the same node identifiers and levels, the same level set,
and unchanged endpoints, roles and tags for all shared arc identifiers.
Arcs may be added or removed. Under that explicit correspondence it reports
which formerly unknown or obstructed obligations acquired witnesses, and
which formerly satisfied obligations lost them.

Renaming, carrier growth, changed level meaning, and reused arc identifiers
with changed semantics return `UNKNOWN_CONTEXT`, no acquired/lost claims,
and explicit context reasons. The before/after checks remain available. A
caller can use a checked bijective renaming to normalize identifiers before
comparison; non-bijective correspondence requires a separate adaptation
proof. Newly witnessed coherence is observational and baseline-relative,
not metaphysical newness. Missing evidence in the baseline does not prove
the coherence never existed.

`stabilize` requires a nonempty `COHERENT` report and an explicit named
`Stabilization` into `HYPERRELATION`, `GRAPH` or `HYPERFORM`. Its finite
`Handoff` binds the whole presentation, the exact obligations and their
criteria, the named target and the mechanism version through canonical
JavaScript Object Notation (JSON) and Secure Hash Algorithm 256-bit
(SHA-256). Node/arc descriptor order is irrelevant; order inside paths is
retained. `verify_stabilization` reruns the checks and recomputes the binding.
Content, level, role, trace, target and obligation mutations invalidate the
receipt. This is integrity checking of a local handoff; signatures,
authority, physical observation and native formation are not provided.

The handoff can record a proposed hyperform target. It does not derive
Hyperstratum's native closed or closing identity. The older `assess` still
refutes a declaration already marked stabilized when it is offered as a
pre-stabilization hyperemergent.

## Finite continuations [FRAME]

`continuation_profile` enumerates all positive-length walks from a starting
node through a supplied finite arc-count horizon, including repetitions and
cycles. The horizon is a dimensionless count, not elapsed time. The result
retains every enumerated path and observed endpoint. Breadth-first
enumeration uses deterministic arc-name ordering.

`complete_within_horizon` is true only when enumeration finishes within the
budget. A stop returns false with `path budget reached`; it does not claim
that unseen continuations are absent. No finite horizon confirms unbounded
continuation capacity or native `~~`, `=~`, or `==`.

## Preserved declarations and source senses [HYPER / FRAME / OPEN]

`hyperemergent` and `hyperemergence` resolve to the same explicitly declared
sense. Plain `emergence` and `emergent` do not resolve. The term pairing is
this repository's declaration; Hyperstratum's cited definition names only
the first. Tyler's existing field/consciousness questions remain recorded
as `OPEN`.

`Candidate` still declares a name, 1 to 64 distinct named levels, and an
optional named stabilization. `assess` returns `REFUTED` on one level or on
declared stabilization, reporting both reasons when both apply. Otherwise
it returns `UNKNOWN`. There is no confirming native verdict and no closure
flag on a candidate.

## Integration ownership and research gates [OPEN]

Hyperstratum owns the cited hyperstack and stabilization-target vocabulary.
Hypermath owns ground, native relations, DerivationPath and its L0/L1/L2/L3
dependency discipline. Hypergrammar owns source-native derivation typing;
Hyperlogic owns its consequence and model distinctions; Hyperchemistry owns
its compositional port relations. This frame does not identify any of those
native mechanisms with its Python graph paths. A satisfiable relation, a
shared endpoint or a named handoff alone establishes none of their closes.

Hyperobjectivity owns hyperobject instantiation; Hypersubjectivity owns the
proposed consciousness/novelty account. Hyperorder's convergence of
divergences and Hyperchaos's convergence toward divergence are separate
field questions, following Tyler's 2026-10-03 distinctions. This frame checks
coherence at recursive levels and can inspect their supplied witnesses; it
does not classify branching or convergence as either field automatically.

The next research gates are substantive constructions, not a requirement
to answer every naming question before work can proceed: a pinned native
path translation with retained witnesses; a falsifiable observation-based
newness criterion; typed transformations that preserve relevant levels;
and a stabilization mechanism that authenticates its formation. Ownership
of the definition, what counts as a level, whether Hyperchemistry emerges
from Hyperphysics, and consciousness's contribution remain open. See
[THEORY.md](THEORY.md) and [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).

The original questions retain their identifiers for source/debt continuity:

- **Q1:** Does the defining text remain owned by Hyperstratum or move here?
- **Q2:** In what sense can a field, such as Hyperchemistry, emerge from another?
- **Q3:** What criterion establishes native hyperemergent coherence and true
  newness? Hypersubjectivity proposes that, against an uncoupled baseline,
  a linked whole exhibits a refutable cross-level coherence that no isolated
  component or renamed edge already has. This frame's acquired-witness
  transition is weaker than that proposed criterion.
- **Q4:** Which sourced mechanisms does each sibling field contribute, and
  how is each actual adapter checked?
- **Q5:** What authenticates the meaning of a level beyond a declared name?
- **Q6:** Are consciousness's proposed novelties from hyperobjects
  hyperemergents, and which field establishes that relationship?

These native questions remain open while the finite constructions proceed.
