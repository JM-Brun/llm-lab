import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const BASE = (process.env.SITE_BROWSER_BASE_URL || "https://jm-brun.github.io/llm-lab").replace(/\/$/, "");
const OUT = "artifacts/site-browser-review";
fs.mkdirSync(OUT, { recursive: true });

const visualCases = ["light", "dark"].flatMap(theme => [
  { lang: "en", viewport: { width: 1440, height: 1000 }, label: "desktop", theme },
  { lang: "fr", viewport: { width: 1440, height: 1000 }, label: "desktop", theme },
  { lang: "en", viewport: { width: 390, height: 844 }, label: "mobile", theme },
  { lang: "fr", viewport: { width: 390, height: 844 }, label: "mobile", theme },
]);

const routeContextCases = visualCases.filter(testCase => testCase.theme === "light");

const cases = [
  ...visualCases.map(testCase => ({
    ...testCase, page: "learning-map.html", kind: "learning-map",
  })),
  ...routeContextCases.flatMap(testCase =>
    ["llm-overview.html", "generation.html", "text-data.html", "tokenization-strategies.html", "unicode-text.html", "tokenizer-design-evaluation.html", "embedding-space.html", "positional-encoding.html", "contextualized-representations.html", "tensors.html", "rope.html", "transformer.html", "queries-keys-values.html", "scaled-dot-product-attention.html", "causal-masking.html", "cross-attention.html", "logits.html", "probabilities.html", "likelihood.html", "decoding-strategies.html", "cross-entropy.html", "loss.html", "gradients.html", "experimental-evaluation.html", "scaling-laws.html", "transformer-architectures.html", "llm-limits.html"].map(page => ({
      ...testCase, page, kind: "route-context",
    }))
  ),
  ...visualCases.flatMap(testCase =>
    ["gpt-config-walkthrough.html", "gpt-ops-walkthrough.html", "transformer-block-walkthrough.html", "gpt-model-walkthrough.html", "gpt-generation-walkthrough.html"].map(page => ({
      ...testCase, page, kind: "build-tour",
    }))
  ),
];

const browser = await chromium.launch({ headless: true });
const stageAnchorCache = new Map();
const report = {
  generatedAt: new Date().toISOString(),
  baseUrl: BASE,
  browser: "Chromium",
  cases: [],
  failures: [],
};

