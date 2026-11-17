(() => {
  "use strict";
  const copy = {
    fr: {tokens:["Vous","Je","Moi","Oui"], probs:["0,6","0,2","0,1","0,1"], next:"savez", other:"Autres tokens (ensemble)", unknown:"Une nouvelle distribution est recalculée pour ce préfixe. Ses valeurs ne sont pas précisées dans l'exemple : nous ne les inventons pas."},
    en: {tokens:["They","Aqueducts","Nothing","Well"], probs:["0.6","0.2","0.1","0.1"], next:"built", other:"Other tokens (combined)", unknown:"A new distribution is recomputed for this prefix. Its values are not specified in the example, so we do not invent them."}
  };
  function init(root) {
    if (root.dataset.initialised === "true") return;
    const lang = document.documentElement.lang.toLowerCase().startsWith("fr") ? "fr" : "en";
    const t = copy[lang], controls = root.querySelector(".next-token-explorer__interactive");
    const prefix = controls && controls.querySelector("output"), list = controls && controls.querySelector("ul");
    const select = controls && controls.querySelector("select");
    const paragraphs = controls ? controls.querySelectorAll("p") : [];
    const status = paragraphs.length > 1 ? paragraphs[1] : null;
    const buttons = controls ? controls.querySelectorAll("button") : [];
    const appendButton = buttons[0] || null, resetButton = buttons[1] || null;
    const missing = [
      ["controls", controls], ["prefix", prefix], ["distribution", list],
      ["token-choice", select], ["next-distribution", status],
      ["append", appendButton], ["reset", resetButton],
    ].filter(([, element]) => !element).map(([name]) => name);
    if (missing.length) {
      root.dataset.initialisationError = missing.join(",");
      console.error("Next-token explorer missing required elements: " + missing.join(", "));
      return;
    }
    root.dataset.initialised = "true";
    let current = "", stage = 0;
    function options(tokens) {
      select.replaceChildren();
      tokens.forEach((token, i) => { const o=document.createElement("option");o.value=String(i);o.textContent=token;select.append(o); });
    }
    function rows(tokens, probs) {
      list.replaceChildren();
      tokens.forEach((token, i) => { const li=document.createElement("li"), name=document.createElement("span"), p=document.createElement("strong");name.textContent=token;p.textContent=probs[i];li.append(name,p);list.append(li); });
    }
    function reset() {
      current = (lang === "fr" ? root.dataset.prefixFr : root.dataset.prefixEn); stage = 0;
      prefix.textContent = current; rows(t.tokens,t.probs); options(t.tokens);
      select.disabled = false; appendButton.disabled = false; status.textContent = "";
    }
    appendButton.addEventListener("click", () => {
      const index = Number(select.value), token = select.options[select.selectedIndex].textContent;
      current += " " + token; prefix.textContent = current;
      if (stage === 0 && index === 0) {
        stage = 1; rows([t.next,t.other],["0.5","0.5"].map(x => lang==="fr" ? x.replace(".",",") : x));
        options([t.next,t.other]);
        select.disabled = true; appendButton.disabled = true;
        status.textContent = lang==="fr" ? "Le préfixe a grandi : la distribution est maintenant conditionnée par le contexte enrichi." : "The prefix has grown: the distribution is now conditioned on the extended context.";
      } else {
        stage = 2; select.disabled = true; appendButton.disabled = true; status.textContent = t.unknown;
      }
    });
    resetButton.addEventListener("click",reset);
    reset(); controls.hidden=false; root.querySelector(".next-token-explorer__fallback").hidden=true;
  }
  function labelTables() {
    document.querySelectorAll(".responsive-card-table table").forEach(table => {
      const headers=Array.from(table.querySelectorAll("thead th"),th=>th.textContent.trim());
      if(!headers.length)return;
      table.querySelectorAll("tbody tr").forEach(row=>Array.from(row.querySelectorAll("td")).forEach((cell,i)=>{if(headers[i])cell.dataset.label=headers[i];}));
      table.classList.add("responsive-card-table__enhanced");
    });
  }
  function start(){document.querySelectorAll("[data-next-token-explorer]").forEach(init);labelTables();}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();
})();
