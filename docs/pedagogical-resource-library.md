# Pedagogical resource library

This curated list supports the editorial method in [the reader-experience guide](reader-experience-and-editorial-method.md). It is a source-discovery tool, not a syllabus and not a substitute for primary evidence. Use it when drafting or revising explanations, figures, diagrams, examples, and interactive demonstrations.

## How to use this library

For each important concept:

1. Start from the learner's question and the claim the page must explain.
2. Look for at least one strong visual or intuitive explanation and, where relevant, one interactive demonstration.
3. Check the underlying claim against primary literature, formal derivations, standards, or official documentation. A polished animation is not evidence by itself.
4. Compare assumptions, notation, examples, simplifications, and omissions across sources. Record meaningful differences.
5. Create an original explanation suited to this book: consistent notation, a worked example, counterexamples, limitations, and links to relevant code/tests when they exist.
6. For figures or animations, prefer original work. If reusing an asset, verify the exact licence and attribution requirements; a publicly viewable image is not automatically reusable. Record provenance in [the visual references page](../site/references.qmd).

Do not add a diagram or animation merely for decoration. It should answer a specific question more clearly than prose alone. Keep figures accessible with captions, alt text, readable labels, and an explanation of what the figure does not show.

## A repeatable improvement loop

Use this lightweight loop for a substantial concept-page revision. The goal is not to research every resource on every page; it is to make a defensible pedagogical decision with minimal overhead.

1. **Name the learner problem.** Write one sentence in the form: “A learner may confuse X with Y; this page should make the distinction observable.”
2. **Select sources by role, not by popularity.** Usually start with one pedagogical/visual source and one primary paper or official technical reference. Add an interactive tool only if manipulating an input can reveal something static prose cannot. Use at most three sources initially; expand the search only when a key claim or design choice remains unresolved.
3. **Compare, do not collect.** Record the useful teaching move, its simplification or omission, and whether it transfers to this page. Do not treat a source's presence in this library as proof that it is current, correct, accessible, or reusable.
4. **Choose an explicit outcome.** Keep the existing page; clarify prose; add a worked example; improve an original diagram; add an interaction; or defer a visual because it would add complexity without learning value. “No visual change” is a valid outcome when justified.
5. **Make the smallest useful change.** Prefer a focused edit that can be evaluated over a page-wide rewrite. For bilingual pages, apply the same learning objective and evidence to both languages; literal translations are not the acceptance criterion.
6. **Validate against the claim.** Check arithmetic or executable examples where relevant, verify technical statements against primary/official sources, check links and image provenance, render the page, inspect responsive layout/accessibility, and compare the language versions.
7. **Record evidence and remaining work.** For a substantial change, add a short entry to page-audit-inventory.md: learner problem, resources consulted and their roles, decision made, files changed, validation actually run, and checks still outstanding. Never label a check as passed unless it was run.

### Compact decision record

Use this small record in the audit inventory or PR description; do not create a separate report for a trivial typo.

| Field | Prompt |
|---|---|
| Learner problem | What likely misconception or difficult step are we addressing? |
| Evidence roles | Which pedagogical source and which primary/official source were useful? |
| Design decision | What changed, and why is it better than the previous version? If nothing changed, why? |
| Risk/limitation | What might the visual, analogy, example, or source cause readers to misunderstand? |
| Validation | What was actually rendered, calculated, tested, or checked? |
| Follow-up | What remains unverified, including the other language or responsive display? |

**Stop condition:** do not keep searching once the learner problem is addressed, the technical claim is grounded, and the remaining uncertainty is documented. If those conditions are not met, state the gap instead of disguising it with more links or decorative graphics.


## Visual explainers and technical diagrams

