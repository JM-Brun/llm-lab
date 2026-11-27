# Understand course redesign — lesson and knowledge migration ledger

**Status:** editorial migration specification; no source lesson content is deleted or moved by this document.  
**Baseline:** data/guided-route.yml and the bilingual pages in site/fr/ and site/en/.  
**Target:** a genuinely linear course of coherent 10–15-minute lessons, grouped into chapters. The chapter is an orientation/grouping unit; the lesson is the unit of learning.  
**Related architecture:** [canonical computational spine](canonical-computational-spine.md), [content ownership map](content-section-mapping.md), [knowledge-preservation ledger](knowledge-preservation-ledger.md), [reader experience and editorial method](reader-experience-and-editorial-method.md).

## 1. Non-negotiable preservation rule

A shorter lesson is acceptable only if the complete useful knowledge remains available in an intentional destination. **No section, example, figure, caveat, exercise, source, or implementation reference is deleted merely to meet a duration target.**

Before changing a source page, create a section-level inventory. Every meaningful item receives exactly one primary disposition:

- **KEEP** — retain in the lesson because it is needed for the lesson outcome.
- **SYNTHESIZE** — merge into the canonical synthesis page for the same concept. Preserve distinct claims, assumptions, caveats, examples and references; link back from the source lesson.
- **DEEPEN** — move to an existing or newly created Deepen page. The destination must be available and linked before the source section is removed.
- **PRACTICE** — move exercises, questions, calculations and experiments to the dedicated Practice companion. The lesson retains a quiet link at the relevant point and at its end.
- **BUILD** — move implementation walkthroughs, API details and code-specific tests to the corresponding Build resource. Keep the minimum conceptual explanation in Understand.
- **REFERENCE** — move chronology, bibliographic catalogues or lookup-only material to the relevant reference page.
- **MERGE-INTO-LESSON** — merge genuine duplication into another canonical lesson. Keep a short local reminder only where it prevents a broken transition.
- **VERIFY** — destination or semantic equivalence has not yet been checked. The source material must remain untouched.

VERIFY is a blocking state, not permission to remove content. A destination page with a similar title is not proof that the knowledge has been preserved.

### Preservation evidence required for every move

The migration record must identify:
1. source page, exact heading/anchor and language pair;
2. the knowledge carried by the section (claims, definitions, equations, assumptions, examples, caveats, figures, citations, exercises, code and links);
3. the target page and exact destination heading/anchor;
4. whether the target is an existing canonical synthesis, an existing Deepen page, or a new page that must be created first;
5. the contextual link from the original lesson;
6. bilingual parity and rendered-link checks;
7. a final comparison confirming that no distinct information was lost.

For merged material, compare propositions and qualifications, not just word counts. For figures and code, preserve attribution/licensing and the explanatory role, not merely the file or snippet.

## 2. Reader-facing course: chapters and lessons

The current nine conceptual stages are the **starting chapter proposal**; confirm their boundaries after the lesson content transfers. The route itself is presented as one ordered list of lessons. The route is a pedagogical progression, not a claim that every lesson is a formal prerequisite of the next. In particular, generation, observed-target scoring and parameter learning remain distinct uses of the shared predictive distribution.

| Chapter | Lesson order | Canonical lesson (FR / EN) | Central learning outcome | Target |
|---|---:|---|---|---:|
| 1. Comprendre ce que prédit un LLM | 1 | llm-overview | Explain what is predicted from a context and distinguish the model, its architecture, its parameters and the surrounding application. | 10–15 min |
| 2. Transformer le texte en entrée | 2 | text-data | Trace text → tokens → token IDs and explain what depends on the tokenizer. | 10–15 min |
| 3. Construire les représentations | 3 | embedding-space | Explain lookup from a token ID to its initial vector. | 10–15 min |
|  | 4 | positional-encoding | Explain why position must be represented and distinguish the main families without deriving every variant. | 10–15 min |
|  | 5 | contextualized-representations | Explain why a token's state depends on its position and surrounding context. | 10–15 min |
| 4. Comprendre le calcul du Transformer | 6 | transformer | Locate the repeated decoder block in the forward computation and follow the transformation from initial to final states. | 10–15 min |
|  | 7 | queries-keys-values | Explain the distinct roles of Q, K and V and predict what changes when one projection changes. | 10–15 min |
|  | 8 | scaled-dot-product-attention | Compute one attention output from scores, normalized weights and value vectors. | 10–15 min |
|  | 9 | causal-masking | Determine which positions are allowed to contribute to a causal prediction. | 10–15 min |
| 5. Produire une distribution prédictive | 10 | logits | Explain how a final hidden state becomes one score per vocabulary token. | 10–15 min |
|  | 11 | probabilites / probabilities | Convert logits into a conditional categorical distribution and interpret its normalization. | 10–15 min |
|  | 12 | entropy | Distinguish uncertainty over all candidates from the surprisal of one observed token. | 10–15 min |
| 6. Générer une continuation | 13 | generation | Trace selection, token feedback, stopping, and the distinction between prompt prefill and incremental decode. | 10–15 min |
| 7. Exploiter et concevoir le contexte | 14 | in-context-learning | Explain how supplied examples can affect predictions while parameters remain fixed. | 10–15 min |
|  | 15 | context-engineering | Explain how an application selects and assembles the context actually passed to the model. | 10–15 min |
| 8. Évaluer une séquence observée | 16 | vraisemblance / likelihood | Factorize and score the probability of an observed sequence under an autoregressive model. | 10–15 min |
|  | 17 | cross-entropy | Compute the per-token penalty for an observed target and connect it to negative log-likelihood. | 10–15 min |
| 9. Apprendre les paramètres | 18 | loss | Aggregate valid token-level costs into a batch objective and explain shifted targets and teacher forcing. | 10–15 min |
|  | 19 | gradients | Trace how the objective's derivatives indicate how parameters should change. | 10–15 min |
|  | 20 | training-loop | Trace one update and repeated updates, including the separate role of validation. | 10–15 min |

