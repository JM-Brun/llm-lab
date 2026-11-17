(() => {
  "use strict";
  const fmt = (x, n = 5) => Number(x).toLocaleString(undefined, { maximumFractionDigits: n });
  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const control = (name) => root.querySelector(`[data-control="${name}"]`);
    const output = (name) => root.querySelector(`[data-out="${name}"]`);
    const rows = root.querySelector("[data-frequency-rows]");
    const lang = root.dataset.lang;
    const number = (x, digits = 5) => lang === "fr"
      ? x.toLocaleString("fr-FR", { maximumFractionDigits: digits })
      : x.toLocaleString("en-US", { maximumFractionDigits: digits });
    function render() {
      const d = Number(control("dim").value);
      const base = Number(control("base").value);
      const p = Number(control("position").value);
      const count = d / 2;
      const frequency = (i) => Math.pow(base, -2 * i / d);
      const fast = frequency(0);
      const slow = frequency(count - 1);
      output("dim").textContent = d;
      output("base").textContent = number(base, 0);
      output("position").textContent = p;
      output("fast").textContent = `ω₀ = ${number(fast, 6)} · λ ≈ ${number(2 * Math.PI / fast, 2)} positions`;
      output("slow").textContent = `ω${count - 1} = ${number(slow, 8)} · λ ≈ ${number(2 * Math.PI / slow, 1)} positions`;
      output("ratio").textContent = number(fast / slow, 1) + "×";
      const indices = [...new Set([0, 1, 2, Math.floor((count - 1) / 3), Math.floor(2 * (count - 1) / 3), count - 2, count - 1])]
        .filter(i => i >= 0 && i < count).sort((a, b) => a - b);
      rows.replaceChildren();
      for (const i of indices) {
        const w = frequency(i);
        const tr = document.createElement("tr");
        [String(i), number(w, 8), number(2 * Math.PI / w, 2), number(p * w, 5)].forEach(value => {
          const td = document.createElement("td");
          td.textContent = value;
          tr.appendChild(td);
        });
        rows.appendChild(tr);
      }
    }
    ["dim", "base", "position"].forEach(name => control(name).addEventListener("input", render));
    ["dim"].forEach(name => control(name).addEventListener("change", render));
    render();
  }
  function start() { document.querySelectorAll(".rope-frequency-explorer").forEach(initialise); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();