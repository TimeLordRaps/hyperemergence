# Hyperemergence: witnessed coherence across levels

## The field's central problem [HYPER / FRAME / OPEN]

Hyperstratum places the hyperemergent among cross-level connections and
relations, before a coherence stabilizes into a named hyperrelation, graph
or hyperform. This makes emergence a problem of formation and changing
presentation: what becomes jointly coherent across levels, what witnesses
that coherence, and what remains available when it is named, transformed or
projected?

This field develops three coupled questions:

1. **Coherence:** which independently represented routes are compatible,
   and at which observational strength?
2. **Development:** which compatibility witnesses become available relative
   to a stated baseline, with the same interpretation of identifiers?
3. **Stabilization:** which distinctions survive the move to a named
   representation, and which source mutations invalidate that handoff?

The finite laboratory answers these questions for supplied typed
presentations. It supplies constructions and counterexamples for research,
rather than declaring that every constructed example is a native
hyperemergent. Coherence, newness, formation and stabilization have separate
evidence requirements.

## Finite objects [FRAME]

Let a presentation be `P = (L, V, E, ell, s, t, role, trace)`:

- `L` is a finite set of declared recursive-level names.
- `V` is a finite set of node identifiers; `ell: V -> L` assigns each node
  its declared level.
- `E` is a finite set of arc identifiers; `s,t: E -> V` assign each arc its
  source and target.
- `role` assigns each arc a declared semantic role.
- `trace` assigns each arc one of `~~`, `=~`, `==`. These are recorded tags,
  not evidence that native Hypermath relations hold.

A route is a start node `v0` and an ordered word `e1...en` of arcs, such that
`s(e1)=v0` and `t(ei)=s(e(i+1))`. Its witness retains the complete vertex
word `v0...vn`, level word, role word and trace word. A zero-length route is
the identity at its starting node. Arc counts and finite horizons are
dimensionless, not physical time or a universal ordinal interpretation.

Levels name recursive interpretation, not metric height. The construction
does not infer that a node called `meta` actually represents another node.
That relation would require a supplied representation rule and its own
obligations. Two identical numerical observations at different labelled
levels likewise do not establish cross-level formation.

An obligation specifies two routes, a common-boundary requirement and one
of three equality strengths:

| Strength | Retained distinction |
|---|---|
| Endpoint coherence | Same start and end; intermediate structure may differ. |
| Observation coherence | Same boundaries and ordered level/role/trace observations; intermediate identifiers may differ. |
| Full path reproduction | Same complete ordered witness. |

Every obligation must actually involve at least two levels in its routes.
A single cross-level route compared with itself witnesses the route's own
structural consistency; it does not establish independent convergence or a
novel coordination. The chosen obligation set must expose the intended
phenomenon, and the report lists that set so this limitation is visible.

## Basic propositions and derivations [FORM within this FRAME]

**1. Composition retains formation records.** If route `p` ends at the start
of route `q`, concatenation of their arc words is a valid route. The shared
boundary vertex occurs once; every arc, intermediate vertex, role and tag
occurs in its original order. This follows directly by checking the new
boundary adjacency in addition to each route's existing adjacencies.

**2. Composition is associative and has local identities.** For composable
`p,q,r`, both `(p;q);r` and `p;(q;r)` have the identical concatenated word and
starting vertex. The identity route contributes no arc. The executable
resource bound also matters: both sides must remain inside the allowed
path-length domain. This is a finite labelled-path construction, not a
discharge of native Hypermath's opaque composition or ordinal obligations.

**3. Coherence strength has a strict filtration.** Full witness equality
implies observation coherence, which implies endpoint coherence, because
each weaker observation is obtained by discarding distinctions from the
stronger record. The reverses fail. Two routes can share endpoints but have
different roles. Two routes can share the whole level/role/trace word but
traverse different intermediate nodes and arc identifiers. Both
counterexamples are executable tests.