This preserves the current 20 canonical lesson identities as the starting inventory; it does **not** assert that all current page bodies already meet the duration target. A page may later be split if its single learning outcome remains too broad after all misplaced material has been transferred. Conversely, two genuinely small lessons may be merged only if the combined lesson still has one coherent outcome and stays within 15 minutes.

### Lesson time is measured, not guessed from word count

The repository's deterministic duration estimator is a **screening estimate**, not a substitute for reading the rendered page. It counts required prose, code, equations and visual elements from the source. A Quarto callout is excluded only when it is explicitly marked `data-reading-time="exclude"`; `collapse="true"` controls presentation and does not by itself make content optional. Keep this marker paired in FR/EN and use it only for material genuinely outside the required learning path. After the estimate, review the rendered lesson and the cognitive work required by its figures, notation and worked example before deciding to split, move or retain content.

The 10–15 minutes cover the required lesson path: prose, diagrams, notation, one worked example and the short synthesis/transition. Dedicated exercises, optional Deepen resources and Build walkthroughs are outside that estimate. Estimate time from the actual rendered FR and EN pages, including time to inspect figures and work through equations; do not use raw word count as the sole proxy.

Each lesson must state: one guiding question, one observable outcome, prerequisites actually needed, the minimum explanation, one worked example or diagram, a concise synthesis, a transition explaining why the next lesson follows, and links to its review and Practice companions.

## 3. Section-level migration decisions for the pages most likely to exceed the target

The following is the first migration ledger derived from the current French source headings and the existing page inventory. These are proposed dispositions, not completed moves. Before moving any section, inspect the complete FR and EN section bodies and record the exact destination anchors using the evidence contract in section 1.

### 3.1 llm-overview — retain orientation, not a second course

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| Ce que le modèle prédit; Du texte à la distribution | **KEEP** | The orientation's central question and the shared predictive mechanism. Keep the end-to-end view concise; detailed mechanisms belong to their canonical lessons. |
| Un calcul, trois usages | **KEEP** | Preserve the key distinction between generation, observed-target scoring and training. This is the conceptual map for the later branches. |
| LLM, Transformer, GPT | **KEEP** | Essential vocabulary and scope distinction. |
| Architecture, apprentissage, utilisation | **KEEP / SYNTHESIZE** | Keep the minimum distinction between architecture, parameter learning and fixed-parameter use; link to the corresponding later chapters. |
| Pourquoi la prédiction peut-elle soutenir des tâches variées ? | **SYNTHESIZE** | Keep a concise transfer explanation; place detailed in-context examples in in-context-learning and application context design in context-engineering. |
| Où se trouve l'information ? | **SYNTHESIZE / DEEPEN** | Keep the minimum model-parameters-versus-context distinction; detailed context assembly belongs to context-engineering, adaptation to post-training, and retrieval/memory boundaries to rag-memory-boundaries. |
| Du modèle au système conversationnel | **DEEPEN / SYNTHESIZE** | Preserve the model/application boundary in the overview; move the full system lifecycle to rag-memory-boundaries and document-retrieval where the section's actual content matches those scopes. |
| Choisir une approche | **SYNTHESIZE** | Keep only the decision cues needed to navigate the course; link to transformer-architectures, post-training, document-retrieval and context-engineering for the relevant choices. |

### 3.2 transformer — make it the block-level map, not a duplicate of its component lessons

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| Situer le réseau dans la génération | **KEEP, concise** | Establish where the forward pass sits inside the autoregressive loop; the full loop belongs to generation. |
| Des identifiants aux représentations d'entrée | **SYNTHESIZE** | Keep a compact input/output map; the canonical explanations remain embedding-space and positional-encoding. Do not repeat their derivations. |
| Les blocs Transformer | **KEEP + DEEPEN TRANSFER — 2026-11-24 pilot** | Keep the two sublayer roles, causal access boundary, residual-stream idea and the block's place in the GPT forward pass at overview level. The detailed MLP explanation, residual equation, LayerNorm/Xiong et al. discussion, pre-LN equations and diagram, attention-versus-MLP figure/table, multi-head dimensions and interpretability caveat now have one bilingual owner in `contextualized-representations-advanced` section 3. The Build walkthrough remains implementation-only. |
| Parallélisme à l'entraînement, génération séquentielle | **SYNTHESIZE / DEEPEN** | Keep the essential distinction in one short comparison; move detailed work/dependency/memory analysis to llm-computational-complexity. Link to generation and training-loop. |
| Profondeur et largeur : deux dimensions de l'architecture | **SYNTHESIZE + MOVED — 2026-11-24 pilot** | Keep only the definitions of depth (number of blocks) and width (`d_model`) in the core lesson. The definitions of `d_head`, `d_ff`, the relation between head count and head dimension, and the GPT-2 124M numerical configuration now live in the canonical `tensors` reference. |
| Trois niveaux à ne pas confondre | **KEEP, concise** | Retain the distinction between attention mechanism, Transformer block and complete model; it prevents a central category error. |
| Des représentations aux logits | **SYNTHESIZE** | Keep the transition and one compact flow diagram; the output projection and logits are taught canonically in logits. |
| Lire aussi le schéma fondateur du Transformer; Parcours de lecture guidée | **MOVED — 2026-11-24 pilot** | The historical explanation, comparison table and architecture distinction now live in `transformer-history` under the original `historical-transformer-diagram` anchor. The five guided-reading questions are in the existing FR/EN `exercises/transformer.qmd` Practice companion; the history page links to them. The old anchor remains on the core page and links to the new canonical location. |

