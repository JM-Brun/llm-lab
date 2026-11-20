(() => {
  "use strict";

  const copy = {
    fr: {
      turns: [
        [["Vous", 0.6], ["Je", 0.2], ["Moi", 0.1], ["Oui", 0.1]],
        [["savez", 0.5], ["êtes", 0.3], ["voyez", 0.2]],
        [[",", 0.8, ""], ["que", 0.1], [":", 0.1, "\u202f"]]
      ],
      distribution: turn => `Distribution du prochain token · tour ${turn}`,
      add: (token, probability) => `Ajouter « ${token} » (probabilité ${probability})`,
      unknown: "La distribution suivante dépend de ce nouveau préfixe. Ses valeurs ne figurent pas dans la trace.",
      end: "La trace s’arrête ici, après trois ajouts."
    },
    en: {
      turns: [
        [["They", 0.6], ["Aqueducts", 0.2], ["Nothing", 0.1], ["Well", 0.1]],
        [["built", 0.5], ["gave", 0.3], ["made", 0.2]],
        [["roads", 0.8], ["bridges", 0.1], ["walls", 0.1]]
      ],
      distribution: turn => `Next-token distribution · turn ${turn}`,
      add: (token, probability) => `Append “${token}” (probability ${probability})`,
      unknown: "The next distribution depends on this new prefix. Its values are outside the worked trace.",
      end: "The worked trace ends here, after three additions."
    }
  };

  function init(root) {
    const lang = document.documentElement.lang.toLowerCase().startsWith("fr") ? "fr" : "en";
    const text = copy[lang];
    const format = new Intl.NumberFormat(lang, { maximumFractionDigits: 1 });
    const basePrefix = lang === "fr" ? root.dataset.prefixFr : root.dataset.prefixEn;
    const controls = root.querySelector(".next-token-explorer__interactive");
    const fallback = root.querySelector(".next-token-explorer__fallback");
    const context = root.querySelector(".next-token-explorer__context");
    const prefix = root.querySelector(".next-token-explorer__prefix");
    const added = root.querySelector(".next-token-explorer__added");
    const status = root.querySelector(".next-token-explorer__status");
    const choices = root.querySelector(".next-token-explorer__choices");
    const heading = choices.querySelector("h4");
    const list = choices.querySelector("ul");
    const reset = root.querySelector(".next-token-explorer__reset");

    function showTurn(turn) {
      heading.textContent = text.distribution(turn + 1);
      const items = text.turns[turn].map(([token, probability, separator = " "], index) => {
        const item = document.createElement("li");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "next-token-explorer__candidate";
        const value = format.format(probability);
        button.setAttribute("aria-label", text.add(token, value));

        const name = document.createElement("span");
        name.textContent = token;
        const number = document.createElement("strong");
        number.textContent = value;
        const bar = document.createElement("span");
        bar.className = "next-token-explorer__bar";
        bar.style.setProperty("--probability", probability);
        bar.setAttribute("aria-hidden", "true");
        button.append(name, number, bar);
        item.append(button);
        button.addEventListener("click", () => {
          prefix.textContent += added.textContent;
          added.textContent = separator + token;
          const followsTrace = index === 0;
          const atLastTurn = turn + 1 === text.turns.length;

          if (followsTrace && !atLastTurn) {
            showTurn(turn + 1);
          } else {
            list.replaceChildren();
            choices.hidden = true;
            status.textContent = followsTrace ? text.end : text.unknown;
            status.hidden = false;
          }

          reset.hidden = false;
          context.focus();
        });
        return item;
      });
      list.replaceChildren(...items);
      choices.hidden = false;
    }

    function restart() {
      prefix.textContent = basePrefix;
      added.textContent = "";
      status.textContent = "";
      status.hidden = true;
      reset.hidden = true;
      showTurn(0);
    }

    reset.addEventListener("click", () => {
      restart();
      list.querySelector("button").focus();
    });

    restart();
    controls.hidden = false;
    fallback.hidden = true;
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
