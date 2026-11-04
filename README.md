# LLM Lab

A reproducible, code-first lab for understanding how language models work—from tokenization and attention to pre-training, fine-tuning, evaluation, and efficiency.

The goal is not to train a production-scale LLM from scratch. It is to implement small, inspectable components, test their mathematical properties, run controlled experiments, and document what the evidence does and does not show.

## Contributing

Contributions can improve concept explanations, French/English parity, reference implementations, numerical tests, reproducible experiments, critical reviews, figures/references, or developer tooling. Each mode has its own acceptance criteria; see [CONTRIBUTING.md](CONTRIBUTING.md) and use the PR template to state which mode your change follows.

The information architecture, metadata ownership boundaries, and knowledge-graph maintenance rules are documented in [docs/information-architecture.md](docs/information-architecture.md).

## Learn through the Quarto site

The project includes a bilingual Quarto website organized around LLM-specific explanations: overview pages connect mechanisms, applied concept pages explain how the mathematics is used in language models, and implementation/tests are linked when they exist. General mathematical foundations belong in the separate `wiki-knowledge` knowledge base; because that wiki is private, public lessons retain all definitions, assumptions, derivations, examples, and caveats needed to understand the LLM application, and cite accessible public references. Pages explicitly distinguish verified code from planned work.

- French introduction: `site/index.qmd`
- English introduction: `site/en/index.qmd`
- Transformer overview: `site/fr/transformer.qmd` and `site/en/transformer.qmd`
- Glossary: `site/fr/glossary.qmd` and `site/en/glossary.qmd`
- Transformer history and timeline: `site/fr/transformer-history.qmd` and `site/en/transformer-history.qmd`
- Guided build route and line-by-line reference-code walkthroughs: `site/fr/build-path.qmd` and `site/en/build-path.qmd`, plus five walkthrough pages per language covering each module of the reference implementation (`gpt-config`, `gpt-ops`, `transformer-block`, `gpt-model`, `gpt-generation`).
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
- Reusable editorial-boundary audit skill: [`.agents/skills/editorial-boundary-audit/SKILL.md`](.agents/skills/editorial-boundary-audit/SKILL.md) — evidence-based overlap analysis, canonical concept ownership, and core-versus-advanced decisions.
- Page metadata and learning-graph contract: [`docs/page-metadata-schema.md`](docs/page-metadata-schema.md) — hidden source map, Quarto keywords, tag vocabulary, and relation semantics.
- Full curriculum plan and source-coverage audit (Raschka is a source, not the table-of-contents authority): [`docs/full-curriculum-plan.md`](docs/full-curriculum-plan.md)
- Page-by-page audit status and source-role log (partial; rendered review still pending): [`docs/page-audit-inventory.md`](docs/page-audit-inventory.md)
- First-pass audit separating general foundations from LLM-specific applications: [`docs/editorial-boundary-audit.md`](docs/editorial-boundary-audit.md)
- Core-route editorial boundary audit (2026-11-04): [`docs/editorial-boundary-audit-2026-11-04.md`](docs/editorial-boundary-audit-2026-11-04.md) — page-level overlap evidence, canonical ownership, and core-versus-optional recommendations.
- Separate exercise-space entry points (navigation scaffolding only; exercises not yet written): [French](site/fr/exercises.qmd) · [English](site/en/exercises.qmd)