for (const testCase of cases) {
  const { lang, viewport, label, theme, page: pagePath, kind } = testCase;
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1, colorScheme: theme });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  page.on("console", msg => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", error => pageErrors.push(String(error)));

  const url = `${BASE}/${lang}/${pagePath}`;
  const item = { lang, viewport, label, theme, page: pagePath, kind, url, consoleErrors, pageErrors };
  const runInteractiveAudit = viewport.width >= 1000 && theme === "light";
  item.auditProfile = runInteractiveAudit ? "full-desktop-light" : "visual-responsive";
  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
    item.httpStatus = response?.status() ?? null;
    if (!response || !response.ok()) throw new Error(`HTTP status ${item.httpStatus}`);
    await page.waitForLoadState("networkidle", { timeout: 1500 }).catch(() => {});
    await page.evaluate(() => document.fonts?.ready.then(() => true));
    await page.waitForTimeout(300);

    item.title = await page.title();
    item.h1 = await page.locator("h1").first().innerText().catch(() => null);
    item.layout = await page.evaluate(() => ({
      viewportWidth: window.innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      overflowCandidates: [...document.querySelectorAll("body *")].map(el => {
        const r = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          id: el.id || null,
          className: typeof el.className === "string" ? el.className.slice(0, 160) : null,
          text: (el.innerText || el.getAttribute("aria-label") || "").trim().slice(0, 100),
          left: Math.round(r.left), right: Math.round(r.right),
          width: Math.round(r.width),
          whiteSpace: style.whiteSpace,
          overflowX: style.overflowX,
        };
      }).filter(x => x.width > 0 && (x.right > window.innerWidth + 1 || x.left < -1))
        .sort((a, b) => b.right - a.right).slice(0, 20),
      pageHeight: document.documentElement.scrollHeight,
      images: [...document.images].map(img => ({
        src: img.currentSrc || img.src,
        loaded: img.complete && img.naturalWidth > 0,
        alt: img.getAttribute("alt"),
        width: Math.round(img.getBoundingClientRect().width),
      })),
      svgs: [...document.querySelectorAll("svg")].map(svg => {
        const r = svg.getBoundingClientRect();
        return {
          viewBox: svg.getAttribute("viewBox"),
          width: Math.round(r.width),
          height: Math.round(r.height),
          clippedByViewport: r.right > window.innerWidth + 1 || r.left < -1,
          title: svg.querySelector("title")?.textContent || null,
          description: svg.querySelector("desc")?.textContent || null,
          ariaLabel: svg.getAttribute("aria-label"),
          ariaLabelledby: svg.getAttribute("aria-labelledby"),
          role: svg.getAttribute("role"),
        };
      }),
      math: {
        katex: document.querySelectorAll(".katex").length,
        mathjax: document.querySelectorAll("mjx-container").length,
        unrenderedMathDelimiters: ["\\(", "\\)", "\\[", "\\]"].reduce((n, delimiter) => n + document.body.innerText.split(delimiter).length - 1, 0),
      },
      disclosures: document.querySelectorAll("details").length,
      links: document.querySelectorAll("a[href]").length,
      buttons: document.querySelectorAll("button").length,
      languageSwitchLinks: [...document.querySelectorAll("a[href]")].filter(a => { const href = a.getAttribute("href") || ""; return href.includes("/en/") || href.includes("/fr/"); }).length,
    }));

    const screenshot = path.join(OUT, `${pagePath.replace(".html", "")}-${lang}-${label}-${theme}.png`);
    await page.screenshot({ path: screenshot, fullPage: true, animations: "disabled" });
    item.screenshot = screenshot;

    // Keyboard and accessibility interaction checks run once per language/page
    // on desktop/light. Mobile and dark cases remain visual/responsive checks.
    if (runInteractiveAudit) {
    // Keyboard traversal: record actual focus targets and whether the browser
    // exposes a visible focus indicator while tabbing through the page.
    await page.evaluate(() => { window.scrollTo(0, 0); document.activeElement?.blur(); });
    item.keyboard = [];
    const seen = new Set();
    for (let i = 0; i < 100; i++) {
      await page.keyboard.press("Tab");
      const focus = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const style = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          text: (el.innerText || el.getAttribute("aria-label") || el.getAttribute("title") || "").trim().slice(0, 100),
          href: el.getAttribute("href"),
          role: el.getAttribute("role"),
          focusVisible: el.matches(":focus-visible"),
          outlineStyle: style.outlineStyle,
          outlineWidth: style.outlineWidth,
          outlineColor: style.outlineColor,
          boxShadow: style.boxShadow,
          inViewport: rect.bottom > 0 && rect.top < window.innerHeight,
        };
      });
      if (!focus) break;
      const key = JSON.stringify([focus.tag, focus.text, focus.href, focus.role]);
      if (seen.has(key)) { item.keyboardTabCycleCompleted = true; break; }
      seen.add(key);
      item.keyboard.push(focus);
    }
    item.keyboardSummary = {
      focusTargets: item.keyboard.length,
      focusVisibleTargets: item.keyboard.filter(x => x.focusVisible).length,
      tabCycleCompleted: Boolean(item.keyboardTabCycleCompleted),
      firstTargets: item.keyboard.slice(0, 12),
    };

    const summary = page.locator("details > summary").first();
    item.keyboardDisclosure = { available: await summary.count() > 0 };
    if (item.keyboardDisclosure.available) {
      await summary.focus();
      const details = summary.locator("xpath=..");
      item.keyboardDisclosure.beforeOpen = await details.evaluate(el => el.hasAttribute("open"));
      await page.keyboard.press("Enter");
      item.keyboardDisclosure.afterOpen = await details.evaluate(el => el.hasAttribute("open"));
      item.keyboardDisclosure.toggledByEnter = item.keyboardDisclosure.beforeOpen !== item.keyboardDisclosure.afterOpen;
    }

    } // end runInteractiveAudit keyboard checks

    if (kind === "learning-map") {
      const mode = page.locator("[data-map-mode]");
      if (await mode.count() !== 1) throw new Error("learning-map mode selector is missing");
      if (await page.locator('label[for="learning-map-mode"]').count() !== 1) {
        throw new Error("learning-map mode selector has no associated label");
      }
      await mode.selectOption("concepts");
      await page.waitForSelector(".map-concept-item", { timeout: 15000 });
      item.learningMapLayout = await page.evaluate(() => ({
        viewportWidth: window.innerWidth,
        documentWidth: document.documentElement.scrollWidth,
        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      }));
      if (item.learningMapLayout.horizontalOverflow) {
        throw new Error("concept view has horizontal overflow");
      }
      const conceptScreenshot = path.join(OUT, `learning-map-concepts-${lang}-${label}-${theme}.png`);
      await page.screenshot({ path: conceptScreenshot, fullPage: true, animations: "disabled" });
      item.learningMapScreenshot = conceptScreenshot;
      const legend = page.locator(".learning-map-concept-legend");
      const relationFilter = page.locator("[data-map-relation-type]");
      const relationOptions = await relationFilter.locator("option").evaluateAll(options =>
        options.map(option => ({ value: option.value, label: option.textContent.trim() }))
      );
      item.learningMap = {
        legendVisible: await legend.isVisible(),
        legendItems: await legend.locator(".map-concept-legend-item").count(),
        conceptButtons: await page.locator(".map-concept-item").count(),
        uniqueConceptIds: await page.locator(".map-concept-item").evaluateAll(items =>
          new Set(items.map(item => item.getAttribute("data-concept-id"))).size
        ),
        relationFilterLabelled: await page.locator('label[for="learning-map-relation-type"]').count() === 1,
        searchLabelled: await page.locator('label[for="learning-map-search"]').count() === 1,
        relationOptions,
      };
      if (!item.learningMap.legendVisible || item.learningMap.legendItems === 0) {
        throw new Error("concept relation legend is missing or empty");
      }
      if (!item.learningMap.conceptButtons) throw new Error("concept list is empty");
      if (!item.learningMap.relationFilterLabelled || !item.learningMap.searchLabelled) {
        throw new Error("learning-map controls are missing accessible labels");
      }
      if (relationOptions.length < 2) throw new Error("relation filter has no usable relation types");
      await relationFilter.selectOption(relationOptions[1].value);
      item.learningMap.filteredConceptButtons = await page.locator(".map-concept-item").count();
      if (!item.learningMap.filteredConceptButtons) throw new Error("relation filter removed every concept");
      await relationFilter.selectOption("");
      const firstConcept = page.locator(".map-concept-item").first();
      const firstConceptId = await firstConcept.getAttribute("data-concept-id");
      await firstConcept.click();
      const pointerPressedIds = await page.locator(".map-concept-item[aria-pressed='true']").evaluateAll(items =>
        [...new Set(items.map(item => item.getAttribute("data-concept-id")))]
      );
      item.learningMap.selectedButtonCount = await page.locator(".map-concept-item[aria-pressed='true']").count();
      item.learningMap.pointerSelection = pointerPressedIds.length === 1 && pointerPressedIds[0] === firstConceptId;
      item.learningMap.detailsTitle = await page.locator(".map-detail-panel .map-detail-title").first().innerText().catch(() => null);
      if (!item.learningMap.pointerSelection || !item.learningMap.detailsTitle) {
        throw new Error("pointer selection did not update one canonical concept and its details panel");
      }
      await page.keyboard.press("Escape");
      item.learningMap.escapeClearsSelection = await page.locator(".map-concept-item[aria-pressed='true']").count() === 0;
      if (!item.learningMap.escapeClearsSelection) {
        throw new Error("Escape did not clear the selected concept");
      }
      await firstConcept.focus();
      await page.keyboard.press("Enter");
      const keyboardPressedIds = await page.locator(".map-concept-item[aria-pressed='true']").evaluateAll(items =>
        [...new Set(items.map(item => item.getAttribute("data-concept-id")))]
      );
      item.learningMap.keyboardActivation = keyboardPressedIds.length === 1 && keyboardPressedIds[0] === firstConceptId;
      if (!item.learningMap.keyboardActivation) {
        throw new Error("Enter did not activate the focused concept button");
      }
      await page.keyboard.press("Escape");
    }

    if (kind === "build-tour") {
      const currentPageId = `${lang}/${pagePath.replace(/\.html$/, "")}`;
      const tour = await page.evaluate(async ({ language, currentId }) => {
        const response = await fetch(`../learning-map-data-${language}.json`);
        if (!response.ok) throw new Error(`learning-map metadata request failed: ${response.status}`);
        const payload = await response.json();
        const byId = new Map(payload.pages.map(item => [item.id, item]));
        const current = byId.get(currentId);
        if (!current) throw new Error(`missing page metadata: ${currentId}`);

        let first = current;
        const backwards = new Set([first.id]);
        while (first.route?.previous) {
          const previous = byId.get(first.route.previous);
          if (!previous || backwards.has(previous.id)) {
            throw new Error("build-tour previous links are missing or cyclic");
          }
          backwards.add(previous.id);
          first = previous;
        }

        const steps = [];
        const visited = new Set();
        let cursor = first;
        let expectedPrevious = null;
        while (cursor) {
          if (visited.has(cursor.id) || cursor.route?.previous !== expectedPrevious) {
            throw new Error("build-tour metadata is cyclic or non-reciprocal");
          }
          visited.add(cursor.id);
          steps.push({ id: cursor.id, previous: cursor.route?.previous ?? null, next: cursor.route?.next ?? null });
          expectedPrevious = cursor.id;
          cursor = cursor.route?.next ? byId.get(cursor.route.next) : null;
          if (steps.at(-1).next && !cursor) throw new Error("build-tour next link targets missing metadata");
        }
        if (steps.length !== 5 || steps.at(-1).next !== null) {
          throw new Error(`expected a finite five-page build tour; found ${steps.length} pages`);
        }
        return steps;
      }, { language: lang, currentId: currentPageId });
      const index = tour.findIndex(step => step.id === currentPageId);
      if (index < 0) throw new Error("current page is not part of its resolved build-tour chain");
      const step = tour[index];
      const lead = page.locator("main .chapter-lead").first();
      const leadText = await lead.innerText();
      const ordinalPattern = lang === "fr"
        ? new RegExp(`\\b${index + 1}\\s+sur\\s+5\\b`, "i")
        : new RegExp(`\\b${index + 1}\\s+of\\s+5\\b`, "i");
      if (!await lead.count() || !ordinalPattern.test(leadText)) {
        throw new Error("build-tour opening does not expose the correct localized step number");
      }
      const siteBreadcrumb = page.locator(".quarto-title-breadcrumbs");
      item.buildTour = {
        ordinal: index + 1,
        leadText,
        siteBreadcrumbCount: await siteBreadcrumb.count(),
        guidedRouteContextCount: await page.locator(".guided-page-context").count(),
      };
      if (item.buildTour.siteBreadcrumbCount !== 1 || item.buildTour.guidedRouteContextCount !== 0) {
        throw new Error("build-tour page must retain one site breadcrumb and no unrelated Understand route context");
      }
      const connectionsHeading = page.locator("main h2").filter({
        hasText: lang === "fr" ? /^Connexions$/ : /^Connections$/,
      }).last();
      const connectionsList = connectionsHeading.locator("xpath=following-sibling::ul[1]");
      const expectedLinks = [
        { target: step.previous, label: lang === "fr" ? "Étape précédente" : "Previous stop" },
        { target: step.next, label: lang === "fr" ? "Étape suivante" : "Next stop" },
      ].filter(link => link.target);
      item.buildTour.navigationLinks = await connectionsList.locator("li").evaluateAll(items =>
        items.map(item => ({
          href: item.querySelector("a[href]")?.getAttribute("href") || null,
          text: item.innerText.trim(),
        }))
      );
      item.buildTour.navigationLinks = item.buildTour.navigationLinks.map(link => ({
        ...link,
        targetId: link.href
          ? new URL(link.href, page.url()).pathname.slice(1).replace(".html", "")
          : null,
      }));
      for (const expected of expectedLinks) {
        const actual = item.buildTour.navigationLinks.filter(link =>
          link.targetId === expected.target && link.text.includes(expected.label)
        );
        if (actual.length !== 1) {
          throw new Error(`build-tour ${expected.label} link to ${expected.target} is missing or duplicated`);
        }
      }
      if (item.buildTour.navigationLinks.some(link =>
        /(?:previous|next) stop|étape (?:précédente|suivante)/i.test(link.text) &&
        !expectedLinks.some(expected => link.targetId === expected.target && link.text.includes(expected.label))
      )) {
        throw new Error("build-tour has an unexpected previous/next link at this sequence boundary");
      }
    }

    if (kind === "route-context") {
      const siteBreadcrumb = page.locator(".quarto-title-breadcrumbs");
      const duplicateBreadcrumb = page.locator(".llm-breadcrumb");
      item.siteBreadcrumb = {
        nativeCount: await siteBreadcrumb.count(),
        nativeText: await siteBreadcrumb.first().innerText().catch(() => ""),
        customDuplicateCount: await duplicateBreadcrumb.count(),
      };
      if (item.siteBreadcrumb.nativeCount !== 1 || item.siteBreadcrumb.customDuplicateCount !== 0) {
        throw new Error("site location must use exactly one native Quarto breadcrumb");
      }

      const context = page.locator(".guided-page-context");
      if (await context.count() !== 1) throw new Error("guided-route context is missing");
      item.routeContext = {
        isMultiple: await context.evaluate(el => el.classList.contains("guided-page-context--multiple")),
        stageLinks: await context.locator('a[href*="learning-map.html#guided-stage-"]').count(),
        currentPageMarkers: await context.locator('[aria-current="page"]').count(),
        visibleCurrentPageText: await context.innerText(),
        listItems: await context.locator("li").count(),
        navLandmark: await context.evaluate(el => el.tagName.toLowerCase() === "nav"),
        accessibleLabel: await context.getAttribute("aria-label"),
      };
      if (!item.routeContext.stageLinks) throw new Error("guided-route context has no stage links");
      const stageFragments = await context.locator('a[href*="learning-map.html#guided-stage-"]').evaluateAll(links =>
        links.map(link => (link.getAttribute("href").split("#")[1] || ""))
      );
      if (!stageAnchorCache.has(lang)) {
        const routeMapPage = await page.context().newPage();
        try {
          await routeMapPage.goto(`${BASE}/${lang}/learning-map.html`, { waitUntil: "domcontentloaded", timeout: 30000 });
          await routeMapPage.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
          const ids = await routeMapPage.locator("[id^='guided-stage-']").evaluateAll(nodes => nodes.map(node => node.id));
          stageAnchorCache.set(lang, new Set(ids));
        } finally {
          await routeMapPage.close();
        }
      }
      const availableStageAnchors = stageAnchorCache.get(lang);
      item.routeContext.stageAnchorsResolve = stageFragments.every(id => availableStageAnchors.has(id));
      if (!item.routeContext.stageAnchorsResolve) throw new Error("guided-route stage link points to a missing anchor");
      if (pagePath === "generation.html") {
        const expectedStages = ["guided-stage-orientation", "guided-stage-prediction"];
        if (!item.routeContext.isMultiple || item.routeContext.navLandmark ||
            item.routeContext.listItems !== 2 || item.routeContext.currentPageMarkers !== 0 ||
            expectedStages.some(id => !stageFragments.includes(id))) {
          throw new Error("multi-stage context is misleading or incomplete");
        }
        const labelledBy = await context.getAttribute("aria-labelledby");
        item.routeContext.accessibleNameReferenceResolves = Boolean(
          labelledBy && await page.locator(`#${labelledBy}`).count() === 1
        );
        if (!item.routeContext.accessibleNameReferenceResolves) {
          throw new Error("multi-stage context has no valid accessible name reference");
        }
      } else {
        const expectedStage = {
          "llm-overview.html": "guided-stage-orientation",
          "text-data.html": "guided-stage-text-input",
          "tokenization-strategies.html": "guided-stage-text-input",
          "unicode-text.html": "guided-stage-text-input",
          "tokenizer-design-evaluation.html": "guided-stage-text-input",
          "embedding-space.html": "guided-stage-representations",
          "positional-encoding.html": "guided-stage-representations",
          "contextualized-representations.html": "guided-stage-representations",
          "tensors.html": "guided-stage-representations",
          "rope.html": "guided-stage-representations",
          "transformer.html": "guided-stage-computation",
          "queries-keys-values.html": "guided-stage-computation",
          "scaled-dot-product-attention.html": "guided-stage-computation",
          "causal-masking.html": "guided-stage-computation",
          "cross-attention.html": "guided-stage-computation",
          "logits.html": "guided-stage-prediction",
          "probabilities.html": "guided-stage-prediction",
          "likelihood.html": "guided-stage-prediction",
          "decoding-strategies.html": "guided-stage-prediction",
          "cross-entropy.html": "guided-stage-learning-evaluation",
          "loss.html": "guided-stage-learning-evaluation",
          "gradients.html": "guided-stage-learning-evaluation",
          "experimental-evaluation.html": "guided-stage-learning-evaluation",
          "scaling-laws.html": "guided-stage-learning-evaluation",
          "transformer-architectures.html": "guided-stage-orientation",
          "llm-limits.html": "guided-stage-orientation",
        }[pagePath];
        const optionalPages = new Set([
          "unicode-text.html", "tokenizer-design-evaluation.html", "tensors.html", "rope.html",
          "cross-attention.html", "decoding-strategies.html", "scaling-laws.html",
          "transformer-architectures.html", "llm-limits.html",
        ]);
        const optionalRole = context.locator(".guided-page-context__role");
        const optionalRoleText = await optionalRole.innerText().catch(() => "");
        const roleMatches = optionalPages.has(pagePath)
          ? /optional|facultatif/i.test(optionalRoleText)
          : await optionalRole.count() === 0;
        if (!expectedStage || item.routeContext.isMultiple || !item.routeContext.navLandmark ||
            item.routeContext.currentPageMarkers !== 0 || stageFragments.length !== 1 ||
            stageFragments[0] !== expectedStage || !item.routeContext.accessibleLabel ||
            item.routeContext.visibleCurrentPageText.includes(item.h1) || !roleMatches) {
          throw new Error("single-stage context repeats the page heading, misstates its route stage/role, or lacks the expected labelled stage link");
        }
      }
      if (["embedding-space.html", "queries-keys-values.html", "scaled-dot-product-attention.html", "causal-masking.html", "logits.html", "cross-entropy.html"].includes(pagePath)) {
        item.routeContext.legacyStepperCount = await page.locator(".pipeline-stepper").count();
        if (item.routeContext.legacyStepperCount !== 0) {
          throw new Error("misleading legacy five-step pipeline stepper is still rendered");
        }
      }
      if (pagePath === "text-data.html") {
        item.routeContext.localProcessStepperCount = await page.locator(".pipeline-stepper").count();
        item.routeContext.localProcessStepperLabel = await page.locator(".pipeline-stepper").getAttribute("aria-label");
        if (item.routeContext.localProcessStepperCount !== 1 ||
            !item.routeContext.localProcessStepperLabel ||
            /learning path|parcours pédagogique/i.test(item.routeContext.localProcessStepperLabel)) {
          throw new Error("text-data local process stepper is missing or mislabelled as a curriculum breadcrumb");
        }
        const openingOrder = await page.locator(".chapter-lead, .callout-tip, .pipeline-stepper").evaluateAll(nodes =>
          nodes.map(node => node.classList.contains("chapter-lead") ? "lead" :
            node.classList.contains("pipeline-stepper") ? "stepper" : "takeaway")
        );
        if (openingOrder.indexOf("lead") < 0 || openingOrder.indexOf("takeaway") < 0 ||
            openingOrder.indexOf("stepper") <= openingOrder.indexOf("takeaway")) {
          throw new Error("text-data process stepper must follow the introductory mental model");
        }
        item.routeContext.openingOrder = openingOrder;
      }
    }

    if (runInteractiveAudit) {
    const calloutSelector = ".callout-header[data-bs-toggle='collapse']";
    const calloutHeaders = page.locator(calloutSelector);
    item.callouts = { count: await calloutHeaders.count() };
    if (item.callouts.count > 0) {
      const callout = calloutHeaders.first();
      const controlsId = await callout.getAttribute("aria-controls");
      const initialExpanded = await callout.getAttribute("aria-expanded");
      const tagName = await callout.evaluate(el => el.tagName.toLowerCase());
      item.callouts.tagName = tagName;
      item.callouts.role = await callout.getAttribute("role");
      item.callouts.tabIndex = await callout.getAttribute("tabindex");
      item.callouts.accessibleName = await callout.getAttribute("aria-label");
      item.callouts.controlsTargetExists = Boolean(
        controlsId && await page.locator(`#${controlsId}`).count() === 1
      );
      if (tagName !== "button" || item.callouts.tabIndex === "-1" ||
          !item.callouts.accessibleName || !item.callouts.controlsTargetExists ||
          !["true", "false"].includes(initialExpanded)) {
        throw new Error("collapsible callout is missing native button semantics, name, or a valid controlled target");
      }

      const initialTargetExpanded = await page.locator(`#${controlsId}`).evaluate(
        el => el.classList.contains("show")
      );
      if ((initialExpanded === "true") !== initialTargetExpanded) {
        throw new Error("callout aria-expanded does not match the controlled panel state before interaction");
      }

      await callout.focus();
      await page.keyboard.press("Enter");
      await page.waitForFunction(
        ({ targetId, expected, selector }) => {
          const trigger = document.querySelector(selector);
          const target = document.getElementById(targetId);
          return target?.classList.contains("show") === expected &&
            trigger?.getAttribute("aria-expanded") === String(expected);
        },
        { targetId: controlsId, expected: !initialTargetExpanded, selector: calloutSelector },
        { timeout: 5000 }
      );

      await page.keyboard.press("Space");
      await page.waitForFunction(
        ({ targetId, expected, selector }) => {
          const trigger = document.querySelector(selector);
          const target = document.getElementById(targetId);
          return target?.classList.contains("show") === expected &&
            trigger?.getAttribute("aria-expanded") === String(expected);
        },
        { targetId: controlsId, expected: initialTargetExpanded, selector: calloutSelector },
        { timeout: 5000 }
      );
      item.callouts.keyboardEnterAndSpace = true;
    }
    } // end runInteractiveAudit callout checks

    if (runInteractiveAudit) {
      const axe = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
        .analyze();
      item.axe = {
        violations: axe.violations.map(v => ({
          id: v.id, impact: v.impact, description: v.description,
          help: v.help, nodes: v.nodes.slice(0, 8).map(n => ({
            target: n.target, html: n.html?.slice(0, 500), summary: n.failureSummary?.slice(0, 500),
          })),
        })),
        violationCount: axe.violations.length,
        passes: axe.passes.length,
        incomplete: axe.incomplete.length,
      };
    } else {
      item.axe = { skipped: true, reason: "Axe runs once per page/language on desktop/light" };
    }

    const blockingAxe = (item.axe.violations || []).filter(v => ["aria-allowed-attr", "color-contrast"].includes(v.id));
    item.axe.blockingViolationCount = blockingAxe.length;
    if (blockingAxe.length) {
      report.failures.push(
        `${pagePath}/${lang}/${label}/${theme}: Axe blocking violations: ${blockingAxe.map(v => v.id).join(", ")}`
      );
    }
    if (item.layout.horizontalOverflow || item.learningMapLayout?.horizontalOverflow) {
      report.failures.push(`${pagePath}/${lang}/${label}/${theme}: horizontal overflow`);
    }
    if (runInteractiveAudit && !item.keyboard.length) report.failures.push(`${pagePath}/${lang}/${label}/${theme}: no keyboard focus targets`);
  } catch (error) {
    item.error = String(error);
    report.failures.push(`${pagePath}/${lang}/${label}/${theme}: ${String(error)}`);
  } finally {
    report.cases.push(item);
    await context.close();
  }
}

await browser.close();
fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify(report, null, 2));
console.log(JSON.stringify({
  generatedAt: report.generatedAt,
  cases: report.cases.map(c => ({
    page: c.page, lang: c.lang, viewport: c.viewport, theme: c.theme, status: c.httpStatus, title: c.title,
    overflow: c.layout?.horizontalOverflow,
    overflowCandidates: c.layout?.overflowCandidates,
    routeContext: c.routeContext,
    learningMap: c.learningMap,
    learningMapLayout: c.learningMapLayout,
    focusTargets: c.keyboardSummary?.focusTargets,
    focusVisibleTargets: c.keyboardSummary?.focusVisibleTargets,
    axeViolations: c.axe?.violationCount,
    error: c.error,
  })),
  failures: report.failures,
}, null, 2));
if (report.failures.length) process.exitCode = 1;
