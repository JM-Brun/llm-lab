# Réconciliation bibliographique ICL — 2026-11-27

## Objet

Réconcilier les références de `fr/in-context-learning` et `en/in-context-learning` avec le catalogue canonique `data/sources.yml`, sans confondre notice bibliographique, consultation d'une source et intégration pédagogique de ses résultats.

## Résultat de la vérification bibliographique

Six notices canoniques ont été ajoutées au catalogue :

| Identifiant canonique | Publication | Identifiant vérifié | Rôle documentaire |
|---|---|---|---|
| `brown-et-al-gpt3-few-shot-2020` | NeurIPS 2020 | arXiv:2005.14165 | Démonstration de la capacité few-shot de GPT-3 sans mise à jour de gradient |
| `olsson-et-al-induction-heads-2022` | Transformer Circuits Thread, 2022 | arXiv:2209.11895 | Hypothèse mécaniste des induction heads |
| `xie-et-al-implicit-bayesian-icl-2022` | ICLR 2022 | arXiv:2111.02080 | Explication théorique par inférence bayésienne implicite dans un cadre de préentraînement spécifié |
| `min-et-al-demonstrations-icl-2022` | EMNLP 2022 | DOI:10.18653/v1/2022.emnlp-main.759 | Étude du rôle des démonstrations et de leurs composantes |
| `yoo-et-al-ground-truth-labels-icl-2022` | EMNLP 2022 | DOI:10.18653/v1/2022.emnlp-main.155 | Réexamen de l'effet des associations entrée-étiquette correctes |
| `xiang-et-al-order-sensitivity-icl-2024` | Findings of ACL 2024 | DOI:10.18653/v1/2024.findings-acl.386 | Approfondissement sur la sensibilité à l'ordre des démonstrations |

Les métadonnées ont été recoupées avec les pages de publication officielles NeurIPS, Transformer Circuits, OpenReview/arXiv et ACL Anthology.

## Décisions de modélisation

- Une notice unique par publication, partagée entre les versions française et anglaise.
- Identifiants pérennes : arXiv pour les prépublications concernées, DOI pour les actes ACL.
- `related.pages` associe les six sources aux deux pages ICL ; `related.concepts` réutilise les concepts déjà existants.
- Aucun nouveau concept canonique n'est créé pour les induction heads, la correction des labels ou l'ordre des démonstrations.
- Les six sources restent `scan_status: partially-scanned`. Min, Yoo, Olsson et Xie sont `integration_status: partially-integrated` après revue ciblée et ajout de contenu FR/EN ; Brown reste différé au-delà de sa référence bibliographique et Xiang reste une ressource d'approfondissement.
- Les licences restent inconnues et les contenus/figures sont link-only tant que les droits ne sont pas vérifiés.
- Aucun statut `integrated` n'est attribué sur la seule base d'une citation dans une bibliographie.

## Lecture pédagogique à préserver

Les résumés officiels montrent que Min et al. (2022) et Yoo et al. (2022) étudient tous deux l'effet des démonstrations et des associations entrée-étiquette, mais que Yoo et al. réexaminent explicitement les résultats antérieurs avec d'autres métriques et configurations expérimentales. Il serait incorrect de réduire ces résultats à une règle générale du type « les labels corrects ne comptent pas » ou à l'affirmation inverse « ils sont toujours nécessaires ». Une synthèse claim-level exige la lecture des protocoles, des métriques, des résultats par tâche/modèle et des limites des deux articles.

Olsson et al. (2022) propose une hypothèse mécaniste sur les induction heads. Le niveau de preuve doit rester explicite : les auteurs rapportent des éléments causaux plus forts dans les petits modèles attention-only et des éléments plus indirects/corrélationnels pour les grands modèles avec MLP. Cette source ne justifie pas d'enseigner que les induction heads expliquent à elles seules tout ICL dans tous les LLM.

Xie et al. (2022) fournit une explication théorique par inférence bayésienne implicite, dans un cadre formalisé de préentraînement à mélange de HMM. Ne pas la présenter comme une description universelle et démontrée du mécanisme de tout modèle entraîné sur des corpus naturels.

Xiang et al. (2024) reste une ressource d'approfondissement sur l'ordre des démonstrations. Son résumé rapporte une sensibilité différente entre les modèles causaux et prefix-LM évalués ; les limites de cette comparaison devront être reprises à partir du protocole complet avant toute généralisation.

