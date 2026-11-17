(() => {
  "use strict";
  const patterns = {
    ramp: [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6],
    alternating: [-1,1,-1,1,-1,1,-1,1],
    constant: [1,1,1,1,1,1,1,1]
  };
  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";
    const c=n=>root.querySelector(`[data-control="${n}"]`);
    const o=n=>root.querySelector(`[data-out="${n}"]`);
    const lang=root.dataset.lang;
    const fmt=x=>x.toLocaleString(lang==="fr"?"fr-FR":"en-US",{maximumFractionDigits:3});
    const strip=root.querySelector("[data-token-strip]");
    const weights=root.querySelector("[data-weight-list]");
    const explanation=root.querySelector("[data-explanation]");
    function render(){
      const pos=+c("position").value, vals=patterns[c("pattern").value];
      const mode=c("attention").value, temp=+c("temperature").value;
      const count=pos+1, q=vals[pos];
      const scores=vals.slice(0,count).map(v=>mode==="uniform"?0:(q*v)/temp);
      const max=Math.max(...scores);
      const exps=scores.map(s=>Math.exp(s-max));
      const sum=exps.reduce((a,b)=>a+b,0);
      const ws=exps.map(x=>x/sum);
      const aggregate=ws.reduce((a,w,i)=>a+w*vals[i],0);
      const entropy=-ws.reduce((a,w)=>a+(w>0?w*Math.log(w):0),0);
      o("position").textContent=pos;
      o("temperature").textContent=fmt(temp);
      o("visible").textContent=count+" / 8";
      o("aggregate").textContent=fmt(aggregate);
      o("entropy").textContent=fmt(entropy)+" nats";
      strip.replaceChildren(); weights.replaceChildren();
      vals.forEach((v,i)=>{
        const el=document.createElement("span");
        el.className="nope-token"+(i<=pos?" is-visible":" is-masked");
        el.textContent=(lang==="fr"?"p":"p")+i+" · "+fmt(v);
        el.setAttribute("aria-label",lang==="fr"?`Position ${i}, valeur ${fmt(v)}, ${i<=pos?"visible":"masquée"}`:`Position ${i}, value ${fmt(v)}, ${i<=pos?"visible":"masked"}`);
        strip.appendChild(el);
        if(i<=pos){
          const row=document.createElement("div");row.className="nope-weight-row";
          const label=document.createElement("span");label.textContent=`p${i}`;
          const track=document.createElement("span");track.className="nope-weight-track";
          const bar=document.createElement("span");bar.className="nope-weight-bar";bar.style.width=(ws[i]*100)+"%";track.appendChild(bar);
          const value=document.createElement("output");value.textContent=fmt(ws[i]);
          row.append(label,track,value);weights.appendChild(row);
        }
      });
      const messages={
        fr:{
          uniform:`Chaque clé du préfixe reçoit le même poids (1/${count}). La sortie est la moyenne des valeurs visibles : elle peut changer avec la longueur du préfixe, mais ce n’est pas une coordonnée de position universelle.`,
          content:"Les scores sont ici le produit scalaire scalaire qᵢ·kⱼ, avec qᵢ et kⱼ représentés par les valeurs jouets, puis softmax. Le contenu influence les poids ; le masque causal, lui, détermine toujours quelles clés existent dans le calcul.",
          constant:"Contre-exemple : les contenus sont tous identiques. Même si le nombre de clés visibles augmente, la sortie agrégée reste identique. La visibilité emboîtée ne garantit donc pas un signal exploitable dans chaque contenu."
        },
        en:{
          uniform:`Every key in the prefix receives equal weight (1/${count}). The output is the mean of visible values: it may change with prefix length, but it is not a universal positional coordinate.`,
          content:"Scores here are scalar qᵢ·kⱼ products, with qᵢ and kⱼ represented by toy values, followed by softmax. Content influences weights; the causal mask still determines which keys enter the computation.",
          constant:"Counterexample: all content values are identical. Even as the number of visible keys grows, the aggregated output stays the same. Nested visibility therefore does not guarantee an exploitable signal for every content sequence."
        }
      };
      explanation.textContent=c("pattern").value==="constant"?messages[lang].constant:messages[lang][mode];
    }
    ["position","pattern","attention","temperature"].forEach(k=>{c(k).addEventListener("input",render);c(k).addEventListener("change",render);});
    render();
  }
  function start(){document.querySelectorAll(".nope-prefix-experiment").forEach(initialise);}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();
})();