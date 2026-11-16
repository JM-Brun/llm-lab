# Fiche de révision — Théorie de l'information et LLM

**Niveau :** socle + ouverture avancée  
**Prérequis :** probabilités, logarithmes, prédiction du prochain token  
**Pages canoniques :** [Entropie](../../site/fr/entropy.qmd) · [Entropie croisée](../../site/fr/cross-entropy.qmd) · [Attention](../../site/fr/scaled-dot-product-attention.qmd)

## 1. Quatre quantités à distinguer

| Quantité | Définition | Question |
|---|---|---|
| Information propre (surprisal) | \\(I(x)=-\\log_2 p(x)\\) | Quelle surprise pour cet événement ? |
| Entropie | \\(H(P)=\\mathbb E_{X\\sim P}[-\\log P(X)]\\) | Quelle surprise moyenne sous P ? |
| Entropie croisée | \\(H(P,Q)=\\mathbb E_{X\\sim P}[-\\log Q(X)]\\) | Quel coût avec le modèle Q lorsque P produit les données ? |
| Divergence KL | \\(D_{KL}(P\\|Q)=\\mathbb E_P[\\log(P/Q)]\\) | Quel écart prédictif entre P et Q ? |

Identité centrale, avec les mêmes conventions de logarithme :

\\[
H(P,Q)=H(P)+D_{KL}(P\\|Q).
\\]

Pour un LLM autorégressif, la surprise du token observé est conditionnelle au préfixe :

\\[
I_t=-\\log_2 p_\\theta(x_t\\mid x_{<t}).
\\]

La somme des surprises donne la longueur idéale d'un code arithmétique adapté, à des conventions de codage près. Avec \\(\\log_2\\), les unités sont des bits ; avec le logarithme naturel, ce sont des nats.

## 2. Pourquoi l'entropie croisée intervient dans l'entraînement

Pour une distribution cible P fixée, \\(H(P)\\) ne dépend pas des paramètres du modèle Q. Minimiser \\(H(P,Q)\\) revient donc à minimiser \\(D_{KL}(P\\|Q)\\). En pratique, on minimise une approximation empirique sur un corpus et un protocole donnés : ce n'est pas une mesure exacte de l'entropie de toute la langue.

## 3. Attention et information mutuelle ne sont pas la même quantité

\\[
I(X;Y)=H(X)-H(X\\mid Y).
\\]

L'information mutuelle est définie à partir d'une distribution jointe. Les poids d'attention sont des coefficients d'agrégation dépendant de l'entrée, calculés à partir de représentations et de projections Q/K. Ils ne sont ni une estimation directe de l'information mutuelle, ni une quantité de bits apportée par un token.

## 4. Compression prédictive : le lien exact

- Un modèle qui attribue de meilleures probabilités aux séquences observées peut réduire leur longueur de code idéale.
- Pour une compression réellement décodable, encodeur et décodeur doivent partager le modèle, le tokenizer et les conventions de codage.
- Il faut compter le coût de stockage ou de transmission du modèle et les surcoûts du format.
- Les poids d'un modèle ne sont pas une archive littérale du corpus.
- « La compression est l'intelligence » est une thèse de recherche, pas une identité mathématique.

Ne pas confondre **compression prédictive des données**, **compression des paramètres du modèle** (quantification, élagage, distillation) et **mémoire de contexte à l'inférence**.

## 5. Deux précautions conceptuelles

**Principe de Landauer.** La borne \\(kT\\ln 2\\) concerne la dissipation minimale associée à l'effacement logique irréversible d'un bit, sous les hypothèses physiques correspondantes. Elle ne démontre pas une limite générale sur l'apprentissage ou la généralisation.

**V-information prédictive.** Cette notion avancée mesure un gain de prédictibilité relativement à une famille de prédicteurs \\(\\mathcal V\\). Elle ne signifie pas que le calcul crée de l'information de Shannon. Voir [Xu et al. (ICLR 2020)](https://openreview.net/forum?id=r1eBeyHFDH).