### 3.3 generation — preserve the complete conceptual inference path and optional serving depth

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| La boucle sur un exemple; Une étape, en notation | **KEEP** | The core autoregressive loop, including fixed parameters and context feedback. |
| Comment le prochain token est-il choisi ? | **KEEP, concise** | Explain selection at the level required to distinguish the distribution from the decoding policy. Detailed strategies belong to decoding-strategies. |
| Du prompt aux tokens suivants : prefill et decode | **KEEP** | Prefill and incremental decode are required vocabulary for understanding actual inference. Keep the conceptual contrast; avoid implementation-level cache internals. |
| Pourquoi l'inférence semble-t-elle parfois lente ? | **KEEP (optional deep dive)** | The detailed TTFT/ITL diagnosis remains in Generation's collapsed optional deep dive. Keep the quantitative KV-cache memory estimate in `llm-computational-complexity` and link to it; do not duplicate the formula. |
| Servir plusieurs requêtes : ordonnancement et réutilisation du cache | **KEEP (optional deep dive)** | Keep the serving/scheduling explanation in Generation's collapsed optional deep dive: TTFT/ITL/TPOT, continuous batching, prefix caching, chunked prefill and speculative decoding. The canonical ownership map assigns this operational story to Generation; no separate Deepen page is needed for the current scope. |
| Ce que la génération ne fait pas | **KEEP** | Preserve the explicit boundary with scoring and parameter learning. |
| Exercices | **PRACTICE** | Move all questions and solutions to the dedicated generation Practice companion; the lesson keeps a contextual link. |
| Ressources d'implémentation complémentaires | **BUILD** | Keep links to the generation walkthrough and relevant Build milestone; do not duplicate code explanations in Understand. |

### 3.4 cross-entropy — one canonical local objective, no duplicate scoring/training chapter

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| Objectif pour un token; Calcul repris du fil rouge | **KEEP** | Canonical per-token cross-entropy definition and worked example. Preserve notation and assumptions. |
| Quand le token choisi et la cible diffèrent | **KEEP** | Essential distinction between a generated choice and an observed training/evaluation target. |
| Intuition visuelle : la perte mesure la surprise du token observé | **KEEP / SYNTHESIZE** | Keep the visual intuition if it adds a distinct interpretation; avoid duplicating the surprisal definition from entropy and vraisemblance. |
| Lien avec le gradient | **SYNTHESIZE** | Keep the short bridge from token penalty to differentiable objective; the derivative and parameter effects belong to gradients. |
| Plusieurs positions : décalage causal et masques | **SYNTHESIZE** | Keep the minimum explanation of position-wise targets and valid-token reduction in loss; construction of shifted examples, padding and masks belongs to the Build resource training-examples. |
| Lien avec la perplexité | **MOVED — 2026-11-24 pilot** | The canonical sequence-level definition, interpretation and comparison conditions now live in vraisemblance / likelihood. That page also states that mean cross-entropy equals mean NLL for one-hot targets and preserves the base-2 formula. The core lesson retains this exact local relation and links to the sequence-level owner. |
| Idées reçues | **KEEP, selective** | Retain warnings specific to cross-entropy; the perplexity-comparability warning is consolidated with the sequence-level definition in vraisemblance / likelihood. |
| Décomposition en entropie cible et divergence KL; Exemple numérique en nats | **MOVED — 2026-11-24 pilot** | The bilingual derivation now has one canonical owner in language-modeling-math, section 3. The distinct non-degenerate numerical example (q=(0.5,0.5), p=(0.75,0.25)) was added there; the core lesson retains a short contextual link. The one-hot case remains in the core lesson. |
| Implémentations — NumPy, PyTorch et stabilité numérique; dimension, réduction et log-softmax examples | **BUILD / DEEPEN** | Move code/API-specific walkthroughs to the appropriate Build implementation resource; preserve numerical-stability and axis/reduction reasoning in language-modeling-math or a dedicated numerical Deepen section. Do not discard counterexamples or framework-contract warnings. |
| Exercices; Exercices complémentaires | **ALREADY SEPARATE / VERIFY** | The main lesson's Exercices heading already links to the dedicated FR/EN Practice pages at exercises/cross-entropy.qmd; it contains no embedded exercise set to move. Preserve that link. The additional foundations collection remains a separate cross-link and should be checked for destination validity, not copied into the lesson. |
| Références | **KEEP / REFERENCE** | Preserve every source and attribution at the canonical destination; references must follow the claims they support. |