## Revue ciblée des articles Min et Yoo

Une lecture ciblée des sections principales et figures pertinentes des deux PDF publiés a été effectuée le 2026-11-27. Les extractions atomiques correspondantes sont :

- `data/extractions/min-et-al-demonstrations-icl-2022.yml`
- `data/extractions/yoo-et-al-ground-truth-labels-icl-2022.yml`

### Min et al. (2022) — quatre composantes des démonstrations

Le protocole couvre des tâches de classification et de choix multiple sur 26 jeux de données, avec 12 modèles ; le nombre de tâches varie selon les modèles, les modèles les plus grands étant évalués sur un sous-ensemble plus réduit. Le réglage par défaut utilise 16 démonstrations et plusieurs graines d'échantillonnage.

Les auteurs distinguent quatre composantes :
1. la distribution des textes d'entrée ;
2. l'espace des étiquettes ;
3. la correspondance entrée-étiquette ;
4. le format des paires entrée-étiquette.

Dans les configurations testées, le remplacement des étiquettes correctes par des étiquettes aléatoires réduit souvent peu la performance agrégée. Les ablations indiquent cependant que la distribution des entrées, l'espace des étiquettes et le format apportent eux aussi du signal. Les modèles MetaICL, entraînés explicitement avec un objectif d'ICL, accentuent encore certains de ces effets.

**Limites déterminantes :** les résultats sont agrégés sur des benchmarks de classification et de choix multiple, ne couvrent pas la génération ouverte et masquent des différences entre couples tâche-modèle. Les auteurs signalent eux-mêmes des cas avec un écart plus marqué entre étiquettes correctes et aléatoires.

### Yoo et al. (2022) — sensibilité à la correction des étiquettes

Yoo et al. réexaminent les conclusions de Min et al. avec d'autres configurations. Ils montrent que des variations raisonnables de méthode d'inférence, de métrique et de sous-ensemble de jeux de données peuvent modifier fortement l'effet mesuré. Leur comparaison initiale oppose notamment une configuration Noisy Channel / macro-F1 / sous-ensemble de classification à une configuration Direct / accuracy / ensemble plus large.

Ils proposent deux mesures :
- **Label-Correctness Sensitivity** : pente de la régression linéaire de la performance sur la proportion d'étiquettes correctes ;
- **Ground-Truth Label Effect Ratio (GLER)** : rapport entre le gain des étiquettes correctes sur les étiquettes aléatoires et le gain des étiquettes correctes sur le baseline sans démonstration, borné dans l'intervalle [0, 1].

Leurs analyses montrent que la correction des associations entrée-étiquette peut avoir un effet important dans certains cas. Cet effet varie avec le jeu de données, la méthode d'inférence, la métrique, la taille du modèle et la formulation du template. Un template plus détaillé peut réduire la sensibilité aux labels tout en préservant la performance. La sensibilité seule peut cependant être trompeuse sur une tâche que le modèle ne sait pas résoudre.

**Limites déterminantes :** les résultats restent sensibles au choix du prompt ; les composantes d'une démonstration sont difficiles à isoler ; la distribution des labels peut introduire des effets confondants.

### Synthèse et intégration dans les pages

Ces articles ne doivent pas être résumés par deux slogans opposés. Min et al. montrent que, dans leurs tâches et configurations, une partie importante du signal des démonstrations vient de la distribution des entrées, de l'espace des labels et du format. Yoo et al. montrent que la correspondance correcte reste déterminante dans certaines configurations et que l'effet dépend du protocole.

La synthèse pédagogique retenue est donc : **une démonstration est multicomposante ; l'effet de la correction des labels est conditionnel au modèle, à la tâche et au protocole.** Les deux pages FR/EN présentent maintenant les quatre composantes dans un tableau et explicitent les conditions de comparaison. La formulation évite de conclure que les labels corrects sont toujours inutiles ou toujours indispensables.

Les notices Min et Yoo passent à `integration_status: partially-integrated`. Les sources restent `scan_status: partially-scanned`, car cette lecture ciblée n'est pas une revue exhaustive de toutes les sections, annexes et détails d'implémentation. Les extractions conservent les localisateurs, niveaux de confiance et limites.

### Anomalie bibliographique à conserver visible

