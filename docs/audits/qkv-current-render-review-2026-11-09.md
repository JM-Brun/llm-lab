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


## Current Quarto/Chromium rendered review — 2026-11-25

The five-tour Build correction was merged in [PR #1618](https://github.com/JM-Brun/llm-lab/pull/1618) at merge commit `225f312fca4aa68431355609d2157843af9457a2`. Its required full-site Quarto/browser workflow completed successfully on the exact PR head `2d073c2e57121179efc9319e3bf0f2f3d259501e` (run [45574557862](https://github.com/JM-Brun/llm-lab/actions/runs/45574557862), browser artifact [15003897316](https://github.com/JM-Brun/llm-lab/actions/runs/45574557862/artifacts/15003897316)). The artifact was downloaded and its four Q/K/V screenshots and `report.json` inspected on 2026-11-25.

### Exact Q/K/V cases inspected

- Chromium, light theme, English and French, desktop 1440 × 1000 and mobile 390 × 844.
- All four page responses were HTTP 200. The report records no browser console errors or page errors.
- No horizontal document overflow at any of the four viewports. The two project-owned diagrams load in each language; desktop image width is 810 px and mobile image width is 313 px. Both localized image `alt` descriptions are present.
- All 15 MathJax spans render in each case; no raw/unrendered math delimiters are reported.
- Desktop Axe: zero violations in both languages (31 passes and one incomplete item per page). Axe is not run on mobile in this profile.
- Desktop keyboard probe: 94 observed focus targets and 94 with visible focus in each language. The disclosure toggles with Enter. The automated traversal did not complete a full tab cycle, so this is not evidence of complete keyboard-path coverage.
- The native Quarto breadcrumb is unique (one native breadcrumb, no custom duplicate). The learning-path context is separately labelled, its stage anchor resolves, and the previous/next links point to Transformer and scaled dot-product attention in the expected language.
- Manual screenshot inspection found no clipping or layout break in the desktop or mobile captures. The mobile-specific vertical Q/K/V and score/weight/output diagrams fit the viewport; their fine labels remain smaller than on desktop and should be considered when planning a touch/screen-reader review.

### Interpretation and remaining boundary

This is fresh rendered evidence for the exact merged source tree, produced by the PR's local Quarto/Chromium review (the report's base URL is `http://127.0.0.1:4173`), not a fresh browser session against the public Pages hostname. The earlier deployment-artifact inspection remains useful structural evidence, but the inspected deployed artifact predates the latest Q/K/V source edits; do not call it the current live screenshot. No manual screen-reader, mobile touch, or assistive-technology session was performed. The browser report's single Axe incomplete item is retained as a limitation; the report does not expose a detailed finding for it.

**Disposition:** current bilingual rendered screenshots, responsive layout, MathJax, browser errors, localized image loading/alt attributes, route context and desktop Axe results are now evidenced for the merged source tree. Keep #483 open for live Pages verification after the updated site is deployed, manual keyboard/touch review, and screen-reader exposure of the diagrams. Keep #447 gated until those remaining accessibility/deployment checks are completed. Third-party media remain link-only/deferred under the existing asset audit; no source scan or asset recreation is warranted.


## Published GitHub Pages artifact — 2026-11-25

After #1619 merged, the main push at `76947990894396b4ee7781e7e2d0d6080785319d` triggered the existing `Publish Quarto site` workflow [45577505144](https://github.com/JM-Brun/llm-lab/actions/runs/45577505144). Both `Render Quarto site` and `Deploy to GitHub Pages` completed successfully. I downloaded and inspected the workflow's `github-pages` artifact [15003974584](https://github.com/JM-Brun/llm-lab/actions/runs/45577505144/artifacts/15003974584), including the current EN/FR Q/K/V HTML and associated SVG assets.

### What the deployed artifact establishes

- Both current pages are present and localized: `en/queries-keys-values.html` and `fr/queries-keys-values.html`.
- The dedicated practice links resolve to existing companions: `../en/exercises/queries-keys-values.html` and `../fr/exercises/queries-keys-values.html`.
- The Further exploration / Approfondir sections retain the expected advanced Q/K/V, attention-variant and Transformer-block links.
- The EN/FR language-switch links are present.
- The two project-owned diagrams per language have localized `alt` text; their mobile and desktop SVG assets are present in the deployment artifact.
- A local-file and fragment-target check across the main lesson found 29 local links per language and zero missing file or fragment targets. The dedicated practice destinations exist.
- The main content contains no visible `type:`, `destination:`, `topic:`, `level:` or `status:` editorial metadata strings.

This closes the **deployment-artifact structural verification** that was still open in the previous section. It is not a live public-host browser session: the public URL fetch was not available from the inspection environment, and no live viewport screenshot was captured after deployment. The Chromium screenshots and visual inspection recorded above remain evidence for the same merged source tree, while the deployment artifact confirms that the published package contains the expected current pages and assets.

**Remaining #483 gates:** live-host browser screenshot/visual confirmation if a reachable browser environment becomes available; manual full keyboard and touch-device review; and manual screen-reader verification of the diagram alternatives. Do not infer these from the successful deployment or from the HTML `alt` attributes. #447 remains gated until the outstanding accessibility review is completed.
