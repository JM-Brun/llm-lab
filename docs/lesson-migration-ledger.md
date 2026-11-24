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

The current nine conceptual stages are retained as **chapters**, but the route is presented as one ordered list of lessons. The route is a pedagogical progression, not a claim that every lesson is a formal prerequisite of the next. In particular, generation, observed-target scoring and parameter learning remain distinct uses of the shared predictive distribution.

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
| Les blocs Transformer | **KEEP** | The central lesson content: block composition, repeated transformations and the role of attention/MLP/residual paths at overview level. Link to Q/K/V and attention for the calculations. |
| Parallélisme à l'entraînement, génération séquentielle | **SYNTHESIZE / DEEPEN** | Keep the essential distinction in one short comparison; move detailed work/dependency/memory analysis to llm-computational-complexity. Link to generation and training-loop. |
| Profondeur et largeur : deux dimensions de l'architecture | **DEEPEN** | Move the extended capacity/compute discussion to llm-computational-complexity or a dedicated architecture-depth resource if its content does not fit there. Keep only definitions needed to read the block stack. |
| Trois niveaux à ne pas confondre | **KEEP, concise** | Retain the distinction between attention mechanism, Transformer block and complete model; it prevents a central category error. |
| Des représentations aux logits | **SYNTHESIZE** | Keep the transition and one compact flow diagram; the output projection and logits are taught canonically in logits. |
| Lire aussi le schéma fondateur du Transformer; Parcours de lecture guidée | **REFERENCE** | Move the historical/source-reading guide to transformer-history; retain a contextual link. |

### 3.3 generation — preserve the complete conceptual inference path; move serving internals

| Existing section | Proposed disposition | Destination / boundary |
|---|---|---|
| La boucle sur un exemple; Une étape, en notation | **KEEP** | The core autoregressive loop, including fixed parameters and context feedback. |
| Comment le prochain token est-il choisi ? | **KEEP, concise** | Explain selection at the level required to distinguish the distribution from the decoding policy. Detailed strategies belong to decoding-strategies. |
| Du prompt aux tokens suivants : prefill et decode | **KEEP** | Prefill and incremental decode are required vocabulary for understanding actual inference. Keep the conceptual contrast; avoid implementation-level cache internals. |
| Pourquoi l'inférence semble-t-elle parfois lente ? | **DEEPEN** | Move the detailed latency explanation to llm-computational-complexity, preserving a short pointer from the lesson. |
| Servir plusieurs requêtes : ordonnancement et réutilisation du cache | **DEEPEN / VERIFY** | Preserve the full serving/scheduling explanation in an existing or newly created inference-serving Deepen resource. llm-computational-complexity can own the compute/memory/KV-cache analysis, but do not assume it already covers scheduling policy. |
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
| Lien avec la perplexité | **MERGE-INTO-LESSON** | vraisemblance owns sequence-level likelihood and perplexity. Keep only the local cross-reference and the precise relation needed to interpret mean token NLL. |
| Idées reçues | **KEEP, selective** | Retain warnings that prevent misreading cross-entropy as truth, accuracy or a probability; move generic information-theory discussion only if its destination is verified. |
| Décomposition en entropie cible et divergence KL; Exemple numérique en nats | **DEEPEN** | The full soft-target/KL derivation belongs to language-modeling-math. Keep the one-hot special case in this lesson. Verify every equation and caveat against the destination before moving. |
| Implémentations — NumPy, PyTorch et stabilité numérique; dimension, réduction et log-softmax examples | **BUILD / DEEPEN** | Move code/API-specific walkthroughs to the appropriate Build implementation resource; preserve numerical-stability and axis/reduction reasoning in language-modeling-math or a dedicated numerical Deepen section. Do not discard counterexamples or framework-contract warnings. |
| Exercices; Exercices complémentaires | **PRACTICE** | Move all exercises, worked answers and feedback to the cross-entropy Practice companion. |
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
| probabilites | Softmax over vocabulary, conditional distribution and normalization; one compact numerical example. | Temperature, top-k/top-p and selection trade-offs → decoding-strategies; calibration theory → a verified evaluation/deepen destination; exercises → Practice. |
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

**Current completion status:** chapter grouping and first-pass section dispositions are documented. No lesson content has yet been removed, moved, merged or declared complete by this ledger. The next content operation must be a bilingual source-to-destination pilot with the preservation evidence attached.