### 3.5 training-loop — teach the learning cycle, not the implementation catalogue

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| Un pas, puis beaucoup; Rejouer un pas sur le premier token; Passer d'une cible à un lot | **KEEP** | One coherent training step: forward computation, objective, gradients, update; then explain repetition over batches. |
| Optimiseur, gradient et taux d'apprentissage | **KEEP, concise** | Define the optimizer's role and learning-rate effect. Detailed optimizer mechanics and comparisons are optional depth. |
| Loss d'entraînement et loss de validation | **KEEP** | Essential distinction between optimization data and held-out monitoring; preserve split assumptions and leakage warning. |
| Le pré-entraînement est la même boucle à grande échelle | **KEEP, concise / DEEPEN** | Keep the conceptual link; move scaling/resource-allocation details to scaling-laws and systems cost details to llm-computational-complexity. |
| Approfondissements; Comparer les optimiseurs | **DEEPEN** | Preserve detailed optimizer comparisons in a dedicated optimizer Deepen resource if no existing canonical destination covers them. Do not place them in the mandatory lesson. |
| Implémentation; Ressources d'implémentation complémentaires; Exemples de workflow complémentaires | **BUILD** | Move implementation steps, APIs, code and workflow walkthroughs to the corresponding Build milestone/resources. Keep only links and the conceptual algorithm in Understand. |
| Pour approfondir | **KEEP as links** | Retain only relevant, verified links; remove dead or duplicate link lists after their destinations are reconciled. |
| Exercises or checks embedded in the source | **PRACTICE** | Move them to the dedicated training-loop Practice companion. |

## 4. First-pass disposition for the remaining core lessons

This inventory identifies the expected boundary; it is not permission to remove a section before its exact content has been checked.

| Lesson | Keep in the 10–15-minute lesson | Candidate transfer (destination must be verified) |
|---|---|---|
| text-data | Text → tokens → IDs; one short comparison showing tokenizer dependence; why tokenization matters. | Unicode internals → unicode-text; algorithms and tokenization trade-offs → tokenization-strategies; tokenizer evaluation → tokenizer-design-evaluation; exercises → Practice companion. |
| embedding-space | Lookup semantics, matrix/vector notation, distinction between initial and contextualized states. | Parameter accounting and geometry → embeddings-deep-dive / tensors; exercises → Practice companion. |
| positional-encoding | Why order matters, where position enters, compact distinction between learned, sinusoidal and rotary families. | Sinusoidal derivation → sinusoidal-positional-encoding; RoPE mechanics → rope; exercises → Practice companion. |
| contextualized-representations | What changes with token position/context; one example showing context dependence; distinction from initial embedding. | Extended geometry/alternative cases → contextualized-representations-advanced; exercises, if present, → Practice companion. |
| queries-keys-values | The three roles, projection from the same block input, and the effect of changing Q/K/V separately. | Extended matrix/architectural variants → queries-keys-values-advanced; exercises → Practice companion. |
| scaled-dot-product-attention | One-query computation: QKᵀ, scaling, mask, softmax and weighted sum of V. | Score variance and scaling derivation → attention-score-scaling; FlashAttention and memory/IO analysis → llm-computational-complexity; implementation → Build; exercises → Practice. |
| causal-masking | Why future positions must be hidden; causal visibility versus other masks; one small mask example. | Padding/document-boundary mask construction → training-examples; API polarity and fully masked row edge cases stay in a verified technical/deep section; exercises → Practice. |
| logits | Output projection, vocabulary dimension, score interpretation and invariance to a common offset. | Extended algebra/numerical cases → language-modeling-math or another verified Deepen resource; exercises → Practice. |
| probabilites | **KEEP** — softmax over the vocabulary, conditional distribution, normalization/calibration, and one compact numerical example. | **MOVED — 2026-11-24** — the temperature equation, interactive explorer, worked calculations, and decoding pipeline now belong to `decoding-strategies`; the probability lesson keeps a concise transition and link. Temperature practice is linked to the existing Generation exercise GE-F. |
| entropy | Predictive entropy over all candidates; distinguish it from surprisal of one observed token; limits of interpretation. | Compression/coding and broader information-theory treatment → compression-revision and experience-information-theory (the latter is an experiment); V-information remains in its verified advanced/experimental destination. |
| in-context-learning | Zero/one/few-shot distinction, effect of supplied examples, and difference from parameter updates. | Research-level mechanistic hypotheses → a Deepen resource only after verifying its current owner; exercises → Practice. |
| context-engineering | Context as application-selected input, one design example, context-window limits and evaluation criteria. | Retrieval algorithms → document-retrieval; RAG and persistent-memory boundaries → rag-memory-boundaries; exercises → Practice. |
| vraisemblance | Autoregressive factorization, observed prefix/target, sequence likelihood and log-likelihood. | Perplexity remains owned here; broader probabilistic derivations → language-modeling-math; exercises → Practice. |
| loss | From token-level cost to batch loss, valid-target masking, shifted targets and teacher forcing at the conceptual level. | Construction of windows, padding, document packing and tensor batches → Build training-examples; exercises → Practice. |
| gradients | Gradient with respect to logits, chain rule and one parameter update interpretation. | Longer calculus/optimization derivations → mathematical Deepen resources; implementation-specific backpropagation → Build; exercises → Practice. |

