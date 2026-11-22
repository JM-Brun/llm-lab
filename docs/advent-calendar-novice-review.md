# LLM Advent Calendar — novice review protocol and results log

> **Status (2026-11-22):** protocol prepared; no novice session has been conducted and no participant results are available. The three entries remain editorial pilots, not learner-validated content.
>
> **Scope:** content comprehension and transfer for days 03 (tokenization), 09 (Q/K/V), and 21 (cross-entropy). This is not a site-navigation, accessibility, or controlled learning-effectiveness study.

Related work:
- Main tracking issue: [#1513 — Design and validate the progressive 24-day LLM Advent Calendar](https://github.com/JM-Brun/llm-lab/issues/1513)
- Pilot entries: [advent-calendar-pilot-content.md](advent-calendar-pilot-content.md)
- Graph relation review: [#416](https://github.com/JM-Brun/llm-lab/issues/416)
- Optional KL mathematical deepening: [PR #1519](https://github.com/JM-Brun/llm-lab/pull/1519)

## 1. What this review must establish

For each pilot, determine whether a novice reader can:

1. understand the central question without opening the canonical lesson first;
2. explain the intended distinction in their own words;
3. complete the active check without facilitator coaching;
4. transfer the idea to a changed example;
5. identify the next useful resource (Understand, Practice, and optional Deepen where applicable).

Also record reading and activity time, confidence, reasoning errors, hints, and production effort. A correct answer obtained after a hint must not be recorded as independent success.

The review is formative. With 3–5 readers, results are qualitative observations, not statistically representative estimates or proof of causal learning gains.

## 2. Participants and session

### Participant profile

Recruit 3–5 readers who:

- have not studied these three LLM Lab lessons recently;
- have no substantial prior familiarity with the specific concept being tested, or can clearly describe their prior exposure;
- can read the selected language (French or English).

Do not require Python experience: these three entries are intended to test conceptual explanations, not coding ability. Record prior exposure separately for tokenization, attention/QKV, and probabilistic loss.

Use anonymous reader codes (P01, P02, …). Obtain consent before recording notes. Do not collect names, contact details, employer, or proprietary text.

### Session procedure

Allow approximately 25–35 minutes for all three entries. Keep the calendar order (03 → 09 → 21) to test the intended progression, but record that later entries may benefit from earlier ones.

For each entry:

1. Ask the baseline question before showing the entry. Record the answer and confidence (1–5); do not correct it.
2. Show only the calendar-sized entry. Do not open the canonical lesson or exercise page yet.
3. Record start and finish times. Ask the reader to think aloud, but do not teach or complete a step for them.
4. Ask the active check from the entry. Record the answer before revealing its correction.
5. Ask the day-specific transfer prompt below. Do not provide hints unless the reader is stuck; record every hint.
6. Ask the reader to explain the central distinction in their own words and rate confidence again (1–5).
7. Only then show the Understand and Practice links (and optional Deepen link if available). Ask what they would open next and why.

Do not treat a facilitator's paraphrase or a response after a hint as an unassisted answer. Record the participant's wording as closely as practical, separating observation from interpretation.

**Important boundary:** the pilot is currently a Markdown content draft, not a rendered calendar interface. This session can assess whether link labels and next steps are understandable when shown; it cannot establish actual navigation discoverability, responsive behavior, keyboard access, or screen-reader usability.

## 3. Day-specific probes and scoring

Score each dimension independently: 0 = incorrect/absent, 1 = partially correct, 2 = correct with adequate reasoning. Record the exact misconception; do not rely on a total score alone.

### Day 03 — Tokenization

**Baseline:** “Does a tokenizer always split text into whole words? Can two tokenizers split the same character string differently?”

**Transfer:** “Two tokenizers process the string `unbelievable`. Tokenizer A returns `["un", "believable"]`; tokenizer B returns `["un", "believ", "able"]`. What differs, what remains the same, and what determines the segmentation?”

**Expected reasoning:**
- A token is not necessarily a whole word; it may be a word, subword, character, or byte sequence, depending on the tokenizer.
- The original character string is the same, but the token sequences differ.
- Segmentation depends on the tokenizer's vocabulary and rules; token boundaries are not an intrinsic property of the text alone.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Token vs word | Assumes every token is a complete word | Recognizes subword tokens but treats them as exceptional or incidental | Explains that tokens may be words, subwords, characters, or byte sequences |
| Tokenizer-dependent segmentation | Assumes one canonical segmentation for a string | Notices that tokenizers may differ but cannot explain why | Explains that vocabulary and segmentation rules determine token boundaries |

### Day 09 — Query, Key, and Value

**Baseline:** “Which objects determine the attention weights, and which object supplies the vectors that are combined?”

**Transfer A — change K:** “Change one key vector K_j, keeping Q, the other keys, V, and the mask fixed. Which score is affected, and what may happen to the attention weights and output?”

**Transfer B — change V:** “Now change one value vector V_j, keeping Q, K, and the mask fixed. Which quantities must remain unchanged, and what may happen to the output?”

**Expected reasoning:**
- Q and K determine compatibility scores; the applicable mask and normalization determine the attention weights.
- Changing one K can change its score and therefore the normalized weight distribution; the aggregated output may change.
- Changing V alone leaves scores and weights unchanged; the output may change, but a change is not mathematically guaranteed if weighted changes cancel.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Q/K/V roles | Confuses the roles or says V determines weights | Identifies some roles but confuses scores, weights, or output | Q/K determine scores and weights; V supplies aggregated content |
| K-only intervention | Says K has no effect or that it directly changes V | Predicts a score change but cannot connect it to normalized weights | Explains the affected score and possible change in weights/output |
| V-only intervention | Says scores/weights must change | Says weights stay fixed but output must always change | Says weights stay fixed and output may, but need not, change |

### Day 21 — Cross-entropy

**Baseline:** “For a fixed observed target, which prediction receives the larger one-token loss: probability 0.8 or probability 0.2? Why?”

**Transfer:** “The observed target is y. The model assigns it probability 0.2. Calculate the local loss in nats. Then explain why this value is not yet the mean loss of a sequence or batch.”

**Expected reasoning:**
- For a one-hot target, ℓ = −ln p(y).
- −ln(0.8) ≈ 0.223 nat and −ln(0.2) ≈ 1.609 nats; the lower target probability incurs the larger cost.
- This is a single-position cost. A sequence/batch objective additionally requires target alignment, valid-position masking, and a stated reduction rule.
- KL divergence is not needed to compute this one-hot loss. Its decomposition with cross-entropy is optional mathematical deepening, not a prerequisite for this core calculation.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Target and prediction | Confuses the target with the predicted distribution | Identifies the target probability but not its role in the formula | Uses the probability assigned by the model to the observed target |
| Log-loss reasoning | Gets sign/direction wrong | Correct direction but incorrect or incomplete calculation | Uses −ln p(y) and obtains the value with the correct unit |
| Local vs aggregated loss | Treats one-token loss as the batch objective | Notices aggregation but omits masks or reduction | Distinguishes local score from masked/reduced sequence or batch objective |
| KL boundary | Claims KL must be known to compute one-hot CE | Recognizes a relation but cannot distinguish core from extension | Computes one-hot CE directly and identifies KL as optional decomposition/deepening |

## 4. Misconception coding

Use one or more codes per observed error. Add a short verbatim excerpt or faithful paraphrase.

| Code | Misconception / reasoning failure |
|---|---|
| TOK-WORD-ASSUMPTION | Assumes every token corresponds to a complete readable word |
| TOK-SEGMENTATION-INVARIANT | Assumes the same character string must yield the same token boundaries with every tokenizer |\n| TOK-ID-MEANING | Treats token IDs as quantities of meaning, similarity, or frequency |
| TOK-CROSS-VOCAB | Assumes equal IDs across tokenizers identify the same token |
| TOK-LOOKUP-CONTEXT | Assumes equal initial embedding lookup forces equal contextualized states |
| QKV-ROLE-SWAP | Swaps or merges Query, Key, and Value roles |
| QKV-V-WEIGHTS | Claims V determines attention scores or weights |
| QKV-INTERVENTION | Cannot predict the effect of changing K or V while other inputs are fixed |
| ATTN-MASK | Ignores which positions are accessible under the mask |
| CE-ENTROPY | Confuses cross-entropy with entropy of the predictive distribution |
| CE-KL | Treats cross-entropy and KL as identical in general, or KL as mandatory for one-hot CE |
| CE-SIGN | Reverses the sign or believes lower target probability lowers the loss |
| CE-AGGREGATION | Confuses a local token cost with a sequence/batch reduction |
| CE-ALIGNMENT | Does not identify which observed token is the target of a prediction |
| OTHER | Record the reasoning explicitly; do not force it into an existing category |

A wrong final answer is not enough to diagnose a misconception. Record the reasoning path, the point where it diverged, and whether the learner self-corrected before feedback. The ID- and embedding-related codes remain in the catalogue for a later day-4/day-5 review; they are not scored as day-3 outcomes in this pilot.

## 5. Results log — leave blank until sessions occur

No participant results are recorded in this version. Do not fill these tables with simulated, inferred, or model-generated learner responses.

### Session-level record

| Reader code | Language | Prior LLM exposure | Prior tokenization / QKV / loss exposure | Consent recorded | Notes |
|---|---|---|---|---|---|
| P01 | pending | pending | pending | pending | |
| P02 | pending | pending | pending | pending | |
| P03 | pending | pending | pending | pending | |
| P04 | optional | optional | optional | optional | |
| P05 | optional | optional | optional | optional | |

### Per-reader, per-day observations

Create one row for each reader and each day. Keep exact answers in a private working note if needed; this repository log should use anonymous codes and omit identifying details.

| Reader | Day | Baseline / confidence | Active check | Transfer answer / score | Time | Confidence after | Hint / navigation issue | Misconception codes |
|---|---:|---|---|---|---:|---|---|---|
| P01 | 03 | pending | pending | pending | pending | pending | pending | |
| P01 | 09 | pending | pending | pending | pending | pending | pending | |
| P01 | 21 | pending | pending | pending | pending | pending | pending | |
| P02 | 03 | pending | pending | pending | pending | pending | pending | |
| P02 | 09 | pending | pending | pending | pending | pending | pending | |
| P02 | 21 | pending | pending | pending | pending | pending | pending | |
| P03 | 03 | pending | pending | pending | pending | pending | pending | |
| P03 | 09 | pending | pending | pending | pending | pending | pending | |
| P03 | 21 | pending | pending | pending | pending | pending | pending | |

Add rows for P04/P05 only if those sessions occur.

### Production-effort record

Measure author/reviewer effort separately from participant time. Record actual elapsed effort; do not retrospectively invent precise estimates.

| Day | Source/content review | Drafting | FR/EN parity | Example / visual work | Editorial review | Revision after reader feedback | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 03 | pending | pending | pending | pending | pending | pending | pending |
| 09 | pending | pending | pending | pending | pending | pending | pending |
| 21 | pending | pending | pending | pending | pending | pending | pending |

## 6. Interpretation and revision rules

- **Scientific or mathematical error:** correct it regardless of how many readers notice it.
- **Repeated misconception:** if at least two readers independently make the same substantive reasoning error, inspect the wording, example, and prerequisite assumptions; do not automatically blame the reader.
- **Transfer failure:** if at least two readers can repeat the explanation but cannot solve the changed example, revise the active check or explanation so it teaches the intended reasoning rather than recognition.
- **Hint dependence:** distinguish independent success, success after a neutral clarification, and success after a conceptual hint.
- **Duration:** investigate an entry if it regularly exceeds the 5–8 minute target; do not shorten it by removing a distinction needed for correct transfer.
- **Resource discovery:** record whether the reader can explain the difference between Understand, Practice, and optional Deepen. This is a content-label check only until a rendered interface is tested.
- **Production effort:** compare actual effort across the three formats before fixing the production contract for all 24 days.

With 3–5 readers, report counts and representative anonymized reasoning patterns, not percentages as if they were population estimates. Preserve negative cases and unresolved ambiguity. A successful active check without successful transfer is not sufficient evidence that the entry teaches the concept.

## 7. Required close-out after the sessions

For each day, publish a short result summary containing:

1. number of readers and their relevant prior exposure;
2. observed completion-time range and median;
3. active-check and transfer outcomes, with the rubric dimensions kept separate;
4. misconception codes and anonymized examples of reasoning errors;
5. hints, facilitator interventions, and resource-discovery observations;
6. editorial changes made and the reason for each;
7. unresolved issues and whether another round is needed.

Only after these results are recorded should the daily content contract be revised and the remaining 21 entries be audited against the revised contract.

**Do not mark the pilots learner-validated, the contract approved, or the 24-day calendar ready until this close-out exists.**
