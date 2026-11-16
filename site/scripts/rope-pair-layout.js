(() => {
  "use strict";
  const rotate = (x, y, a) => [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
  const fmt = (v) => v.map(x => x.toFixed(3)).join(", ");
  function init(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const fr = root.dataset.lang === "fr";
    const control = name => root.querySelector(`[data-layout-control="${name}"]`);
    const out = name => root.querySelector(`[data-layout-out="${name}"]`);
    const initialInterleaved = [1, 2, 3, 4];
    function render() {
      const a0 = Number(control("a0").value), a1 = Number(control("a1").value);
      const mismatch = control("mismatch").checked;
      const p0 = rotate(initialInterleaved[0], initialInterleaved[1], a0);
      const p1 = rotate(initialInterleaved[2], initialInterleaved[3], a1);
      const interleaved = [p0[0], p0[1], p1[0], p1[1]];
      const splitInput = [initialInterleaved[0], initialInterleaved[2], initialInterleaved[1], initialInterleaved[3]];
      let splitOutput;
      if (mismatch) {
        const wrong0 = rotate(splitInput[0], splitInput[1], a0);
        const wrong1 = rotate(splitInput[2], splitInput[3], a1);
        splitOutput = [wrong0[0], wrong1[0], wrong0[1], wrong1[1]];
      } else {
        const s0 = rotate(splitInput[0], splitInput[2], a0);
        const s1 = rotate(splitInput[1], splitInput[3], a1);
        splitOutput = [s0[0], s1[0], s0[1], s1[1]];
      }
      const maxDiff = Math.max(...interleaved.map((v, i) => Math.abs(v - splitOutput[i])));
      out("a0").textContent = fr ? a0.toFixed(2).replace(".", ",") : a0.toFixed(2);
      out("a1").textContent = fr ? a1.toFixed(2).replace(".", ",") : a1.toFixed(2);
      out("interleaved").textContent = `[${fmt(interleaved)}]`;
      out("split").textContent = `[${fmt(splitOutput)}]`;
      if (mismatch) {
        out("result").textContent = fr
          ? `Les conventions sont mélangées : écart maximal après permutation = ${maxDiff.toFixed(6)}. Des formes de tenseurs valides ne garantissent pas une rotation correcte.`
          : `The conventions are mixed: maximum difference after permutation = ${maxDiff.toFixed(6)}. Valid tensor shapes do not guarantee a correct rotation.`;
      } else {
        out("result").textContent = fr
          ? `Équivalence vérifiée après permutation : écart maximal = ${maxDiff.toFixed(6)}.`
          : `Equivalence after permutation: maximum difference = ${maxDiff.toFixed(6)}.`;
      }
    }
    ["a0", "a1", "mismatch"].forEach(name => control(name).addEventListener("input", render));
    render();
  }
  function start() { document.querySelectorAll(".rope-pair-layout").forEach(init); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();