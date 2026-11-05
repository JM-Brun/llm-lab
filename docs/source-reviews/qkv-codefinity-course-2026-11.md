# Source review — Codefinity, “Queries, Keys, and Values: The Building Blocks”

**Source ID:** `codefinity-qkv-building-blocks`  
**Creator/publisher:** Codefinity  
**Source type / language / audience:** Course lesson / English / introductory lesson within a course labelled Advanced  
**Review date:** 2026-11-05  
**Canonical URL:** https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b

## 1. Scope, provenance and scan status

The lesson page was directly opened and rechecked on 2026-11-05. The page reader exposed the lesson title, introductory paragraph, definition, bank/river example, explanatory recap, one four-option multiple-choice check, and its position as Section 1 / Chapter 2 of *Neural Network Attention Mechanisms*. It also resolved the two inline image references to versioned CDN URLs: a Note/definition icon and a question-mark icon. These are interface/section icons, not explanatory Q/K/V figures. The parent course overview was also directly inspected: it labels the course Advanced, reports three modules, ten chapters and ten assignments, and exposes the complete chapter-title outline. The other lesson bodies and assignments were not inspected.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored lesson text | partially inspected | Visible text from introduction through the knowledge check | JavaScript-dependent course; complete runtime and any hidden text not inspected |
| Figures/media | Two interface SVGs identified by exact CDN URL; bytes not inspected | “Note” icon: `https://cdn.codefinity.com/master/f42d6a4a7b49c3a3f94ea4c125d3d5938acf2e8f/_next/static/media/definition.c461b802.svg?q=75&w=64`; question-mark icon: `https://cdn.codefinity.com/master/f42d6a4a7b49c3a3f94ea4c125d3d5938acf2e8f/_next/static/media/question-blue-sign-rounded.5e7468bd.svg?q=75&w=64` | The page reader rejected both SVG responses because of the `image/svg+xml` content type; visual content, creator and licence remain uninspected |
| Code/data | not exposed | No code or data visible in retrieved lesson | Wider course may contain interactive tasks |
| Comments/community | not exposed | No comments visible | Absence cannot be inferred |
| Linked resources | not inspected | No technical outbound references exposed | Full DOM not available |
| Metadata/version | partial | Course, section and lesson identifiers; course title; parent course level and outline | Publication/update date and revision unknown; other lesson bodies not inspected |
| Licence/reuse rights | unknown | No licence statement established | Text and figures remain link-only |

**Overall status: partially-scanned.** The lesson text exposed by the page reader was reviewed, but the interactive environment, media, broader course sequence, links and rights were not.

## 2. Atomic contribution inventory

The complete structured extraction is [`data/extractions/codefinity-qkv-building-blocks.yml`](../../data/extractions/codefinity-qkv-building-blocks.yml).

| Item | Contribution | Technical status | Pedagogical value | Disposition |
|---|---|---|---|---|
| Role definitions | Q seeks, K offers matching representation, V carries aggregated content | Correct at introductory level | Low complementarity; existing lesson is more precise | Already covered |
| Geometric alignment | Q/K as vectors whose alignment contributes to compatibility | Qualitative in source; project-authored bridge now supplies the dot-product geometry and its limits | High complementarity with the index-card analogy when bounded mathematically | Integrated as optional bilingual note |
| Bank/river example | Lexical polysemy: riverbank vs financial institution | Illustrative, not empirical; differs from the Q/K/V page’s pronoun-coreference example | High complementarity as a contrast between two context-dependent language phenomena; full bank treatment remains elsewhere | Integrated by reference in bilingual contrast |
| Multiple-choice check | Distractors distinguish the roles of Q, K and V | Visible question; feedback behaviour unknown | Moderate as an assessment-design reference | Integrate by reference |
| Scope boundary | No equations or detailed attention computation in retrieved lesson | Accurate for inspected text only | High value for source curation | Integrate by reference |

## 3. Technical assessment

### Correct and useful

- Q, K and V are distinct vector representations with complementary roles.
- A query is compared with keys; values provide the content that is aggregated using attention weights.
- The lesson correctly emphasizes that all three roles are needed for matching and information transfer.

### Claims requiring qualification

- **Geometric alignment:** the source says alignment between Q and K controls information flow. This is a qualitative picture, not a definition of cosine similarity. In scaled dot-product attention, compatibility scores are computed using dot products, scaled, normalized with softmax (subject to masking), and used to form a weighted sum of V. A larger geometric alignment is not itself a direct semantic-relevance measurement.
- **Bank example:** the river interpretation is a useful illustration of lexical ambiguity. It does not show that a specific model or head detects the river sense, nor that one value is hard-selected. Standard attention combines accessible value vectors according to a distribution of weights.
- **Value wording:** describing V as the “actual content” is a beginner-friendly contrast with matching, but V is still a learned numerical representation, not raw text or a human-readable semantic payload.

### Scope not covered in the retrieved lesson

No projection equations, dimensions, score computation, scaling, softmax, weighted-sum derivation, masking, multi-head decomposition, self-/cross-attention distinction, implementation or numerical example were exposed. This is a limitation of the inspected lesson text, not proof that the broader Codefinity course omits those topics.

## 4. Source-local knowledge model

The lesson's reconstructed source graph is intentionally small:

`Q leftrightarrow K` matching → compatibility/alignment → attention contribution of `V`.