La première page du PDF Min et al. écrit le nom du deuxième auteur « Xinyi Lyu », tandis que la notice ACL Anthology, sa page auteur et le dépôt de code indiquent « Xinxi Lyu ». La notice canonique conserve provisoirement la forme de l'ACL Anthology, sans masquer cette divergence. Une correction définitive nécessite une confirmation bibliographique indépendante.

## Revue ciblée d'Olsson et Xie

### Olsson et al. (2022) — induction heads et force des preuves

La revue de la publication Transformer Circuits distingue explicitement trois niveaux de preuve :

- **Petits Transformers attention-only :** preuves mécanistes et causales fortes. Les auteurs combinent l'analyse du circuit à deux têtes, la coïncidence avec une transition de phase pendant l'entraînement, des perturbations architecturales et des ablations directes.
- **Petits modèles avec MLP :** certaines preuves causales subsistent, mais les interactions entre attention et MLP rendent les ablations plus difficiles à interpréter.
- **Modèles de grande taille avec MLP :** les preuves que les induction heads expliquent la majorité de l'ICL sont surtout indirectes et corrélationnelles. Les auteurs n'ont pas réalisé d'ablations complètes des têtes sur leurs modèles pleine échelle et signalent des hypothèses alternatives, notamment d'autres mécanismes de composition.

La page ne présente donc plus les induction heads comme une explication générale. Elle indique le circuit de copie étudié et sépare explicitement la force des preuves selon la famille de modèles. L'extraction est dans `data/extractions/olsson-et-al-induction-heads-2022.yml`.

### Xie et al. (2022) — cadre théorique bayésien

La revue du PDF ICLR 2022 confirme un cadre théorique où les documents de préentraînement sont générés sous un mélange de HMM indexés par un concept latent. Les exemples d'un prompt partagent un concept `θ*` ; le modèle peut l'inférer implicitement et marginaliser les concepts possibles pour produire une distribution prédictive.

Le résultat formel dépend d'hypothèses explicites : adéquation du modèle à la distribution de préentraînement, concept du prompt appartenant à la famille considérée, propriétés des délimiteurs, contrôle du décalage entre distribution de préentraînement et distribution des prompts, et condition de distinguabilité formulée à l'aide de divergences KL. Le papier montre également que la longueur des exemples peut apporter un signal supplémentaire.

Les expériences GINC contrôlent un mélange synthétique de HMM ; elles montrent des comportements ICL dans des Transformers et des LSTMs, mais ne démontrent pas que tout LLM sur corpus naturel applique universellement cette explication bayésienne. Les auteurs observent aussi des échecs d'extrapolation vers des concepts absents de la famille de préentraînement.

Un encadré facultatif a été ajouté aux deux pages pour présenter ce cadre comme une explication théorique conditionnelle, distincte des induction heads qui relèvent de l'interprétabilité mécaniste. L'extraction est dans `data/extractions/xie-et-al-implicit-bayesian-icl-2022.yml`.

Les notices Olsson et Xie passent à `integration_status: partially-integrated`. Leurs statuts de scan restent partiels : les sections pertinentes ont été étudiées, mais les annexes et tous les détails expérimentaux n'ont pas été audités exhaustivement.

## Limites de cette passe d'ingestion

Cette passe combine la vérification bibliographique des six notices et une lecture ciblée des sections pertinentes des publications Min, Yoo, Olsson et Xie. Quatre extractions atomiques evidence-linked ont été créées. Aucun résultat expérimental n'a été reproduit ; les annexes et détails d'implémentation n'ont pas été audités exhaustivement.

Min, Yoo, Olsson et Xie sont partiellement intégrés aux pages FR/EN. Xiang reste une ressource facultative d'approfondissement ; son protocole complet doit encore être étudié.

## Sources de vérification

- Brown et al., [NeurIPS 2020 proceedings](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) et [arXiv:2005.14165](https://arxiv.org/abs/2005.14165).
- Olsson et al., [Transformer Circuits Thread](https://www.transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) et [arXiv:2209.11895](https://arxiv.org/abs/2209.11895).
- Xie et al., [OpenReview — ICLR 2022](https://openreview.net/forum?id=RdJVFCHjUMI) et [arXiv:2111.02080](https://arxiv.org/abs/2111.02080).
- Min et al., [ACL Anthology — EMNLP 2022](https://aclanthology.org/2022.emnlp-main.759/).
- Yoo et al., [ACL Anthology — EMNLP 2022](https://aclanthology.org/2022.emnlp-main.155/).
- Xiang et al., [ACL Anthology — Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.386/).