## 5. Destination rules: synthesis before fragmentation

A move should prefer the following order:

1. **Existing canonical synthesis page for the same notion**, if it already owns the concept and can absorb the material without becoming overloaded.
2. **Existing Deepen page**, if the material is an extension, derivation, variant, history or advanced technical detail.
3. **A new Deepen page**, only when the material has a coherent independent question and no existing destination can own it. Create and validate this destination before removing the source section.
4. **Build or Practice companion**, when the primary objective is implementation or learner action. The Understand lesson retains enough conceptual explanation to remain self-contained.

Do not create a new page merely to preserve a heading. Merge genuinely overlapping explanations into the canonical owner, but preserve every non-overlapping result, example, caveat, reference and visual.

### Important boundary cases

- Teacher forcing is part of the standard training explanation. Keep its conceptual meaning in the Understand lesson; training-examples owns the detailed input/target alignment and data construction for Build.
- Prefill and incremental decode are core inference vocabulary. Keep their conceptual distinction in generation; cache layout, scheduling and serving optimization belong to Deepen/Build.
- Cross-entropy is the token-level bridge from observed-target scoring to the training objective. Do not collapse it into batch loss, and do not duplicate the sequence-level likelihood/perplexity explanation.
- Entropy over the predictive distribution and surprisal of an observed token answer different questions. Both must remain explicit after any merge.
- The same concept may be linked from several chapters, but its full canonical explanation should have one owner.

## 6. Migration gates

A source page may be shortened only when all gates pass:

- [ ] FR and EN source sections have been inventoried at heading/anchor level.
- [ ] Every source section and embedded element has a disposition; no blank or implicit deletions.
- [ ] Every MOVE/SYNTHESIZE item has a concrete target page and destination anchor.
- [ ] New target pages are created before the source is edited.
- [ ] Target pages preserve all distinct claims, assumptions, equations, examples, figures, attributions and caveats.
- [ ] The source lesson links to the destination at the point where the reader needs it.
- [ ] The source lesson still teaches its stated outcome without requiring an optional page.
- [ ] Exercises and questions are on their dedicated Practice companions, with answers/feedback preserved.
- [ ] Build material is linked, not copied wholesale into Understand.
- [ ] FR/EN semantic parity, metadata, concept resources, page hierarchy, suggested route and generated navigation are reconciled.
- [ ] Rendered links, equations, diagrams, responsive layout and keyboard navigation are checked.
- [ ] Required lesson duration is measured on the rendered page in both languages and is at most 15 minutes.
- [ ] A before/after preservation review confirms that every inventoried knowledge item is still available.

If any gate fails, keep the source section and mark the migration VERIFY. A shorter page is not a success if it has become dependent on optional reading or has lost its scientific qualifications.

## 7. Recommended implementation sequence

1. Freeze the current bilingual source baseline and record exact page/section inventories.
2. Complete the oversized-page migrations (llm-overview, transformer, generation, cross-entropy, training-loop) with destination pages prepared first. The first-pass audit also identified scaled-dot-product-attention and entropy as pages needing removal of non-core or Practice material; include them in the same preservation pass.
3. Move all embedded exercises/questions to their dedicated Practice companions without changing their pedagogical content or feedback.
4. Re-measure the 20 lessons. Split only where one lesson still contains multiple independent learning outcomes or exceeds 15 minutes after correct transfers.
5. Encode the approved chapter/lesson structure once in the canonical route data; generate/validate sidebars, chapter labels, review route, previous/next links and overview from that source.
6. Reconcile FR/EN metadata and concept-resource links after the final destinations are known.
7. Validate the shared computational spine and ensure the reader sees the distinct inference, scoring and training branches without a false dependency chain.

**Current completion status (updated 2026-11-24):** chapter grouping and first-pass section dispositions are documented. Three bilingual content pilots are complete at source-text level: the cross-entropy/KL/perplexity transfer (section 8), the Transformer overview narrowing (section 9), and the temperature/decoding transfer from Probabilities to the existing decoding-strategies Deepen page (section 11). A source-level duration audit of Generation and the training loop confirms that their mandatory paths are bounded once explicitly optional material is separated. Generation's serving/latency content remains in its collapsed optional deep dive, consistent with `content-section-mapping.md`; its KV-cache memory formula remains owned by `llm-computational-complexity`. Quarto rendering, local-link checks, learning-map/graph generation and automated Playwright desktop/mobile/keyboard review now pass for the revised pages. Generated map-list, map-data and guided-route fragments have been refreshed; the CI freshness suite is being rerun. Rendered reading-time measurements and learner validation remain pending. Continue with bounded bilingual transfers only where a destination is explicit; do not split or move content solely from raw page word counts.


## 8. Completed bilingual pilot — cross-entropy, KL and perplexity (2026-11-24)

**Status: source-to-destination transfer completed; Quarto rendering, local-link checks and automated browser review passed.** Rendered reading-time measurement and learner validation remain pending.

