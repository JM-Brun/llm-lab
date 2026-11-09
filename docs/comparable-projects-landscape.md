# Comparable learning projects — positioning map

**Status:** dated snapshot; entries checked against their public pages on 2026-11-09 unless noted.  
**Purpose:** this document records the public projects that address, fully or partly, the same reader question as LLM Lab ("how do language models actually work?") and the concrete differences between them and this lab. It is a positioning map for maintainers: it is not a source-ingestion backlog, not a syllabus, and not a claim of equivalence. Inclusion does not mean a project was scanned, audited, or endorsed.  
**Relation to other documents:** resources used as teaching sources remain catalogued in [annotated references](references.md) and the [pedagogical resource library](pedagogical-resource-library.md). This page does not change any ingestion or licensing decision.

## Snapshot comparison

| Project | Format and access | Languages | Primary reader question | Has that LLM Lab lacks | LLM Lab differs by |
|---|---|---|---|---|---|
| Karpathy — Neural Networks: Zero to Hero | Free video course with notebooks | English only | "Can I build the pieces myself, in code, from first principles?" | A complete from-scratch training path ending in trained models and a built tokenizer | Text-first bilingual site; conceptual inference route before build dependencies; per-page self-checks, misconceptions and evidence gates |
| Raschka — Build a Large Language Model (From Scratch) + companion repo | Book (paid) with free code | English (French adaptation exists separately) | "What is the standard end-to-end construction path?" | End-to-end pretraining and fine-tuning chapters with exercise solutions | Understand/Build/Deepen/Practice destinations; FR/EN parity as a reviewed contract; explicit unimplemented-status disclosure |
| Hugging Face LLM Course | Free course with notebooks | English and French editions | "How do I use and adapt models with the HF ecosystem?" | Fine-tuning, LoRA, SFT, GRPO/reasoning and agents chapters; notebook-first practice | Framework-independent NumPy core; bilingual parity treated as a hard contract; understanding-first route |
| Anthropic Academy (Building with the Claude API) | Free video course with certificate | English | "How do I build applications on top of models?" | Applied API/usage training at scale | Internals-first scope: parameters, attention, scoring and training rather than API usage |
| fast.ai — Practical Deep Learning for Coders | Free video course | English | "How do I train practical deep-learning models top-down?" | Broad DL practice beyond language models | LLM-specific conceptual spine; no blanket math prerequisite; bilingual |
| Stanford CS336 — Language Modeling from Scratch | University course (lectures + assignments) | English | "What is the full engineering and theory of training LMs at scale?" | Advanced, assignment-driven depth; scaling and systems coverage | Advanced mathematics available when needed rather than a blanket prerequisite; learner route without enrollment |
| mlabonne/llm-course | Free GitHub roadmap + Colab notebooks | English | "What should I study next, in what order?" | A broad curated roadmap across LLM topics | Depth over breadth on the core spine; evidence inventory; bilingual |
| mneves75/llmdeepdive | Free open-source course site (MIT) | English + Brazilian Portuguese | "How do LLMs actually work, down to serving and silicon?" | 380 lessons over 26 tracks; one real model worked throughout; serving stacks, hardware, multimodal, agent engineering; quiz-gated explanations; build-enforced parity | French/English pair; open progressive disclosure instead of gated disclosure; small inspectable random-init models with an explicit no-training-yet status; formative exercise hub |
| Jay Alammar — Illustrated series (+ Hands-On LLMs with M. Grootendorst) | Free articles; book | English | "Can I see the architecture and data flow visually?" | Canonical visual narratives for GPT-2/Transformer | Explanations embedded in a full staged route with checks; figures reused only with verified rights |
| 3Blue1Brown — neural network and LLM lessons | Free videos | English | "What is the geometric intuition behind attention, entropy, gradients?" | Exceptional animated intuition | Text with worked examples, counterexamples, self-checks; bilingual |

Notes on verification basis: the Anthropic Academy and CS336 rows rely on 2026 course roundups rather than a full syllabus inspection; the HF LLM Course chapter list (13 chapters including reasoning/GRPO material, updated through mid-2026) comes from third-party roundups dated September 2026, while the course's French edition URL is already recorded in [references](references.md). Recheck each project's current page before using a row for a concrete decision.

## What each comparison teaches

### Karpathy — Neural Networks: Zero to Hero

