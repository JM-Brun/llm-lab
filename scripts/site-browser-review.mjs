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

const cases = [
  ...visualCases.map(testCase => ({
    ...testCase, page: "queries-keys-values.html", kind: "qkv",
  })),
  ...visualCases.map(testCase => ({
    ...testCase, page: "learning-map.html", kind: "learning-map",
  })),
  ...visualCases.flatMap(testCase =>
    ["llm-overview.html", "generation.html"].map(page => ({
      ...testCase, page, kind: "route-context",
    }))
  ),
];

const browser = await chromium.launch({ headless: true });
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
  try {
    const response = await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
    item.httpStatus = response?.status() ?? null;
    if (!response || !response.ok()) throw new Error(`HTTP status ${item.httpStatus}`);
    await page.evaluate(() => document.fonts?.ready.then(() => true));
    await page.waitForTimeout(1000);

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

    if (kind === "learning-map") {
      const mode = page.locator("[data-map-mode]");
      if (await mode.count() !== 1) throw new Error("learning-map mode selector is missing");
      if (await page.locator('label[for="learning-map-mode"]').count() !== 1) {
        throw new Error("learning-map mode selector has no associated label");
      }
      await mode.selectOption("concepts");
      await page.waitForSelector(".map-concept-item", { timeout: 15000 });
      const legend = page.locator(".learning-map-concept-legend");
      const relationFilter = page.locator("[data-map-relation-type]");
      const relationOptions = await relationFilter.locator("option").evaluateAll(options =>
        options.map(option => ({ value: option.value, label: option.textContent.trim() }))
      );
      item.learningMap = {
        legendVisible: await legend.isVisible(),
        legendItems: await legend.locator(".map-concept-legend-item").count(),
        conceptButtons: await page.locator(".map-concept-item").count(),
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
      await page.locator(".map-concept-item").first().click();
      item.learningMap.selectedConcept = await page.locator(".map-concept-item[aria-pressed='true']").count() === 1;
      item.learningMap.detailsTitle = await page.locator(".map-detail-panel .map-detail-title").first().innerText().catch(() => null);
      if (!item.learningMap.selectedConcept || !item.learningMap.detailsTitle) {
        throw new Error("selecting a concept did not update its accessible details panel");
      }
      await page.keyboard.press("Escape");
      item.learningMap.escapeClearsSelection = await page.locator(".map-concept-item[aria-pressed='true']").count() === 0;
      if (!item.learningMap.escapeClearsSelection) {
        throw new Error("Escape did not clear the selected concept");
      }
    }

    if (kind === "route-context") {
      const context = page.locator(".guided-page-context");
      if (await context.count() !== 1) throw new Error("guided-route context is missing");
      item.routeContext = {
        isMultiple: await context.evaluate(el => el.classList.contains("guided-page-context--multiple")),
        stageLinks: await context.locator('a[href*="learning-map.html#guided-stage-"]').count(),
        currentPageMarkers: await context.locator('[aria-current="page"]').count(),
        listItems: await context.locator("li").count(),
        navLandmark: await context.evaluate(el => el.tagName.toLowerCase() === "nav"),
        accessibleLabel: await context.getAttribute("aria-label"),
      };
      if (!item.routeContext.stageLinks) throw new Error("guided-route context has no stage links");
      const stageFragments = await context.locator('a[href*="learning-map.html#guided-stage-"]').evaluateAll(links =>
        links.map(link => (link.getAttribute("href").split("#")[1] || ""))
      );
      const routeMapPage = await context.context().newPage();
      try {
        await routeMapPage.goto(`${BASE}/${lang}/learning-map.html`, { waitUntil: "networkidle", timeout: 60000 });
        item.routeContext.stageAnchorsResolve = await routeMapPage.evaluate(ids =>
          ids.every(id => id && document.getElementById(id) !== null), stageFragments
        );
      } finally {
        await routeMapPage.close();
      }
      if (!item.routeContext.stageAnchorsResolve) throw new Error("guided-route stage link points to a missing anchor");
      if (pagePath === "llm-overview.html") {
        if (item.routeContext.isMultiple || !item.routeContext.navLandmark ||
            item.routeContext.currentPageMarkers !== 1) {
          throw new Error("single-stage context is not exposed as a labelled breadcrumb");
        }
      } else if (pagePath === "generation.html") {
        if (!item.routeContext.isMultiple || item.routeContext.navLandmark ||
            item.routeContext.listItems !== 2 || item.routeContext.currentPageMarkers !== 0) {
          throw new Error("multi-stage context is misleading or incomplete");
        }
      }
    }

    const axe = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    item.axe = {
      violations: axe.violations.map(v => ({
        id: v.id, impact: v.impact, description: v.description,
        help: v.help, nodes: v.nodes.slice(0, 8).map(n => ({
          target: n.target, summary: n.failureSummary?.slice(0, 500),
        })),
      })),
      violationCount: axe.violations.length,
      passes: axe.passes.length,
      incomplete: axe.incomplete.length,
    };

    if (item.layout.horizontalOverflow) report.failures.push(`${pagePath}/${lang}/${label}/${theme}: horizontal overflow`);
    if (!item.keyboard.length) report.failures.push(`${pagePath}/${lang}/${label}/${theme}: no keyboard focus targets`);
  } catch (error) {
    item.error = String(error);
    report.failures.push(`${lang}/${label}: ${String(error)}`);
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
    focusTargets: c.keyboardSummary?.focusTargets,
    focusVisibleTargets: c.keyboardSummary?.focusVisibleTargets,
    axeViolations: c.axe?.violationCount,
    error: c.error,
  })),
  failures: report.failures,
}, null, 2));
if (report.failures.length) process.exitCode = 1;