- Source: site/fr/cross-entropy.qmd, section “Décomposition en entropie cible et divergence KL”; site/en/cross-entropy.qmd, section “Decomposition into target entropy and KL divergence”.
- Destination: site/fr/language-modeling-math.qmd and site/en/language-modeling-math.qmd, section 3 (“Cibles souples et divergence KL” / “Soft targets and KL divergence”).
- Preserved and consolidated: the general target-distribution cross-entropy formula, the identity H(q,p) = H(q) + D_KL(q || p), the fixed-target minimization interpretation, assumptions on normalized distributions, logarithm base/units, non-negativity, equality at q=p, support caveats, and the warning that language entropy is not a universal constant but depends on distribution, context, corpus and tokenization.
- Additional example preserved: q=(0.5,0.5), p=(0.75,0.25), with H(q)=0.693 nat, H(q,p)=0.837 nat and KL=0.144 nat. This example was added to both Deepen pages so the non-degenerate worked calculation is not lost when the duplicated core derivation is removed.
- Core lesson after migration: keeps the one-hot token penalty, the equivalence between mean cross-entropy and mean NLL for one-hot targets computed over the same valid positions with the same reduction convention, and concise links to the Deepen and sequence-scoring owners; it no longer repeats the full soft-target/KL derivation or the sequence-level perplexity definition.
- Perplexity transfer: the duplicated formula and interpretation were consolidated into the canonical likelihood pages. Their existing comparison caveats were retained; the base-2 form and the one-hot equivalence were added there. The cross-entropy pages keep only the local equivalence and a link to likelihood.
- Metadata: the bilingual cross-entropy pages now link to language-modeling-math through their related resources; their existing likelihood relation remains explicit.
- Not moved in this pilot: the NumPy/PyTorch implementation and numerical-stability material, multi-position alignment/masking explanation, remaining misconceptions and references. The main cross-entropy page already delegates exercises to its dedicated FR/EN Practice companions; this was verified rather than treated as a move.

**Validation still required:** render both language pages; inspect equations and links; compare the final Deepen section against the removed source material; verify page metadata and generated navigation; measure the mandatory lesson duration. This pilot does not certify the entire cross-entropy lesson or the full route.

## 9. Completed bilingual pilot — Transformer overview (2026-11-24)

**Status: source-to-destination transfer completed; Quarto rendering, local-link checks and automated browser review passed.** The Understand route and page identity are unchanged; rendered reading-time measurement and learner validation remain pending.

### Source and destinations

| Source content in site/fr/transformer.qmd / site/en/transformer.qmd | Canonical destination | Preservation result |
|---|---|---|
| Detailed MLP/feed-forward explanation; residual connection equation; LayerNorm purpose and Xiong et al. (2020) qualification; pre-LN equations and Mermaid diagram; attention-versus-MLP image and comparison table; multi-head dimension example and interpretability caveat | contextualized-representations-advanced.qmd / en/contextualized-representations-advanced.qmd, section 3 | Consolidated into the existing advanced treatment of contextual dependencies and block sublayers. The core lesson retains the two sublayer roles, the residual-stream/normalization overview, and links to both theory depth and Build. |
| Detailed depth/width distinctions, d_head, d_ff, head-count relation and GPT-2 124M values | tensors.qmd / en/tensors.qmd, “Dimensions architecturales d'un bloc Transformer” / “Architectural dimensions of a Transformer block” | Added a canonical architecture-dimension reference while retaining only depth and width definitions in the core lesson. |
| Original 2017 encoder–decoder diagram reading, explanatory table of historical labels, and architecture distinction | transformer-history.qmd / en/transformer-history.qmd, #historical-transformer-diagram | Moved to the historical reference, adjacent to its chronology. The old anchor remains on the core page as a link to the new location. |

The five guided-reading questions (locate, explain, compare, transfer, reconstruct) now live in the existing FR/EN `exercises/transformer.qmd` Practice companion, with suggested answers derived from the historical explanation. The history page links to that section; no questions remain embedded in the reference narrative.

### Core lesson after migration

- Still teaches the decoder-only GPT forward pass: input representations → repeated blocks → final normalization/output projection → logits.
- Keeps the contextual system diagram, a concise account of attention versus MLP, the training-parallelism/generation-sequentiality distinction, depth/width intuition, the three-level distinction (attention / block / complete GPT), and the boundary between logits and decoding.
- Keeps the dedicated Practice link and generated route includes.
- Does not turn the Build walkthrough into a theory prerequisite. transformer-block-walkthrough and gpt-model-walkthrough remain separate implementation resources.

### Preservation and validation

- FR/EN source sections were transferred to existing canonical pages; no image, equation, historical question, source attribution or example was intentionally discarded.
- Page-map metadata and reciprocal discovery links were updated; the guided route order and data/guided-route.yml were intentionally left unchanged.
- Remaining checks: Quarto render both languages; verify local links and the legacy anchor; inspect Mermaid, MathJax and moved figures; check bilingual semantic parity; measure the rendered mandatory lesson duration; inspect responsive and keyboard behavior.


## 10. Bounded source audit — Generation and training loop (2026-11-24)

**Status: source-level audit only.** No lesson content was moved or removed in this pass. Counts below are approximate source-text counts, not rendered reading-time measurements. The counting pass excluded front matter, HTML comments, generated include directives, fenced code, HTML tags and Markdown link destinations. The *mandatory* count stops before the explicitly optional section; the *total* includes optional prose and navigation text. Figures, equation-reading time and interaction time are not represented by these counts.

