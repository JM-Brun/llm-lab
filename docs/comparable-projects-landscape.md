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
| mlabonne/llm-course | Free GitHub roadmap, topic maps, curated links and linked Colab notebooks | English | "How do I progress from foundations to building, tuning and deploying LLM systems?" | Broad Scientist + Engineer coverage: pre/post-training, preference alignment, evaluation, quantization, RAG, agents, optimization, deployment and security | A narrower internals-first conceptual spine; tested NumPy reference; explicit separation of conceptual and implementation paths; FR/EN parity and evidence gates |
| mneves75/llmdeepdive | Free open-source course site (MIT) | English + Brazilian Portuguese | "How do LLMs actually work, down to serving and silicon?" | 380 lessons over 26 tracks; one real model worked throughout; serving stacks, hardware, multimodal, agent engineering; quiz-gated explanations; build-enforced parity | French/English pair; open progressive disclosure instead of gated disclosure; small inspectable random-init models with an explicit no-training-yet status; formative exercise hub |
| Jay Alammar — Illustrated series (+ Hands-On LLMs with M. Grootendorst) | Free articles; book | English | "Can I see the architecture and data flow visually?" | Canonical visual narratives for GPT-2/Transformer | Explanations embedded in a full staged route with checks; figures reused only with verified rights |
| 3Blue1Brown — neural network and LLM lessons | Free videos | English | "What is the geometric intuition behind attention, entropy, gradients?" | Exceptional animated intuition | Text with worked examples, counterexamples, self-checks; bilingual |
| Cohere — LLM University (LLMU) | Free interactive courses with in-browser notebooks | English | "How do LLMs and the NLP stack around them work, hands-on?" | A complete, corporate-maintained curriculum (introduction to LLMs, embeddings, prompting) with an integrated notebook environment | Vendor-independent core; staged conceptual route before any tooling; FR/EN parity; per-page self-checks and evidence gates |
| Princeton COS 597G — Understanding Large Language Models (Fall 2023) | Public graduate seminar materials (paper-reading course) | English | "What does the primary research literature say about how LLMs work?" | A structured paper-reading path with student-led lectures covering analysis, training, and impact | Non-researcher route; worked numerical examples and tested small implementations; bilingual |
| jaymody/picoGPT — GPT in 60 Lines of NumPy | Free blog post + MIT-licensed minimal code | English | "Can I read a complete GPT-2 inference implementation in one sitting?" | A minimal, readable forward pass over real pretrained GPT-2 weights | The same NumPy-first idea extended into a staged bilingual route with page contracts, tests, and an explicit no-trained-model status |
| poloclub Transformer Explainer + bbycroft LLM Visualization | Free interactive browser visualizations | English | "Can I see and manipulate a live Transformer computation?" | Live attention and data-flow exploration on a real model, in the browser | Text route with worked examples and counterexamples; local NumPy micro-workbenches; bilingual |

Notes on verification basis: the four rows added on 2026-11-09 (Cohere LLM University, Princeton COS 597G, picoGPT, Transformer Explainer/LLM Visualization) were checked against their public pages the same day, except the COS 597G syllabus, which was reached via search and still needs its canonical URL pinned. Recheck each project's current page before using a row for a concrete decision. the Anthropic Academy and CS336 rows rely on 2026 course roundups rather than a full syllabus inspection; the HF LLM Course chapter list (13 chapters including reasoning/GRPO material, updated through mid-2026) comes from third-party roundups dated September 2026, while the course's French edition URL is already recorded in [references](references.md). Recheck each project's current page before using a row for a concrete decision.

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

### Cohere LLM University and Princeton COS 597G

