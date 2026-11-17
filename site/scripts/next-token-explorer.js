(() => {
  "use strict";
  const copy = {
    fr: {
      tokens: ["Vous", "Je", "Moi", "Oui"],
      probs: ["0,6", "0,2", "0,1", "0,1"],
      next: "savez",
      other: "Autres tokens (ensemble)",
      prefixLabel: "Préfixe actuel :",
      choose: "Choisir le token à ajouter",
      append: "Ajouter au préfixe",
      reset: "Réinitialiser",
      unknown: "Une nouvelle distribution est recalculée pour ce préfixe. Ses valeurs ne sont pas précisées dans l'exemple : nous ne les inventons pas.",
      extended: "Le préfixe a grandi : la distribution est maintenant conditionnée par le contexte enrichi."
    },
    en: {
      tokens: ["They", "Aqueducts", "Nothing", "Well"],
      probs: ["0.6", "0.2", "0.1", "0.1"],
      next: "built",
      other: "Other tokens (combined)",
      prefixLabel: "Current prefix:",
      choose: "Choose the token to append",
      append: "Append to prefix",
      reset: "Reset",
      unknown: "A new distribution is recomputed for this prefix. Its values are not specified in the example, so we do not invent them.",
      extended: "The prefix has grown: the distribution is now conditioned on the extended context."
    }
  };

  function init(root) {
    if (root.dataset.initialised === "true") return;
    const lang = document.documentElement.lang.toLowerCase().startsWith("fr") ? "fr" : "en";
    const t = copy[lang];
    const controls = root.querySelector(".next-token-explorer__interactive");
    const fallback = root.querySelector(".next-token-explorer__fallback");
    const basePrefix = lang === "fr" ? root.dataset.prefixFr : root.dataset.prefixEn;
    if (!controls || !fallback || !basePrefix) {
      root.dataset.initialisationError = "container-or-prefix";
      console.error("Next-token explorer is missing its container or language prefix");
      return;
    }

    const prefixLine = document.createElement("p");
    const prefixLabel = document.createElement("strong");
    const prefix = document.createElement("output");
    prefix.className = "next-token-explorer__prefix";
    prefixLabel.textContent = t.prefixLabel;
    prefixLine.append(prefixLabel, document.createTextNode(" "), prefix);

    const list = document.createElement("ul");
    list.className = "next-token-explorer__distribution";
    list.setAttribute("aria-live", "polite");

    const actions = document.createElement("div");
    actions.className = "next-token-explorer__actions";
    const label = document.createElement("label");
    label.htmlFor = "next-token-choice";
    label.textContent = t.choose;
    const select = document.createElement("select");
    select.id = "next-token-choice";
    select.className = "next-token-explorer__choice";
    const appendButton = document.createElement("button");
    appendButton.type = "button";
    appendButton.className = "next-token-explorer__append";
    appendButton.textContent = t.append;
    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.className = "secondary next-token-explorer__reset";
    resetButton.textContent = t.reset;
    actions.append(label, select, appendButton, resetButton);

    const status = document.createElement("p");
    status.className = "next-token-explorer__next";
    status.setAttribute("role", "status");
    controls.replaceChildren(prefixLine, list, actions, status);

    let current = "", stage = 0;
    function options(tokens) {
      select.replaceChildren();
      tokens.forEach((token, i) => {
        const option = document.createElement("option");
        option.value = String(i);
        option.textContent = token;
        select.append(option);
      });
    }
    function rows(tokens, probs) {
      list.replaceChildren();
      tokens.forEach((token, i) => {
        const item = document.createElement("li");
        const name = document.createElement("span");
        const probability = document.createElement("strong");
        name.textContent = token;
        probability.textContent = probs[i];
        item.append(name, probability);
        list.append(item);
      });
    }
    function reset() {
      current = basePrefix;
      stage = 0;
      prefix.textContent = current;
      rows(t.tokens, t.probs);
      options(t.tokens);
      select.disabled = false;
      appendButton.disabled = false;
      status.textContent = "";
    }
    appendButton.addEventListener("click", () => {
      const index = Number(select.value);
      const token = select.options[select.selectedIndex].textContent;
      current += " " + token;
      prefix.textContent = current;
      if (stage === 0 && index === 0) {
        stage = 1;
        rows([t.next, t.other], ["0.5", "0.5"].map(value => lang === "fr" ? value.replace(".", ",") : value));
        options([t.next, t.other]);
        select.disabled = true;
        appendButton.disabled = true;
        status.textContent = t.extended;
      } else {
        stage = 2;
        select.disabled = true;
        appendButton.disabled = true;
        status.textContent = t.unknown;
      }
    });
    resetButton.addEventListener("click", reset);
    reset();
    controls.hidden = false;
    fallback.hidden = true;
    root.dataset.initialised = "true";
  }

  function labelTables() {
    document.querySelectorAll(".responsive-card-table table").forEach(table => {
      const headers = Array.from(table.querySelectorAll("thead th"), th => th.textContent.trim());
      if (!headers.length) return;
      table.querySelectorAll("tbody tr").forEach(row =>
        Array.from(row.querySelectorAll("td")).forEach((cell, index) => {
          if (headers[index]) cell.dataset.label = headers[index];
        })
      );
      table.classList.add("responsive-card-table__enhanced");
    });
  }

  function start() {
    document.querySelectorAll("[data-next-token-explorer]").forEach(init);
    labelTables();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
