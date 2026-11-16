# Théorie de l'information et LLM — synthèse documentaire

## Sources et périmètre
- Wayland Zhang, [Information Theory Is All You Need (to Understand LLMs)](https://waylandz.com/blog/information-theory-and-llm/), 17 février 2026 ; l'auteur indique une réécriture d'un texte du 27 mars 2025.
- [Dépôt des notebooks anglais et chinois](https://github.com/waylandzhang/information-theory-and-language-models).
- Xu et al. (2020), [A Theory of Usable Information Under Computational Constraints](https://arxiv.org/abs/2002.10689), notice et abstract consultés.

Le texte de l'article a été inspecté intégralement. Le notebook anglais a été inspecté statiquement dans ses 18 cellules, mais n'a pas été exécuté. Les figures n'ont pas été auditées comme fichiers image. Le papier V-information complet a été relu : définitions, propriétés, borne PAC, apprentissage de structure, expériences et discussion sur l'équité. Les expériences des auteurs n'ont pas été reproduites. L'audit du notebook a aussi identifié une visualisation qui appelle à tort « approximation de MI » une divergence KL ligne-par-ligne entre poids d'attention et distribution uniforme ; ce calcul n'est pas une information mutuelle.

## Synthèse des six contributions

| Partie | Valeur pédagogique | Vérification / limite | Décision LLM Lab |
|---|---|---|---|
| Information et entropie | Relie rareté, surprise et incertitude moyenne | Définitions standard ; préciser le contexte en prédiction autorégressive | Déjà couvert |
| Cross-entropy | Relie entraînement et théorie de l'information | (H(P,Q)=H(P)+D_{KL}(P\|Q)) est exact avec conventions cohérentes | Référencer la leçon existante |
| Attention et information mutuelle | Introduit les dépendances contextuelles | L'attention ne calcule pas la MI ; ses poids ne sont pas des bits ni une estimation de MI | Ajouter un garde-fou |
| Borne thermodynamique | Invite à réfléchir aux limites physiques | Landauer concerne l'effacement irréversible, pas une limite générale d'apprentissage | Corriger l'inférence |
| Compression et intelligence | Met en lumière le lien prédiction / longueur de code | L'efficacité de codage ne définit pas à elle seule l'intelligence | Qualifier le slogan |
| V-information | Cadre défini relativement à une famille de prédicteurs ; le papier ICLR 2020 complet a été audité | Les garanties PAC dépendent de la complexité et des hypothèses de perte bornée | Concept avancé optionnel ; distinct de MI |

## Distinctions essentielles

### Surprise, entropie, cross-entropy et KL

\[
I(x)=-\log_2p(x),\quad
H(P)=\mathbb E_{X\sim P}[-\log P(X)]
\]

\[
H(P,Q)=H(P)+D_{KL}(P\|Q).
\]

Dans un LLM autorégressif, chaque probabilité est conditionnelle au préfixe. Le NLL empirique estime un coût sous la distribution d'évaluation ; il ne révèle pas exactement l'entropie vraie de toute la langue.

### Attention et information mutuelle

\[
I(X;Y)=H(X)-H(X\mid Y).
\]

L'information mutuelle dépend d'une distribution jointe. Les poids d'attention dépendent des représentations, des projections Q/K, du masque et de l'entrée ; ils pondèrent l'agrégation des valeurs. L'analogie peut motiver une intuition de dépendance, mais les quantités ne sont pas interchangeables.

### Landauer et apprentissage

La relation (kT\ln2) exprime une borne de dissipation thermique par bit effacé dans un processus logiquement irréversible, sous les hypothèses physiques correspondantes. Elle ne démontre pas qu'un modèle ne peut apprendre aucune régularité absente sous forme d'exemple explicite dans son échantillon. L'inférence statistique dépend des hypothèses sur la distribution sous-jacente, du biais inductif, de la classe de modèles et du protocole d'évaluation.

### Compression et intelligence

Un meilleur modèle probabiliste peut réduire la longueur de code idéale attendue si le codeur et le décodeur partagent le même modèle et le même protocole. Cela ne prouve ni que les poids forment une archive du corpus, ni que générer équivaut à décompresser, ni que la compression résume toutes les dimensions de l'intelligence.

## Décisions d'intégration
- **Socle :** conserver les pages canoniques Entropie et Entropie croisée ; elles expliquent déjà les définitions et la décomposition KL.
- **Clarification :** expliciter que les poids d'attention ne sont pas l'information mutuelle.
- **Correction :** ne pas utiliser Landauer comme preuve d'une borne générale d'apprentissage.
- **Approfondissement :** intégrer `v-information` comme concept avancé optionnel après audit du papier primaire et une expérience XOR illustrative ; ne pas le confondre avec MI.
- **Expérimentation :** construire des expériences originales ; ne pas importer figures ou code du notebook sans audit de droits.

Le concept canonique avancé `v-information` est ajouté après audit complet du papier primaire ; il reste hors du parcours fondamental.

## Fiche et expériences
- [Fiche de révision](../revision-sheets/information-theory-and-llms-2026-11.md)
- [Expérience de compression prédictive](../../experiments/predictive-compression/README.fr.md)
- [Mini-expérience sur entropie, cross-entropy, KL et information mutuelle](../../experiments/information-theory-llm/README.fr.md).

## Expérience complémentaire : dépendance à la famille de prédicteurs

- [Expérience V-information (README anglais)](../../experiments/information-theory-llm/README.md)
- [Expérience V-information (README français)](../../experiments/information-theory-llm/README.fr.md)
- [Expérience séquences / entropie / zlib](../../experiments/sequence-compression/README.fr.md)

Sur une distribution XOR équilibrée, l'information mutuelle de Shannon vaut 1 bit. Une famille de prédicteurs constante ne gagne aucun bit avec l'entrée (V-information = 0), tandis qu'une famille autorisant un prédicteur sensible à l'interaction exploite une grande partie de cette prédictibilité. Le résultat dépend donc de la famille, conformément à la définition. Une seconde expérience compare H0, H1 et la taille zlib avec une graine fixe.

## Conclusion
L'article est utile comme carte conceptuelle, mais ne doit pas être adopté sans filtre. On conserve son pont entropie → cross-entropy → prédiction, on limite l'analogie attention/MI, on rejette l'inférence Landauer telle quelle, on qualifie le slogan compression/intelligence et on enseigne V-information comme notion avancée dépendante de la famille de prédicteurs.

Voir la [revue détaillée](../source-reviews/wayland-zhang-information-theory-llm-2026-11.md) et l'[extraction structurée](../../data/extractions/wayland-zhang-information-theory-llm-2026.yml).