## 6. Deux expériences à savoir interpréter

### XOR et famille de prédicteurs

Deux bits équilibrés \\(X_1,X_2\\) déterminent \\(Y=X_1\\oplus X_2\\). L'information mutuelle de Shannon vaut 1 bit. Une famille limitée aux prédicteurs constants ne tire aucun gain de l'entrée : sa V-information vaut 0. Une famille capable de représenter l'interaction XOR exploite cette dépendance. Avec une probabilité correcte de 0,9 sur chaque exemple, le gain illustratif vaut :

\\[
1+\\log_2(0.9)\\approx 0.848\\text{ bit}.
\\]

C'est un exemple jouet sur une distribution finie, pas une reproduction de la borne PAC ni des expériences du papier.

### Dépendance séquentielle et zlib

Sur trois sources synthétiques de 20 000 symboles, la comparaison donne :

| Source | H0 (bits/symbole) | H1 (bits/symbole) | zlib (bits/symbole) |
|---|---:|---:|---:|
| Motif répété | 2,000 | 0,000 | 0,019 |
| Markov, P(rester)=0,9 | 1,997 | 0,634 | 0,872 |
| IID uniforme | 2,000 | 2,000 | 2,505 |

H0 ignore l'ordre ; H1 mesure les dépendances au pas précédent ; zlib mesure la taille d'un vrai flux compressé, avec ses surcoûts. Les valeurs zlib peuvent varier selon les versions de Python et zlib. Ce n'est pas un benchmark de LLM.

## 7. Mini-calculs

- Si \\(p=1/8\\), alors \\(I=-\\log_2(1/8)=3\\) bits.
- Si \\(p=1/2\\), alors \\(I=1\\) bit.
- Si le modèle Q égale P, alors \\(D_{KL}(P\\|Q)=0\\) et \\(H(P,Q)=H(P)\\).

## 8. Auto-évaluation

1. L'entropie est-elle la surprise d'un token particulier ?
2. Pourquoi l'entropie croisée est-elle au moins égale à l'entropie cible ?
3. Pourquoi les poids d'attention ne sont-ils pas l'information mutuelle ?
4. Que borne exactement le principe de Landauer ?
5. Pourquoi la V-information dépend-elle de la famille de prédicteurs ?
6. Pourquoi H1 distingue-t-elle les sources que H0 ne distingue pas ici ?
7. Quels coûts faut-il ajouter à une longueur de code idéale pour parler d'une compression réelle ?

<details>
<summary>Corrigé</summary>

1. Non. L'entropie est une moyenne ; le surprisal concerne un événement précis.
2. Parce que \\(H(P,Q)=H(P)+D_{KL}(P\\|Q)\\) et que la divergence KL est non négative.
3. Ce sont des coefficients d'agrégation calculés à partir de représentations, pas une statistique d'une distribution jointe.
4. La dissipation minimale liée à un effacement logiquement irréversible, pas une limite générale d'apprentissage.
5. Parce qu'elle compare les meilleures prédictions accessibles avec et sans information latérale dans cette classe.
6. H0 ne regarde que les fréquences marginales ; H1 prend en compte les transitions entre symboles successifs.
7. Le modèle partagé, le tokenizer, les conventions de codage, les métadonnées et le coût de stockage/transmission du modèle.

</details>

## 9. Ressources et approfondissement

- [Leçon canonique : entropie](../../site/fr/entropy.qmd)
- [Expérience V-information et théorie de l'information](../../experiments/information-theory-llm/README.fr.md)
- [Expérience séquences, entropie et zlib](../../experiments/sequence-compression/README.fr.md)
- [Synthèse documentaire](../source-syntheses/information-theory-and-llms-2026-11.md)
- [Revue critique de l'article et du notebook](../source-reviews/wayland-zhang-information-theory-llm-2026-11.md)
- [Article original](https://waylandz.com/blog/information-theory-and-llm/)
