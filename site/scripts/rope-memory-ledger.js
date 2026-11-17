(() => {
  "use strict";
  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const c = n => root.querySelector(`[data-control="${n}"]`);
    const o = n => root.querySelector(`[data-out="${n}"]`);
    const lang = root.dataset.lang;
    const fmt = n => n.toLocaleString(lang === "fr" ? "fr-FR" : "en-US", {maximumFractionDigits: 2});
    const mib = bytes => bytes / (1024 * 1024);
    function render() {
      const seq=+c("seq").value, fraction=+c("fraction").value/100, batch=+c("batch").value;
      const heads=+c("heads").value, dim=+c("dim").value, bytes=+c("bytes").value;
      const rotary=Math.max(2,Math.floor(dim*fraction/2)*2);
      const ropeBytes=2*seq*(rotary/2)*bytes;
      const kvBytes=2*batch*seq*heads*dim*bytes;
      ["seq","batch","heads","dim"].forEach(k=>o(k).textContent=c(k).value);
      o("fraction").textContent=c("fraction").value+"%";
      o("bytes").textContent=bytes+(lang==="fr"?" octets":" bytes");
      o("rope").textContent=fmt(mib(ropeBytes))+" MiB";
      o("kv").textContent=fmt(mib(kvBytes))+" MiB";
      o("ratio").textContent=fmt(kvBytes/ropeBytes)+"×";
      o("rotary").textContent=rotary+" / "+dim;
    }
    ["seq","fraction","batch","heads","dim","bytes"].forEach(k=>{c(k).addEventListener("input",render);c(k).addEventListener("change",render);});
    render();
  }
  function start(){document.querySelectorAll(".rope-memory-ledger").forEach(initialise);}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();
})();