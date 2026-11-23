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

## Deployment artifact inspection — 2026-11-23

The Q/K/V practice-navigation update was merged in [PR #1558](https://github.com/JM-Brun/llm-lab/pull/1558) at commit `4f0302ae1dad3f68fcee6f48cd606245f617fa92`. The `Publish Quarto site` workflow ran on that exact `main` commit (run [45210029278](https://github.com/JM-Brun/llm-lab/actions/runs/45210029278)); its `Render Quarto site` and `Deploy to GitHub Pages` jobs both completed successfully. The GitHub Pages deployment artifact (artifact ID `14834778755`) was downloaded and inspected locally.

### What the artifact establishes

- Both generated pages exist: `fr/queries-keys-values.html` and `en/queries-keys-values.html`.
- Both contain the updated, single reader-facing link to their dedicated Q/K/V practice companion.
- Both contain the language switch, advanced Q/K/V destination, canonical previous/next navigation and expected bilingual headings.
- The two project-owned figures per language are present with localized, descriptive `alt` attributes.
- Each `<picture>` includes a mobile SVG source selected at `(max-width: 600px)` and a desktop fallback image.
- The generated HTML contains 14 inline-math wrappers and one display-math wrapper per language. This is a structural observation only; it is not evidence that MathJax rendered them correctly in a live browser.
- All local file targets and local HTML fragment targets referenced from the main lesson content resolve in the downloaded artifact for both languages.
- The generated DOM contains Quarto's responsive breadcrumb variants and a separate learning-path context; the source does not introduce a second custom breadcrumb component.

Comparing the deployment commit with current `main` shows that subsequent commits changed calendar pages and documentation, not the Q/K/V pages, shared stylesheet or Quarto configuration. The inspected artifact therefore remains representative of the current Q/K/V page inputs and shared presentation configuration.

### Limits

This is inspection of the exact Pages deployment artifact and its generated HTML, not a fresh live-URL browser session. A headless Chromium attempt in the present inspection environment did not complete, so no new screenshots, viewport rendering, console report or visual clipping assessment is claimed here. The earlier PR #1032 screenshots remain useful historical visual evidence for the refined diagrams, but do not validate the current deployed practice-link placement.

No manual screen-reader, touch-device or complete keyboard session was performed. The generated `alt` attributes and SVG `<title>`/`<desc>` metadata do not establish how a screen reader announces the images. These items remain open under #483 and #584.

### Asset-provenance disposition

The existing asset audit already gives an explicit conservative disposition for every identified external media placement; no further source scan or asset recreation is justified:

- Nishanthan K / DEV and the author-controlled Medium mirror: the retrieved DEV overview is link-only because figure-specific reuse permission is unverified; the mirror's in-body placeholder remains unresolved and link-only.
- Neha KK / Medium: all three captioned figure placements and the uncaptioned placement remain link-only; the image bytes and figure-specific reuse terms are unavailable.
- Codefinity: the two resolved SVGs are interface/section icons, not explanatory Q/K/V figures; do not copy them. No substantive explanatory figure was exposed in the retrieved lesson text, and the course remains partially scanned.
- LLM Lab: retain the independently authored bilingual project SVGs; no third-party artwork is embedded.

**Disposition:** the media-reuse decision is explicit (link-only/deferred wherever provenance or permission is incomplete). The rendered-page gate is partially advanced by the inspected deployment artifact, but remains open for current browser screenshots/visual review and manual assistive-technology/touch verification. Do not close #483 or unblock #447 on the basis of this artifact alone.