| Resource | Best use | Notes |
|---|---|---|
| [ByteByteGo — Visual Guides](https://bytebytego.com/guides/) · [YouTube](https://www.youtube.com/@ByteByteGo) | System diagrams, architecture, data flow, and compact step-by-step explanations | Strong reference for visual hierarchy and diagram composition; many topics are system-design oriented rather than mathematical LLM explanations. |
| [Vizuara](https://vizuara.ai/) · [YouTube](https://www.youtube.com/@vizuara) | AI/ML concepts, technical walkthroughs, and visual teaching | Inspect topic-specific lessons for ways to sequence intuition, equations, and implementation. |
| [The Synthetic Mind](https://www.youtube.com/@the-synthetic-mind) | AI and synthetic-media/ML topics explained visually | Use relevant videos as a source of presentation ideas; verify technical claims independently. |
| [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) | Transformer architecture, attention, tensor/data flow | A useful model for pairing a high-level visual narrative with technical terminology. |
| [Distill](https://distill.pub/) | Interactive research explanations and visual reasoning | Particularly useful for learning how interaction can expose structure; check each article's claims and publication context. |
| [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) | Interactive, token-by-token Transformer inference | Useful for connecting tokens, attention, activations, and outputs; treat its interface as an illustration of a particular model and implementation. |
| [BertViz](https://github.com/jessevig/bertviz) | Inspecting attention patterns in Transformer models | Good for exploratory visualization, but attention patterns alone do not establish causal explanations or model reasoning. |
| [TensorFlow Embedding Projector](https://projector.tensorflow.org/) | Exploring embeddings and dimensionality-reduction projections | Explicitly explain that 2D/3D projections can distort distances and neighbourhoods. |
| [NN-SVG](https://alexlenail.me/NN-SVG/) | Producing clean neural-network architecture diagrams | Diagram generation tool; check whether its visual conventions fit the model being described. |

## Intuition, mathematics, and scientific explanation

| Resource | Best use | Notes |
|---|---|---|
| [3Blue1Brown](https://www.youtube.com/@3blue1brown) | Linear algebra, calculus, neural networks, attention, gradient descent | Excellent reference for geometric intuition, animation pacing, and carefully staged visual arguments. |
| [Science Étonnante](https://www.youtube.com/@ScienceEtonnante) | French-language scientific explanations, analogies, and reasoning | Useful for narrative structure and intuition; validate technical details against sources appropriate to the claim. |
| [StatQuest](https://www.youtube.com/@statquest) | Statistics, probability, ML methods, and neural networks | Useful for decomposing terminology and building explanations in small steps. |
| [Serrano.Academy](https://www.youtube.com/@SerranoAcademy) | Geometric explanations of ML, neural networks, and NLP | Useful for accessible visual reasoning and alternative explanations of model mechanisms. |
| [Andrej Karpathy — Zero to Hero](https://www.youtube.com/@AndrejKarpathy) | Connecting conceptual explanations to executable implementations | Especially useful for tracing the path from mathematical idea to code and training behavior. |
| [Sebastian Raschka — LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch) | A code-first reference for LLM architecture and implementation | An important comparison point, not the sole authority for curriculum, explanations, or coverage. |
| [Seeing Theory](https://seeing-theory.brown.edu/) | Interactive probability and statistics | Useful for distributions, inference, and uncertainty; check that the chosen visualization supports the precise mathematical claim. |
| [3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) | Geometric intuition for vectors, matrices, and linear transformations | Use alongside formal definitions and examples that match the notation used in this book. |

## Official and primary sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — original Transformer paper.
- [PyTorch documentation and tutorials](https://pytorch.org/tutorials/) — implementation semantics and executable examples.
- [Hugging Face documentation](https://huggingface.co/docs) — model, tokenizer, training, and inference interfaces.
- [The Deep Learning textbook](https://www.deeplearningbook.org/) — mathematical foundations and formal context.

Use primary papers for original technical contributions, official documentation for software contracts, and controlled experiments for empirical claims. Pedagogical sources help explain a result but do not replace evidence.

## Topic-to-resource lookup

| Topic | Useful starting points | Questions to ask |
|---|---|---|
| Vectors, matrices, derivatives, gradients | 3Blue1Brown; Seeing Theory | What is the geometric meaning? Which assumptions are hidden by the picture? |
| Probability, likelihood, cross-entropy | StatQuest; Seeing Theory; primary/statistical references | What is random, what is conditioned on, and what quantity is actually optimized? |
| Transformer and self-attention | Illustrated Transformer; Vizuara; Transformer Explainer; original paper | What are the axes and tensor shapes? What is omitted from the simplified diagram? |
| Embeddings and similarity | Embedding Projector; Distill; primary papers | Which distances are preserved, and what distortions are introduced by projection or normalization? |
| Training and optimization | 3Blue1Brown; Karpathy; PyTorch docs | Which quantity changes at each step? What do gradients and optimizer state represent? |
| Architecture and inference data flow | ByteByteGo; Vizuara; Hugging Face docs | Which components and interfaces are conceptual versus implementation-specific? |
| Evaluation and uncertainty | StatQuest; primary evaluation papers; official metric documentation | What is the estimand, split unit, baseline, uncertainty, and failure mode? |

## Contribution checklist

When adding or revising a concept page, consider and record the relevant items in the PR:

- [ ] Searched this library for a clear intuition, diagram, figure, animation, or interactive demonstration.
- [ ] Compared more than one explanation for important or easily misunderstood concepts, where useful.
- [ ] Identified what each source simplifies or leaves unexplained.
- [ ] Checked technical claims against suitable primary or official sources.
- [ ] Added an original figure/example or explained why prose is the better medium.
- [ ] Checked image licences, attribution, alt text, captions, and rendered layout for any visual material.
- [ ] Kept the French and English pages substantively equivalent.
- [ ] Avoided presenting illustrative visualizations as proof of a scientific claim.

This checklist is intended to encourage useful research, not impose a fixed number of sources or figures on every page.
