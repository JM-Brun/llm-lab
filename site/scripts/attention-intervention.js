(() => {
  "use strict";

  function initialize(root) {
    const controls = root.querySelector("[data-attention-controls]");
    const select = controls.querySelector("select");
    const comparison = root.querySelector("[data-attention-comparison]");
    const afterWeights = comparison.querySelector("[data-attention-after-weights]");
    const afterOutput = comparison.querySelector("[data-attention-output]");
    const number = new Intl.NumberFormat(root.lang, { maximumFractionDigits: 3 });
    const separator = root.lang === "fr" ? " ; " : ", ";
    const vector = (values) => `(${values.map((value) => number.format(value)).join(separator)})`;

    function calculate(intervention) {
      const query = [1, 1];
      const keys = [[1, 1], intervention === "key" ? [1, 1] : [0, 0]];
      const values = [[2, 0], intervention === "value" ? [0, 8] : [0, 4]];
      const rawScores = keys.map((key) =>
        query.reduce((sum, coordinate, index) => sum + coordinate * key[index], 0),
      );
      const scaledScores = rawScores.map((score) => score / Math.sqrt(query.length));
      const maxScore = Math.max(...scaledScores);
      const exponentials = scaledScores.map((score) => Math.exp(score - maxScore));
      const normalizer = exponentials.reduce((sum, value) => sum + value, 0);
      const weights = exponentials.map((value) => value / normalizer);
      const contributions = values.map((value, index) =>
        value.map((coordinate) => weights[index] * coordinate),
      );

      const [first, second] = contributions;
      const output = first.map((coordinate, index) => coordinate + second[index]);
      return { keys, values, rawScores, scaledScores, weights, contributions, output };
    }

    const baseline = calculate("baseline");
    comparison.querySelector("[data-attention-before-weights]").textContent = vector(baseline.weights);
    comparison.querySelector("[data-attention-before-output]").textContent = vector(baseline.output);

    function update() {
      const result = select.value === "baseline" ? baseline : calculate(select.value);
      const { keys, values, rawScores, scaledScores, weights, contributions, output } = result;
      afterWeights.textContent = vector(weights);
      afterOutput.textContent = vector(output);

      for (const [index, position] of ["a", "b"].entries()) {
        const cells = {
          key: vector(keys[index]),
          raw: number.format(rawScores[index]),
          scaled: number.format(scaledScores[index]),
          weight: number.format(weights[index]),
          value: vector(values[index]),
          term: vector(contributions[index]),
        };
        for (const [row, text] of Object.entries(cells)) {
          root.querySelector(`[data-${position}="${row}"]`).textContent = text;
        }
      }
    }

    update();
    select.addEventListener("change", update);
    controls.hidden = false;
    comparison.hidden = false;
    root.querySelectorAll("[data-attention-static-summary]").forEach((item) => {
      item.hidden = true;
    });
  }

  document.querySelectorAll("[data-attention-intervention]").forEach(initialize);
})();
