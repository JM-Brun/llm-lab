// Browser-audit implementation is independent of Quarto output: PR checks reuse
// the exact-base published artifact and rebuild only when that cache is unavailable.
import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const BASE = (process.env.SITE_BROWSER_BASE_URL || "https://jm-brun.github.io/llm-lab").replace(/\/$/, "");
const OUT = "artifacts/site-browser-review";
fs.mkdirSync(OUT, { recursive: true });


// The published site currently exposes only the light Quarto theme.
// Do not label prefers-color-scheme emulation as dark-theme coverage.
const visualCases = [
  { lang: "en", viewport: { width: 1440, height: 1000 }, label: "desktop", theme: "light" },
  { lang: "fr", viewport: { width: 1440, height: 1000 }, label: "desktop", theme: "light" },
  { lang: "en", viewport: { width: 390, height: 844 }, label: "mobile", theme: "light" },
  { lang: "fr", viewport: { width: 390, height: 844 }, label: "mobile", theme: "light" },
];

const routeContextCases = visualCases.filter(testCase => testCase.theme === "light" && testCase.label === "desktop");
const representationResponsiveCases = visualCases.filter(testCase => testCase.label === "mobile");
const transformerOverviewResponsiveCases = visualCases.filter(testCase => testCase.label === "mobile");
const movedModuleResponsiveCases = visualCases.filter(testCase => testCase.label === "mobile");

// Review bilingual exercise collections at desktop and mobile sizes.
// Exercise IDs are semantic, language-neutral anchors rather than opaque codes.
const exerciseHubCases = visualCases;

const cases = [
  // The French homepage is the site root; English has its own /en/ landing page.
  ...visualCases.map(testCase => ({
    ...testCase, page: "index.html", kind: "homepage",
  })),
  // The Advent calendar and its first three guided days are reviewed directly
  // whenever their source pages change; they are not part of the core route matrix.
  ...visualCases.map(testCase => ({
    ...testCase, page: "advent-calendar.html", kind: "advent-calendar",
  })),
  ...visualCases.flatMap(testCase =>
    ["advent-calendar-day-01.html", "advent-calendar-day-02.html", "advent-calendar-day-03.html"].map(page => ({
      ...testCase, page, kind: "advent-day",
    }))
  ),
  ...visualCases.map(testCase => ({
    ...testCase, page: "learning-map.html", kind: "learning-map",
  })),
  ...exerciseHubCases.map(testCase => ({
    ...testCase, page: "exercises.html", kind: "exercise-hub",
  })),
  ...exerciseHubCases.flatMap(testCase =>
    ["attention", "foundations", "generation", "text-data", "transformer"].map(collection => ({
      ...testCase, page: `exercises-${collection}.html`, kind: "exercise-collection",
    }))
  ),
  // #1208: keep the moved module Practice companions in the bilingual browser baseline.
  ...exerciseHubCases.flatMap(testCase =>
    ["exercises/context-engineering.html", "exercises/document-retrieval.html", "exercises/generation.html", "exercises/gradients.html", "exercises/llm-computational-complexity.html", "exercises/loss.html", "exercises/training-loop.html"].map(page => ({
      ...testCase, page, kind: "practice-companion",
    }))
  ),
  ...visualCases.map(testCase => ({
    ...testCase, page: "llm-overview.html", kind: "spine-overview",
  })),
// PR #1507: review all three visual recall cards at desktop and mobile widths.
  ...visualCases.flatMap(testCase =>
    ["revision-inference-generation.html", "revision-positional-encoding.html", "revision-queries-keys-values.html"].map(page => ({
      ...testCase, page, kind: "visual-recall-card",
    }))
  ),
  ...routeContextCases.flatMap(testCase =>
    ["llm-overview.html", "generation.html", "text-data.html", "tokenization-strategies.html", "unicode-text.html", "tokenizer-design-evaluation.html", "embedding-space.html", "positional-encoding.html", "contextualized-representations.html", "tensors.html", "rope.html", "transformer.html", "queries-keys-values.html", "scaled-dot-product-attention.html", "causal-masking.html", "attention-score-scaling.html", "cross-attention.html", "logits.html", testCase.lang === "fr" ? "probabilites.html" : "probabilities.html", testCase.lang === "fr" ? "vraisemblance.html" : "likelihood.html", "decoding-strategies.html", "cross-entropy.html", "loss.html", "gradients.html", "training-loop.html", testCase.lang === "fr" ? "evaluation-experimentale.html" : "experimental-evaluation.html", "scaling-laws.html", "transformer-architectures.html", "llm-limits.html"].map(page => ({
      ...testCase, page, kind: "route-context",
    }))
  ),
  // #1208: the extracted RAG, retrieval and context-engineering modules need the same desktop route-context checks.
  ...routeContextCases.flatMap(testCase =>
    ["rag-memory-boundaries.html", "context-engineering.html", "document-retrieval.html"].map(page => ({
      ...testCase, page, kind: "route-context",
    }))
  ),
  // #1208: review the moved modules at narrow width in both languages as well.
  ...movedModuleResponsiveCases.flatMap(testCase =>
    ["rag-memory-boundaries.html", "context-engineering.html", "document-retrieval.html"].map(page => ({
      ...testCase, page, kind: "moved-module-mobile",
    }))
  ),
  // #320: inspect the complete text → representations entry chain on mobile
  // in both languages, in addition to the desktop route-context baseline.
  ...representationResponsiveCases.flatMap(testCase =>
    ["text-data.html", "embedding-space.html", "positional-encoding.html", "tensors.html"].map(page => ({
      ...testCase, page, kind: "route-context",
    }))
  ),
  // #347: review the Build bridge and desktop training entry without
  // treating either as an additional guided-route stage. Only light is a
  // rendered site theme; color-scheme dark is not dark-theme coverage.
  ...visualCases.filter(testCase => testCase.theme === "light").map(testCase => ({
    ...testCase, page: "build-path.html", kind: "training-build-review",
  })),
  ...visualCases.filter(testCase => testCase.theme === "light" && testCase.label === "desktop").map(testCase => ({
    ...testCase, page: "training-examples.html", kind: "training-build-review",
  })),
  ...visualCases.filter(testCase => testCase.theme === "light" && testCase.label === "mobile").map(testCase => ({
    ...testCase, page: "generation.html", kind: "training-build-review",
  })),
  // Focused mobile review of the Transformer system overview (FR/EN).
  // Desktop keyboard/Axe coverage remains in the route-context matrix.
  ...transformerOverviewResponsiveCases.map(testCase => ({
    ...testCase, page: "transformer.html", kind: "transformer-overview-mobile",
  })),
  // Focused mobile review for prediction, decoding, attention, scoring and training.
  // Keep the full logits → probabilities → entropy → likelihood → loss chain
  // represented at narrow width; desktop/light route-context cases above remain
  // the keyboard/Axe baseline.
  ...visualCases.filter(testCase => testCase.label === "mobile").flatMap(testCase =>
    ["logits.html", testCase.lang === "fr" ? "probabilites.html" : "probabilities.html", "entropy.html", "decoding-strategies.html", "queries-keys-values.html", "scaled-dot-product-attention.html", "transformer-architectures.html", "causal-masking.html", "attention-score-scaling.html", testCase.lang === "fr" ? "vraisemblance.html" : "likelihood.html", "cross-entropy.html", "loss.html", "gradients.html", "training-loop.html", "training-examples.html", testCase.lang === "fr" ? "evaluation-experimentale.html" : "experimental-evaluation.html"].map(page => ({
      ...testCase, page, kind: "attention-training-mobile",
    }))
  ),
  ...visualCases.flatMap(testCase =>
    ["gpt-config-walkthrough.html", "gpt-ops-walkthrough.html", "transformer-block-walkthrough.html", "gpt-model-walkthrough.html", "gpt-generation-walkthrough.html"].map(page => ({
      ...testCase, page, kind: "build-tour",
    }))
  ),
  ...visualCases.flatMap(testCase =>
    ["attention-score-scaling.html", "cross-attention.html", "rope.html", "unicode-text.html", "tensors.html", "cosine-similarity.html", testCase.lang === "fr" ? "linearite-embeddings.html" : "embedding-linearity.html", "language-modeling-math.html", "mathematical-foundations.html", "llm-computational-complexity.html", "universal-artificial-intelligence.html"].map(page => ({
      ...testCase, page, kind: "deep-dive-parent",
    }))
  ),
];