The bank/river sentence motivates contextual lexical ambiguity, while the quiz tests whether the learner can distinguish the key role from the query and value roles. These are editorially reconstructed relationships, not a formal ontology authored by Codefinity. The graph and ordered teaching route are recorded in the extraction.

## 5. Teaching route

**Observed route:** short motivation → vector-role definition → bank/river example → one multiple-choice check → explanatory recap.

The route is concise and question-led. It does not expose a derivation or implementation sequence. The quiz's distractors are useful because they target role confusion directly, but the available evidence does not show whether the platform gives explanatory feedback or tracks mastery.

## 6. Course-level route comparison

The parent course overview places the target lesson in this sequence:

1. **Foundations of Attention:** motivation → Q/K/V → relevance scoring.
2. **Self-Attention and Multi-Head Attention:** contextual representations → scaling/softmax → multi-head attention → causal/padding masks.
3. **Attention Inside Transformers:** block placement → self-/cross-attention → long-range reasoning and interpretability.

The course declares an Advanced level, while this particular lesson uses an introductory explanatory style. This is why the source catalogue classifies its technical level as mixed rather than assuming the lesson is advanced from the course label.

The local sequence is compatible with LLM Lab's separation of the Q/K/V projections from the subsequent scaled-dot-product-attention computation. The later module ordering differs from LLM Lab's broader prerequisite-oriented route, but the overview alone does not provide enough instructional detail to justify adopting it. Course-level titles are not evidence of prerequisite relations.

## 7. Differential comparison with LLM Lab

| Learner question | Codefinity treatment | Existing project treatment | Gap or complementarity | Decision |
|---|---|---|---|---|
| What does each vector do? | Search / offer-to-match / information passed | Index-card analogy plus learned projections and explicit Q/K vs V distinction | Rephrasing, not a new model | Already covered |
| How can Q/K matching be pictured numerically? | Geometric alignment of Q and K vectors | Index-card analogy on the Q/K/V page; dot-product/scaling/softmax on the next page | Adds a spatial lens and bridges role intuition to vector algebra | Integrated as a collapsible geometric view, explicitly bounded against cosine similarity and nearest-neighbour interpretations |
| What kinds of language phenomena need context? | “bank” in a riverside sentence (lexical polysemy) | Q/K/V page uses pronoun coreference; contextualized-representations has the fuller bank example | Distinct phenomena: competing senses of one word versus competing antecedents for a pronoun | Integrated as a compact contrast; link to the canonical bank discussion rather than duplicating it |
| How do I check the key role? | One multiple-choice question with role-confusion distractors | Existing bilingual QKV self-check and extended exercises | Potential assessment-design reference, not missing content | Integrate by reference |
| How is attention calculated? | Not in the retrieved text | Dedicated scaled-dot-product-attention lesson | Project has deeper, more rigorous treatment | No change |

### Comparison across the three structures

- **Semantic knowledge graph:** no missing canonical concept or relation identified.
- **Pedagogical route:** Codefinity uses a compact local sequence; it does not justify changing the canonical route.
- **Site navigation:** no new page, sidebar item, prerequisite edge or route card is justified.

## 8. Integration decision and actual learning-system changes

The source does not add a new canonical mechanism, but it does add two complementary teaching contributions. The first review incorrectly treated the bank example as simply redundant and the geometric framing as a deferred idea. The differential comparison now distinguishes topic overlap from explanatory function.

1. **Geometric Q/K perspective — integrated.** The bilingual Q/K/V pages now include an optional collapsible note that links the geometric intuition to the dot product, explains that both vector norms and angle matter, and connects scores to scaling, softmax and weighted aggregation. It explicitly rules out equating dot product with cosine similarity or interpreting attention as hard nearest-neighbour retrieval. This adds a spatial lens alongside the existing index-card analogy without replacing the formal next lesson.
2. **Lexical polysemy — integrated by reference.** The Q/K/V pages now contrast Codefinity’s *bank* example (competing senses of one word) with Neha KK’s pronoun example (competing antecedents / coreference). The comparison teaches that context-dependent language phenomena are not all the same task. It links back to the fuller contextualized-representations lesson rather than duplicating its bank discussion.
3. **Q/K/V role definitions — already covered.** The existing page has the clearer formulation, learned projections and dimensions.
4. **Multiple-choice distractors — retained as an assessment-design reference.** The existing self-check and exercises make a new quiz unnecessary now.

- **Concept graph:** no change; no durable concept or relation is missing.
- **Bilingual pages:** updated with two optional, attributed perspectives.
- **Learning routes/navigation:** no change; optional depth does not create a new prerequisite.
- **Exercises/experiments:** no new activity; quiz pattern remains available for future exercise revision.
- **Build/implementation:** no change.
- **Visual assets:** no source image copied; original media remains uninspected and rights unknown.
- **New pages:** none.

## 9. Validation, provenance and open work

- The source is registered in `data/sources.yml` and its atomic items are in the extraction YAML.
- The Q/K/V source collection index links this review and extraction.
- The parent course overview was inspected for module/chapter titles only; no content from the other lessons or assignments is attributed to the target lesson.
- The linked images remain uninspected; no reuse rights are established.
- The wider course sequence and interactive quiz feedback remain uninspected.
- No CI, Quarto render, link check or visual browser validation is claimed by this source review.

**Conclusion:** Codefinity’s most useful contribution is not a new Q/K/V definition. It is a complementary geometric explanation and a second kind of language example. These are now integrated into the existing bilingual lesson in bounded optional sections, while the canonical graph and learning route remain stable.
