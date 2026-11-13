# Guided learning with the classic Transformer architecture diagram

**Status:** instructional design contract, 2026-11-13  
**Canonical home:** `site/{fr,en}/transformer.qmd`  
**Related source audit:** [#758 — Jay Alammar: The Illustrated Transformer and The Illustrated GPT-2](https://github.com/JM-Brun/llm-lab/issues/758)  
**Curriculum owner:** Understand route, computation stage; supported by Practice and Build cross-links  
**Principle:** one canonical explanation, revisited progressively; no parallel Transformer chapter.

## 1. Purpose

The familiar Transformer architecture diagram is part of the core learning experience. Learners should progressively learn to read its information flow, explain each component, relate its labels to LLM Lab's canonical concepts, distinguish the historical architecture from modern GPT, and reconstruct the computation in their own words.

The diagram is a shared visual anchor. Individual lessons explain its components; learners then return to the whole. This is a teaching contract, not a claim of mastery based on page visits.

## 2. Three visual objects that must remain distinct

1. **Original Transformer (Vaswani et al., 2017):** encoder–decoder architecture, with encoder self-attention, decoder masked self-attention, encoder–decoder cross-attention, position-wise feed-forward networks, residual additions, normalization and vocabulary projection.
2. **Decoder-only GPT:** a stack of causal Transformer blocks, with no separate encoder stream and no encoder–decoder cross-attention. LLM Lab's original `transformer-stack-{fr,en}.svg` is the GPT-specific system and block diagram.
3. **Expanded block view:** normalization, attention, residual addition, normalization, MLP and residual addition in a specified pre-LN example. It is a common arrangement, not a universal definition.

The 2017 diagram must not be presented as a generic blueprint for every modern LLM. The GPT diagram must not erase the historical encoder–decoder design or cross-attention's role in sequence-to-sequence and multimodal architectures.

## 3. Progressive reading sequence

### Pass 1 — recognize the whole

Locate input/output embeddings, positional information, encoder and decoder stacks, self-attention, masked self-attention, cross-attention, feed-forward sublayers, residual-addition/normalization steps, output projection and softmax. The goal is orientation, not full mathematical understanding.

### Pass 2 — trace information flow

- Encoder self-attention: Q, K and V derive from encoder representations.
- Decoder masked self-attention: Q, K and V derive from decoder-side representations, subject to the causal mask.
- Encoder–decoder cross-attention: Q comes from the decoder; K and V come from encoder outputs.
- Feed-forward sublayer: transforms each position independently, with parameters shared across sequence positions.
- Output head: projects decoder states to vocabulary logits; softmax is downstream of logits.

The Q/K/V, scaled attention, causal masking and cross-attention pages remain the authoritative explanations; do not duplicate their derivations in the overview.

### Pass 3 — map historical labels to canonical concepts

| Historical label | Canonical concept | Qualification |
|---|---|---|
| Input / Output Embedding | Token IDs and embedding lookup | Decoder inputs are shifted in the original training setup |
| Positional Encoding | Positional information | Original paper uses fixed sinusoids; modern models may use learned positions, RoPE or other mechanisms |
| Multi-Head Attention | Q/K/V projections and scaled dot-product attention | Distinguish self-attention from cross-attention |
| Masked Multi-Head Attention | Causal masking | Prevents access to future target positions |
| Encoder–Decoder Attention | Cross-attention | Q from decoder; K/V from encoder |
| Add & Norm | Residual addition and normalization | Original diagram is post-LN; common GPT blocks are often pre-LN or use variants such as RMSNorm |
| Feed Forward | Position-wise MLP | Same MLP parameters are applied at every sequence position |
| Linear | Vocabulary projection / language-model head | Produces logits, not probabilities |
| Softmax | Probability transformation | Separate from the Transformer block and token selection |

### Pass 4 — compare architecture families

- **Encoder-only:** contextualizes an input sequence; no autoregressive decoder stack.
- **Encoder–decoder:** reads an input with an encoder and constructs/generates an output with a decoder that can cross-attend to encoder outputs.
- **Decoder-only:** predicts sequence continuations through causal self-attention; this is the GPT focus of the main page.

Explain changes in information flow, masks and typical objectives without claiming every model in a family has one fixed task.

### Pass 5 — reconstruct and transfer

Learners should be able to narrate a representation's path; explain permitted information flow and causal masking; distinguish attention (between positions) from MLP (within each position); explain the residual stream and normalization; distinguish hidden states, logits, probabilities and generated tokens; and identify omissions such as tensor shapes, parameter sharing, parallel computation, training targets, caching and inference costs.

## 4. Relationship to the LLM Lab learning system

### Understand — canonical conceptual route

The existing `transformer.qmd` page owns the system-level explanation. It introduces the GPT stack and block, then guides the reading of the original diagram and links each label to canonical concept pages. The existing eight-stage guided route already places `transformer` in the computation stage. Do not add a duplicate stage or make the historical diagram a prerequisite before the learner sees the GPT overview.

Canonical destinations:
- embeddings: `embedding-space.qmd`;
- positional information: `positional-encoding.qmd`, optional `sinusoidal-positional-encoding.qmd`;
- Q/K/V: `queries-keys-values.qmd`;
- scaled attention: `scaled-dot-product-attention.qmd`;
- causal masking: `causal-masking.qmd`;
- cross-attention: optional `cross-attention.qmd`;
- block implementation concepts: `transformer-block-walkthrough.qmd`;
- practice transfer: `exercises-transformer.qmd` (TF-D).
- logits and probabilities: `logits.qmd`, `probabilites.qmd` / `probabilities.qmd`;
- architecture comparison: `transformer-architectures.qmd`.

### Practice & experiment — retrieval and transfer

Extend existing Transformer exercises and the practice catalogue rather than creating a parallel exercise page. Candidate tasks:
1. label a blank or partially labelled architecture;
2. trace Q/K/V provenance in the three attention sublayers;
3. predict which decoder positions a causal mask blocks;
4. classify operations as cross-position mixing, position-wise transformation, residual path, normalization or output projection;
5. explain which operations are absent from decoder-only GPT;
6. identify where logits end and decoding/generation begins.

Test reasoning, not only label recall. Interactive visualization is an optional enhancement, not a prerequisite.

### Build — implementation crosswalk

Build remains independent of Understand. Cross-reference existing block/model walkthroughs and tested code rather than turning the concept page into a code tutorial. Learners should locate embedding lookup, positional mechanism, Q/K/V projections, attention, causal mask, MLP, residual additions, normalization, repeated block stack and vocabulary projection. A code walkthrough must describe the implementation's actual architecture; do not infer it from the historical diagram.

### Deepen — optional precision

Keep derivations, tensor shape algebra, positional variants, cross-attention detail, architecture history and research caveats in existing Deepen pages. The original diagram is a route into these pages, not a reason to duplicate them in Understand.

## 5. Visual and rights policy

- Link to the original paper and Jay Alammar's explanation; do not copy their diagrams into the repository without asset-specific rights verification.
- Retain existing LLM Lab diagrams during source and rights audits.
- Keep the current GPT-specific SVG distinct from any future original encoder–decoder diagram.
- Any new project-authored figure must be scientifically reviewed, bilingual where it contains text, responsive, accessible, and accompanied by meaningful alt text.
- A figure should clarify a concept, not imply completeness.

## 6. Scientific qualifications

- The 2017 Transformer is encoder–decoder; GPT is decoder-only.
- The original paper's Add & Norm ordering is post-LN; the current GPT block SVG illustrates pre-LN.
- The original positional encoding is sinusoidal; this is not universal in modern LLMs.
- Cross-attention uses decoder-side queries and encoder-side keys/values.
- The MLP is position-wise, with parameters shared across positions; attention mixes information across positions.
- Linear projection produces logits. Softmax maps logits to probabilities; selection and autoregressive feedback are downstream decoding/generation.
- Parallel computation across positions during training does not make autoregressive generation fully parallel.
- Diagrams omit tensor, parameter, optimization and systems details; they are not universal implementation specifications.

## 7. Acceptance and validation

- [x] Existing canonical page retained; no duplicate chapter created.
- [x] Original encoder–decoder diagram distinguished from decoder-only GPT.
- [x] Historical labels mapped to canonical LLM Lab concepts.
- [x] Progressive reading passes and architecture comparison added to the bilingual canonical page.
- [x] Added TF-D to the existing bilingual Transformer exercise collection: original encoder–decoder labels, cross-attention Q/K/V provenance, logits versus softmax, GPT omissions, and post-LN versus pre-LN.
- [ ] Source audit #758 completed, including separate assessment of *The Illustrated Transformer* and *The Illustrated GPT-2*.
- [ ] FR/EN semantic parity checked after rendered build.
- [ ] Internal links resolve in both languages.
- [ ] Historical post-LN versus current pre-LN distinction checked.
- [ ] Alt text, reading order, keyboard and screen-reader behavior reviewed; distinguish manual evidence from automated checks.
- [ ] Novice and experienced learners asked to annotate/read the diagram; record observed confusions before claiming learner benefit.

Publication or CI success alone does not establish learner mastery.

## 8. Maintenance triggers

Revisit when the canonical Transformer page or component destinations change; a new architecture enters the core route; the Build implementation changes its block or normalization design; a source audit discovers a materially better explanation; learner validation reveals persistent confusion; or licensing/accessibility evidence changes.


## 9. Lightweight learner-validation protocol

The purpose of this test is to discover where the explanation fails, not to demonstrate that the page is effective. Run it with at least one learner who is new to Transformers and one who already knows the basic architecture. Two participants are a diagnostic pilot, not statistically representative evidence.

### Preparation

- Use the rendered page in the participant's preferred language and a normal desktop or mobile viewport.
- Do not explain the diagram before the first task.
- Ask for permission to take notes. Do not collect names or other identifying information.
- Record the page/viewport, task completion, pauses, navigation detours, incorrect explanations and requests for clarification. Do not treat time-on-page or self-reported satisfaction as evidence of understanding.

### 15–20 minute session

1. **Unaided orientation (2 min):** show the canonical Transformer page and ask: “What do you think this diagram represents? Talk me through what you notice.”
2. **Information flow (4 min):** ask the learner to trace one encoder representation and one decoder representation. Then ask where Q, K and V originate in encoder–decoder attention.
3. **Architecture distinction (3 min):** ask what changes when moving from the 2017 encoder–decoder model to decoder-only GPT. Ask specifically what happens to the encoder stream and cross-attention.
4. **Mechanism distinction (3 min):** ask the learner to explain the roles of attention, the position-wise feed-forward network, Add & Norm, Linear and Softmax. Probe logits versus probabilities without supplying the answer.
5. **Transfer (3 min):** present a short claim: “GPT is the original Transformer with the encoder removed.” Ask whether this is sufficient and what else changes.
6. **Practice hand-off (2–5 min):** ask the learner to attempt TF-D, using hints only if they choose to. Note whether the exercise tests reasoning or merely repeats wording from the page.

Use neutral prompts (“What makes you say that?”, “Where do you see that?”). Do not correct the learner during the diagnostic tasks. Afterward, explain any misconception that could leave them with a materially false model.

### Observation rubric

For each task, record one of:

- **Independent:** correct explanation without help.
- **Recovered:** correct after rereading or navigating to a linked canonical page.
- **Prompted:** correct only after a non-leading clarification prompt.
- **Incorrect:** persistent misconception or incorrect information-flow account.
- **Not attempted:** time, accessibility or navigation prevented a meaningful attempt.

Record the learner's own wording for misconceptions, then classify them:

- architecture confusion (encoder-only / encoder–decoder / decoder-only);
- information-flow confusion (self-attention versus cross-attention; Q/K/V provenance);
- operation confusion (attention versus MLP; residual versus normalization);
- output confusion (hidden state versus logits versus probabilities versus selected token);
- historical/current-design confusion (post-LN versus pre-LN; sinusoidal versus modern positional mechanisms);
- interaction/accessibility friction (reading order, link discoverability, keyboard or screen-reader issue).

### Decision rules

- A single critical misconception reproduced by both participants warrants a wording or diagram revision before broader rollout.
- A novice failing a task but recovering through a clearly discoverable canonical link may indicate a navigation/prerequisite issue rather than a factual defect.
- An experienced learner finding the page too elementary is not, by itself, a reason to add advanced material to the main route; check whether the promised high-level distinction, caveat or transfer insight is missing.
- Any keyboard, screen-reader, contrast or responsive-layout blocker is logged separately from conceptual performance and addressed as an accessibility defect.
- After a revision, rerun only the affected tasks with a fresh reader where possible. Keep the original observation and revision rationale so improvements are auditable.

### Reporting template

Record date, language, viewport, participant experience level (novice / experienced only), tasks attempted, rubric outcomes, verbatim misconception notes without personal identifiers, accessibility observations, resulting content changes and unresolved questions. Do not publish participant details or claim general effectiveness from this small pilot.

### Exit criteria for this validation task

- At least one novice and one experienced reader have completed the protocol.
- All critical misconceptions and interaction blockers have an explicit disposition (fix, accepted limitation with rationale, or further investigation).
- Any resulting content changes have passed the relevant automated checks.
- The issue/PR record distinguishes observed evidence from hypotheses and does not claim mastery from a small pilot.