- **What they are:** LLM University (https://cohere.com/llmu) is a free, corporate-maintained curriculum with interactive in-browser notebooks, including an introduction-to-LLMs course (page checked 2026-11-09). Princeton COS 597G (Fall 2023), *Understanding Large Language Models*, is a graduate research seminar whose paper-based materials remain public; its syllabus was reached via search on 2026-11-09 and the canonical URL should be pinned at the next direct check before this row is used for a decision.
- **Difference in kind:** LLMU teaches understanding and use together, anchored to one vendor's platform and notebook environment. COS 597G treats understanding as reading the primary research literature, assuming prior ML coursework. LLM Lab stays vendor-independent, teaches through small inspectable NumPy models with tests, and keeps research papers as reference material rather than as the route itself.
- **Use in this project:** LLMU is a peer for polished integrated notebook practice; COS 597G is a pointer for readers who finish the core route and want a research reading path. Neither is a content source.

### Minimal readable implementations (picoGPT)

- **What it is:** jaymody/picoGPT (https://github.com/jaymody/picoGPT) implements GPT-2 inference in about 60 lines of NumPy over real pretrained weights, explained in the companion blog post *GPT in 60 Lines of NumPy*; MIT-licensed (repo checked 2026-11-09).
- **Difference in kind:** picoGPT shows that a complete forward pass can be read in one sitting; it is inference-only, a single artifact, and English-only, and it runs real pretrained weights. LLM Lab spreads the same NumPy-first idea across a staged bilingual route with metadata contracts, per-page checks, tests, an audit trail, and an explicit no-trained-model status.
- **Use in this project:** a benchmark for minimal readability when comparing the Build branch; not a syllabus and not a source to copy from.

### Visual explainers (Alammar, 3Blue1Brown, animated visualizations)

- These answer complementary questions (visual intuition) rather than offering a route. Their role and reuse boundaries are already recorded in [references](references.md) and the resource library; the 2026 TeachingNLP literature (e.g. AnimatedLLM) confirms interactive visualization as an active research direction, which supports LLM Lab's interactive explorations without changing their evidence status (illustration, not measurement).

Interactive model explorers such as poloclub's Transformer Explainer (https://poloclub.github.io/transformer-explainer/) and the 3D LLM Visualization (https://bbycroft.net/llm) sit between visual explainers and tools: readers manipulate a live computation rather than read a route. LLM Lab's micro-workbenches and interactive explorers stay text-embedded and evidence-bounded (checked 2026-11-09).

## Where LLM Lab stands out — and gaps to keep visible

**Standing out:** bilingual FR/EN semantic parity as a reviewed contract (rare; the nearest peer enforces EN/pt-BR); the four-destination structure (Understand/Build/Deepen/Practice) with a generated guided route; an evidence culture (audit inventory, distinction between illustration/test/experimental result, provenance-gated figures); a bilingual formative exercise hub; explicit publication of what is not implemented.

**Gaps vs the field, to keep honestly visible rather than disguised:** no end-to-end corpus-to-training-to-evaluation pipeline yet (Karpathy, Raschka, HF); adaptation/fine-tuning chapters not yet written (HF); serving/efficiency and hardware depth deferred (llmdeepdive); no trained-model experience in the core (all peers anchor on real checkpoints at some point). These gaps are already recorded in project status; this map should not be used to claim parity with any of the projects above.

## Maintenance

Re-dating rule: update a row when a project materially changes (scope, language, licence, access model) and record the recheck date; do not add every new tutorial that repeats existing explanations. Entries relying on third-party roundups should be replaced by direct page checks before being used for decisions.


## 2026-11-12 comparative update — two explicit learning journeys

This update directly inspects the current public structure of [mlabonne/llm-course](https://github.com/mlabonne/llm-course) and Microsoft's [LLM Fundamentals](https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals), and reconciles them with the previously extracted comparison of Raschka, Hugging Face and other peers. It updates the landscape; it does not create a new curriculum or imply that every linked notebook has been executed.

### Comparative position at a glance

| Dimension | LLM Lab | mlabonne/llm-course | Microsoft Learn — LLM Fundamentals |
|---|---|---|---|
| Main purpose | Explain how LLMs work, then make mechanisms inspectable through a small implementation and evidence-based practice | Provide a broad roadmap from foundations to model research/building and production application engineering | Give application developers the minimum LLM mental model needed before building agents |
| Structure | Two independent primary paths: Understand (conceptual) and Build (implementation dependency); Deepen and Practice support both | Three broad tracks: optional LLM Fundamentals, LLM Scientist, LLM Engineer; topic clusters and external resources | One compact foundation module inside a larger sequential Agent Development Journey |
| Starting assumptions | No blanket advanced-math prerequisite; local prerequisites introduced just in time | Fundamentals are optional/reference material; assumes learner will navigate a broad set of external resources and notebooks | Developer-oriented; explicitly permits experienced readers to skip fundamentals and move to agents |
| Core technical spine | Text/tokens → representations → Transformer computation → prediction → inference → scoring/learning; separate data/training branch | Architecture, tokenization, attention, pretraining, post-training, alignment, evaluation, quantization, merging; plus engineering topics | Definition and weights/architecture → tokens → pretraining/post-training/reasoning → inference/context → API messages and sampling → capabilities/limits → tool calling |
| Practical work | Maintained NumPy reference, tests, exercises and controlled experiments; currently no end-to-end trained model | Roadmap links to Colab notebooks and tools; implementation is distributed across external notebooks/platforms | Conceptual developer guide; its next step is to build agents with Agent Framework |
| Application engineering | Deliberately outside the current core; agent systems are not the central learning outcome | Major Engineer track: APIs/local models, prompting, vector stores, RAG, agents, optimization, deployment and security | Explicit continuation: agents, tools/MCP, skills, middleware, context providers, agent composition, A2A and workflows |
| Evidence model | Distinguishes explanation, tests, illustrative output and experimental evidence; status and limitations are explicit | Curated roadmap and linked hands-on resources; evidence quality varies by linked resource and is not centrally normalized | Explanatory guidance and trade-off framing; not a reproducible research or implementation audit |
| Language/access | French and English, parity treated as a maintained contract; open site and repository | English; open GitHub repository, free roadmap and linked notebooks | English and French Learn editions; official documentation |
| Best fit | Learners who want a rigorous, inspectable mental model and a small implementation without vendor lock-in | Learners who want breadth across the current LLM research and engineering ecosystem | Developers who need a concise foundation to make sensible choices when building agents |

### 1. mlabonne/llm-course — breadth across the LLM lifecycle

**Observed structure (repository README, checked 2026-11-12):**

1. **LLM Fundamentals** is explicitly optional and serves as a reference for mathematics, Python, neural networks and NLP.
2. **The LLM Scientist** focuses on building and improving models: architecture, pretraining, post-training data, fine-tuning, preference alignment (including DPO/PPO/GRPO), evaluation, quantization, model merging and newer directions such as multimodality, interpretability and test-time compute.
3. **The LLM Engineer** focuses on applications and deployment: running models, prompting and structured outputs, vector storage, RAG, agents, inference optimization, deployment and security.
4. **Notebooks and tools** link out to Colab, RunPod, Hugging Face and other resources. The repository is primarily a roadmap/resource index, not a single self-contained executable course. Linked notebooks are separate artifacts and should be inspected individually before claiming reproducibility or current compatibility.

**What transfers to LLM Lab:**

- Make the full lifecycle visible so readers can see what lies beyond a small GPT: post-training, evaluation, quantization, inference optimization, RAG, agents and security.
- Keep optional foundations available for reference rather than forcing every learner through a long mathematics prerequisite.
- Use a clear distinction between model-building work (Scientist) and application engineering (Engineer).
- Treat evaluation, data quality, alignment and security as first-class topics, not footnotes after architecture.

**What should not be copied:**

- Its breadth-first roadmap is not a substitute for LLM Lab's worked conceptual sequence.
- A link to a notebook is not equivalent to a maintained implementation, test suite or reproducible experiment.
- LLM Lab should not expand into every engineering topic merely to match the roadmap. Agent/application engineering belongs in a clearly labelled adjacent path or external-resource handoff unless a distinct project objective is approved.

**Positioning decision:** mlabonne is the strongest breadth/lifecycle map among these three, while LLM Lab is more explicit about conceptual ownership, implementation dependencies, bilingual parity and evidence status. The gap is not simply a missing list of topics; it is the absence of some complete end-to-end practical branches (training, adaptation and modern application engineering), already disclosed in project status.

### 2. Microsoft Learn — LLM Fundamentals as the on-ramp to agents

**Observed scope (page last updated 2026-08-25; checked 2026-11-12):**

The page is intentionally developer-oriented. It covers the definition of an LLM and the distinction between learned weights and architecture; tokens and token IDs; pretraining, SFT, RLHF and reasoning-oriented reinforcement learning; autoregressive inference, context windows, prefill/decode and KV cache; chat-completion message roles; temperature and non-determinism; strengths and limitations; and the mechanics of tool calling as structured token generation interpreted by application code.

It then bridges directly to the Agent Framework: instructions, tools/MCP, sessions/context, middleware and reliability. The wider [Agent Development Journey](https://learn.microsoft.com/en-us/agent-framework/journey/) continues through agents, tools, skills, middleware, context providers, agents-as-tools, A2A and workflows. The French Learn edition is also available at [Principes fondamentaux de LLM](https://learn.microsoft.com/fr-fr/agent-framework/journey/llm-fundamentals).

**What transfers to LLM Lab:**

- Explain the practical implications of context windows, prefill/decode, KV cache, latency, token cost and streaming alongside the conceptual mechanism.
- Make the software boundary in tool use unmistakable: the model emits a structured request; the host application executes it and returns the observation.
- Connect model capabilities and limitations to downstream system design, rather than presenting them as an abstract checklist.
- Offer a short, clearly marked transition for readers whose goal is application/agent development.

**What should not be copied:**

- Microsoft's page compresses mechanisms for developer orientation; it is not a substitute for mathematical derivations, worked numerical examples, implementation tests or a full training curriculum.
- Some simplifications are context-dependent (for example, temperature-zero determinism and the description of reasoning training). LLM Lab should state assumptions and model/provider variation rather than turn rules of thumb into universal guarantees.
- Agent Framework-specific API and workflow instruction should remain outside the vendor-independent LLM core.

**Positioning decision:** Microsoft is the best concise bridge from an LLM mental model to agent application architecture. LLM Lab should provide more inspectable foundations, then link outward to this journey when the learner's objective changes from understanding/building a model to engineering an agent.

### 3. Reconciliation with the previously extracted peer landscape

The earlier comparison remains useful and is not replaced by these two additions:

- **Raschka** remains the closest end-to-end from-scratch GPT construction reference; its implementation chapters are a useful coverage baseline for LLM Lab's incomplete training path.
- **Hugging Face LLM Course** remains the strongest ecosystem-oriented learning path for Transformers, datasets, tokenizers, fine-tuning and model sharing.
- **Karpathy Zero to Hero** remains a strong first-principles neural-network and GPT build sequence.
- **Stanford CS336** represents deeper academic treatment of language-model training and systems.
- **mneves75/llmdeepdive** remains a close peer for broad model-internals coverage, bilingual delivery (EN/pt-BR), quizzes and serving/hardware depth.
- **Cohere LLM University** provides integrated notebook practice in a vendor-maintained learning environment.
- **Princeton COS 597G** offers a research-paper seminar route rather than a beginner implementation course.
- **picoGPT, Jay Alammar, 3Blue1Brown, Transformer Explainer and bbycroft** are best treated as focused implementation or visual companions, not full curricula.

The comparison is about learning goals, sequence, scope, practice and evidence—not a ranking of quality or a claim that the resources have equivalent depth.

### 4. Curriculum implications — prioritized, without duplicating existing work

| Priority | Implication | Decision / destination |
|---|---|---|
| P1 | Make the boundary between a small educational GPT and a useful pretrained assistant explicit | Preserve the existing status disclosure; do not imply the random-init model demonstrates language quality |
| P1 | Close the actual Build gap from corpus/tokenizer preparation through training, validation, checkpointing and held-out evaluation | Continue under existing G1b/G2/G8/G9 ownership and linked issues; do not create duplicate milestones |
| P1 | Improve the evaluation thread: baselines, leakage/contamination, uncertainty, error analysis and reproducibility | Integrate with existing evaluation pages and experiment protocol |
| P2 | Add a concise practical inference/serving bridge: prefill vs decode, KV cache, throughput/latency and memory | Extend canonical Deepen pages where ownership already exists; link to engineering references for deployment specifics |
| P2 | Make post-training distinctions navigable: SFT, preference optimization/RL, reasoning training, prompting and retrieval are not interchangeable | Keep the existing post-training page and separate Build adaptation branch; add only missing learning outcomes |
| P2 | Provide a short “from LLMs to agents” handoff covering tool-call boundary, context/memory and orchestration | Prefer a clearly labelled external pathway/resource handoff before creating a full agent-engineering curriculum |
| P3 | Add breadth topics such as multimodality, model merging, interpretability and security | Keep as optional Deepen or curated external resources until a concrete audience and evidence-backed scope justify expansion |

**Non-goal:** matching the number of modules or topics in mlabonne or Microsoft. The success criterion is a coherent, accurate and testable learning experience, not topic-count parity.

### 5. Source and evidence record

- [mlabonne/llm-course README](https://github.com/mlabonne/llm-course) — primary source for the three-track structure and linked roadmap topics; repository inspected 2026-11-12. Individual Colab notebooks were not executed.
- [Microsoft Learn — LLM Fundamentals](https://learn.microsoft.com/en-us/agent-framework/journey/llm-fundamentals) — official page inspected 2026-11-12; page reports last update 2026-08-25.
- [Microsoft Learn — Agent Development Journey](https://learn.microsoft.com/en-us/agent-framework/journey/) — official continuation map inspected 2026-11-12.
- [Microsoft Learn — Parcours de développement de l’agent (FR)](https://learn.microsoft.com/fr-fr/agent-framework/journey/) — French journey landing page inspected 2026-11-12.
- Existing internal baseline: [Raschka/Hugging Face comparative audit](source-reviews/learning-path-comparison-2026-11-05.md), plus the peer entries and verification caveats above.

**Maintenance:** recheck the primary pages when their structure changes materially. Do not treat this dated snapshot as a live syllabus; do not infer notebook execution, learner outcomes, or full source audits from README descriptions alone.
