(() => {
  "use strict";

  const explorer = document.querySelector("[data-temperature-explorer]");
  const table = document.querySelector(".probability-example table");
  if (!explorer || !table) return;

  const candidates = [...table.tBodies[0].rows].map(row => ({
    label: row.cells[0].textContent.trim(),
    logit: Math.log(Number(row.cells[2].textContent)),
  }));
  if (!candidates.length || candidates.some(candidate => !Number.isFinite(candidate.logit))) return;

  const locale = document.documentElement.lang;
  const percent = new Intl.NumberFormat(locale, { style: "percent", maximumFractionDigits: 1 });
  const temperature = new Intl.NumberFormat(locale, { maximumFractionDigits: 2 });
  const slider = explorer.querySelector("input[type=range]");
  const output = explorer.querySelector("output");
  const bars = explorer.querySelector("[data-temperature-bars]");

  const rows = candidates.map(({ label }) => {
    const row = document.createElement("div");
    row.className = "prob-bar-row";

    const name = document.createElement("span");
    name.className = "prob-bar-label text-break";
    name.textContent = label;

    const track = document.createElement("div");
    track.className = "prob-bar-track";
    track.setAttribute("aria-hidden", "true");
    const fill = document.createElement("div");
    fill.className = "prob-bar-fill";
    track.append(fill);

    const value = document.createElement("span");
    value.className = "prob-bar-value text-nowrap";
    row.append(name, track, value);
    bars.append(row);
    return { fill, value };
  });

  function render() {
    const tau = slider.valueAsNumber;
    const scaled = candidates.map(({ logit }) => logit / tau);
    const maximum = Math.max(...scaled);
    const exponentials = scaled.map(logit => Math.exp(logit - maximum));
    const total = exponentials.reduce((sum, value) => sum + value, 0);

    output.value = temperature.format(tau);
    slider.setAttribute("aria-valuetext", output.value);
    rows.forEach(({ fill, value }, index) => {
      const probability = exponentials[index] / total;
      fill.style.width = `${probability * 100}%`;
      value.textContent = percent.format(probability);
    });
  }

  slider.addEventListener("input", render);
  for (const preset of explorer.querySelectorAll("[data-temperature]")) {
    preset.addEventListener("click", () => {
      slider.value = preset.dataset.temperature;
      render();
    });
  }
  render();
  explorer.hidden = false;
})();