// PRs use a changed-page profile; the complete matrix remains available for
// scheduled/manual audits. The workflow supplies changed paths via the PR API.
if (process.env.SITE_BROWSER_PROFILE === "targeted") {
  const allCases = [...cases];
  const changedFiles = (process.env.SITE_BROWSER_CHANGED_FILES || "")
    .split(/\r?\n/)
    .map(file => file.trim())
    .filter(Boolean);
  const changedPages = new Set(changedFiles
    .filter(file => /^site\/(en|fr)\/.+\.qmd$/.test(file))
    .map(file => file.replace(/^site\/(en|fr)\//, "").replace(/\.qmd$/, ".html")));
  // New Quarto pages are not necessarily represented in the fixed site-review
  // matrix yet. Add a bilingual desktop/mobile case for each changed page so
  // new content receives the same math, layout, keyboard and Axe checks.
  const renderConfig = fs.readFileSync(path.resolve("site/_quarto.yml"), "utf8");
  const changedPageTargets = changedFiles
    .map(file => file.match(/^site\/(en|fr)\/(?!exercises\/)(.+)\.qmd$/))
    .filter(Boolean)
    .filter(([, language, slug]) => renderConfig.includes(`${language}/${slug}.qmd`))
    .map(([, language, slug]) => ({ language, page: `${slug}.html` }));
  for (const { language, page } of changedPageTargets) {
    if (cases.some(testCase => testCase.lang === language && testCase.page === page)) continue;
    cases.push(...visualCases
      .filter(testCase => testCase.lang === language)
      .map(testCase => ({ ...testCase, page, kind: "changed-page" })));
  }
  const changedCompanions = changedFiles
    .map(file => file.match(/^site\/(en|fr)\/exercises\/([a-z0-9-]+)\.qmd$/))
    .filter(Boolean);
  for (const [, language, slug] of changedCompanions) {
    const page = `exercises/${slug}.html`;
    changedPages.add(page);
    cases.push(...visualCases.filter(testCase => testCase.lang === language).map(testCase => ({
      ...testCase, page, kind: "practice-companion",
    })));
  }
  // Q/K/V matrix diagrams are shared by the bilingual page; an SVG-only
  // change still needs a rendered browser screenshot of that page.
  if (changedFiles.some(file => /^site\/images\/queries-keys-values(?:-en)?\.svg$/.test(file))) {
    changedPages.add("queries-keys-values.html");
  }
  const hasSharedChromeChange = changedFiles.some(file =>
    /^site\/(includes|filters)\//.test(file)
  );
  const hasGlobalSiteChange = changedFiles.some(file =>
    /^site\/(\.quarto|_quarto\.yml|.*\.(css|scss|js))$/.test(file) ||
    /^site\/_extensions\//.test(file) || /^scripts\//.test(file)
  ) || hasSharedChromeChange;

  if (hasGlobalSiteChange || changedPages.size === 0) {
    const smokePages = new Set(["learning-map.html", "llm-overview.html", "index.html", "text-data.html"]);
    const targetedReviewPages = new Set(["exercises.html", "transformer.html", "decoding-strategies.html", "logits.html", "probabilities.html", "probabilites.html", "entropy.html", "scaled-dot-product-attention.html", "transformer-architectures.html", "likelihood.html", "vraisemblance.html", "cross-entropy.html", "loss.html", "gradients.html", "training-loop.html", "generation.html", "text-data.html", "tokenization-strategies.html", "embedding-space.html", "positional-encoding.html", "contextualized-representations.html", "tensors.html", "training-examples.html", "experimental-evaluation.html", "evaluation-experimentale.html", "build-path.html", "queries-keys-values.html", "llm-limits.html", "llm-computational-complexity.html", "rag-memory-boundaries.html", "context-engineering.html", "document-retrieval.html", "exercises/context-engineering.html", "exercises/document-retrieval.html", "exercises/generation.html", "exercises/gradients.html", "exercises/llm-computational-complexity.html", "exercises/loss.html", "exercises/training-loop.html"]);
    const sidebarPilotPages = new Set(["text-data.html", "embedding-space.html", "positional-encoding.html", "contextualized-representations.html", "queries-keys-values.html"]);
    // A Quarto sidebar change must inspect the linked section entry and its children.
    // they share page-navigation, responsive, and rendered-math assertions.
    // When a sidebar change and this audit script change travel together,
    // keep the browser run focused on the affected section. A script-only
    // change still exercises the broader targeted review profile.
    const reviewScriptOnly = changedFiles.includes("scripts/site-browser-review.mjs")
      && !changedFiles.includes("site/_quarto.yml");
    const selectedPages = new Set([
      ...smokePages,
      ...(reviewScriptOnly || hasSharedChromeChange ? targetedReviewPages : []),
      ...(changedFiles.includes("site/_quarto.yml") ? sidebarPilotPages : []),
      ...changedPages,
    ]);
    for (let i = cases.length - 1; i >= 0; i--) {
      if (!selectedPages.has(cases[i].page)) cases.splice(i, 1);
    }
  } else {
    for (let i = cases.length - 1; i >= 0; i--) {
      if (!changedPages.has(cases[i].page)) cases.splice(i, 1);
    }
  }
  if (cases.length === 0) {
    const smokePages = new Set(["learning-map.html", "llm-overview.html", "index.html", "text-data.html"]);
    cases.push(...allCases.filter(testCase => smokePages.has(testCase.page)));
    console.log("No dedicated browser case matched the changed page; using global smoke cases.");
  }
  console.log(JSON.stringify({ profile: "targeted", changedFiles, changedPages: [...changedPages], selectedCases: cases.length }));
}

const browser = await chromium.launch({ headless: true });
const stageAnchorCache = new Map();
const report = {
  generatedAt: new Date().toISOString(),
  baseUrl: BASE,
  browser: "Chromium",
  cases: new Array(cases.length),
  failures: [],
};

async function retryAfterNavigation(page, operation) {
  try {
    return await operation();
  } catch (error) {
    // The French homepage can perform a client-side language/path fixup just
    // after DOMContentLoaded. If that replaces the document during the first
    // readiness probe, wait for the resulting navigation and retry once.
    if (!/execution context was destroyed|navigation/i.test(String(error))) throw error;
    await page.waitForNavigation({ waitUntil: "domcontentloaded", timeout: 10000 }).catch(() => {});
    return operation();
  }
}

async function waitForFonts(page) {
  let timeoutId;
  try {
    await Promise.race([
      page.evaluate(() => document.fonts?.ready.then(() => true)),
      new Promise(resolve => { timeoutId = setTimeout(resolve, 1000); }),
    ]);
  } finally {
    clearTimeout(timeoutId);
  }
}

async function waitForMath(page) {
  // Quarto's MathJax typesetting is asynchronous. DOMContentLoaded plus two
  // animation frames is not enough: on a cold or contended browser run the
  // audit can inspect Pandoc's source spans before MathJax has replaced them.
  // Wait for the actual rendered output, not for a fixed sleep or networkidle.
  await page.waitForFunction(() => {
    const spans = [...document.querySelectorAll("span.math")];
    return spans.length === 0 || spans.every(span => span.querySelector(".katex, mjx-container"));
  }, null, { timeout: 15000 }).catch(async () => {
    const state = await page.evaluate(() => ({
      mathSpans: document.querySelectorAll("span.math").length,
      renderedSpans: [...document.querySelectorAll("span.math")]
        .filter(span => span.querySelector(".katex, mjx-container")).length,
      mathJaxPresent: Boolean(window.MathJax),
      mathJaxStartup: Boolean(window.MathJax?.startup),
      mathJaxTypeset: typeof window.MathJax?.typesetPromise,
      mathJaxScript: [...document.scripts].map(script => script.src).filter(src => /mathjax/i.test(src)),
    }));
    throw new Error(`MathJax did not finish rendering within 15s: ${JSON.stringify(state)}`);
  });
}

async function checkLocalizedSearch(context, mapUrl, lang) {
  const page = await context.newPage();
  try {
    await page.goto(mapUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    const query = lang === "fr" ? "token" : "attention";
    const trigger = page.locator("#quarto-search button.aa-DetachedSearchButton");
    const input = page.locator("input.aa-Input");
    const results = page.locator(".aa-Panel a[href]");
    await trigger.press("Enter");
    await input.fill(query);
    await results.first().waitFor({ state: "visible" });

    const hrefs = await results.evaluateAll(links => links.map(link => link.href));
    const localePath = new URL(`${BASE}/${lang}/`).pathname;
    const rootPages = [new URL(`${BASE}/index.html`).pathname, new URL(`${BASE}/references.html`).pathname];
    for (const href of hrefs) {
      const result = new URL(href);
      if (result.origin !== new URL(mapUrl).origin ||
          !(result.pathname.startsWith(localePath) || (lang === "fr" && rootPages.includes(result.pathname)))) {
        throw new Error(`Site search ${lang}/${query} returned an out-of-language result: ${href}`);
      }
    }

    await input.press("Escape");
    await input.waitFor({ state: "hidden" });
    await trigger.press("Enter");
    await input.fill(query);
    await results.first().waitFor({ state: "visible" });
    const destinations = await results.evaluateAll(links => links.map(link => link.href));
    const mapPath = new URL(mapUrl).pathname;
    const index = destinations.findIndex(href => new URL(href).pathname !== mapPath);
    if (index < 0) throw new Error(`Site search ${lang}/${query} has no result outside the map`);
    const destination = new URL(destinations[index]);
    const [response] = await Promise.all([
      // Quarto rewrites ?q= with history.replaceState during navigation.
      page.waitForResponse(response => response.request().isNavigationRequest() &&
        new URL(response.url()).pathname === destination.pathname),
      page.waitForURL(url => url.pathname === destination.pathname && url.hash === destination.hash,
        { waitUntil: "domcontentloaded" }),
      results.nth(index).click(),
    ]);
    const arrived = new URL(page.url());
    const resultLanguage = (await page.locator("html").getAttribute("lang"))?.split("-")[0];
    if (!response.ok() || arrived.pathname !== destination.pathname ||
        arrived.hash !== destination.hash || resultLanguage !== lang) {
      throw new Error(`Site search ${lang}/${query} did not open ${destination.href}`);
    }
    return { query, resultCount: hrefs.length, destination: arrived.pathname + arrived.hash };
  } finally {
    await page.close();
  }
}

async function reviewAttentionDisclosures(page, context, mobile) {
  const steps = page.locator("details.attention-computation-step");
  const equation = steps.first().locator("xpath=..").locator(":scope > p .math.display");
  if (await steps.count() !== 5 || !await equation.isVisible()) {
    throw new Error("Attention must show its complete equation beside five optional steps.");
  }
  await page.emulateMedia({ reducedMotion: "reduce" });
  const cdp = await context.newCDPSession(page);
  try {
    const { root } = await cdp.send("DOM.getDocument");
    const { nodeIds } = await cdp.send("DOM.querySelectorAll", {
      nodeId: root.nodeId,
      selector: "details.attention-computation-step > summary",
    });
    for (const [index, step] of (await steps.all()).entries()) {
      const summary = step.locator(":scope > summary");
      const math = step.locator(".math").first();
      const expectExpanded = async expanded => {
        const { nodes: [node] } = await cdp.send("Accessibility.getPartialAXTree", {
          nodeId: nodeIds[index], fetchRelatives: false,
        });
        if (node.role?.value !== "DisclosureTriangle" || !node.name?.value ||
            node.properties?.find(property => property.name === "expanded")?.value?.value !== expanded ||
            await math.isVisible() !== expanded) {
          throw new Error(`Attention step ${index + 1} does not expose its name, state and equation.`);
        }
      };
      await expectExpanded(false);
      if (mobile) {
        await summary.tap();
      } else {
        if (index === 0) await summary.focus();
        else await page.keyboard.press("Tab");
        if (!await summary.evaluate(element => element === document.activeElement &&
            element.matches(":focus-visible") && getComputedStyle(element).outlineStyle !== "none")) {
          throw new Error(`Attention step ${index + 1} has no visible keyboard focus.`);
        }
        await page.keyboard.press("Enter");
      }
      await expectExpanded(true);
      if (!await step.evaluate(element => getComputedStyle(element).animationName === "none")) {
        throw new Error(`Attention step ${index + 1} animates with reduced motion requested.`);
      }
      if (mobile) await summary.tap();
      else await page.keyboard.press("Space");
      await expectExpanded(false);
    }
  } finally {
    await cdp.detach();
  }
  return { steps: 5, activation: mobile ? "touch emulation" : "keyboard", reducedMotion: true };
}

async function runCase(testCase, caseIndex) {
  const startedAt = performance.now();
  const { lang, viewport, label, theme, page: pagePath, kind } = testCase;
  const mobileAttention = label === "mobile" && pagePath === "scaled-dot-product-attention.html";
  const mobileTraining = label === "mobile" && pagePath === "training-examples.html";
  const context = await browser.newContext({
    viewport, deviceScaleFactor: 1, colorScheme: theme, hasTouch: mobileAttention,
    reducedMotion: mobileTraining ? "reduce" : "no-preference",
  });
  const page = await context.newPage();
  page.setDefaultTimeout(5000);
  const consoleErrors = [];
  const pageErrors = [];
  page.on("console", msg => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", error => pageErrors.push({ name: error.name, message: error.message, stack: error.stack || null }));

  const url = kind === "homepage"
    ? (lang === "fr" ? `${BASE}/` : `${BASE}/en/`)
    : `${BASE}/${lang}/${pagePath}`;
  const item = { lang, viewport, label, theme, page: pagePath, kind, url, consoleErrors, pageErrors };
  const runInteractiveAudit = viewport.width >= 1000 && theme === "light";
  item.auditProfile = runInteractiveAudit ? "full-desktop-light" : "visual-responsive";
  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
    item.httpStatus = response?.status() ?? null;
    if (!response || !response.ok()) throw new Error(`HTTP status ${item.httpStatus}`);
    // The French homepage is served from the site root. Quarto's generated
    // homepage scripts can still trigger a same-document navigation after
    // DOMContentLoaded; wait for the initial load event before evaluating the
    // page so a transient navigation cannot destroy the execution context.
    await page.waitForLoadState("load", { timeout: 30000 });
    // Do not wait for networkidle: analytics, remote fonts, and persistent requests
    // can keep the network busy after the DOM is already auditable.
    // A remote font or stylesheet must not stall the entire audit indefinitely.
    await retryAfterNavigation(page, () => waitForFonts(page));
    await retryAfterNavigation(page, () => waitForMath(page));
    // Let layout and paint settle without an unconditional wall-clock sleep.
    await retryAfterNavigation(page, () =>
      page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))))
    );

    item.title = await page.title();

    const retiredCalendarDay = pagePath.match(/^advent-calendar-day-(0[1-3])\.html$/);
    if (pagePath === "advent-calendar.html" || retiredCalendarDay) {
      const expectedCalendar = new URL(`${BASE}/${lang}/scientific-calendar.html`);
      const retiredPath = new URL(url).pathname;
      const currentPath = new URL(page.url()).pathname;
      const redirected = currentPath === expectedCalendar.pathname;
      if (!redirected) {
        throw new Error(`Retired calendar route must redirect to ${expectedCalendar.pathname}; reached ${currentPath} from ${retiredPath}.`);
      }

      // The redirect is progressive enhancement: the destination must also be
      // reachable through an ordinary link when JavaScript is unavailable.
      const staticContext = await browser.newContext({ javaScriptEnabled: false, viewport });
      try {
        const staticPage = await staticContext.newPage();
        const retiredUrl = `${BASE}/${lang}/${pagePath}`;
        const staticResponse = await staticPage.goto(retiredUrl, { waitUntil: "load", timeout: 30000 });
        if (!staticResponse?.ok()) throw new Error(`No-script fallback returned HTTP ${staticResponse?.status()}.`);
        const calendarLink = staticPage.locator('main a[href*="scientific-calendar"]');
        if (await calendarLink.count() !== 1 || !await calendarLink.isVisible()) {
          const links = await staticPage.locator("a[href]").evaluateAll(nodes => nodes.map(node => ({ href: node.getAttribute("href"), text: node.textContent?.trim() })));
          throw new Error(`Retired calendar route must expose one visible fallback link to the scientific calendar; found ${await calendarLink.count()} matching links. Links: ${JSON.stringify(links)}`);
        }
        if (retiredCalendarDay) {
          const canonicalByDay = {
            "01": "llm-overview.html",
            "02": "generation.html",
            "03": "text-data.html",
          };
          const canonicalLink = staticPage.locator(`main a[href*="${canonicalByDay[retiredCalendarDay[1]].replace(".html","")}"]`);
          if (await canonicalLink.count() !== 1 || !await canonicalLink.isVisible()) {
            const links = await staticPage.locator("a[href]").evaluateAll(nodes => nodes.map(node => ({ href: node.getAttribute("href"), text: node.textContent?.trim() })));
            throw new Error(`Retired mini-lesson must retain its visible link to the canonical learning resource; found ${await canonicalLink.count()} matching links. Links: ${JSON.stringify(links)}`);
          }
        }
      } finally {
        await staticContext.close();
      }

      item.retiredCalendarRoute = {
        redirected,
        destination: expectedCalendar.pathname,
        noScriptFallback: true,
        canonicalResourceFallback: Boolean(retiredCalendarDay),
      };
    }

    if (["probabilites.html", "probabilities.html"].includes(pagePath)) {
      const flowFits = await page.locator("ol.probability-flow").evaluate(
        flow => flow.children.length === 6 && flow.scrollWidth <= flow.clientWidth + 1
      );
      if (!flowFits) throw new Error("The probability flow must fit without horizontal scrolling.");
    }

    if (pagePath === "decoding-strategies.html") {
      const explorer = page.locator("[data-temperature-explorer]");
      await explorer.waitFor({ state: "visible" });
      const workedRows = await page.locator(".probability-example tbody tr").evaluateAll(rows =>
        rows.map(row => ({
          label: row.cells[0].textContent.trim(),
          exponential: Number(row.cells[2].textContent),
          probability: Number(row.cells[3].textContent.trim().replace(",", ".")),
        }))
      );
      const readBars = () => explorer.locator(".prob-bar-row").evaluateAll(rows =>
        rows.map(row => ({
          label: row.querySelector(".prob-bar-label").textContent.trim(),
          probability: parseFloat(row.querySelector(".prob-bar-value").textContent.replace(",", ".")) / 100,
        }))
      );
      const baseline = await readBars();
      if (workedRows.length !== 4 || JSON.stringify(baseline) !== JSON.stringify(workedRows.map(
        ({ label, probability }) => ({ label, probability })
      ))) {
        throw new Error("The temperature explorer must start with the worked example's labels and probabilities.");
      }
      await explorer.locator('button[data-temperature="0.5"]').press("Enter");
      const cold = await readBars();
      const total = workedRows.reduce((sum, row) => sum + row.exponential ** 2, 0);
      if (cold.length !== workedRows.length || cold.some((row, index) =>
        row.label !== workedRows[index].label ||
        Math.abs(row.probability - workedRows[index].exponential ** 2 / total) > 0.0005
      )) {
        throw new Error("The cold preset must normalize the squared exponentials of the worked example.");
      }
      await explorer.locator('button[data-temperature="1"]').press("Enter");
      if (JSON.stringify(await readBars()) !== JSON.stringify(baseline)) {
        throw new Error("The standard-temperature preset must restore the worked distribution.");
      }
    }
    if (pagePath === "scaled-dot-product-attention.html") {
      item.attentionDisclosures = await reviewAttentionDisclosures(page, context, mobileAttention);
      const lab = page.locator("[data-attention-intervention]");
      const summary = lab.locator(":scope > summary");
      await summary.focus();
      await summary.press("Enter");
      const choice = lab.getByRole("combobox");
      const read = selector => lab.locator(selector).innerText();
      const comparison = lab.locator("[data-attention-comparison]");
      if (!await comparison.isVisible() || !await choice.evaluate(select =>
        select.closest("[data-attention-controls]").nextElementSibling.matches("[data-attention-comparison]"))) {
        throw new Error("The before-and-after comparison must be visible directly below the intervention control.");
      }
      const baselineWeight = await read('[data-b="weight"]');
      const baselineScore = await read('[data-b="raw"]');
      const expected = lang === "fr"
        ? { baseline: "(1,609 ; 0,782)", weights: "(0,804 ; 0,196)", equalWeights: "(0,5 ; 0,5)", value: "(1,609 ; 1,565)", key: "(1 ; 2)", half: "0,5" }
        : { baseline: "(1.609, 0.782)", weights: "(0.804, 0.196)", equalWeights: "(0.5, 0.5)", value: "(1.609, 1.565)", key: "(1, 2)", half: "0.5" };

      if (await read("[data-attention-output]") !== expected.baseline ||
          await read("[data-attention-after-weights]") !== expected.weights) {
        throw new Error("The attention lab must begin at the baseline.");
      }
      await choice.selectOption("value");
      if (await read('[data-b="weight"]') !== baselineWeight ||
          await read('[data-b="raw"]') !== baselineScore ||
          await read("[data-attention-after-weights]") !== expected.weights ||
          await read("[data-attention-output]") !== expected.value) {
        throw new Error("Changing only V must preserve the scores and weights and change the weighted output.");
      }
      await choice.selectOption("key");
      if (await read('[data-b="raw"]') !== "2" ||
          await read('[data-a="weight"]') !== expected.half ||
          await read('[data-b="weight"]') !== expected.half ||
          await read("[data-attention-after-weights]") !== expected.equalWeights ||
          await read("[data-attention-output]") !== expected.key) {
        throw new Error("Equal keys must give equal weights over both accessible positions.");
      }
      if (await read("[data-attention-before-weights]") !== expected.weights ||
          await read("[data-attention-before-output]") !== expected.baseline) {
        throw new Error("The Before column must stay fixed after an intervention.");
      }
      await choice.selectOption("baseline");
      if (await read("[data-attention-output]") !== expected.baseline ||
          await read("[data-attention-after-weights]") !== expected.weights) {
        throw new Error("The After column must return to the baseline after reset.");
      }
    }
    if (kind === "homepage") {
      // Quarto's index.html URL fixup iterates every <a> and assumes href is
      // a string. SVGAnchorElement.href is an SVGAnimatedString, so report
      // non-string href properties without changing the rendered page.
      item.linkHrefDiagnostics = await page.evaluate(() => ({
        nonStringHrefAnchors: [...document.querySelectorAll("a")]
          .filter(link => typeof link.href !== "string")
          .map(link => ({
            namespaceURI: link.namespaceURI,
            hrefAttribute: link.getAttribute("href"),
            hrefType: typeof link.href,
            hrefConstructor: link.href?.constructor?.name || null,
            outerHTML: link.outerHTML.slice(0, 1000),
          })),
        svgAnchors: [...document.querySelectorAll("svg a")].map(link => ({
          hrefAttribute: link.getAttribute("href"),
          hrefType: typeof link.href,
          hrefConstructor: link.href?.constructor?.name || null,
          outerHTML: link.outerHTML.slice(0, 1000),
        })),
        scripts: [...document.scripts].map(script => ({
          src: script.src || null,
          inlinePreview: script.src ? null : script.textContent.trim().slice(0, 180),
        })),
      }));

      item.homepageOrientation = await page.evaluate(() => {
        const readLinks = selector => [...document.querySelectorAll(selector)].map(link => ({
          label: link.textContent.trim().replace(/\s+/g, " "),
          path: new URL(link.getAttribute("href"), document.baseURI).pathname,
        }));
        return {
          // Quarto's sidebar is global navigation. Homepage route choices are
          // the entry cards, transversal Practice links and hero actions.
          entryCards: readLinks(".learning-entry-grid .learning-entry-link"),
          // Select from the semantic Practice section, not its nested styling wrapper.
          // The wrapper may be transformed by Pandoc while the section and links remain valid.
          practiceLinks: readLinks(".learning-practice a"),
          practiceContainerPresent: Boolean(document.querySelector(".learning-practice")),
          practiceAnchorCount: document.querySelectorAll(".learning-practice a").length,
          heroLinks: readLinks(".hero-actions a"),
          nextLinks: readLinks(".page-navigation .nav-page-next a"),
          nextAccessibleName: document.querySelector(".page-navigation .nav-page-next a")?.getAttribute("aria-label"),
          entryCardCount: document.querySelectorAll(".learning-entry-grid .learning-entry").length,
        };
      });
      const expectedPractice = lang === "fr"
        ? ["exercises.html", "evaluation-experimentale.html"]
        : ["exercises.html", "experimental-evaluation.html"];
      const endsWith = (actual, expected) => actual.length === expected.length
        && expected.every((suffix, index) => actual[index].path.endsWith(`/${lang}/${suffix}`));
      const cardsOk = item.homepageOrientation.entryCardCount === 3
        && endsWith(item.homepageOrientation.entryCards, ["llm-overview.html", "build-path.html", "deepen.html"]);
      const practiceOk = endsWith(item.homepageOrientation.practiceLinks, expectedPractice);
      const heroOk = item.homepageOrientation.heroLinks.length === 2
        && endsWith(item.homepageOrientation.heroLinks, ["llm-overview.html", "learning-map.html"]);
      if (!cardsOk) throw new Error("homepage must expose the three expected Understand / Build / Deepen entry cards");
      if (!practiceOk) throw new Error(
        `homepage transversal Practice links are missing or misrouted (container present: ${item.homepageOrientation.practiceContainerPresent}; anchors: ${item.homepageOrientation.practiceAnchorCount}; observed: ${JSON.stringify(item.homepageOrientation.practiceLinks)})`,
      );
      if (!heroOk) throw new Error("homepage hero actions are missing or misrouted");
      const { nextLinks, nextAccessibleName } = item.homepageOrientation;
      if (!endsWith(nextLinks, ["learning-map.html"]) || !nextLinks[0].label ||
          !nextAccessibleName?.includes(nextLinks[0].label)) {
        throw new Error("The homepage next link must visibly name the local learning map and expose the same destination to assistive technology.");
      }
    }
    if (pagePath === "training-examples.html") {
      const comparison = page.locator("#stride-window-example");
      const windows = await comparison.locator(":scope > ul > li").count();
      if (windows !== 2 || !await comparison.evaluate(element => element.scrollWidth <= element.clientWidth + 1)) {
        throw new Error("The two stride examples must reflow within the reading column.");
      }
      if (mobileTraining) {
        const diagramLabel = page.locator("main svg.mermaid-js .nodeLabel > p").first();
        await diagramLabel.waitFor({ state: "visible" });
        const fontSize = await diagramLabel.evaluate(element => {
          const scale = element.closest("foreignObject").getScreenCTM().a;
          return parseFloat(getComputedStyle(element).fontSize) * scale;
        });
        if (fontSize < 12) throw new Error(`Mermaid labels shrink to ${fontSize.toFixed(2)}px under reduced motion.`);

        const mathFocus = await page.evaluate(() => {
          const callout = document.querySelector("main .callout-header[data-bs-toggle='collapse']");
          if (!callout) return { available: false, reason: "missing callout" };
          const candidates = [...document.querySelectorAll("mjx-container:not([display=true])")]
            .filter(element =>
              element.getClientRects().length > 0 &&
              Boolean(element.compareDocumentPosition(callout) & Node.DOCUMENT_POSITION_FOLLOWING)
            );
          // MathJax may render inline expressions outside the tab order (tabIndex=-1).
          // Only exercise the help overlay when a real keyboard-focusable expression exists.
          const target = candidates.filter(element => element.tabIndex >= 0).at(-1);
          if (!target) {
            return {
              available: false,
              reason: "no keyboard-focusable inline MathJax expression before callout",
              visibleExpressions: candidates.length,
            };
          }
          target.focus();
          return {
            available: document.activeElement === target,
            tabIndex: target.tabIndex,
            expression: (target.textContent || "").trim().slice(0, 80),
          };
        });
        let mathHelpAvailable = false;
        let mathHelpFits = null;
        if (mathFocus.available) {
          const help = page.locator("mjx-container:focus:not([display=true]) > mjx-help");
          mathHelpAvailable = await help.waitFor({ state: "visible", timeout: 1000 })
            .then(() => true)
            .catch(() => false);
          if (mathHelpAvailable) {
            mathHelpFits = await help.evaluate(element => {
              const { left, right } = element.getBoundingClientRect();
              return left >= 0 && right <= window.innerWidth;
            });
          }
          await page.keyboard.press("Tab");
          const pageFits = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
          if (mathHelpFits === false || !pageFits) {
            throw new Error("MathJax's inline help widened the page during keyboard traversal.");
          }
        }
        item.trainingAccessibility = {
          reducedMotion: true,
          mermaidLabelPx: fontSize,
          mathHelpAvailable,
          mathHelpFits,
          mathFocus,
        };
      }
    }
    if (kind === "spine-overview") {
      item.svgDiagnostics = await page.evaluate(() => [...document.querySelectorAll("svg")].map((svg, index) => {
        const rect = svg.getBoundingClientRect();
        const invalidTransforms = [...svg.querySelectorAll("[transform]")].map(el => ({
          tag: el.tagName.toLowerCase(),
          className: typeof el.className === "object" ? el.className.baseVal : String(el.className || ""),
          transform: el.getAttribute("transform"),
          outerHTML: el.outerHTML.slice(0, 1200),
        })).filter(item => /undefined|NaN|Infinity/.test(item.transform || ""));
        return {
          index,
          className: typeof svg.className === "object" ? svg.className.baseVal : String(svg.className || ""),
          viewBox: svg.getAttribute("viewBox"),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          hidden: rect.width === 0 || rect.height === 0 || getComputedStyle(svg).display === "none",
          invalidTransforms,
          parent: svg.parentElement?.outerHTML.slice(0, 700) || null,
        };
      }));
    }
    item.h1 = await page.locator("h1").first().innerText().catch(() => null);

    if (kind === "exercise-hub") {
      const expectedCollectionPages = [
        "exercises-foundations.html",
        "exercises-text-data.html",
        "exercises-attention.html",
        "exercises-transformer.html",
        "exercises-generation.html",
      ];
      item.exerciseHub = await page.evaluate(expectedPages => {
        const lang = document.documentElement.lang || "en";
        const anchors = lang.startsWith("fr")
          ? ["fondations", "donnees-textuelles", "attention", "transformer", "generation"]
          : ["foundations", "text-data", "attention", "transformer", "generation"];
        const collectionLinks = [...document.querySelectorAll("main a[href]")].map(link => ({
          href: link.href,
          text: link.textContent.trim().replace(/\s+/g, " "),
        }));
        const missingCollectionPages = expectedPages.filter(expected =>
          !collectionLinks.some(link => new URL(link.href).pathname.endsWith("/" + expected))
        );
        return {
          collectionAnchors: anchors.map(id => ({ id, exists: Boolean(document.getElementById(id)) })),
          collectionLinks,
          missingCollectionPages,
        };
      }, expectedCollectionPages);
      if (item.exerciseHub.collectionAnchors.some(anchor => !anchor.exists)) {
        throw new Error("one or more canonical exercise collection anchors are missing");
      }
      if (item.exerciseHub.missingCollectionPages.length) {
        throw new Error(`missing exercise collection links: ${item.exerciseHub.missingCollectionPages.join(", ")}`);
      }
    }
    if (kind === "practice-companion") {
      const lessonSlug = pagePath.split("/").pop().replace(/\.html$/, "");
      // Some Practice pages are self-contained; require a collection link only when
      // a shared collection is mapped or a matching published collection exists.
      const collectionRequired = [
        "probabilities",
        "probabilites",
        "scaled-dot-product-attention",
      ].includes(lessonSlug) || fs.existsSync(
        path.resolve("site/_site", lang, `exercises-${lessonSlug}.html`)
      );
      item.practiceCompanion = await page.evaluate(({ lessonSlug, collectionRequired }) => {
        const links = [...document.querySelectorAll("main a[href]")].map(link => {
          const target = new URL(link.href);
          const rect = link.getBoundingClientRect();
          const style = getComputedStyle(link);
          return {
            path: target.pathname,
            hash: target.hash,
            text: link.textContent.trim().replace(/\s+/g, " "),
            visible: rect.width > 0 && rect.height > 0 &&
              style.display !== "none" && style.visibility !== "hidden",
          };
        });
        const lessonLink = links.find(link =>
          link.path.endsWith(`/${lessonSlug}.html`) && link.visible
        );
        // Probability practice reuses shared Foundations and Generation collections;
        // it intentionally has no redundant one-to-one exercises-probabilities collection.
        const collectionTargets = {
          probabilities: [
            { slug: "exercises-foundations", hash: "" },
            { slug: "exercises-generation", hash: "#ex-generation-temperature" },
          ],
          probabilites: [
            { slug: "exercises-foundations", hash: "" },
            { slug: "exercises-generation", hash: "#ex-generation-temperature" },
          ],
          // This topic-specific Practice page points to the shared Attention collection.
          "scaled-dot-product-attention": [
            { slug: "exercises-attention", hash: "#attention" },
          ],
          // The text-data collection uses a translated section anchor in French;
          // validate the collection destination without assuming an English anchor.
          "text-data": [
            { slug: "exercises-text-data", hash: "" },
          ],
        };
        const expectedCollections = collectionTargets[lessonSlug] ?? [
          { slug: `exercises-${lessonSlug}`, hash: `#${lessonSlug}` },
        ];
        const collectionLink = links.find(link =>
          expectedCollections.some(({ slug, hash }) =>
            link.path.endsWith(`/${slug}.html`) && (!hash || link.hash === hash)
          ) && link.visible
        );
        const selfCheckHeading = [...document.querySelectorAll("main h2")].some(heading =>
          /check (?:the essential idea|your understanding)|vérifier (?:l['’]idée essentielle|sa compréhension)/i.test(heading.textContent)
        );
        return { lessonLink, collectionLink, collectionRequired, selfCheckHeading };
      }, { lessonSlug, collectionRequired });
      if (!item.practiceCompanion.lessonLink) {
        throw new Error("practice companion must expose a visible return link to its matching lesson");
      }
      if (item.practiceCompanion.collectionRequired && !item.practiceCompanion.collectionLink) {
        throw new Error("practice companion must expose a visible link to its declared extended exercise collection");
      }
      if (!item.practiceCompanion.selfCheckHeading) {
        throw new Error("practice companion must expose its learner-facing self-check section");
      }
      const details = page.locator("main details");
      const detailsCount = await details.count();
      const summariesCount = await details.locator("summary").count();
      const openDetailsAtLoad = await details.evaluateAll(nodes => nodes.filter(node => node.open).length);
      if (detailsCount < 1 || summariesCount !== detailsCount || openDetailsAtLoad !== 0) {
        throw new Error("practice companion must expose one or more native, initially collapsed worked-answer disclosures");
      }
      const summary = details.locator("summary").first();
      await summary.focus();
      await page.keyboard.press("Enter");
      await page.waitForFunction(() => document.querySelector("main details")?.open === true);
      await page.keyboard.press("Space");
      await page.waitForFunction(() => document.querySelector("main details")?.open === false);
      item.practiceCompanion.nativeDisclosureKeyboard = true;
    }
    if (kind === "exercise-collection") {
      const sourcePath = new URL(`../site/${lang}/${pagePath.replace(/\.html$/, ".qmd")}`, import.meta.url);
      const source = fs.readFileSync(sourcePath, "utf8");
      const expectedIds = [...source.matchAll(/^### .+ \{#(ex-[a-z0-9-]+)\}[ \t]*$/gm)]
        .map(([, id]) => id);
      const presentIds = await page.locator('main section.level3[id^="ex-"] > h3')
        .evaluateAll(headings => headings.map(heading => heading.parentElement.id));
      const details = page.locator("main details");
      const detailsCount = await details.count();
      const summariesCount = await details.locator("summary").count();
      const openDetailsAtLoad = await details.evaluateAll(nodes => nodes.filter(node => node.open).length);
      item.exerciseCollection = {
        expectedIds,
        presentIds,
        detailsCount,
        summariesCount,
        openDetailsAtLoad,
      };
      if (!expectedIds.length || expectedIds.length !== presentIds.length ||
          expectedIds.some((id, index) => id !== presentIds[index])) {
        throw new Error(`exercise headings differ from source: expected [${expectedIds.join(", ")}], rendered [${presentIds.join(", ")}]`);
      }
      if (detailsCount === 0 || summariesCount !== detailsCount || openDetailsAtLoad !== 0) {
        throw new Error("exercise hints/solutions must use native collapsed details/summary disclosures in each collection");
      }
      const firstSummary = page.locator("main details > summary").first();
      await firstSummary.focus();
      await page.keyboard.press("Enter");
      await page.waitForFunction(() => [...document.querySelectorAll("main details")].some(node => node.open));
      await page.keyboard.press("Space");
      await page.waitForFunction(() => [...document.querySelectorAll("main details")].every(node => !node.open));
      item.exerciseCollection.nativeDisclosureKeyboard = true;
    }
    // Quarto footer navigation follows editorial sidebar order, independently
    // of document-level rel metadata, the guided route, and the computational graph.
    // Validate the actual visible control and its localized accessible name.
    item.pageNavigation = await page.evaluate(() => {
      const readLink = (direction) => {
        const selector = direction === "previous" ? ".page-navigation .nav-page-previous a.pagination-link" : ".page-navigation .nav-page-next a.pagination-link";
        const link = document.querySelector(selector);
        return {
          href: link?.href || null,
          title: link?.querySelector(".nav-page-text")?.textContent?.trim().replace(/\s+/g, " ") || null,
          ariaLabel: link?.getAttribute("aria-label") || null,
          enhanced: link?.dataset.navigationLabelEnhanced === "true",
          classes: link?.className || null,
          outerHTML: link?.outerHTML.slice(0, 1800) || null,
        };
      };
      const navigation = document.querySelector(".page-navigation");
      return {
        language: document.documentElement.lang || null,
        previous: readLink("previous"),
        next: readLink("next"),
        navigationPresent: Boolean(navigation),
        navigationHTML: navigation?.outerHTML.slice(0, 3600) || null,
        accessibilityFixScriptPresent: [...document.scripts].some(script => script.textContent.includes("enhancePageNavigation")),
      };
    });
    const expectedCoreNavigation = {
      "text-data.html": { previous: "language-representation.html", next: "embedding-space.html" },
      "embedding-space.html": { previous: "text-data.html", next: "positional-encoding.html" },
      "generation.html": { previous: "entropy.html", next: "in-context-learning.html" },
    }[pagePath];
    if (expectedCoreNavigation) {
      for (const [direction, expectedTarget] of Object.entries(expectedCoreNavigation)) {
        const actualTarget = item.pageNavigation[direction].href
          ? new URL(item.pageNavigation[direction].href).pathname.split("/").pop()
          : null;
        if (actualTarget !== expectedTarget) {
          throw new Error(`${pagePath} ${direction} navigation should target ${expectedTarget}, got ${actualTarget}`);
        }
      }
    }
    const guidedOnlyNavigation = {
      "cross-entropy.html": [lang === "fr" ? "vraisemblance.html" : "likelihood.html", "loss.html"],
      "loss.html": ["cross-entropy.html", "gradients.html"],
      "training-loop.html": ["gradients.html", "build-path.html"],
    }[pagePath];
    if (guidedOnlyNavigation) {
      const targets = await page.locator("main .route-nav-card:visible").evaluateAll(links =>
        links.map(link => new URL(link.href).pathname.split("/").pop())
      );
      if (item.pageNavigation.navigationPresent || JSON.stringify(targets) !== JSON.stringify(guidedOnlyNavigation)) {
        throw new Error(`${pagePath} should use the guided cards without competing sidebar pagination`);
      }
    }
    for (const direction of ["previous", "next"]) {
      const navigation = item.pageNavigation[direction];
      const visible = Boolean(navigation.href);
      if (visible) {
        const prefix = lang === "fr" ? (direction === "previous" ? "Page précédente" : "Page suivante") : (direction === "previous" ? "Previous page" : "Next page");
        const normalizedAriaLabel = navigation.ariaLabel?.replace(/\s+:/g, ":");
        if (!normalizedAriaLabel?.startsWith(prefix)) throw new Error(direction + " footer link lacks a localized directional accessible name");
      }
    }
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
      }).filter(x => x.right > window.innerWidth + 1 || x.left < -1)
        .sort((a, b) => b.right - a.right).slice(0, 60),
      marginOverflow: [...document.querySelectorAll("body *")].map(el => {
        const r = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return {
          tag: el.tagName.toLowerCase(),
          className: typeof el.className === "string" ? el.className.slice(0, 80) : null,
          text: (el.innerText || "").trim().slice(0, 60),
          right: Math.round(r.right),
          width: Math.round(r.width),
          marginRight: style.marginRight,
        };
      }).filter(x => x.right <= window.innerWidth + 1 && x.right + parseFloat(x.marginRight) > window.innerWidth + 1).slice(0, 10),
      bodyBox: (() => {
        const r = document.body.getBoundingClientRect();
        return {
          left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width),
          scrollWidth: document.body.scrollWidth,
          bodyMinWidth: getComputedStyle(document.body).minWidth,
          htmlMinWidth: getComputedStyle(document.documentElement).minWidth,
        };
      })(),
      overflowRootCause: (() => {
        const target = window.innerWidth + 1;
        if (document.documentElement.scrollWidth <= target) return null;
        const found = [];
        let tested = 0;
        for (const el of document.querySelectorAll("body *")) {
          if (tested++ > 3000) break;
          const prev = el.style.display;
          el.style.display = "none";
          const fixed = document.documentElement.scrollWidth <= target;
          el.style.display = prev;
          if (fixed) found.push(el);
          if (found.length >= 40) break;
        }
        const leaves = found.filter(el => !found.some(other => other !== el && el.contains(other)));
        return leaves.map(el => {
          const r = el.getBoundingClientRect();
          return {
            tag: el.tagName.toLowerCase(),
            className: typeof el.className === "string" ? el.className.slice(0, 80) : null,
            text: (el.innerText || "").trim().slice(0, 80),
            html: el.innerHTML.replace(/\s+/g, " ").slice(0, 150),
            left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width),
          };
        });
      })(),
      pageHeight: document.documentElement.scrollHeight,
      images: [...document.images].map(img => {
        const src = img.currentSrc || img.src;
        const parsed = new URL(src, window.location.href);
        return {
          src,
          loaded: img.complete && img.naturalWidth > 0,
          localAsset: parsed.origin === window.location.origin && parsed.pathname.includes("/images/"),
          alt: img.getAttribute("alt"),
          width: Math.round(img.getBoundingClientRect().width),
        };
      }),
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
        mathSpans: document.querySelectorAll("span.math").length,
        mathSpansRendered: [...document.querySelectorAll("span.math")].filter(span => span.querySelector(".katex, mjx-container")).length,
        unrenderedMathDelimiters: ["\\(", "\\)", "\\[", "\\]"].reduce((n, delimiter) => n + document.body.innerText.split(delimiter).length - 1, 0),
      },
      disclosures: document.querySelectorAll("details").length,
      links: document.querySelectorAll("a[href]").length,
      buttons: document.querySelectorAll("button").length,
      metaFlows: [...document.querySelectorAll(".pipeline-stepper")].map(el => {
        const r = el.getBoundingClientRect();
        return {
          label: el.getAttribute("aria-label"),
          left: Math.round(r.left),
          right: Math.round(r.right),
          width: Math.round(r.width),
          scrollWidth: el.scrollWidth,
          clientWidth: el.clientWidth,
          display: getComputedStyle(el).display,
          direction: getComputedStyle(el).flexDirection,
        };
      }),
      languageSwitchLinks: [...document.querySelectorAll("a[href]")].filter(a => { const href = a.getAttribute("href") || ""; return href.includes("/en/") || href.includes("/fr/"); }).length,
    }));

    const brokenLocalImages = (item.layout.images || []).filter(image => image.localAsset && !image.loaded);
    if (brokenLocalImages.length) {
      report.failures.push(
        `${pagePath}/${lang}/${label}/${theme}: local image assets failed to load: ${brokenLocalImages.map(image => image.src).join(", ")}`
      );
    }

    if (label === "mobile") {
      const clippedMetaFlow = (item.layout.metaFlows || []).find(flow =>
        flow.left < -1 || flow.right > item.layout.viewportWidth + 1 ||
        flow.scrollWidth > flow.clientWidth + 1
      );
      if (clippedMetaFlow) {
        throw new Error("meta-flow is clipped or horizontally scrollable on mobile: " + JSON.stringify(clippedMetaFlow));
      }
    }

    const capturePage = kind !== "route-context" || label === "desktop" ||
      ["text-data.html", "embedding-space.html", "positional-encoding.html", "tensors.html"].includes(pagePath);
    if (capturePage) {
      const safePageName = pagePath.replace(/[^a-z0-9-]+/gi, "-").replace(/^-|-$/g, "");
      const screenshot = path.join(OUT, `${safePageName}-${lang}-${label}-${theme}.png`);
      await page.screenshot({ path: screenshot, fullPage: true, animations: "disabled", timeout: 30000 });
      item.screenshot = screenshot;
    }

    // Keyboard and accessibility interaction checks run once per language/page
    // on desktop/light. Mobile cases remain visual/responsive checks.
    if (runInteractiveAudit) {
    // Keyboard traversal: record actual focus targets and whether the browser
    // exposes a visible focus indicator while tabbing through the page.
    await page.evaluate(() => { window.scrollTo(0, 0); document.activeElement?.blur(); });
    item.keyboard = [];
    const seen = new Set();
    // Bound traversal from the rendered page's actual sequentially focusable
    // elements instead of a fixed sample size. The old 60-Tab cap silently
    // truncated dense pages such as the learning map and mislabeled them as
    // incomplete cycles even when no keyboard defect was present.
    const focusableCount = await page.evaluate(() => [...document.querySelectorAll("*")]
      .filter(el => el.tabIndex >= 0 && !el.matches(":disabled") &&
        el.getClientRects().length > 0 &&
        getComputedStyle(el).visibility !== "hidden" &&
        getComputedStyle(el).display !== "none").length);
    const tabTraversalLimit = Math.min(500, Math.max(60, focusableCount + 2));
    item.keyboardSummary = {
      expectedFocusableElements: focusableCount,
      traversalLimit: tabTraversalLimit,
      traversalLimitReached: false,
    };
    for (let i = 0; i < tabTraversalLimit; i++) {
      await page.keyboard.press("Tab");
      const focus = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        // Use element identity, not accessible text/href, because repeated
        // labels and destinations can legitimately occur in navigation.
        if (!el.__siteAuditFocusId) {
          window.__siteAuditNextFocusId = (window.__siteAuditNextFocusId || 0) + 1;
          Object.defineProperty(el, "__siteAuditFocusId", { value: window.__siteAuditNextFocusId });
        }
        const style = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return {
          id: el.__siteAuditFocusId,
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
      if (seen.has(focus.id)) { item.keyboardTabCycleCompleted = true; break; }
      seen.add(focus.id);
      item.keyboard.push(focus);
    }
    item.keyboardSummary = {
      ...item.keyboardSummary,
      focusTargets: item.keyboard.length,
      focusVisibleTargets: item.keyboard.filter(x => x.focusVisible).length,
      tabCycleCompleted: Boolean(item.keyboardTabCycleCompleted),
      traversalLimitReached: !item.keyboardTabCycleCompleted && item.keyboard.length >= tabTraversalLimit,
      firstTargets: item.keyboard.slice(0, 12),
    };

    // The homepage diagram uses SVG groups with role=link rather than native
    // anchors. Verify the promised Enter activation, not only tab focusability.
    if (kind === "homepage") {
      const svgKeyboardPage = await page.context().newPage();
      try {
        await svgKeyboardPage.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
        const svgLink = svgKeyboardPage.locator(".llm-flow .flow-node[role='link']").first();
        if (await svgLink.count() !== 1) {
          throw new Error("homepage SVG keyboard link is missing");
        }
        const target = await svgLink.getAttribute("data-href");
        if (!target) throw new Error("homepage SVG keyboard link has no destination");
        const expectedUrl = new URL(target, url).href;
        await svgLink.focus();
        await svgKeyboardPage.keyboard.press("Enter");
        await svgKeyboardPage.waitForURL(expectedUrl, { timeout: 5000 });
        item.svgKeyboardActivation = {
          target,
          expectedUrl,
          actualUrl: svgKeyboardPage.url(),
          activatedWithEnter: svgKeyboardPage.url() === expectedUrl,
        };
        if (!item.svgKeyboardActivation.activatedWithEnter) {
          throw new Error("homepage SVG link did not navigate with Enter");
        }
      } finally {
        await svgKeyboardPage.close();
      }
    }

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
      item.localizedSiteSearch = await checkLocalizedSearch(context, url, lang);
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
      await page.screenshot({ path: conceptScreenshot, fullPage: true, animations: "disabled", timeout: 30000 });
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
      const focusedConceptId = await page.locator(".map-concept-item:focus").getAttribute("data-concept-id", { timeout: 3000 });
      if (!item.learningMap.escapeClearsSelection || focusedConceptId !== firstConceptId) {
        throw new Error("Escape did not clear the selection and restore focus to the concept");
      }
      await page.keyboard.press("Enter");
      const keyboardPressedIds = await page.locator(".map-concept-item[aria-pressed='true']").evaluateAll(items =>
        [...new Set(items.map(item => item.getAttribute("data-concept-id")))]
      );
      item.learningMap.keyboardActivation = keyboardPressedIds.length === 1 && keyboardPressedIds[0] === firstConceptId;
      if (!item.learningMap.keyboardActivation) {
        throw new Error("Enter did not activate the focused concept button");
      }
      await page.keyboard.press("Escape");

      await mode.selectOption("pages");
      const firstArea = page.locator(".map-area-card").first();
      const firstAreaId = await firstArea.getAttribute("data-area-id");
      await firstArea.press("Enter");
      if (!await page.locator("[data-map-home]:focus").count()) {
        throw new Error("Opening a territory did not focus its Back button");
      }
      await page.keyboard.press("Escape");
      const focusedAreaId = await page.locator(".map-area-card:focus").getAttribute("data-area-id", { timeout: 3000 });
      if (focusedAreaId !== firstAreaId) {
        throw new Error("Escape did not restore focus to the original territory");
      }

      await page.keyboard.press("Enter");
      const pageChip = page.locator("[data-map-viewport] [data-page-id]").first();
      const selectedPageId = await pageChip.getAttribute("data-page-id");
      await pageChip.click();
      await page.reload();
      const currentPage = page.locator('[data-map-viewport] [data-page-id][aria-current="true"]');
      if (await currentPage.getAttribute("data-page-id", { timeout: 5000 }) !== selectedPageId) {
        throw new Error("The map did not restore the selected page from the URL");
      }
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

        const buildHubId = `${language}/build-path`;
        let first = current;
        const backwards = new Set([first.id]);
        while (first.route?.previous && first.route.previous !== buildHubId) {
          const previous = byId.get(first.route.previous);
          if (!previous || backwards.has(previous.id)) {
            throw new Error("build-tour previous links are missing or cyclic");
          }
          backwards.add(previous.id);
          first = previous;
        }
        const entryPrevious = first.route?.previous ?? null;
        if (entryPrevious) {
          const hub = byId.get(entryPrevious);
          if (!hub || hub.route?.next !== first.id) {
            throw new Error("build-tour entry from the Build hub is not reciprocal");
          }
        }

        const steps = [];
        const visited = new Set();
        let cursor = first;
        let expectedPrevious = entryPrevious;
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
      ].filter(link => link.target && !(index === 0 && link.target === `${lang}/build-path`));
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

      if (index === 0) {
        const returnLabel = lang === "fr" ? "Retour au parcours Build" : "Back to the Build path";
        item.buildTour.returnCardData = await page.locator(".route-nav-cards").evaluateAll(cards =>
          cards.map(card => ({
            html: card.outerHTML,
            links: [...card.querySelectorAll("a")].map(link => ({
              href: link.getAttribute("href"),
              text: link.innerText.trim(),
            })),
          }))
        );
        const returnCards = item.buildTour.returnCardData.flatMap(card => card.links).filter(link =>
          link.text.toLocaleLowerCase().includes(returnLabel.toLocaleLowerCase())
        );
        const returnTarget = returnCards.length === 1 && returnCards[0].href
          ? new URL(returnCards[0].href, page.url()).pathname
          : null;
        if (returnCards.length !== 1 || !returnTarget?.endsWith("/build-path.html")) {
          throw new Error(
            "first build-tour page must expose one explicitly labelled return to the Build hub "
            + JSON.stringify(item.buildTour.returnCardData)
          );
        }
      }
      if (item.buildTour.navigationLinks.some(link =>
        /(?:previous|next) stop|étape (?:précédente|suivante)/i.test(link.text) &&
        !expectedLinks.some(expected => link.targetId === expected.target && link.text.includes(expected.label))
      )) {
        throw new Error("build-tour has an unexpected previous/next link at this sequence boundary");
      }
    }

    if (kind === "deep-dive-parent") {
      const currentPageId = `${lang}/${pagePath.replace(".html", "")}`;
      const parents = await page.evaluate(async ({ language, currentId }) => {
        const response = await fetch(`../learning-map-data-${language}.json`);
        if (!response.ok) throw new Error(`learning-map metadata request failed: ${response.status}`);
        const payload = await response.json();
        const current = payload.pages.find(candidate => candidate.id === currentId);
        if (!current) throw new Error(`missing page metadata: ${currentId}`);
        return current.parents || [];
      }, { language: lang, currentId: currentPageId });
      if (!parents.length) throw new Error("deep-dive page has no declared canonical parent");
      const mainLinks = await page.locator("main a[href]").evaluateAll(links =>
        links.map(link => ({ href: link.getAttribute("href"), text: link.innerText.trim() }))
      );
      const resolvedLinks = mainLinks.map(link => ({
        ...link,
        targetId: link.href
          ? new URL(link.href, page.url()).pathname.slice(1).replace(".html", "")
          : null,
      }));
      item.deepDiveParent = { parents, resolvedLinks };
      for (const parent of parents) {
        if (!resolvedLinks.some(link => link.targetId === parent)) {
          throw new Error(`deep-dive page does not expose a link back to canonical parent ${parent}`);
        }
      }
      if (pagePath === "entropy.html") {
        const map = page.locator("main .pipeline-stepper.meta-flow").first();
        const audit = await map.evaluate(el => ({
          comparisonCount: el.querySelectorAll(".meta-flow__comparison-item").length,
          text: el.textContent || "",
          className: el.className,
        })).catch(() => ({ comparisonCount: 0, text: "", className: "missing map" }));
        if (audit.comparisonCount !== 2 || !/surprise/i.test(audit.text) ||
            !/cross-entropy|entropie croisée/i.test(audit.text)) {
          throw new Error("entropy map must distinguish predictive entropy, observed-token surprise, and cross-entropy; rendered map: " + JSON.stringify(audit));
        }
      }
    }

    if (pagePath === "build-path.html") {
      const guidedContextCount = await page.locator(".guided-page-context").count();
      item.routeContext = { expectedAbsent: true, guidedContextCount };
      if (guidedContextCount !== 0) {
        throw new Error("Build pages must not expose the Understand guided-route context");
      }
    }

    if (kind === "route-context") {
      const sidebarEntryTargets = {
        "text-data.html": "text-data.html",
        "embedding-space.html": "embedding-space.html",
        "positional-encoding.html": "embedding-space.html",
        "contextualized-representations.html": "embedding-space.html",
      };
      if (Object.hasOwn(sidebarEntryTargets, pagePath)) {
        item.linkedSidebarSection = await page.evaluate(({ language, entryPage }) => {
          const sidebar = document.querySelector("#quarto-sidebar");
          if (!sidebar) return { sidebarPresent: false };
          const targetPath = `/${language}/${entryPage}`;
          const matches = [...sidebar.querySelectorAll("a[href]")].filter(anchor => {
            const url = new URL(anchor.getAttribute("href"), document.baseURI);
            return url.pathname.endsWith(targetPath);
          });
          const target = matches[0] || null;
          const ancestors = [];
          for (let node = target, depth = 0; node && depth < 6; node = node.parentElement, depth += 1) {
            ancestors.push({
              tag: node.tagName.toLowerCase(),
              className: typeof node.className === "string" ? node.className : "",
              buttons: [...node.querySelectorAll("button")].map(button => ({
                label: button.getAttribute("aria-label"),
                expanded: button.getAttribute("aria-expanded"),
                className: button.className,
              })),
            });
          }
          const currentPath = `/${language}/${location.pathname.split("/").pop()}`;
          const currentLinks = [...sidebar.querySelectorAll("a[href]")].filter(anchor =>
            new URL(anchor.getAttribute("href"), document.baseURI).pathname.endsWith(currentPath)
          );
          return {
            sidebarPresent: true,
            entryLinkCount: matches.length,
            entryHref: target?.getAttribute("href") || null,
            entryText: target?.textContent.trim().replace(/\s+/g, " ") || null,
            entryAriaCurrent: target?.getAttribute("aria-current") || null,
            currentPageLinkCount: currentLinks.length,
            ancestors,
          };
        }, { language: lang, entryPage: sidebarEntryTargets[pagePath] });
        if (!item.linkedSidebarSection.sidebarPresent || item.linkedSidebarSection.entryLinkCount !== 1) {
          throw new Error("linked sidebar section must expose exactly one canonical entry link in the Quarto sidebar");
        }
        if (item.linkedSidebarSection.currentPageLinkCount !== 1) {
          throw new Error("the current lesson must remain directly reachable exactly once in the Quarto sidebar");
        }
      }

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
      const contextFreePage = [
        "experimental-evaluation.html", "evaluation-experimentale.html",
      ].includes(pagePath);
      if (contextFreePage) {
        if (await context.count() !== 0) {
          throw new Error("this page must not expose generated guided-route context in its lesson content");
        }
        item.routeContext = {
          expectedAbsent: true,
          reason: "Evaluation is cross-cutting, not a guided-route stage.",
        };
      } else {
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
          // Cache the in-flight load, not only its result: parallel cases for
          // the same language must share one learning-map navigation.
          stageAnchorCache.set(lang, (async () => {
            const routeMapPage = await page.context().newPage();
            try {
              await routeMapPage.goto(`${BASE}/${lang}/learning-map.html`, { waitUntil: "domcontentloaded", timeout: 30000 });
              const ids = await routeMapPage.locator("[id^='guided-stage-']").evaluateAll(nodes => nodes.map(node => node.id));
              return new Set(ids);
            } finally {
              await routeMapPage.close();
            }
          })());
        }
        const availableStageAnchors = await stageAnchorCache.get(lang);
        item.routeContext.stageAnchorsResolve = stageFragments.every(id => availableStageAnchors.has(id));
        if (!item.routeContext.stageAnchorsResolve) throw new Error("guided-route stage link points to a missing anchor");
        const multiStagePages = {
          "cross-entropy.html": ["guided-stage-scoring", "guided-stage-training"],
        };
        if (multiStagePages[pagePath]) {
          const expectedStages = multiStagePages[pagePath];
          if (!item.routeContext.isMultiple || item.routeContext.navLandmark ||
              item.routeContext.listItems !== expectedStages.length ||
              item.routeContext.currentPageMarkers !== 0 ||
              expectedStages.length !== stageFragments.length ||
              expectedStages.some(id => !stageFragments.includes(id))) {
            throw new Error("multi-stage context does not match the page's canonical and optional route memberships");
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
            "attention-score-scaling.html": "guided-stage-computation",
            "cross-attention.html": "guided-stage-computation",
            "logits.html": "guided-stage-prediction",
            "probabilities.html": "guided-stage-prediction",
            "probabilites.html": "guided-stage-prediction",
            "generation.html": "guided-stage-inference",
            "likelihood.html": "guided-stage-scoring",
            "vraisemblance.html": "guided-stage-scoring",
            "decoding-strategies.html": "guided-stage-inference",
            "loss.html": "guided-stage-training",
            "gradients.html": "guided-stage-training",
            "training-loop.html": "guided-stage-training",
            "scaling-laws.html": "guided-stage-training",
            "transformer-architectures.html": "guided-stage-orientation",
            "llm-limits.html": "guided-stage-orientation",
            "context-engineering.html": "guided-stage-context-use",
            "rag-memory-boundaries.html": "guided-stage-context-use",
            "document-retrieval.html": "guided-stage-context-use",
          }[pagePath];
          const optionalPages = new Set([
            "unicode-text.html", "tokenization-strategies.html", "tokenizer-design-evaluation.html", "tensors.html", "rope.html",
            "cross-attention.html", "attention-score-scaling.html", "decoding-strategies.html", "scaling-laws.html",
            "transformer-architectures.html", "llm-limits.html", "rag-memory-boundaries.html", "document-retrieval.html",
          ]);
          const optionalRole = context.locator(".guided-page-context__role");
          const optionalRoleText = await optionalRole.innerText().catch(() => "");
          const roleMatches = optionalPages.has(pagePath)
            ? /optional|facultatif|facultative/i.test(optionalRoleText)
            : await optionalRole.count() === 0;
          if (!expectedStage || item.routeContext.isMultiple || !item.routeContext.navLandmark ||
              item.routeContext.currentPageMarkers !== 0 || stageFragments.length !== 1 ||
              stageFragments[0] !== expectedStage || !item.routeContext.accessibleLabel ||
              item.routeContext.visibleCurrentPageText.includes(item.h1) || !roleMatches) {
            throw new Error("single-stage context repeats the page heading, misstates its route stage/role, or lacks the expected labelled stage link");
          }
        }
        if (["queries-keys-values.html", "scaled-dot-product-attention.html", "causal-masking.html", "logits.html", "cross-entropy.html"].includes(pagePath)) {
          const localDiagram = page.locator(".pipeline-stepper");
          item.routeContext.localDiagramCount = await localDiagram.count();
          item.routeContext.localDiagramLabel = await localDiagram.getAttribute("aria-label");
          item.routeContext.localDiagramRole = await localDiagram.getAttribute("role");
          item.routeContext.localDiagramCurrentCount = await localDiagram.locator('[aria-current="step"]').count();
          if (item.routeContext.localDiagramCount !== 1 ||
              !item.routeContext.localDiagramLabel ||
              /learning path|parcours pédagogique/i.test(item.routeContext.localDiagramLabel) ||
              item.routeContext.localDiagramRole !== "group" ||
              item.routeContext.localDiagramCurrentCount !== 0) {
            throw new Error("core computation diagram must be one correctly labelled group without a false current-step marker");
          }
        }
        if (pagePath === "queries-keys-values.html") {
          const audit = await page.locator("main .pipeline-stepper.meta-flow").first().evaluate(el => ({
            branchCount: el.querySelectorAll(".meta-flow__branches .meta-flow__branch").length,
            currentCount: el.querySelectorAll("[aria-current='step']").length,
            text: el.textContent || "",
            className: el.className,
          })).catch(() => ({ branchCount: 0, currentCount: 0, text: "", className: "missing map" }));
          if (audit.branchCount !== 3 || audit.currentCount !== 0) {
            throw new Error("Q/K/V must be shown as three parallel branches without marking a branch as a current navigation step; rendered map: " + JSON.stringify(audit));
          }
        }
        if (pagePath === "positional-encoding.html") {
          const audit = await page.evaluate(() => {
            const flow = document.querySelector("main .pipeline-stepper.meta-flow");
            if (flow) {
              return {
                kind: "flow",
                comparisonCount: flow.querySelectorAll(".meta-flow__comparison-item").length,
                text: flow.textContent || "",
              };
            }
            // A semantic comparison table is an equally valid representation:
            // each positional mechanism is an alternative, not a pipeline stage.
            const table = [...document.querySelectorAll("main table")].map(element => ({
              headers: [...element.querySelectorAll("thead th")].map(cell => cell.textContent.trim()),
              rows: [...element.querySelectorAll("tbody tr")].map(row =>
                [...row.querySelectorAll("th, td")].map(cell => cell.textContent.trim())
              ),
            })).find(candidate =>
              /^(mechanism|mécanisme)$/i.test(candidate.headers[0] || "") &&
              candidate.rows.length >= 3
            );
            return table
              ? { kind: "table", ...table }
              : { kind: "missing", comparisonCount: 0, text: "" };
          });
          const legacyFlowIsValid = audit.kind === "flow" &&
            audit.comparisonCount === 2 && /RoPE/i.test(audit.text) &&
            /absolute|absolu/i.test(audit.text);
          const tableLabels = audit.kind === "table" ? audit.rows.map(row => row[0] || "") : [];
          const comparisonTableIsValid = audit.kind === "table" &&
            audit.rows.length === 3 &&
            tableLabels.some(label => /absolute|absolu/i.test(label)) &&
            tableLabels.some(label => /RoPE/i.test(label)) &&
            tableLabels.some(label => /relative bias|biais relatif/i.test(label));
          if (!legacyFlowIsValid && !comparisonTableIsValid) {
            throw new Error("positional mechanisms must be presented as alternatives in a comparison flow or table; rendered audit: " + JSON.stringify(audit));
          }
        }
        if (pagePath === "generation.html") {
          if (await page.locator(".meta-flow__loop").count() !== 1) {
            throw new Error("autoregressive generation map must expose its feedback loop");
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
    }

    if (kind === "visual-recall-card") {
      const card = page.locator("main .visual-recall");
      if (await card.count() !== 1) {
        throw new Error("revision page must expose exactly one visual recall card");
      }
      const diagram = card.locator(".visual-recall__diagram[role='img'][aria-label]");
      if (await diagram.count() !== 1) {
        throw new Error("visual recall diagram must expose one named image role");
      }
      const accessibleName = (await diagram.getAttribute("aria-label") || "").trim();
      const geometry = await card.evaluate(element => {
        const rect = element.getBoundingClientRect();
        const diagram = element.querySelector(".visual-recall__diagram");
        const diagramRect = diagram?.getBoundingClientRect();
        const lanes = [...(diagram?.querySelectorAll(".visual-recall__lane") || [])];
        return {
          left: rect.left,
          right: rect.right,
          viewportWidth: window.innerWidth,
          cardOverflow: element.scrollWidth > element.clientWidth + 1,
          diagramOverflow: Boolean(diagram && diagram.scrollWidth > diagram.clientWidth + 1),
          laneOverflow: lanes.some(lane => lane.scrollWidth > lane.clientWidth + 1),
          diagramLeft: diagramRect?.left ?? null,
          diagramRight: diagramRect?.right ?? null,
        };
      });
      if (!accessibleName || geometry.left < -1 || geometry.right > geometry.viewportWidth + 1 ||
          geometry.cardOverflow || geometry.diagramOverflow || geometry.laneOverflow ||
          geometry.diagramLeft < -1 || geometry.diagramRight > geometry.viewportWidth + 1) {
        throw new Error("visual recall card is unnamed, clipped, or horizontally overflowing: " + JSON.stringify({ accessibleName, geometry }));
      }
      const disclosure = card.locator("details");
      if (await disclosure.count() !== 1) {
        throw new Error("visual recall card must expose exactly one answer disclosure");
      }
      const summary = disclosure.locator("summary");
      if (!(await summary.evaluate(element => element.tabIndex >= 0))) {
        throw new Error("visual recall answer summary must be keyboard focusable");
      }
      if (label === "desktop") {
        await summary.focus();
        await page.keyboard.press("Enter");
        if (!await disclosure.evaluate(element => element.open)) {
          throw new Error("visual recall answer did not open with Enter");
        }
        await page.keyboard.press("Space");
        if (await disclosure.evaluate(element => element.open)) {
          throw new Error("visual recall answer did not close with Space");
        }
        item.visualRecallKeyboard = true;
      }
      item.visualRecallCard = { accessibleName, geometry };
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

      // The entropy lessons place their optional callout inside a native disclosure.
      // Reveal it through the same keyboard path a reader uses before trying to focus it.
      const openedDisclosures = [];
      for (const disclosure of await callout.locator("xpath=ancestor::details").all()) {
        if (await disclosure.evaluate(element => !element.open)) {
          const summary = disclosure.locator(":scope > summary");
          await summary.press("Enter");
          if (!await disclosure.evaluate(element => element.open)) {
            throw new Error("the disclosure containing the callout did not open from the keyboard");
          }
          openedDisclosures.push(summary);
        }
      }

      await callout.focus();
      if (!await callout.evaluate(element => element === document.activeElement)) {
        throw new Error("the callout trigger did not receive keyboard focus");
      }
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
      for (const summary of openedDisclosures.reverse()) await summary.press("Enter");
      item.callouts.keyboardEnterAndSpace = true;
    }
    } // end runInteractiveAudit callout checks

    if (runInteractiveAudit) {
      const scanner = new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]);
      const axe = await scanner.analyze();
      const violations = [...axe.violations];
      if (kind === "learning-map") {
        // Keep the concept audit as well as the selected-page details above.
        await page.locator("[data-map-mode]").selectOption("concepts");
        const conceptsAudit = await scanner.analyze();
        violations.push(...conceptsAudit.violations);
      }
      item.axe = {
        violations: violations.map(v => ({
          id: v.id, impact: v.impact, description: v.description,
          help: v.help, nodes: v.nodes.slice(0, 8).map(n => ({
            target: n.target, html: n.html?.slice(0, 500), summary: n.failureSummary?.slice(0, 500),
          })),
        })),
        violationCount: violations.length,
        passes: axe.passes.length,
        incomplete: axe.incomplete.length,
      };
    } else {
      item.axe = { skipped: true, reason: "Axe runs once per page/language on desktop/light" };
    }

    if (pagePath === "generation.html") {
      const trace = page.locator("[data-generation-trace]");
      if (await trace.getByRole("listitem").count() !== 3) {
        report.failures.push(`${lang}/${label}: the worked trace must expose three ordered turns.`);
      }
      if (await trace.evaluate(node => node.scrollWidth > node.clientWidth + 1)) {
        report.failures.push(`${lang}/${label}: the worked generation trace overflows its container.`);
      }
    }

    if (kind === "spine-overview") {
      if (pageErrors.length) {
        report.failures.push(pagePath + "/" + lang + "/" + label + "/" + theme + ": uncaught page errors: " + pageErrors.map(error => error.message).join(" | "));
      }
      const explorer = page.locator("[data-next-token-explorer]");
      try {
        const controls = explorer.locator(".next-token-explorer__interactive");
        const prefix = explorer.locator("#next-token-context");
        const context = explorer.getByRole("group", { name: lang === "fr" ? /^Préfixe actuel/ : /^Current prefix/ });
        const candidate = explorer.locator(".next-token-explorer__candidate");
        const status = explorer.locator(".next-token-explorer__status");
        const reset = explorer.locator(".next-token-explorer__reset");
        await controls.waitFor({ state: "visible", timeout: 5000 });
        if (!(await page.locator("main h2#llm-transformer-gpt, main #llm-transformer-gpt > h2").count()) ||
            !(await page.locator("#one-computation-three-uses p .math.inline").count())) {
          throw new Error("the surprisal calculation and the following section must render as math and a heading");
        }

        const fallbackHref = new URL(
          await explorer.locator(`.next-token-explorer__fallback [lang="${lang}"] a`).getAttribute("href"),
          page.url()
        );
        const response = await page.request.get(fallbackHref.href);
        if (!response.ok()) throw new Error("the worked trace could not be loaded");
        const turns = await page.evaluate(({ html, anchor }) => {
          const lesson = new DOMParser().parseFromString(html, "text/html");
          return [...lesson.querySelectorAll(`#${anchor} [data-generation-trace] > li`)].map(turn => {
            const prefix = turn.querySelector("[data-generation-prefix]");
            const distribution = turn.querySelector("[data-generation-distribution]");
            const chosen = turn.querySelector("[data-generation-choice]");
            return {
              prefix: prefix.textContent.trim(),
              appended: prefix.querySelector("mark")?.textContent.trim() ?? null,
              distribution: [...distribution.textContent.matchAll(/[«“]\s*([^»”]+?)\s*[»”]\s+(\d[,.]\d)/g)]
                .map(([, token, probability]) => [token, probability]),
              chosen: chosen.textContent.trim().slice(1, -1).trim(),
            };
          });
        }, { html: await response.text(), anchor: fallbackHref.hash.slice(1) });
        if (turns.length !== 3) throw new Error("the generation lesson should provide three worked turns");
        if (turns.some((turn, index) => turn.appended !== (turns[index - 1]?.chosen ?? null))) {
          throw new Error("each worked turn must highlight the token selected on the previous turn");
        }

        const currentPrefix = () => prefix.evaluate(node =>
          node.querySelector(".next-token-explorer__prefix").textContent +
          node.querySelector("mark").textContent
        );
        const normalizePrefix = value => value.replaceAll("’", "'").replace(/\s+/g, " ");
        const firstCandidateIsFocused = () => candidate.first().evaluate(node => node === document.activeElement);
        const readDistribution = () => candidate.evaluateAll(buttons =>
          buttons.map(button => [button.querySelector("span").textContent, button.querySelector("strong").textContent])
        );

        await candidate.first().focus();
        for (const [index, turn] of turns.entries()) {
          if (await controls.evaluate(node => node.scrollWidth > node.clientWidth + 1)) {
            throw new Error("the next-token controls overflow their container");
          }
          const visibleDistribution = await readDistribution();
          if (turn.distribution.length < 2 || JSON.stringify(visibleDistribution) !== JSON.stringify(turn.distribution)) {
            throw new Error("the displayed distribution differs from the generation lesson");
          }
          if (normalizePrefix(await currentPrefix()) !== normalizePrefix(turn.prefix)) {
            throw new Error("the displayed prefix differs from the generation lesson");
          }
          if (index > 0) await page.keyboard.press("Tab");
          if (!(await firstCandidateIsFocused())) throw new Error("the next turn is not reachable by keyboard");
          await page.keyboard.press("Enter");
          if (!(await currentPrefix()).endsWith(turn.chosen)) {
            throw new Error("the selected token did not extend the prefix");
          }
          if (!(await context.evaluate(node => node === document.activeElement))) {
            throw new Error("focus did not move to the updated prefix");
          }
        }

        const end = lang === "fr" ? "trois ajouts" : "three additions";
        if (await candidate.count() || !(await status.textContent()).includes(end)) {
          throw new Error("the final worked turn did not end the trace");
        }

        await page.keyboard.press("Tab");
        if (!(await reset.evaluate(node => node === document.activeElement))) {
          throw new Error("restart is not reachable from the completed trace");
        }
        await page.keyboard.press("Space");
        if (normalizePrefix(await currentPrefix()) !== normalizePrefix(turns[0].prefix) ||
            await reset.isVisible() || !(await firstCandidateIsFocused())) {
          throw new Error("restart did not restore the initial state and focus");
        }

        await candidate.nth(1).click();
        const alternative = turns[0].distribution[1][0];
        const staticAlternative = await explorer.locator(`[lang="${lang}"] [data-alternative-distribution]`).textContent();
        const alternativeDistribution = [...staticAlternative.matchAll(/[«“]([^»”]+)[»”]\s+(\d[,.]\d)/g)]
          .map(([, token, probability]) => [token.trim(), probability]);
        const turnHeading = await explorer.locator("#next-token-distribution").textContent();
        if (!(await currentPrefix()).endsWith(alternative) ||
            !turnHeading.endsWith("2") ||
            alternativeDistribution.length < 2 ||
            JSON.stringify(await readDistribution()) !== JSON.stringify(alternativeDistribution)) {
          throw new Error("the second worked branch must show its own localized distribution");
        }
        const sum = alternativeDistribution.reduce((total, [, probability]) =>
          total + Number(probability.replace(",", ".")), 0);
        if (Math.abs(sum - 1) > 1e-9) throw new Error("the alternative distribution must sum to one");
        await page.keyboard.press("Tab");
        if (!(await firstCandidateIsFocused())) throw new Error("the alternative turn is not reachable by keyboard");
        await page.keyboard.press("Enter");
        const alternativeEnd = lang === "fr" ? "après deux ajouts" : "after two additions";
        if (!(await currentPrefix()).endsWith(alternativeDistribution[0][0]) || await candidate.count() ||
            !(await status.textContent()).includes(alternativeEnd)) {
          throw new Error("the alternative worked branch must end after its second token");
        }
        await reset.click();
        await candidate.nth(2).click();
        const unworked = turns[0].distribution[2][0];
        const unknown = lang === "fr" ? "ce nouveau préfixe" : "this new prefix";
        if (!(await currentPrefix()).endsWith(unworked) || await candidate.count() ||
            !(await status.textContent()).includes(unknown)) {
          throw new Error("a branch outside the worked trace retained stale probabilities");
        }
        item.nextTokenExplorer = { matchesLesson: true, keyboard: true, restart: true, alternativeBranch: true, unknownBranch: true };

        if (label === "mobile") {
          const noScript = await browser.newContext({ javaScriptEnabled: false, viewport });
          try {
            const staticPage = await noScript.newPage();
            // With scripting disabled, the stylesheet controls which fallback link is visible.
            await staticPage.goto(page.url(), { waitUntil: "load" });
            const staticExplorer = staticPage.locator("[data-next-token-explorer]");
            if (await staticExplorer.locator(".next-token-explorer__interactive").isVisible() ||
                await staticExplorer.locator(".next-token-explorer__fallback a:visible").count() !== 1 ||
                await staticExplorer.locator("[data-alternative-distribution]:visible").count() !== 1) {
              throw new Error("the localized fallback should replace inactive controls without JavaScript");
            }
            await staticExplorer.locator(".next-token-explorer__fallback a:visible").click();
            if (staticPage.url() !== fallbackHref.href) {
              throw new Error("the fallback should link to the trace in the same language");
            }
            item.nextTokenExplorer.withoutJavaScript = true;
          } finally {
            await noScript.close();
          }
        }
      } catch (error) {
        item.nextTokenExplorer = { error: error.message };
        report.failures.push(pagePath + "/" + lang + "/" + label + "/" + theme + ": next-token explorer failed: " + error.message);
      }

      // The shortened bilingual overview keeps three substantive comparison tables responsive; the probability example remains compact and is intentionally excluded.
      const responsiveTables = page.locator(".responsive-card-table table");
      const responsiveTableCount = await responsiveTables.count();
      if (responsiveTableCount !== 3) {
        report.failures.push(pagePath + "/" + lang + "/" + label + "/" + theme + ": expected three responsive comparison tables (architecture families, model dimensions, information residence), found " + responsiveTableCount);
      }
      const enhancedTableCount = await page.locator(".responsive-card-table table.responsive-card-table__enhanced").count();
      if (responsiveTableCount && enhancedTableCount !== responsiveTableCount) {
        report.failures.push(pagePath + "/" + lang + "/" + label + "/" + theme + ": only " + enhancedTableCount + "/" + responsiveTableCount + " responsive tables were enhanced");
      }
      if (responsiveTableCount && viewport.width <= 700) {
        const mobileCells = await page.locator(".responsive-card-table table.responsive-card-table__enhanced tbody td").evaluateAll(cells =>
          cells.map(cell => ({ display: getComputedStyle(cell).display, label: cell.dataset.label || "" }))
        );
        if (mobileCells.some(cell => cell.display !== "grid" || !cell.label)) {
          report.failures.push(pagePath + "/" + lang + "/" + label + "/" + theme + ": responsive table cells are not rendered as labelled mobile cards");
        }
      }
      item.responsiveTables = { count: responsiveTableCount, enhanced: enhancedTableCount };
    }

    if (pagePath === "transformer-architectures.html" && viewport.width <= 700) {
      try {
        const region = page.locator('.table-responsive[role="region"][tabindex="0"]');
        await region.focus();
        const isScrollable = await region.evaluate(node => node.scrollWidth > node.clientWidth);
        if (isScrollable) {
          await page.keyboard.press("ArrowRight");
          await page.waitForFunction(() => document.activeElement?.scrollLeft > 0, null, { timeout: 2000 });
        } else {
          throw new Error("the focusable table region has no horizontal scroll range");
        }
      } catch (error) {
        report.failures.push(`${pagePath}/${lang}/${label}/${theme}: keyboard table scrolling failed: ${error.message}`);
      }
    }

    if (kind === "homepage" && pageErrors.length) {
      report.failures.push(`${pagePath}/${lang}/${label}/${theme}: uncaught page errors: ${pageErrors.join(" | ")}`);
    }
    if (kind === "spine-overview" && consoleErrors.some(message => message.includes("translate(undefined, NaN)"))) {
      const malformedSvgCount = (item.svgDiagnostics || []).reduce((count, svg) => count + svg.invalidTransforms.length, 0);
      report.failures.push(`${pagePath}/${lang}/${label}/${theme}: malformed SVG transforms (${malformedSvgCount} offending elements; see svgDiagnostics and consoleErrors)`);
    }
    const blockingAxe = (item.axe.violations || []).filter(v => ["aria-allowed-attr", "color-contrast", "nested-interactive"].includes(v.id));
    item.axe.blockingViolationCount = blockingAxe.length;
    if (blockingAxe.length) {
      const details = blockingAxe.flatMap(violation =>
        violation.nodes.slice(0, 8).map(node =>
          `${violation.id} ${node.target.join(" ")}: ${(node.failureSummary || node.html || "no node details").replace(/\\s+/g, " ").slice(0, 700)}`
        )
      );
      report.failures.push(
        `${pagePath}/${lang}/${label}/${theme}: Axe blocking violations: ${blockingAxe.map(v => v.id).join(", ")}. ${details.join(" | ")}`
      );
    }
    // Quarto renders each equation inside its pandoc math span client-side.
    // A math span with no rendered output means the reader sees raw source
    // text instead of an equation, so treat it as a blocking audit failure.
    const mathSummary = item.layout.math;
    const unrenderedMath = mathSummary.mathSpans - mathSummary.mathSpansRendered;
    // Entropy is an equation-heavy lesson. Zero parsed math spans means the
    // source delimiters were stripped as Markdown escapes, not that math passed.
    const equationBearingPages = new Set(["entropy.html", "scaled-dot-product-attention.html", "language-representation.html"]);
    if (equationBearingPages.has(pagePath) && mathSummary.mathSpans === 0) {
      report.failures.push(`${pagePath}/${lang}/${label}/${theme}: expected lesson equations, but Quarto produced no math spans`);
    }
    if (unrenderedMath > 0) {
      report.failures.push(
        `${pagePath}/${lang}/${label}/${theme}: ${unrenderedMath} of ${mathSummary.mathSpans} math expressions did not render (pandoc math span without KaTeX or MathJax output)`
      );
    }

    if (item.layout.horizontalOverflow || item.learningMapLayout?.horizontalOverflow) {
      let overflowing = (item.layout.overflowCandidates || []).filter(c => c.right <= item.layout.documentWidth + 1).slice(0, 10).map(c => `${c.tag}${c.className ? "." + String(c.className).split(" ")[0] : ""}[left=${c.left},right=${c.right}]`).join(" | ");
      if (!overflowing) {
        const causes = (item.layout.overflowRootCause || []).map(c => `${c.tag}${c.className ? "." + String(c.className).split(" ")[0] : ""}[left=${c.left},right=${c.right},w=${c.width}]:${c.html}`).join(" ; ");
        overflowing = `rootCause: ${causes}`;
      }
      report.failures.push(`${pagePath}/${lang}/${label}/${theme}: horizontal overflow (document ${item.layout.documentWidth}px vs viewport ${item.layout.viewportWidth}px): ${overflowing}`);
    }
    if (runInteractiveAudit && !item.keyboard.length) report.failures.push(`${pagePath}/${lang}/${label}/${theme}: no keyboard focus targets`);
  } catch (error) {
    item.error = String(error);
    report.failures.push(`${pagePath}/${lang}/${label}/${theme}: ${String(error)}`);
  } finally {
    item.durationMs = Math.round(performance.now() - startedAt);
    report.cases[caseIndex] = item;
    await context.close();
  }
}

