(() => {
  "use strict";
  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const fr = root.dataset.lang === "fr";
    const control = name => root.querySelector('[data-control="' + name + '"]');
    const output = name => root.querySelector('[data-out="' + name + '"]');
    const fmt = value => Number(value).toLocaleString(fr ? "fr-FR" : "en-US", { minimumFractionDigits: 3, maximumFractionDigits: 3 });
    const explanations = fr ? {
      conditioned: "Le biais jouet est b(hᵢ, Δ) = α · tanh(hᵢ) · (−|Δ| / 4). Il dépend à la fois d'une caractéristique de l'état caché de la requête et du décalage relatif. La formule sert à visualiser une dépendance, pas à reproduire un modèle publié.",
      bucketed: "Le biais jouet consulte une petite table selon |Δ| : 0, 1, 2–3, 4–7 ou 8+. Dans T5, les valeurs sont apprises par tête et indexées par buckets de positions relatives ; cette table chiffrée est seulement illustrative.",
      none: "Aucun terme positionnel relatif n'est ajouté : le score affiché ne contient que le terme de contenu. Cela ne dit rien, à lui seul, des autres mécanismes positionnels éventuellement présents ailleurs dans le modèle."
    } : {
      conditioned: "The toy bias is b(hᵢ, Δ) = α · tanh(hᵢ) · (−|Δ| / 4). It depends on both a query hidden-state feature and relative offset. This formula visualizes a dependency; it does not reproduce a published model.",
      bucketed: "The toy bias looks up a small table by |Δ|: 0, 1, 2–3, 4–7, or 8+. T5 learns per-head values indexed by relative-position buckets; the numeric table here is illustrative only.",
      none: "No relative-position term is added: the displayed score contains only the content term. This alone says nothing about other positional mechanisms that may exist elsewhere in a model."
    };
    function render() {
      const content = +control("content").value;
      const distance = +control("distance").value;
      const state = +control("state").value;
      const strength = +control("strength").value;
      const mode = control("mode").value;
      let bias = 0;
      if (mode === "conditioned") bias = strength * Math.tanh(state) * (-Math.abs(distance) / 4);
      if (mode === "bucketed") {
        const d = Math.abs(distance);
        const bucket = d === 0 ? 0 : d === 1 ? 1 : d <= 3 ? 2 : d <= 7 ? 3 : 4;
        const illustrativePerBucket = [-0.1, -0.25, -0.4, -0.55, -0.7];
        bias = strength * illustrativePerBucket[bucket];
      }
      output("content").textContent = fmt(content);
      output("distance").textContent = (distance > 0 ? "+" : "") + distance;
      output("state").textContent = fmt(state);
      output("strength").textContent = fmt(strength);
      output("content-term").textContent = fmt(content);
      output("bias").textContent = fmt(bias);
      output("total").textContent = fmt(content + bias);
      root.querySelector("[data-explanation]").textContent = explanations[mode];
    }
    ["content", "distance", "state", "strength", "mode"].forEach(name => {
      control(name).addEventListener("input", render);
      control(name).addEventListener("change", render);
    });
    render();
  }
  function start() { document.querySelectorAll(".relative-bias-decomposition").forEach(initialise); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();