- **What it is:** a video course building neural networks from backpropagation up to a working GPT and a tokenizer, in code (https://karpathy.ai/zero-to-hero.html).
- **Difference in kind:** the progression is implementation-led; understanding follows the build. LLM Lab deliberately runs the conceptual inference route first (fixed parameters, black-box generation, then mechanisms), and keeps the construction dependencies in a separate Build branch. Karpathy's medium is unscripted video plus notebooks; LLM Lab's medium is a bilingual static site with a generated route, tests and an audit trail.
- **Use in this project:** listed in the resource library for connecting conceptual explanations to executable implementations; not a syllabus to mirror.

### Sebastian Raschka — Build a Large Language Model (From Scratch)

- **What it is:** a book with a free companion repository (https://github.com/rasbt/LLMs-from-scratch) covering tokenization through pretraining and fine-tuning.
- **Difference in kind:** the chapter order follows the construction path. LLM Lab treats it as a "major implementation and scope reference, not a mandatory table of contents" (README): the public route separates understanding from building, publishes FR/EN parity, and keeps the missing end-to-end training pipeline visible instead of implied. 2026 roundups also announce a companion book on reasoning models; verify its status at the publisher before relying on it.

### Hugging Face LLM Course

- **What it is:** the free official course over the HF ecosystem (https://huggingface.co/learn/llm-course), with French and English editions.
- **Difference in kind:** ecosystem- and tooling-first (Transformers, Datasets, TRL, PEFT), extending in 2026 into SFT/LoRA and GRPO-based reasoning chapters. LLM Lab's core is framework-independent NumPy, and adaptation/fine-tuning remain planned milestones stated as gaps. The HF course demonstrates the breadth LLM Lab has not reached; LLM Lab offers a dependency-free conceptual spine the course does not attempt, and treats FR/EN parity as a reviewed contract rather than a translation track.

### Anthropic Academy and fast.ai

- Adjacent rather than competing: they answer "build with models" or "train practical deep learning", not "understand how language models work inside". They are recorded here because learners encounter them in the same searches and may need help choosing (see the roundups cited above).

### Stanford CS336 and mlabonne/llm-course

- CS336 represents the academic depth route (theory + engineering at scale, advanced prerequisites). mlabonne's course represents the roadmap style (breadth, links, notebooks). LLM Lab occupies the space between: rigorous but just-in-time mathematics, a bounded conceptual spine, and no enrollment or strong ML background required.

### mneves75/llmdeepdive

- **What it is:** a free MIT-licensed bilingual (English/Brazilian Portuguese) interactive course (https://github.com/mneves75/llmdeepdive; https://llmdeepdive.com), 380 lessons over 26 tracks as of the 2026-11-09 check: model internals from parameters to efficient inference, worked through one real model (a Qwen checkpoint); serving stacks, silicon, multimodal and world models; then agent-system engineering with CI-checked code.
- **Why it matters here:** it is the closest public peer on two axes LLM Lab also treats as first-class: bilingual parity enforced by the build, and evidence-oriented pedagogy (per-claim citations, Feynman-style layering).
- **Differences:** the language pair (EN/pt-BR, not FR/EN); the scope (it already covers serving, hardware, multimodal and agents, which LLM Lab lists as long-term goals); the model anchor (one real pretrained checkpoint vs LLM Lab's small random-init models with an explicit no-trained-model status); and the disclosure model (explanations unlock only after a correct quiz answer vs LLM Lab's open pages plus a formative exercise hub with hidden answers).
- **Decision for this project:** a peer to watch for scope and bilingual tooling ideas; not a source to copy content from.

### Visual explainers (Alammar, 3Blue1Brown, animated visualizations)

- These answer complementary questions (visual intuition) rather than offering a route. Their role and reuse boundaries are already recorded in [references](references.md) and the resource library; the 2026 TeachingNLP literature (e.g. AnimatedLLM) confirms interactive visualization as an active research direction, which supports LLM Lab's interactive explorations without changing their evidence status (illustration, not measurement).

## Where LLM Lab stands out — and gaps to keep visible

**Standing out:** bilingual FR/EN semantic parity as a reviewed contract (rare; the nearest peer enforces EN/pt-BR); the four-destination structure (Understand/Build/Deepen/Practice) with a generated guided route; an evidence culture (audit inventory, distinction between illustration/test/experimental result, provenance-gated figures); a bilingual formative exercise hub; explicit publication of what is not implemented.

**Gaps vs the field, to keep honestly visible rather than disguised:** no end-to-end corpus-to-training-to-evaluation pipeline yet (Karpathy, Raschka, HF); adaptation/fine-tuning chapters not yet written (HF); serving/efficiency and hardware depth deferred (llmdeepdive); no trained-model experience in the core (all peers anchor on real checkpoints at some point). These gaps are already recorded in project status; this map should not be used to claim parity with any of the projects above.

## Maintenance

Re-dating rule: update a row when a project materially changes (scope, language, licence, access model) and record the recheck date; do not add every new tutorial that repeats existing explanations. Entries relying on third-party roundups should be replaced by direct page checks before being used for decisions.
