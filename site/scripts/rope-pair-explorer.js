(() => {
  "use strict";

  const rotate = (vector, angle) => {
    const [x, y] = vector;
    const cosine = Math.cos(angle);
    const sine = Math.sin(angle);
    return [cosine * x - sine * y, sine * x + cosine * y];
  };
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
  const fmt = (value, digits = 3) => value.toFixed(digits);

  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const get = (name) => root.querySelector(`[data-control="${name}"]`);
    const out = (name) => root.querySelector(`[data-out="${name}"]`);
    const drawing = root.querySelector("[data-drawing]");
    const lang = root.dataset.lang;
    const qMarker = lang === "fr" ? "rope-arrow-q-fr" : "rope-arrow-q-en";
    const kMarker = lang === "fr" ? "rope-arrow-k-fr" : "rope-arrow-k-en";
    const q = [3.2, 1.1];
    const k = [1.4, 3.0];
    const scale = 34;
    const origin = [260, 150];
    const svgNS = "http://www.w3.org/2000/svg";

    function line(vector, color, marker, dashed, label) {
      const x = origin[0] + vector[0] * scale;
      const y = origin[1] - vector[1] * scale;
      const element = document.createElementNS(svgNS, "line");
      element.setAttribute("x1", origin[0]);
      element.setAttribute("y1", origin[1]);
      element.setAttribute("x2", x);
      element.setAttribute("y2", y);
      element.setAttribute("stroke", color);
      element.setAttribute("stroke-width", dashed ? "2" : "3");
      element.setAttribute("stroke-dasharray", dashed ? "6 5" : "none");
      if (marker) element.setAttribute("marker-end", `url(#${marker})`);
      drawing.appendChild(element);
      const text = document.createElementNS(svgNS, "text");
      text.setAttribute("x", x + 7);
      text.setAttribute("y", y - 7);
      text.setAttribute("fill", color);
      text.setAttribute("font-size", "13");
      text.textContent = label;
      drawing.appendChild(text);
    }

    function render() {
      const m = Number(get("m").value);
      const n = Number(get("n").value);
      const theta = Number(get("theta").value);
      const shift = Number(get("shift").value);
      const qm = rotate(q, m * theta);
      const kn = rotate(k, n * theta);
      const shiftedQ = rotate(q, (m + shift) * theta);
      const shiftedK = rotate(k, (n + shift) * theta);
      const score = dot(qm, kn);
      const shiftedScore = dot(shiftedQ, shiftedK);
      ["m", "n", "shift"].forEach((key) => { out(key).textContent = get(key).value; });
      out("theta").textContent = lang === "fr" ? theta.toFixed(2).replace(".", ",") : theta.toFixed(2);
      out("angles").textContent = `q: ${fmt(m * theta)} rad · k: ${fmt(n * theta)} rad`;
      out("dot").textContent = fmt(score);
      out("relative").textContent = `${n - m}`;
      out("shifted").textContent = `${fmt(shiftedScore)} (écart ${fmt(shiftedScore - score)})`;
      if (lang === "en") out("shifted").textContent = `${fmt(shiftedScore)} (difference ${fmt(shiftedScore - score)})`;
      drawing.replaceChildren();
      line(q, "#2563eb", null, true, "q");
      line(qm, "#2563eb", qMarker, false, "qₘ");
      line(k, "#d97706", null, true, "k");
      line(kn, "#d97706", kMarker, false, "kₙ");
    }

    ["m", "n", "theta", "shift"].forEach((key) => get(key).addEventListener("input", render));
    render();
  }

  function start() {
    document.querySelectorAll(".rope-pair-explorer").forEach(initialise);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();