**4. Checked transport preserves endpoint composition.** A structure map
`F` maps each source node to a target node and each source arc to a target
route with exactly the mapped boundaries. Substitution of these arc images
into a composable source route yields a valid target route, since every
adjacent pair still shares its mapped boundary. Thus
`F(p;q)=F(p);F(q)` as arc words, whenever the transported routes fit the
resource bounds. Cross-level participation and role/trace preservation are
additional requirements: a boundary-preserving map can collapse levels or
change observations, so it need not preserve those stronger obligations.

**5. A collided image cannot determine its formation route.** Suppose two
distinct witnessed routes `p != q` satisfy `F(p)=F(q)`. No function of the
image alone can recover both originals: applying a putative inverse to the
same image must return a single value, whereas recovery demands both `p`
and `q`. A container carrying the original witnesses can preserve them;
the obstruction concerns the projected image alone. The demonstration does
exactly that: retain the source witnesses and expose the lossy projection.

**6. A pure change of identifiers supplies no structural novelty.** A
bijective node/arc renaming preserves incidence, levels, roles and trace
tags. It transports every existing route to a corresponding route. Any
coherence newly attributed to the renamed version by checking its new
identifiers against the unaligned old version is a comparison error. The
development checker therefore requires a fixed typed carrier and stable
semantics for shared arc identifiers. Unaligned identifiers produce
`UNKNOWN_CONTEXT`, not a newly witnessed claim.

**7. Arc extension is monotone for existing witnesses in a fixed context.**
If existing nodes, levels and arc meanings remain identical and the new
presentation only adds arcs, every previously reconstructed route remains
available with the same witness. Any already satisfied obligation remains
satisfied. Previously missing evidence can become available. This proves
monotonicity of the selected finite checks; it does not prove that the
underlying phenomenon became newly real when a record was added.

**8. Stabilization bindings are mutation-sensitive.** A handoff binds the
entire typed presentation, obligations, comparison strengths, named target
and mechanism version. Recomputing the binding after changing an arc,
role, level or obligation rejects the old receipt. This is a content and
mechanism integrity property. It establishes neither who authorized the
handoff nor that the finite target is a native hyperform.

## Worked case: a coherence with two explanations [FRAME]

The case in `examples/coherent.json` has:

```txt
seed (base) --a/open-left--> left (meta) --b/join-left--> joined (whole)
seed (base) --c/open-right-> right (meta) --d/join-right-> joined (whole)
```

Both `(a,b)` and `(c,d)` reconstruct from `seed` to `joined`. The endpoint
obligation is satisfied. Their role words differ, so observation coherence
fails, and their intermediate nodes and arcs differ, so exact reproduction
fails. Specifying endpoint and exact obligations together yields `PARTIAL`.
This does not weaken the exact requirement into a pass.

Give both first arcs role `open` and both second arcs role `join`, retaining
equal trace words. Now observation coherence is satisfied, even though
the explanation paths remain distinct. Alter one trace tag or one role and
that stronger observation obligation is obstructed again. The three
strengths answer different questions.

The projected presentation has `origin --summary--> result`. Map `seed`,
`left` and `right` to `origin`, and `joined` to `result`. Contract `a` and
`c` to identity routes; map `b` and `d` to `summary`. Both source routes now
have the exact same image. The finite map preserves the common outcome and
destroys the ability to infer which explanation supplied it. An endpoint
table alone cannot be an L2 DerivationPath.

Remove `d` from the baseline. The right route is missing evidence and its
coherence obligation is `UNKNOWN`. Restore it under the same typed
context, and the endpoint obligation acquires a witness. This is an
observed change in available evidence. It does not establish that
hyperemergence first occurred at the moment of restoration.

The endpoint-only obligation set is coherent, so it can be bound to the
named graph `joined-outcome-v1`. The two-obligation partial set cannot be
handed off as complete. Removing `d` afterward invalidates the endpoint
handoff. Naming the graph moves the declared presentation to a stable
target; it does not reconstruct its native formation history.

