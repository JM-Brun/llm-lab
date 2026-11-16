# Fiche de révision — Théorie de l'information et LLM

**Niveau :** socle + ouverture avancée  
**Prérequis :** probabilités, logarithmes, prédiction du prochain token  
**Pages canoniques :** [Entropie](../../site/fr/entropy.qmd) · [Entropie croisée](../../site/fr/cross-entropy.qmd) · [Attention](../../site/fr/scaled-dot-product-attention.qmd)

## 1. Quatre quantités à ne pas confondre

| Quantité | Formule | Question |
|---|---|---|
| Information propre | (I(x)=-\log_2p(x)) | Combien de bits représente cet événement ? |
| Entropie | (H(P)=-\sum_xP(x)\log P(x)) | Quelle est la surprise moyenne sous P ? |
| Entropie croisée | (H(P,Q)=-\sum_xP(x)\log Q(x)) | Quel coût obtient-on en codant P avec Q ? |
| Divergence KL | (D_{KL}(P\|Q)=\sum_xP(x)\log\frac{P(x)}{Q(x)}) | Quel écart sépare P et Q ? |

Identité centrale : (H(P,Q)=H(P)+D_{KL}(P\|Q)).

Pour un LLM autorégressif :
\[
I_t=-\log_2p_\theta(x_t\mid x_{<t}),\qquad L(x_{1:T})\approx\sum_t I_t.
\]

Le coût est en bits avec \(\log_2\), en nats avec le logarithme naturel.

## 2. Le lien avec l'entraînement

Minimiser l'entropie croisée revient à minimiser la divergence KL lorsque la distribution cible P est fixée, car H(P) ne dépend pas des paramètres de Q. Les mesures empiriques dépendent du corpus, du tokenizer et du protocole.

## 3. Attention et information mutuelle

(I(X;Y)=H(X)-H(X\mid Y)).

L'information mutuelle est une propriété d'une distribution jointe. Les poids d'attention sont des coefficients d'agrégation calculés à partir de représentations, de requêtes et de clés. Ils ne sont pas une estimation directe de l'information mutuelle ni une mesure en bits de l'information apportée par un token.

## 4. Compression : ce que l'on peut affirmer

- Un meilleur modèle prédictif peut réduire la longueur de code idéale attendue si un codeur entropique l'utilise.
- Il faut un codeur, un décodeur, le même modèle, le même tokenizer et les mêmes conventions.
- Il faut compter le coût de stockage/transmission du modèle.
- Les poids ne sont pas une archive littérale du corpus.
- « La compression est l'intelligence » est une thèse, pas une identité mathématique.

## 5. Deux pièges conceptuels

**Landauer :** (kT\ln2) concerne la dissipation minimale associée à l'effacement irréversible d'un bit. Cela ne prouve pas qu'un modèle ne peut pas généraliser au-delà des exemples littéralement vus.

**V-information :** notion avancée tenant compte de la famille de prédicteurs ou des contraintes computationnelles de l'observateur. Elle ne signifie pas que le calcul crée de l'information de Shannon. Voir [Xu et al. (2020)](https://arxiv.org/abs/2002.10689).

## 6. Mini-exemple

Si (p=1/8), alors (I=-\log_2(1/8)=3) bits. Si (p=1/2), le coût idéal est 1 bit. Un token plus prévisible coûte donc moins cher à encoder, à condition d'utiliser un protocole adapté.

## 7. Auto-évaluation

1. L'entropie est-elle la surprise d'un token particulier ?
2. Pourquoi (H(P,Q)\geq H(P)) ?
3. Les poids d'attention sont-ils des informations mutuelles ?
4. Que mesure exactement la borne de Landauer ?
5. Pourquoi une bonne compression ne suffit-elle pas à définir l'intelligence ?

<details>
<summary>Corrigé</summary>

1. Non : l'entropie est la surprise moyenne ; la surprise observée concerne un événement précis.
2. Parce que (H(P,Q)=H(P)+D_{KL}(P\|Q)) et que la KL est non négative.
3. Non : ce sont des coefficients d'agrégation.
4. Une limite physique de dissipation thermique lors d'un effacement logiquement irréversible.
5. La compression mesure une efficacité de représentation/prédiction, pas toutes les dimensions de l'intelligence.

</details>

## 8. Pour aller plus loin
- [Expérience prédictive](../../experiments/predictive-compression/README.fr.md)
- [Synthèse documentaire](../source-syntheses/information-theory-and-llms-2026-11.md)
- [Article original](https://waylandz.com/blog/information-theory-and-llm/)

## 9. V-information : l'information utilisable dépend de l'observateur

Xu et al. (ICLR 2020) définissent une quantité relative à une famille de prédicteurs \\(\\mathcal V\\) :

\\[
I_{\\mathcal V}(X\\to Y)=H_{\\mathcal V}(Y\\mid\\varnothing)-H_{\\mathcal V}(Y\\mid X).
\\]

Elle mesure le gain de prédictibilité obtenu grâce à l'entrée, pour cette famille et cette perte. Une famille restreinte peut ne pas exploiter une structure pourtant présente. La quantité est directionnelle en général. Avec une famille non restreinte, elle retrouve l'information mutuelle de Shannon.

**À ne pas confondre :** la violation apparente de l'inégalité de traitement des données concerne cette notion d'information utilisable sous contraintes, pas l'information mutuelle de Shannon. Le théorème PAC du papier dépend notamment d'une perte logarithmique bornée et de la complexité de la famille.

**Exemple XOR :** deux bits déterminent parfaitement leur XOR (1 bit d'information mutuelle), mais un prédicteur constant ne gagne rien à observer les bits. Un prédicteur capable de représenter leur interaction exploite presque toute cette information.

Référence : [Xu et al., *A Theory of Usable Information Under Computational Constraints*, ICLR 2020](https://openreview.net/forum?id=r1eBeyHFDH). Voir aussi l'[expérience V-information](../../experiments/information-theory-llm/README.fr.md) et l'[expérience H0/H1/zlib](../../experiments/sequence-compression/README.fr.md).
