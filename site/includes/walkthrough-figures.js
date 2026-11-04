/*
 * LLM Lab — Interactive walkthrough figures (guided-build tour pages).
 * Links code "chips" (buttons) to the matching parts of an adjacent SVG diagram.
 * Access contract: hover highlights temporarily, click or keyboard toggles a
 * pinned selection, and the caption is an aria-live region, so hover is never
 * the only way to reach the information. No external dependencies.
 */
(function () {
  "use strict";

  function tokens(value) {
    return String(value || "").split(/\s+/).filter(Boolean);
  }

  function setupFigure(fig) {
    var chips = Array.prototype.slice.call(fig.querySelectorAll(".wf-chip"));
    if (!chips.length) return;
    var note = fig.querySelector(".wf-note");
    var parts = Array.prototype.slice.call(fig.querySelectorAll("[data-wf-part]"));
    var defaultNote = fig.getAttribute("data-wf-default") || (note ? note.textContent : "");
    var pinned = null;

    function setNote(text) {
      if (note) note.textContent = text;
    }

    function render(chip) {
      var links = chip ? tokens(chip.getAttribute("data-wf-links")) : [];
      parts.forEach(function (part) {
        var own = tokens(part.getAttribute("data-wf-part"));
        var lit = own.some(function (t) { return links.indexOf(t) !== -1; });
        part.classList.toggle("wf-lit", lit);
      });
      chips.forEach(function (c) {
        c.setAttribute("aria-pressed", String(c === pinned));
      });
      fig.classList.toggle("wf-focus", Boolean(chip));
      setNote(chip ? (chip.getAttribute("data-wf-note") || defaultNote) : defaultNote);
    }

    chips.forEach(function (chip) {
      chip.addEventListener("mouseenter", function () { render(chip); });
      chip.addEventListener("mouseleave", function () { render(pinned); });
      chip.addEventListener("focus", function () { render(chip); });
      chip.addEventListener("blur", function () { render(pinned); });
      chip.addEventListener("click", function () {
        pinned = (pinned === chip) ? null : chip;
        render(pinned || chip);
      });
    });

    fig.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && pinned) {
        var chip = pinned;
        pinned = null;
        render(null);
        chip.focus();
        event.preventDefault();
      }
    });
  }

  function init() {
    document.querySelectorAll("figure.wf-fig").forEach(setupFigure);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