// Each case owns its own browser context, so a small worker pool can safely
// overlap navigation, layout checks, keyboard checks, and Axe analysis.
// GitHub's ubuntu-24.04 hosted runner has enough headroom for four independent
// contexts; keep the pool bounded to avoid unbounded Chromium process growth.
const workerCount = Math.min(4, cases.length);
let nextCaseIndex = 0;
const auditStartedAt = performance.now();
await Promise.all(Array.from({ length: workerCount }, async () => {
  while (nextCaseIndex < cases.length) {
    const index = nextCaseIndex++;
    await runCase(cases[index], index);
  }
}));
report.durationMs = Math.round(performance.now() - auditStartedAt);

await browser.close();
fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify(report, null, 2));
console.log(JSON.stringify({
  generatedAt: report.generatedAt,
  durationMs: report.durationMs,
  cases: report.cases.map(c => ({
    page: c.page, lang: c.lang, viewport: c.viewport, theme: c.theme, status: c.httpStatus, title: c.title, durationMs: c.durationMs,
    overflow: c.layout?.horizontalOverflow,
    overflowCandidates: c.layout?.overflowCandidates,
    routeContext: c.routeContext,
    learningMap: c.learningMap,
    learningMapLayout: c.learningMapLayout,
    focusTargets: c.keyboardSummary?.focusTargets,
    focusVisibleTargets: c.keyboardSummary?.focusVisibleTargets,
    axeViolations: c.axe?.violationCount,
    mathSpans: c.layout?.math?.mathSpans,
    unrenderedMath: (c.layout?.math?.mathSpans ?? 0) - (c.layout?.math?.mathSpansRendered ?? 0),
    error: c.error,
  })),
  failures: report.failures,
}, null, 2));
// Surface every failure as a GitHub Actions error annotation so the exact
// failing case is visible in the run summary without downloading artifacts.
for (const failure of report.failures) {
  console.error(`::error::${failure}`);
}
if (report.failures.length > 0) {
  process.exitCode = 1;
}