## Integration and semantic boundaries [FRAME / OPEN]

| Field | Evidence it can contribute | Gate still required here |
|---|---|---|
| Hyperstratum | Hyperstack, hyperemergent sense, named stabilization targets. | Translate its recursive representations into typed levels without erasing level distinctions. |
| Hypermath | Source-native ground, relation filtration, witnessed derivation-path and transport research. | Supply actual Form/step correspondence and operational reproduction evidence. |
| Hypergrammar | Typed derivation chains and source-language constraints. | Check an actual candidate translation, rather than citing an unrelated valid example. |
| Hyperlogic | Models, consequences and source-native closes. | Establish the required consequence; satisfiable finite rows alone are insufficient. |
| Hyperchemistry | Port relations, compatibility assignments and composition witnesses. | Retain assignment/operation order; endpoint projection alone loses formation. |
| Hyperobjectivity / Hypersubjectivity | Instantiation and proposed novelty/consciousness accounts. | Bind their particular inputs, baseline and observation rules; typed coherence alone does not discharge novelty. |
| Hyperorder | Convergence of divergences, following Tyler's present distinction. | Show its divergence/convergence mechanism and then inspect cross-level coherence of that evidence. |
| Hyperchaos | Convergence toward divergence and divergences of divergences. | Retain which divergence layer is being compared; branching alone is not this criterion. |

The publicly inspected
[Hypermath revision](https://github.com/TimeLordRaps/hypermath/tree/dc89cbb4f154844ca4909d7c1c359ee3882323e2)
distinguishes continuation overlap (`~~`), coinciding outcomes (`=~`) and
mutual path reproduction (`==`). Its
[witnessed path layers](https://github.com/TimeLordRaps/hypermath/blob/dc89cbb4f154844ca4909d7c1c359ee3882323e2/docs/research/PATH_LAYERS.md)
and
[transport construction](https://github.com/TimeLordRaps/hypermath/blob/dc89cbb4f154844ca4909d7c1c359ee3882323e2/docs/research/PATH_TRANSPORT.md)
keep native generation and reproduction obligations open. This frame
respects the same distinction; assigning an arc the literal tag `==`
does not discharge it. L0 ground, L1 relations, L2 operations and L3
ordinatics remain source-owned layers, not labels for Python class depth.

## Research program and refutable next constructions [OPEN]

**Native path adaptation.** Build a pinned adapter from actual source
derivation entries, retaining endpoints, steps and trace-level evidence.
Reject an endpoint-only candidate and an order-reversed candidate. A
successful adapter must state precisely which native propositions it
establishes and which it only represents.

**Observation-based newness.** Define the observation domain and uncoupled
baseline before measuring novelty. Require stable identity correspondence
and a witness unavailable under the baseline's licensed mechanisms. A
changed label, an added record of an already available route, or a forgotten
baseline witness must not count. The current fixed-context development
checker supplies an evidence transition, not that stronger theorem.

**Recursive representation compatibility.** Add explicit representation
maps between base, meta and whole presentations. Supply role-preserving
transport laws and counterexamples where a valid operational graph has an
incompatible representation structure. Graph reachability alone should
remain insufficient.

**Coherence beyond paired routes.** Develop finite gluing constraints for
three or more local views. Pairwise agreement may lack a single joint
assignment; an independent inconsistent-cycle counterexample should be a
required gate. The current implementation reports only listed route-pair
obligations and does not claim a complete gluing theory.

**Formation-aware stabilization.** A named handoff should retain which
witnesses formed its relation, graph or hyperform, who is authorized to name
it, and what mutation invalidates it. Content hashing is one bounded
integrity mechanism; native closing identity and formation remain separate
construction tasks.

**Finite-to-unbounded continuation.** A complete horizon profile does not
establish unbounded capacity. An extension theorem or a checked invariant
would be needed before lifting any finite observation to native continuation
claims. Resource truncation must remain explicit evidence loss.