The site uses carefully attributed illustrations embedded from their original source when suitable. It does not mirror or redistribute external image files. An accessible URL is not a licence: check reuse terms before copying or modifying a figure. The site can be rendered locally with the [Quarto CLI](https://quarto.org/docs/get-started/). Generate the page/concept graph data and the bilingual guided-route Markdown partials first; Quarto expands Markdown includes before its project pre-render hooks, so these files must exist before rendering.

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python scripts/build_learning_map.py
quarto render site
```

The generated JSON and Markdown fragments are build artifacts and are ignored by Git. The rendered site is written to `site/_site/`. The Quarto CLI is a separate system dependency; it is not installed by `uv`.

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
- **Keep French and English equivalent.** Preserve the same claims, qualifications, examples, and references in both versions.
- **Prefer application, not artificial brevity.** Focus examples and interpretation on LLMs, but retain every definition, assumption, derivation, example, caveat, and exercise needed for the reader to understand the application. Repeat general material when necessary; never shorten a lesson solely to eliminate overlap with the private Wiki.
- **Hide answer keys by default.** Control-question answers should be revealed only when the reader expands them.

## Learning principles

- **Understand before scaling:** start with small tensors, toy corpora, and small models.
- **Verify implementations:** test shapes, masks, gradients, and numerical behavior.
- **Measure rather than assume:** record baselines, seeds, compute costs, limitations, and failure cases.
- **Keep experiments reproducible:** version code, configuration, data provenance, and evaluation procedures.
- **Separate teaching from performance:** readable reference implementations first; optimized kernels and libraries as comparisons.
- **Use public, appropriately licensed data:** document provenance and avoid committing datasets, model weights, credentials, or generated artifacts.

## Learning path

The [canonical learning path](docs/learning-path.md) is the single source of truth for module order, prerequisites, evidence and implementation status. The public site separates four destinations: Understand (conceptual explanations), Build (the G0–G9 from-scratch GPT route), Deepen (optional technical and mathematical depth), and Practice & experiment (exercises and evidence-producing investigations).

The from-scratch route demonstrates inference before training, then prepares training examples and proceeds to learning and verification. G2 is a training-data branch, not a prerequisite for understanding inference. A1–A4 form a separate pretrained-model adaptation route; E1 covers evaluation across routes. These are not fixed calendar stages, and planned modules must not be read as completed implementations.

See [the learning path](docs/learning-path.md) for the authoritative module-level objectives and evidence gates, the [roadmap](docs/roadmap.md) for priorities and acceptance criteria, and the [experiment protocol](docs/experiment-protocol.md) for reporting requirements.

## Repository layout

- `src/llm_lab/`: reusable, typed Python implementations.
- `tests/`: unit and numerical tests.
- `notebooks/`: optional explanatory notebooks; core logic should remain importable from `src`.
- `experiments/`: versioned configurations and runnable experiment entry points.
- `reports/`: concise, evidence-backed results and limitations.
- `docs/`: learning path, mathematical foundations, experiment protocol, annotated references, and roadmap.
- `site/`: Quarto website sources in French and English.

## Quick start

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Install the optional deep-learning dependencies when a module needs them:

```bash
uv sync --dev --extra ml
```

Install the Git hooks once per clone:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

The first `uv sync` creates or updates `uv.lock`; commit that file so collaborators and CI can reproduce the resolved environment.

## Hardware policy

Core exercises should run on CPU with small inputs. Later experiments may offer PyTorch CPU/MPS/CUDA or MLX alternatives where appropriate. No module should require a large GPU just to understand the concept. Record device, software versions, runtime, and peak memory for performance claims.

## Research and references

The project builds on existing educational work rather than presenting established techniques as original. See [the annotated references](docs/references.md) and [the Quarto figure provenance page](site/references.qmd). Each experiment should cite the method, implementation, dataset, and evaluation setup it uses.

## Status

Current scope: a bilingual Quarto learning site, a tested NumPy reference implementation of a small decoder-only GPT — configuration, numerical building blocks, attention primitives, one pre-LN Transformer block, the assembled model and the autoregressive generation loop in `src/llm_lab/foundations/`, plus cross-entropy loss/gradient helpers, a minimal sliding-window input/target construction for training examples, and top-k/top-p truncation filters for decoding distributions, available in the generation loop as optional sampling-only parameters — and automated Python/Quarto checks. The reference covers inference and training-example construction: the corpus/tokenizer pipeline, the training loop and end-to-end evaluation remain planned; see [`docs/roadmap.md`](docs/roadmap.md) for verified status, priorities, and completion criteria. Passing CI verifies configured checks, not research claims or visual quality.

## License

No license has been selected yet. Until a license is added, do not assume that others have permission to reuse, modify, or redistribute this repository's code.
