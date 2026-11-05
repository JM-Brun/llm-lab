# Q/K/V — complementary explanatory perspectives

**Status:** active synthesis dossier  
**Review date:** 2026-11-05  
**Canonical pages:** [Q/K/V (FR)](../../site/fr/queries-keys-values.qmd) · [Q/K/V (EN)](../../site/en/queries-keys-values.qmd) · [Contextualized representations (FR)](../../site/fr/contextualized-representations.qmd) · [Scaled dot-product attention (FR)](../../site/fr/scaled-dot-product-attention.qmd)

## 1. Learning question and scope

How can a learner understand what queries, keys and values do, and why contextual attention can use information from other positions?

This dossier compares explanatory contributions, not only technical topic coverage. The goal is to combine distinct intuitions and examples into a coherent lesson without turning the page into a list of source summaries.

## 2. Canonical coverage before this integration

The Q/K/V page already taught:

- an **index-card/search analogy** for distinguishing query, key and value;
- learned projections from a common input representation, with dimensions;
- the distinction that Q/K determine weights while V supplies the aggregated content;
- a **pronoun-coreference example** to motivate contextual information flow;
- a hand-off to the next page for dot-product scores, scaling, softmax and weighted aggregation;
- warnings against treating attention as literal symbolic search, nearest-neighbour retrieval, or a universal semantic-relevance measure.

The contextualized-representations page already used lexical ambiguity (the word *bank*) to motivate context-dependent meaning. The same example was therefore not new at the project level, but its pedagogical role had not been compared with the pronoun example on the Q/K/V page.

## 3. Source contribution map

| Source | Extracted item(s) | Explanatory lens | Learner question | Distinct value | Limits |
|---|---|---|---|---|---|
| Neha KK, [Understanding QKV](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b) | Existing extraction: pronoun example | Linguistic / coreference | Which earlier token or entity does a pronoun refer to? | Makes cross-position reference and contextual information flow concrete | Illustrative only; no measured model/head/weights |
| Nishanthan K, [How QKV Work](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a) | Existing extraction: visual and card/search framing | Diagrammatic / functional | How do Q, K and V play different roles? | Gives a compact role-oriented visual narrative | Media provenance and reuse rights remain unresolved |
| Codefinity, [Queries, Keys, and Values](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b) | [Geometric alignment](../../data/extractions/codefinity-qkv-building-blocks.yml) · [Bank polysemy](../../data/extractions/codefinity-qkv-building-blocks.yml) · quiz distractors | Geometric / lexical polysemy / formative assessment | How can vector matching be pictured? How can context disambiguate one word with multiple senses? | Bridges conceptual Q/K roles to vector geometry; contrasts lexical polysemy with coreference | Geometry is qualitative in the source; bank example is illustrative, not model evidence |

## 4. Synthesis: what each perspective contributes

### 4.1 Functional analogy and vector geometry answer different questions

The index-card analogy answers **what the roles are**: Q asks, K is compared, V carries the content to be combined.

The geometric perspective answers **what kind of objects are being compared**: Q and K are numerical vectors, and their dot product is influenced by both angle and magnitude:

[
q^	op k = lVert qVert,lVert kVertcos(	heta).
]

This distinction matters. Describing vectors as “aligned” can tempt the learner to think only about angle or cosine similarity. The dot product is not generally cosine similarity because the vector norms also matter. In scaled dot-product attention, scores are divided by \\(\sqrt{d_k}\\), normalized with softmax over accessible keys, and used to weight values. No hard nearest-neighbour selection is implied.

**Integration:** the geometric perspective is an optional, collapsible note on both Q/K/V pages. It is attributed to Codefinity but rewritten in original project language and mathematically bounded. The original Codefinity figure was not reused: it was not visually inspected and its reuse rights are unknown.

### 4.2 Coreference and lexical polysemy are complementary examples

The two examples share a broad theme—context affects interpretation—but teach different phenomena:

| Example | Ambiguity type | Learner focuses on |
|---|---|---|
| “The animal didn't cross the road because it was tired.” | Coreference | Competing antecedents for a pronoun |
| “He sat by the bank,” in a river context | Lexical polysemy | Competing senses of one word |

Treating both as merely “the bank example already exists” would miss their different teaching functions. The contrast helps learners transfer the idea of contextual information flow beyond one linguistic task.

**Integration:** a compact optional comparison appears on both Q/K/V pages. The full bank discussion remains owned by contextualized-representations and is linked rather than duplicated. Both examples are explicitly labelled illustrative; neither is evidence that a particular attention head alone performs the linguistic task.

### 4.3 Assessment design

Codefinity's single multiple-choice question targets confusion between query, key and value. LLM Lab already has a self-check and extended exercises, so a new quiz would duplicate the activity. The useful part to retain is the distractor principle: test whether learners confuse the search representation, matching representation and transmitted content.

**Integration:** keep as a source-linked design reference for the next exercise revision; no new quiz now.

## 5. Convergence, differences and evidence

- The sources converge on the high-level functional split between Q/K matching and V aggregation. This is pedagogical convergence, not independent empirical confirmation.
- The sources differ in explanatory lens: index-card analogy, vector geometry, pronoun coreference and lexical polysemy.
- None of the tutorial examples demonstrates the internal behaviour of a measured model or a specific attention head.
- The geometric intuition is useful only when connected to the actual dot-product calculation and bounded against cosine-similarity / nearest-neighbour misconceptions.
- The parent Codefinity course outline places Q/K/V between attention motivation and relevance scoring, then covers self-attention, scaling/softmax, multi-head attention, masking, encoder/decoder placement, cross-attention and interpretability. Only the outline was inspected; the other lesson bodies and assignments were not scanned.

## 6. Integration decisions

| Contribution | Destination | Decision |
|---|---|---|
| Functional Q/K/V definitions | Existing canonical page | Already covered; retain source provenance only |
| Geometric Q/K lens | Q/K/V FR/EN, optional collapsed note | Integrated |
| Bank lexical-polysemy example | Q/K/V FR/EN contrast with coreference; full treatment remains contextualized-representations | Integrated by reference |
| Pronoun coreference example | Q/K/V FR/EN | Retained as a distinct example |
| Q/K/V role-confusion distractors | Exercise design backlog | Reference; revisit when exercises are next revised |
| Codefinity media | Asset register / future audit | Not reused; inspect actual image and rights before any reuse |
| Canonical graph and learning route | — | No change justified |

## 7. Current result and remaining opportunities

The bilingual Q/K/V pages now offer a layered explanation:

1. **Core intuition:** index-card analogy.
2. **Optional alternative lens:** geometric view of query-key compatibility, with a precise dot-product qualification.
3. **Contextual transfer:** coreference versus lexical polysemy.
4. **Formal next step:** scaled dot-product attention on the following page.

No new page, concept, graph edge or prerequisite is introduced. This is deliberate: the new value is explanatory complementarity, not ontology growth.

Potential next work, only if later sources justify it:

- add a numerical vector example that contrasts dot product and cosine similarity;
- inspect and compare the original Codefinity figure with other Q/K/V visual explanations;
- compare quiz distractors across sources and revise the existing exercise set;
- inspect further course chapters only if their full content can be accessed, not infer their substance from titles.

## 8. Traceability

- Codefinity source review: [qkv-codefinity-course-2026-11](../source-reviews/qkv-codefinity-course-2026-11.md)
- Codefinity extraction: [codefinity-qkv-building-blocks.yml](../../data/extractions/codefinity-qkv-building-blocks.yml)
- Living source collection: [qkv-source-collection](../source-reviews/qkv-source-collection.md)
- Workflow: [external-source integration](../workflows/source-to-learning-system-integration.md)
