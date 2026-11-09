# Q/K/V current-main rendered review — 2026-11-09

**Purpose:** satisfy the remaining rendered-page evidence gate in issue [#483](https://github.com/JM-Brun/llm-lab/issues/483) by reusing the existing Quarto/Chromium workflow on the current main source tree. This is a bounded verification task, not a new browser framework or source/media audit.

## Scope

- English and French Q/K/V lesson pages.
- Desktop and mobile viewports, using the existing workflow matrix.
- Rendered mathematical expressions and the aligned Q/K/V projection equation.
- Project-owned Q/K/V SVG loading and localized alternative text.
- Responsive overflow, browser errors, keyboard/focus behavior, disclosures and Axe findings where the existing harness covers them.
- Breadcrumb and previous/next destinations where the existing assertions cover them.

## Evidence rules

- The PR-local Quarto render is evidence for the exact main-derived source tree tested; it is not automatically evidence of the deployed GitHub Pages host.
- Inspect screenshots and the JSON report rather than relying on a passing workflow summary.
- Distinguish desktop-only Axe results from mobile rendering checks.
- Distinguish keyboard automation from manual touch-device and screen-reader testing.
- Do not infer SVG accessibility-tree exposure from source `<title>`/`<desc>` metadata alone.
- Keep third-party image provenance and reuse rights separate; do not copy or recreate assets without verified bytes, creator and permission/licence.

## Exit criteria

Record exact workflow run, tested commit, viewport/browser cases, screenshots/report artifact, observed results and limitations. Link reproducible defects to existing issues. This report is intentionally a pre-run scope record; it contains no result claims.
