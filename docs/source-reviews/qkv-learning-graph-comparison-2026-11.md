# QKV tutorial: source learning graph and route comparison

**Source:** [Nishanthan K — How Query, Key, and Value (QKV) Work in Transformers](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a)  
**Source record:** `nishanthan-k-qkv-transformers-devto`  
**Extraction record:** `data/extractions/nishanthan-k-qkv-transformers-devto.yml`  
**Review date:** 2026-11-04  
**Purpose:** reconstruct the source's pedagogical model, compare it with LLM Lab's canonical concept graph and learning route, and record justified changes.

## 1. Method and evidence boundary

This is a reconstruction of the article's teaching structure, not a graph supplied by its author. Nodes and edges below are inferred from the article's sections and explanations. The article body is available through indexed DEV content in this review; the source remains `partially-scanned` because current direct-page retrieval, embedded media, publication metadata and reuse rights have not all been verified. The article's figure is not visually inspected and is not represented as a verified asset node.

The reconstruction separates:
- **domain concepts and computational objects** (what the mechanism contains);
- **process relations** (how the computation transforms them);
- **pedagogical anchors** (examples and learner motivations);
- **learning order** (the order in which the article introduces the material).

The article does not state formal prerequisites or explicit measurable learning outcomes. Those are inferred cautiously from its explanations.

## 2. Reconstructed source knowledge graph

### 2.1 Computational subgraph

```mermaid
flowchart LR
    X["Input representations X"]
    WQ["Learned W_Q"] --> Q["Queries Q"]
    WK["Learned W_K"] --> K["Keys K"]
    WV["Learned W_V"] --> V["Values V"]
    X --> Q
    X --> K
    X --> V
    Q --> S["Scores S = QKᵀ"]
    K --> S
    S --> SCALE["Scale by √d_k"]
    MASK["Optional causal mask"] --> SOFTMAX["Softmax"]
    SCALE --> SOFTMAX
    SOFTMAX --> A["Attention weights A"]
    A --> AGG["Weighted aggregation A V"]
    V --> AGG
    AGG --> O["Head output O_i"]
    O --> CONCAT["Concatenate head outputs"]
    HEADS["Other head outputs O_j"] --> CONCAT
    CONCAT --> WO["Output projection W_O"]
    WO --> H["Multi-head output representation"]
```

Interpretation:
- The same input representation stream is projected into three learned spaces.
- Q and K jointly determine the score matrix; V supplies the vectors combined by the resulting weights.
- Scaling and softmax transform raw scores into normalized weights; a causal mask restricts which positions are accessible.
- Weighted aggregation produces an output representation. In multi-head attention, several head computations run in parallel, then their outputs are concatenated and projected.
- The diagram is a conceptual reconstruction. It does not encode tensor batch dimensions, residual connections, normalization, the feed-forward sublayer, or a full Transformer block.

### 2.2 Pedagogical anchors

| Anchor | Learner difficulty it targets | Role in the source |
|---|---|---|
| `bank` in financial vs river contexts | A token's interpretation depends on surrounding context | Motivates contextual interaction between positions |
| `it` → `the animal` | A token may depend on another position to construct a useful representation | Illustrates a cross-position dependency |
| Search / document retrieval analogy | Distinguishing what is requested, what is matched, and what content is returned | Gives an intuitive entry point for Q, K and V |
| Winner-take-all contrast | Mistaking attention for selecting one highest-scoring token | Emphasizes weighted aggregation over multiple Values |

The examples are illustrations of why contextual processing is useful. They do not demonstrate that an individual attention head performs complete lexical disambiguation or coreference resolution.

## 3. Reconstructed source learning route

The article's six numbered sections imply the following local sequence:

```mermaid
flowchart TD
    A["1. Identify Q, K and V roles"]
    B["2. Motivate attention with contextual examples"]
    C["3. Generate learned projections"]
    D["4. Compute QKᵀ scores"]
    E["5. Scale scores and apply softmax / mask"]
    F["6. Aggregate Values into an output"]
    G["7. Extend to multi-head attention"]
    A --> B --> C --> D --> E --> F --> G
```

The article actually introduces the role analogy before its contextual examples; both together form its motivation stage. The route is therefore best read as:

1. Name the three roles and give an intuitive analogy.
2. Explain why tokens need contextual information, using lexical ambiguity and pronoun reference.
3. Show how learned projections produce Q, K and V.
4. Follow the score → scale → softmax → weighted aggregation pipeline.
5. Generalize one attention computation to multiple heads.

### Inferred learning outcomes

After reading, a learner should be able to:
- distinguish the functional roles of Q, K and V;
- explain that Q, K and V are learned projections of input representations;
- write the core score, scaling, softmax and aggregation equations;
- explain why attention combines multiple Value vectors rather than selecting one token;
- describe, at a high level, how multiple heads are combined.

### What the source route leaves implicit or outside scope

- No explicit prerequisite list, learning-outcome checklist or retrieval-practice activity.
- No worked numerical example or tensor-shape walkthrough.
- The causal mask is mentioned briefly rather than developed as a separate mechanism.
- No detailed account of cross-attention, residual paths, normalization, the MLP or the complete Transformer block.
- No implementation or experiment is provided.
- Backpropagation is mentioned as the way the projection matrices are learned, but the optimization path is not developed.
- KV-cache is not part of the article's numbered exposition; it appears only in a reader comment and is tracked separately.

## 4. LLM Lab's current model

### 4.1 Canonical concept graph before this comparison

The relevant existing nodes are:
- `query`, `key`, `value`;
- `self-attention`;
- `causal-mask`;
- `positional-encoding`;
- `contextualized-representation`;
- `softmax`.

Existing relations already express Q/K/V as parts of self-attention, the causal mask as a constraint, positional information as a contribution, and self-attention as a contributor to contextualized representations.

The relevant pre-change subgraph can be summarized as follows:

```mermaid
flowchart LR
    Q["Query"] --> SA["Self-attention"]
    K["Key"] --> SA
    V["Value"] --> SA
    CM["Causal mask"] -. constrains .-> SA
    PE["Positional encoding"] -. contributes .-> SA
    TE["Token embedding"] --> CR["Contextualized representation"]
    SA --> CR
    CR --> OP["Output projection"] --> L["Logits"] --> SM["Softmax"] --> CE["Cross-entropy"]
```

This is a coarse lifecycle graph, not an explicit attention-computation graph: it skips the score, scaling, normalized-weight and weighted-aggregation intermediates.

The graph does not yet give distinct canonical identities to the score matrix, normalized attention weights, the scaled-dot-product operation, or multi-head attention. These are nevertheless explicitly taught by the published pages.

### 4.2 Canonical learner route

The current conceptual route is deliberately broader than the article:

`contextualized representations → Transformer overview → Q/K/V → scaled dot-product attention → causal masking`

The reader-facing computation stage in `data/guided-route.yml` groups the Transformer overview, Q/K/V, scaled attention and causal masking under one objective: connect projections, weights, aggregation and masking. The implementation route is separate and reaches the multi-head implementation in the Transformer-block walkthrough.

### 4.3 Existing depth and learning supports

| Dimension | Existing LLM Lab treatment |
|---|---|
| Context motivation | Dedicated contextualized-representations lesson with both lexical ambiguity and cross-position pronoun reference |
| Q/K/V roles | Dedicated bilingual page; learned projections, dimensions, role separation, self-/cross-attention boundary and misconception checks |
| Score and weight pipeline | Dedicated bilingual attention lesson; matrix shapes, explicit scaling, additive mask formulation, numerical worked example and a numerical workbench |
| Causal masking | Separate bilingual lesson and explicit route step |
| Multi-head attention | Conceptual overview in Transformer page; concrete tensor splitting and output projection in the implementation walkthrough |
| Retrieval practice | Self-checks and exercises |
| Mathematical depth | Derivation of the scaling factor and softmax saturation behavior |
| Implementation | Separate Build route with inspectable tensor shapes and tests |

## 5. Differential comparison

