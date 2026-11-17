(() => {
  "use strict";
  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const lang = root.dataset.lang;
    const fr = lang === "fr";
    const layersEl = root.querySelector("[data-layers]");
    const summary = root.querySelector("[data-summary]");
    const inheritance = root.querySelector("[data-inheritance]");
    const rope = fr ? "RoPE : rotation de Q et K" : "RoPE: rotate Q and K";
    const nope = fr ? "NoPE : pas de rotation explicite" : "NoPE: no explicit rotation";
    let pattern = [true, true, false, true, false, false];
    const labels = fr ? ["Couche 1","Couche 2","Couche 3","Couche 4","Couche 5","Couche 6"] : ["Layer 1","Layer 2","Layer 3","Layer 4","Layer 5","Layer 6"];
    function render() {
      layersEl.replaceChildren();
      pattern.forEach((usesRope, index) => {
        const card = document.createElement("article");
        card.className = "hybrid-layer-card" + (usesRope ? " is-rope" : " is-nope");
        const heading = document.createElement("h4");
        heading.textContent = labels[index];
        const toggleLabel = document.createElement("label");
        toggleLabel.className = "hybrid-layer-toggle";
        const toggle = document.createElement("input");
        toggle.type = "checkbox";
        toggle.checked = usesRope;
        toggle.setAttribute("aria-label", fr ? labels[index] + " : appliquer RoPE" : labels[index] + ": apply RoPE");
        toggle.addEventListener("change", () => { pattern[index] = toggle.checked; render(); });
        const toggleText = document.createElement("span");
        toggleText.textContent = usesRope ? rope : nope;
        toggleLabel.append(toggle, toggleText);
        const local = document.createElement("p");
        local.textContent = usesRope
          ? (fr ? "Q et K sont tournés avant le score d'attention." : "Q and K are rotated before the attention score.")
          : (fr ? "Q et K ne reçoivent pas de rotation positionnelle dans cette couche." : "Q and K receive no positional rotation in this layer.");
        const flow = document.createElement("p");
        flow.className = "hybrid-layer-flow";
        flow.textContent = index === 0
          ? (fr ? "Entrée : embeddings / états initiaux" : "Input: embeddings / initial states")
          : (fr ? "Entrée : états cachés de la couche " + index : "Input: hidden states from layer " + index);
        const mask = document.createElement("span");
        mask.className = "hybrid-mask-tag";
        mask.textContent = fr ? "Masque causal conservé" : "Causal mask retained";
        card.append(heading, toggleLabel, local, flow, mask);
        layersEl.appendChild(card);
      });
      const count = pattern.filter(Boolean).length;
      summary.textContent = fr
        ? count + " couche(s) sur 6 appliquent RoPE. Le masque causal reste présent dans les 6 couches."
        : count + " of 6 layers apply RoPE. The causal mask remains present in all 6 layers.";
      const first = pattern.indexOf(true);
      inheritance.textContent = first >= 0 && pattern.some((v, i) => i > first && !v)
        ? (fr
          ? "Après la première couche RoPE, les couches NoPE ultérieures reçoivent des états contextualisés qui peuvent déjà porter des distinctions liées au contexte et à la position. Elles n'ajoutent simplement pas de nouvelle rotation RoPE. Leur conservation et leur usage ne sont pas garantis."
          : "After the first RoPE layer, later NoPE layers receive contextualized states that may already carry context- and position-related distinctions. They simply add no new RoPE rotation. Retention and use are not guaranteed.")
        : (fr
          ? "Les états cachés circulent d'une couche à la suivante, quel que soit le choix local. Sans couche RoPE, le masque causal et le contenu restent présents, mais aucune rotation RoPE n'est ajoutée."
          : "Hidden states flow from one layer to the next regardless of the local choice. With no RoPE layer, causal masking and content remain, but no RoPE rotation is added.");
    }
    root.querySelectorAll("[data-preset]").forEach(button => button.addEventListener("click", () => {
      const preset = button.dataset.preset;
      pattern = pattern.map((_, i) => preset === "all-rope" ? true : preset === "all-nope" ? false : preset === "alternating" ? i % 2 === 0 : i < 2);
      render();
    }));
    render();
  }
  function start() { document.querySelectorAll(".hybrid-rope-nope").forEach(initialise); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();