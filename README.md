# LLM Lab

A reproducible, code-first lab for understanding how language models work—from tokenization and attention to pre-training, fine-tuning, evaluation, and efficiency.

The goal is not to train a production-scale LLM from scratch. It is to implement small, inspectable components, test their mathematical properties, run controlled experiments, and document what the evidence does and does not show.

## Contributing

Contributions can improve concept explanations, French/English parity, reference implementations, numerical tests, reproducible experiments, critical reviews, figures/references, or developer tooling. Each mode has its own acceptance criteria; see [CONTRIBUTING.md](CONTRIBUTING.md) and use the PR template to state which mode your change follows.

## Learn through the Quarto site

The project includes a bilingual Quarto website organized around LLM-specific explanations: overview pages connect mechanisms, applied concept pages explain how the mathematics is used in language models, and implementation/tests are linked when they exist. General mathematical foundations belong in the separate `wiki-knowledge` knowledge base; because that wiki is private, public lessons retain all definitions, assumptions, derivations, examples, and caveats needed to understand the LLM application, and cite accessible public references. Pages explicitly distinguish verified code from planned work.

- French introduction: `site/index.qmd`
- English introduction: `site/en/index.qmd`
- Transformer overview: `site/fr/transformer.qmd` and `site/en/transformer.qmd`
- Glossary: `site/fr/glossary.qmd` and `site/en/glossary.qmd`
- Transformer history and timeline: `site/fr/transformer-history.qmd` and `site/en/transformer-history.qmd`
- Dedicated attention concepts: Q/K/V, scaled dot-product attention, and causal masking, each with French and English pages under `site/fr/` and `site/en/`
- Applied mathematical chain (logits → probabilities → token likelihood/loss → gradients): `site/fr/mathematical-foundations.qmd` and `site/en/mathematical-foundations.qmd`
- Transformer tensor shapes and axes, in French and English: `site/fr/tensors.qmd` and `site/en/tensors.qmd`
- Cross-entropy and KL divergence: `site/fr/cross-entropy.qmd` and `site/en/cross-entropy.qmd`
- Critical notes on cosine similarity: `site/fr/cosine-similarity.qmd` and `site/en/cosine-similarity.qmd`
- Critical notes on embedding linearity: `site/fr/linearite-embeddings.qmd` and `site/en/embedding-linearity.qmd`
- Visual references and image provenance: `site/references.qmd`
- Live backlog dashboard (priority filters, current slice, dependencies and next work): [`docs/backlog-dashboard.md`](docs/backlog-dashboard.md)
- Prioritized roadmap and acceptance criteria: [`docs/roadmap.md`](docs/roadmap.md)
- Shared reader-experience and editorial method: [`docs/reader-experience-and-editorial-method.md`](docs/reader-experience-and-editorial-method.md) — progressive disclosure, non-linear navigation, page types, and review criteria.
- Page metadata and learning-graph contract: [`docs/page-metadata-schema.md`](docs/page-metadata-schema.md) — hidden source map, Quarto keywords, tag vocabulary, and relation semantics.
- Full curriculum plan and source-coverage audit (Raschka is a source, not the table-of-contents authority): [`docs/full-curriculum-plan.md`](docs/full-curriculum-plan.md)
- Page-by-page audit status and source-role log (partial; rendered review still pending): [`docs/page-audit-inventory.md`](docs/page-audit-inventory.md)
- First-pass audit separating general foundations from LLM-specific applications: [`docs/editorial-boundary-audit.md`](docs/editorial-boundary-audit.md)
- Separate exercise-space entry points (navigation scaffolding only; exercises not yet written): [French](site/fr/exercises.qmd) · [English](site/en/exercises.qmd)

The site uses carefully attributed illustrations embedded from their original source when suitable. It does not mirror or redistribute external image files. An accessible URL is not a licence: check reuse terms before copying or modifying a figure. The site can be rendered locally with the [Quarto CLI](https://quarto.org/docs/get-started/).

```bash
quarto render site
```

The rendered site is written to `site/_site/`. The Quarto CLI is a separate system dependency; it is not installed by `uv`.

## Page composition

- Contributor entry point and template map: [page-template guide](docs/page-template-guide.md) and [page archetype map](docs/site-page-design-system.md).
- Canonical soft composition model and reusable patterns: [page-template system](docs/page-template-system.md), [scientific page patterns](docs/page-patterns.md), and [implementation-page patterns](docs/implementation-page-patterns.md).

## Editorial and content principles

These are repository-maintenance guidelines, not reader-facing lessons; they belong here rather than on the public site homepages.

- **Separate canonical scope from reader-facing completeness.** The private Wiki owns reusable, domain-general treatments; the public LLM Lab book must teach all mathematics needed for its LLM learning path. Intentional overlap is expected and is not a defect.
- **Introduce terms before relying on them.** Define unfamiliar vocabulary on first use or link to another public page in this book. Private Wiki links are never a substitute for a necessary explanation.
- **Intuition with provenance.** Explain the problem a concept addresses and distinguish original research, official documentation, pedagogical explanations, and illustrations.
- **Progressive disclosure, non-linear navigation.** Lead with the question and mental model; let readers choose whether to follow a derivation, implementation, or research branch. Related links form a learning graph, not a mandatory chain. Apply the shared [reader-experience method](docs/reader-experience-and-editorial-method.md).
- **State assumptions and limits.** Use counterexamples to distinguish plausible but incorrect interpretations.
- **Connect mathematics to code carefully.** Identify existing implementations and tests, or state clearly when they do not exist.
- **Keep public pages self-contained.** A private wiki, file, or note may inform research but cannot be a prerequisite for readers of the public site.
