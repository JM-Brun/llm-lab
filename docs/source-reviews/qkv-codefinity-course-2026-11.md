# Source review — Codefinity, “Queries, Keys, and Values: The Building Blocks”

**Source ID:** `codefinity-qkv-building-blocks`  
**Creator/publisher:** Codefinity  
**Source type / language / audience:** Course lesson / English / introductory learner  
**Review date:** 2026-11-05  
**Canonical URL:** https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b

## 1. Scope, provenance and scan status

The lesson page was directly opened. The page reader exposed the lesson title, introductory paragraph, definition, bank/river example, explanatory recap, one four-option multiple-choice check, and its position as Section 1 / Chapter 2 of *Neural Network Attention Mechanisms*.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored lesson text | partially inspected | Visible text from introduction through the knowledge check | JavaScript-dependent course; complete runtime and any hidden text not inspected |
| Figures/media | identified, not inspected | Two image slots exposed in page text | Image retrieval failed; no bytes, visual composition, creator or licence inspected |
| Code/data | not exposed | No code or data visible in retrieved lesson | Wider course may contain interactive tasks |
| Comments/community | not exposed | No comments visible | Absence cannot be inferred |
| Linked resources | not inspected | No technical outbound references exposed | Full DOM not available |
| Metadata/version | partial | Course, section and lesson identifiers; course title | Publication/update date and revision unknown |
| Licence/reuse rights | unknown | No licence statement established | Text and figures remain link-only |

**Overall status: partially-scanned.** The lesson text exposed by the page reader was reviewed, but the interactive environment, media, broader course sequence, links and rights were not.

## 2. Atomic contribution inventory

The complete structured extraction is [`data/extractions/codefinity-qkv-building-blocks.yml`](../../data/extractions/codefinity-qkv-building-blocks.yml).

| Item | Contribution | Technical status | Pedagogical value | Disposition |
|---|---|---|---|---|
| Role definitions | Q seeks, K offers matching representation, V carries aggregated content | Correct at introductory level | Low complementarity; existing lesson is more precise | Already covered |
| Geometric alignment | Q/K as arrows whose alignment controls information flow | Qualitative only; score function unspecified | Moderate alternative intuition, with risk of implying cosine/nearest-neighbour matching | Defer |
| Bank/river example | Lexical ambiguity contextualized by river-related information | Illustrative, not empirical | Low; same example already exists in canonical contextualization lesson | Already covered |
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

## 6. Differential comparison with LLM Lab

| Learner question | Codefinity treatment | Existing project treatment | Gap or complementarity | Decision |
|---|---|---|---|---|
| What does each vector do? | Search / offer-to-match / information passed | Index-card analogy plus learned projections and explicit Q/K vs V distinction | Rephrasing, not a new model | Already covered |
| How does matching look geometrically? | Arrows in high-dimensional space; alignment | Formal dot-product score, scaling, softmax and weighted aggregation on the next page | Alternative visual intuition, but incomplete and easy to overread | Preserve in extraction; defer publication |
| How does context disambiguate a word? | “bank” in a riverside sentence | Bank ambiguity already appears in contextualized-representations; QKV page separately uses pronoun reference | Same example is already represented; the pronoun example serves a distinct cross-position learner difficulty | No page edit |
| How do I check the key role? | One multiple-choice question with role-confusion distractors | Existing bilingual QKV self-check and extended exercises | Potential assessment-design reference, not missing content | Integrate by reference |
| How is attention calculated? | Not in the retrieved text | Dedicated scaled-dot-product-attention lesson | Project has deeper, more rigorous treatment | No change |

### Comparison across the three structures

- **Semantic knowledge graph:** no missing canonical concept or relation identified.
- **Pedagogical route:** Codefinity uses a compact local sequence; it does not justify changing the canonical route.
- **Site navigation:** no new page, sidebar item, prerequisite edge or route card is justified.

## 7. Integration decision

**No published-page or canonical-graph edit is justified.** The bank example is already present in the project's contextualized-representations treatment and the current Q/K/V page has a separate pronoun-context example. Adding Codefinity's role definitions or another search analogy would stack explanations without a distinct learner benefit.

The geometric framing is retained as a candidate alternative mental model, not published yet: a future use would need to connect vector intuition to dot-product scores, scaling, softmax and weighted aggregation, while explicitly rejecting the inference that attention is cosine similarity or hard nearest-neighbour retrieval.

The quiz is retained as an assessment-design reference. It may inform a future revision of distractors, but the existing self-check and extended exercises make a new quiz unnecessary now.

- **Concept graph:** no change.
- **Pages:** none.
- **Learning routes/navigation:** none.
- **Exercises/experiments:** none.
- **Build/implementation:** none.
- **Visual assets:** none; no source image copied.
- **New pages:** none.

## 8. Validation, provenance and open work

- The source is registered in `data/sources.yml` and its atomic items are in the extraction YAML.
- The Q/K/V source collection index links this review and extraction.
- The linked images remain uninspected; no reuse rights are established.
- The wider course sequence and interactive quiz feedback remain uninspected.
- No CI, Quarto render, link check or visual browser validation is claimed by this source review.

**Conclusion:** Codefinity contributes a concise beginner-facing formulation and a role-confusion quiz, but no unique technical content or unfilled pedagogical gap relative to the current LLM Lab Q/K/V and contextualization lessons. Its useful alternative framing is preserved for future synthesis without increasing the published curriculum.
