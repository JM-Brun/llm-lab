(() => {
  "use strict";
  const Q = [[1.0, 0.2], [0.4, 1.0], [0.8, -0.3]];
  const K = [[0.8, 0.5], [0.1, 1.1], [1.0, -0.2]];
  const V = [[1.0, 0.0], [0.0, 2.0], [2.0, 1.0]];
  const theta = 0.55;
  const rotate = ([x, y], a) => [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
  const fmt = (x) => x.toFixed(3);
  const vec = (v) => `[${fmt(v[0])}, ${fmt(v[1])}]`;
  const softmax = (values) => {
    const max = Math.max(...values);
    const exps = values.map((v) => Math.exp(v - max));
    const sum = exps.reduce((a, b) => a + b, 0);
    return exps.map((v) => v / sum);
  };

  function init(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const lang = root.dataset.lang;
    const fr = lang === "fr";
    const control = (name) => root.querySelector(`[data-pipe-control="${name}"]`);
    const output = (name) => root.querySelector(`[data-pipe-out="${name}"]`);
    const set = (name, value) => { output(name).textContent = value; };
    const labels = fr
      ? {token:"token", masked:"masqué", no:"aucun", q:"Q", k:"K", v:"V", allowed:"autorisé", future:"futur exclu", insight:"Observation : ", causalOn:"Le masque causal empêche la requête de consulter les tokens futurs.", causalOff:"Sans masque causal, la requête peut consulter aussi les positions futures."}
      : {token:"token", masked:"masked", no:"none", q:"Q", k:"K", v:"V", allowed:"allowed", future:"future excluded", insight:"Observation: ", causalOn:"The causal mask prevents the query from reading future tokens.", causalOff:"Without the causal mask, the query can also read future positions."};

    function table(headers, rows) {
      const t = document.createElement("table");
      t.className = "rope-pipeline-table";
      const head = document.createElement("thead");
      const hr = document.createElement("tr");
      headers.forEach((h) => { const th = document.createElement("th"); th.textContent = h; hr.appendChild(th); });
      head.appendChild(hr); t.appendChild(head);
      const body = document.createElement("tbody");
      rows.forEach((row) => { const tr = document.createElement("tr"); row.forEach((cell) => { const td = document.createElement("td"); td.textContent = String(cell); tr.appendChild(td); }); body.appendChild(tr); });
      t.appendChild(body);
      return t;
    }

    function render() {
      const i = Number(control("query").value);
      const useRope = control("rope").checked;
      const causal = control("causal").checked;
      set("query", String(i));
      const q = useRope ? rotate(Q[i], i * theta) : Q[i];
      const keys = K.map((v, j) => useRope ? rotate(v, j * theta) : v);
      const scores = keys.map((key) => dot(q, key) / Math.sqrt(2));
      const visible = scores.map((_, j) => !causal || j <= i);
      const weights = softmax(scores.map((s, j) => visible[j] ? s : -1e9));
      const result = [0, 0];
      weights.forEach((w, j) => { if (visible[j]) { result[0] += w * V[j][0]; result[1] += w * V[j][1]; } });

      output("projections").replaceChildren(table(["i", "Qᵢ", "Kᵢ", "Vᵢ"], Q.map((v, j) => [j, vec(v), vec(K[j]), vec(V[j])])));
      output("rotations").replaceChildren(table(["position", "Qᵢ utilisé", "Kⱼ utilisé", "Vⱼ"], [[i, vec(q), "—", "—"], ...keys.map((key, j) => [j, "—", vec(key), vec(V[j])])]));
      output("scores").replaceChildren(table(["clé j", "score brut"], scores.map((s, j) => [j, fmt(s)])));
      output("mask").replaceChildren(table(["clé j", "visibilité"], visible.map((v, j) => [j, v ? labels.allowed : labels.future])));
      output("weights").replaceChildren(table(["clé j", "poids"], weights.map((w, j) => [j, visible[j] ? fmt(w) : "0.000"])));
      output("output").replaceChildren(table(["sortie", "valeur"], [["Σⱼ αᵢⱼ Vⱼ", vec(result)]]));
      const message = causal ? labels.causalOn : labels.causalOff;
      set("insight", labels.insight + message + (useRope ? (fr ? " RoPE est appliqué à Q et K, jamais à V dans cet exemple." : " RoPE is applied to Q and K, never V, in this example.") : (fr ? " RoPE est désactivé : les scores n'utilisent pas de rotation positionnelle." : " RoPE is off: scores use no positional rotation.")));
    }
    ["query", "rope", "causal"].forEach((name) => control(name).addEventListener("input", render));
    render();
  }
  function start() { document.querySelectorAll(".rope-attention-pipeline").forEach(init); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();