| Dimension | DEV article | LLM Lab | Assessment |
|---|---|---|---|
| Entry point | Short Q/K/V analogy, then contextual examples | Contextual representations and Transformer orientation precede Q/K/V | Different scales; the project's system-first route is coherent |
| Motivation | Two compact linguistic examples in one article | Examples live in the contextualization lesson and link forward to Q/K/V | Already integrated; retain the cross-link rather than duplicate examples |
| Q/K/V intuition | Concise role descriptions | Role separation plus explicit learned-projection framing and boundaries | Project is more precise; article's brevity is useful but not a missing concept |
| Computation sequence | Scores → scaling → softmax → weighted Values | Same sequence, with shapes, mask semantics, numerical example and derivation | Project has materially greater explanatory depth |
| Causal mask | Brief mention in the softmax section | Separate concept and lesson | Project's separation is better for scope and mastery |
| Multi-head attention | Compact final section | Overview and separate implementation treatment | Project intentionally distributes this by depth |
| Prerequisites | Implicit | Explicit upstream route through representations and Transformer | Project is stronger |
| Practice | No explicit self-check in the article | Self-checks, exercises and numerical workbench | Project is stronger |
| Concept graph | Reconstructed here from prose | Canonical YAML graph, bilingual stable IDs and typed relations | Project's graph is authoritative but under-represents intermediate attention objects |
| Visual | User identified a potentially stronger illustration; exact asset still unavailable | Existing project diagrams are present | No visual judgement until the exact original asset is retrieved and inspected |

## 6. Graph changes justified by the comparison

The article does not justify importing its content wholesale. It does expose a mismatch between LLM Lab's own lesson structure and its concept graph: the canonical attention lesson carefully distinguishes raw scores, normalized weights and the attention operation, but the concept graph collapses these into the broad `self-attention` node.

The following reusable concepts are therefore added to the canonical graph, with bilingual labels/definitions and links to their existing teaching pages:

| Concept ID | Why it deserves a stable node | Canonical resources |
|---|---|---|
| `attention-score` | Raw query–key compatibility values are distinct from normalized weights | FR/EN scaled-dot-product-attention |
| `attention-weight` | Normalized, mask-conditioned coefficients are distinct from raw scores and Value vectors | FR/EN scaled-dot-product-attention |
| `scaled-dot-product-attention` | The complete score → scale → normalize → aggregate operation is a reusable mechanism used beyond this article | FR/EN scaled-dot-product-attention |
| `multi-head-attention` | Parallel attention heads and their output projection are a durable architectural mechanism | FR/EN Transformer overview and Transformer-block walkthrough |

Existing `softmax` and `causal-mask` concepts are associated with the scaled-attention lesson as well as their current canonical pages. Typed relations connect Q/K/V and the score/weight objects to scaled-dot-product attention, softmax to attention weights, the causal mask to the attention operation, and single-head attention to the multi-head composition.

These additions do **not** create new pages, duplicate explanations, or change the reader-facing route. They make the graph reflect distinctions already taught by LLM Lab. The graph remains a semantic model; the learning route remains a separate pedagogical sequence.

## 7. Route decision

**No change to the six-stage guided route or the page-level suggested route is warranted by this source.**

Reasons:
- The article is a short local tutorial, not a complete curriculum.
- Its section order is already covered across the contextualization, Transformer, Q/K/V and scaled-attention lessons.
- LLM Lab deliberately separates conceptual understanding, optional depth and implementation.
- Moving multi-head attention into the core Q/K/V page would blur page ownership and duplicate the Transformer overview / Build treatment.
- Repeating the `bank` and `it` examples in Q/K/V would duplicate the contextualized-representations lesson.

The article remains useful as an optional beginner-oriented alternative explanation. The canonical route should retain the existing system-first progression.

## 8. Workflow improvements

For tutorial/course/article sources, the extraction workflow should now explicitly reconstruct:
1. the source's local concept/process graph, with typed nodes and relations;
2. its teaching sequence, prerequisites and inferred learning outcomes;
3. its examples, analogies, checks and omissions;
4. the current project's corresponding concept subgraph and canonical route;
5. the difference between semantic graph edges and pedagogical route edges;
6. candidate improvements with an explicit accept/defer/reject decision.

Do not add every source node to the canonical graph. Add only stable concepts or relations that expose a durable gap in LLM Lab's model. Do not copy the source's route into the project's route without demonstrating a learner benefit. Record when a source changes the graph, the route, both, or neither.

## 9. Decision summary

- **Graph:** enriched with four stable concepts and typed relations for distinctions already taught but previously absent from the canonical concept registry.
- **Route:** intentionally unchanged; current staged and depth-separated route is more complete and already incorporates the useful contextual examples.
- **Pages:** no new page and no duplicated example.
- **Source:** remains partially scanned; exact article image and reuse rights remain unresolved.
- **Traceability:** this comparison is linked from the source review and extraction hand-off.