| Lesson | FR mandatory / total | EN mandatory / total | Source-level decision |
|---|---:|---:|---|
| Generation | ~1,604 / 2,707 words | ~1,465 / 2,427 words | Keep the four core sections: autoregressive loop, notation, token selection and prefill/decode. Keep latency and multi-request serving inside the existing collapsed optional deep dive. No split is justified by this source estimate. |
| Training loop | ~1,589 / 2,269 words | ~1,333 / 1,901 words | Keep one coherent path: one update, extension to a batch, optimizer/learning-rate role, train versus validation loss, and pretraining at scale. Keep implementation and extended optimizer material under Further exploration; no split is justified by this source estimate. |

### Generation — ownership and boundary

The current FR/EN pages place TTFT, ITL, TPOT, KV-cache behavior, continuous batching, prefix caching, chunked prefill and speculative decoding inside the collapsed optional section **“Approfondissement facultatif : latence et optimisations d'inférence”** / **“Optional deep dive: inference latency and optimizations”**. This is consistent with the canonical ownership row in `docs/content-section-mapping.md`: Generation owns the operational inference/serving story as optional depth, while `llm-computational-complexity` owns quantitative compute/memory accounting, including the KV-cache memory formula. The earlier proposal in section 3.3 to move the latency and serving sections elsewhere was therefore too broad and has been corrected. Preserve the link from the serving explanation to the KV-cache memory estimate.

The mandatory path remains self-contained: it introduces the autoregressive loop, distinguishes model distribution from token-selection policy, explains prompt prefill versus incremental decode, and keeps the boundary between generation, parameter learning and application-supplied context. The FR/EN revision companions and dedicated Practice pages are already linked. Do not split this lesson unless a rendered timed review demonstrates that the mandatory path exceeds the target or contains independent outcomes.

### Training loop — ownership and boundary

The mandatory path has one coherent outcome: explain how a prediction becomes a parameter update, how updates repeat over batches, and why validation is a separate fixed-parameter measurement. The page's optional section contains the runnable micro-code, the conceptual SGD/Adam/AdamW comparison, the Newton-method clarification, and implementation/workflow resources. Keep the concise optimizer overview because the canonical ownership map assigns the conceptual SGD/Adam/AdamW overview and learning-rate role to this lesson; detailed optimizer formulas, schedules and gradient clipping remain outside the core lesson.

The FR/EN revision companions and dedicated Practice pages are present. The lesson also links to the existing loss-aggregation transfer exercise rather than embedding it. No split is justified from the source estimate. A rendered review should still confirm that the visible Further exploration section is clearly distinguished from the mandatory path and that the diagrams/equations fit the 10–15-minute target.

### Evidence boundary and next step

This pass validates source ownership, section boundaries, bilingual presence and the existence of review/Practice destinations. It does **not** certify visual hierarchy, actual reading time, responsive rendering, keyboard/screen-reader behavior or learner comprehension. The next useful action is to run the same rendered-duration and first-screen review on the two remaining oversized candidates with explicit migration decisions, then update the ledger only after their destination checks. No new route, page, registry or issue is created by this audit.

## 11. Completed bilingual pilot — predictive distribution versus decoding (2026-11-24)

**Status: source-to-destination transfer completed at source-text level.** The Understand route remains unchanged: the probability lesson still follows logits and precedes entropy. No concept, route stage, page identity or new page was added.

### Source and destination

| Source | Destination | Preservation decision |
|---|---|---|
| `site/fr/probabilites.qmd` / `site/en/probabilities.qmd`, section on temperature and decoding strategy | `site/fr/decoding-strategies.qmd` / `site/en/decoding-strategies.qmd`, section 2 (`#temperature`) | The temperature equation, interactive explorer, no-JavaScript fallback, worked calculation from 60% to approximately 85.7%, concentration/flattening interpretation, uniform-limit behavior and probability-ratio property are now owned by the optional decoding deep dive. |
| Probability-page supplementary temperature material: decoding pipeline figure, stable-softmax micro-workbench, and four-logit comparison table | Same bilingual decoding-strategies section, inside an optional disclosure | Preserves the visual pipeline, executable NumPy example, three-temperature comparison and all displayed values. The generic PyTorch softmax/numerical-accuracy references remain with the probability lesson. |
| Probability lesson's selection transition and generation lesson's temperature pointer | `probabilities.qmd` and `generation.qmd` | The probability lesson retains the compact logits → optional temperature → softmax → optional filtering → selection overview, with a link to the deep dive. Generation keeps the concise operational intuition and now links to the decoding owner for detailed treatment. |
| Probability revision and Practice companions | `revision-probabilites.qmd` and `exercises/probabilites.qmd` | Revision now treats temperature as an optional decoding transformation rather than a core explanation. The dedicated per-lesson Practice companion remains the probability question page. It links to the shared Foundations collection for softmax/NLL and to the Generation collection's GE-F exercise for temperature; the entropy/observed-score transfer remains in the existing entropy exercise destination. No duplicate probability-only collection is created, and no question or worked answer is discarded. |

### Pedagogical rationale

The probability lesson answers **how logits become the model's base conditional distribution and what its probabilities mean**. Temperature is applied to logits before softmax; top-k/top-p filter and renormalize candidates; argmax or sampling selects a token. These are decoding-policy operations, not additional steps in the construction or interpretation of the base distribution. The short transition remains in the probability lesson so the learner can see where the sibling generation branch begins, while the detailed mechanics live in the optional Deepen destination. The FR/EN Transformer Explainer links that previously targeted the old probability-page explorer now point to the decoding section, and their related-page metadata has been updated.

This aligns the page ownership with `docs/content-section-mapping.md` and the canonical computational spine: the predictive distribution is the shared output; generation applies a selection policy, whereas scoring and training consume observed targets through separate branches. The entropy lesson retains only the concise relation between temperature and the entropy of the resulting distribution, with a link to the decoding deep dive; it does not repeat the temperature mechanism. The move does not make temperature a prerequisite for understanding the distribution.

### Validation boundary

The source-level transfer preserves the bilingual interactive controls, fallback, calculation, figure, code and table. The route and concept registries are unchanged. Quarto rendering, local-link/anchor checks, learning-map/graph generation and the automated Playwright desktop/mobile/keyboard review passed. The generated map-list, map-data and guided-route fragments have now been refreshed; the CI freshness suite is being rerun. Rendered reading-time measurement and learner validation remain pending.

## 12. Bilingual migration pilot — entropy, predictive compression and V-information (2026-11-24)

**Status: source-to-destination consolidation prepared in this branch; Quarto, link, generated-map and rendered checks remain pending CI.** The canonical route is unchanged.

### Source and destinations

| Source material in site/fr/entropy.qmd / site/en/entropy.qmd | Canonical destination | Preservation decision |
|---|---|---|
| Predictive entropy, finite-vocabulary bounds, the four-token numerical example, expected surprisal, and the distinction between distribution entropy and one observed token | Entropy lesson | **KEEP** — these are the lesson's single learning outcome and remain in the mandatory path. The temperature paragraph also remains as a short bridge to decoding, with the detailed mechanism owned by decoding-strategies. |
| Perplexity definition and tokenizer/protocol comparison caveat | site/fr/vraisemblance.qmd / site/en/likelihood.qmd | **SYNTHESIZE** — the entropy lesson now points to the canonical sequence-scoring explanation rather than repeating the definition. |
| Cross-entropy H(q,p), its relation to source entropy and KL divergence | site/fr/cross-entropy.qmd / site/en/cross-entropy.qmd | **SYNTHESIZE** — the lesson retains a concise distinction and contextual link; the formal definition and decomposition stay with the canonical cross-entropy treatment. |
| Predictive compression, ideal code length, the need for a shared entropy coder/decoder, the distinction from model compression, and the model-compression synthesis link | site/fr/compression-revision.qmd / site/en/compression-revision.qmd | **SYNTHESIZE** — the optional block in Entropy was duplicative of the existing compression resource. The resource already owns predictive coding, exact reconstruction requirements, model/runtime budgets, the non-archive caveat for model weights, and the limitations of compression claims. The model-compression source synthesis is linked from its model-reduction section. |
| Predictive V-information, its dependence on the predictor family, and the XOR illustration | site/fr/experience-information-theory.qmd / site/en/experience-information-theory.qmd | **TRANSFER + SYNTHESIZE** — the existing experiment page already contains the formal definition, optional-ignorance condition, controlled examples and limitations. The XOR example, Xu et al. (2020) primary-paper reference, and the original XOR experiment link are now included there, alongside the existing controlled V-information experiment. |
| H0/H1 versus zlib sequence-compression experiment | experience-information-theory.qmd / experience-information-theory.qmd | **TRANSFER** — preserve the separate empirical comparison and its caveats through a contextual link in the entropy-rate experiment section. |
| Shannon, Cover & Thomas, and 3Blue1Brown references | Entropy lesson | **KEEP** — these sources continue to support the core information-theoretic definition and intuition. |

### Core lesson after consolidation

- Explains entropy of the full conditional next-token distribution, its bounds and a worked numerical example.
- Makes explicit that entropy is expected surprisal, not the surprise of one observed target.
- Keeps the high-confidence/wrong counterexample, calibration caveat and concise temperature effect.
- Links to Likelihood for perplexity and sequence-level scoring; Cross-entropy for H(q,p); Compression and LLMs for predictive coding; and the information-theory experiment for V-information.
- Keeps the existing Practice companion and the chapter order. No route stage, lesson identity, prerequisite, page or concept node is added or removed.

### Validation boundary

The transfer preserves the coding distinctions, equations, experimental paths and primary references by assigning them to existing canonical destinations. Both the predictive-compression toy experiment and the distinct H0/H1-versus-zlib sequence experiment remain directly reachable; the model-compression source synthesis remains linked from the canonical compression resource. The new XOR illustration supplements (rather than replaces) the existing controlled V-information table. The FR/EN metadata adds reciprocal discovery links between Entropy and the compression resource. The canonical data/guided-route.yml sequence remains logits → probabilities → entropy → generation → context use → likelihood → cross-entropy → loss → gradients → training loop; no computational or pedagogical dependency is inferred from the content moves.

**Pending:** render FR/EN; verify all local links and anchors; check the preserved equations and experiment paths; regenerate and validate page maps/knowledge graph/route fragments; inspect desktop/mobile and keyboard behavior; compare the two languages semantically. Do not mark the migration complete until those checks pass.
