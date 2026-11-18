# Audit du graphe de connaissances et du catalogue des sources — 18 novembre 2026

## Synthèse

L'ingestion récente a produit un enrichissement réel du graphe conceptuel et des parcours bilingues, mais la couverture de provenance reste hétérogène. Le risque principal n'est pas un graphe vide ou mal structuré : c'est qu'une partie des sources cataloguées ne dispose pas encore d'une extraction atomique, d'une inspection suffisamment complète ou d'une décision d'intégration explicite.

Cet audit est un état des lieux statique de la branche `main` au 18 novembre 2026. Les comptages ci-dessous ne remplacent pas l'exécution des validateurs, des tests et une revue scientifique des contenus.

## 1. État quantitatif observé

| Élément | Nombre |
|---|---:|
| Sources dans `data/sources.yml` | 124 |
| Extractions YAML dédiées (hors README) | 68 |
| Concepts canoniques | 102 |
| Nœuds du graphe computationnel | 72 |
| Sources sans fichier d'extraction dédié | 56 |

Métadonnées de sources :
- 44 sources ont une date de publication inconnue.
- 112 sources ont un statut de licence `unknown`.
- 119 sources sont marquées `partially-scanned`.
- Statuts d'intégration observés : 54 `integrated`, 43 `partially-integrated`, 17 `reviewed`, 8 `deferred`.

Les champs de classification `tags` et `concept_ids` sont présents dans les 124 fiches. Onze fiches ont cependant une liste `concept_ids` vide. Les tags ne doivent pas être confondus avec des concepts, des domaines ou des statuts.

## 2. Effet des ingestions récentes sur le graphe

### Compression, information et intelligence

Les concepts canoniques couvrent désormais notamment `surprisal`, `predictive-compression`, `minimum-description-length`, `entropy-coding`, `arithmetic-coding`, `kolmogorov-complexity`, `algorithmic-probability`, `solomonoff-induction`, `aixi`, `aixi-tl`, `free-energy-principle` et `active-inference`.

Des relations explicites relient ces notions, tout en maintenant des distinctions importantes : MDL n'est pas la simple compression d'un modèle ; compression prédictive et compression du modèle sont différentes ; FEP, inférence active et AIXI ne sont pas interchangeables.

L'extraction de Lewis Hemens documente notamment le coût de description du modèle et celui des données conditionnelles, les limites des résultats forward/reverse rapportés sur enwik8, et les extensions vers AIXI et l'inférence active. Les résultats empiriques non reproduits sont signalés comme tels.

Les deux vidéos 3Blue1Brown structurent une progression entre codage préfixe, surprisal, entropie, taux d'entropie, entropie croisée, perte de pré-entraînement et distillation. Les reconstructions pédagogiques indiquent explicitement leurs limites (transcriptions/captions, absence de revue audiovisuelle exhaustive).

### Vue d'ensemble des LLM

L'extraction Karpathy couvre le corpus, la tokenisation, le Transformer, la prédiction du prochain token, le pré-entraînement, le post-entraînement, l'inférence, le contexte, l'usage d'outils, les capacités et le RL. Le commit d'ingestion du 18 novembre a aussi réparé des identifiants et références bilingues mal formés avant de relier les pages d'aperçu FR/EN.

### Graphe computationnel

Le graphe computationnel est bien séparé du graphe conceptuel et des parcours d'apprentissage. Il distingue notamment génération, scoring d'une cible observée, évaluation et entraînement. Cette séparation est structurante et doit être conservée.

## 3. Qualité du catalogue et traçabilité

### Points solides
- Taxonomie contrôlée pour les types de sources, niveaux techniques, contributions, publics, états de scan/intégration et types d'extraction.
- Tags organisés par facettes et espaces de noms ; les concepts canoniques disposent de leurs propres identifiants.
- Les extractions peuvent préserver un graphe pédagogique local, des localisateurs précis, les limites de preuve et les éléments inférés.
- La politique de droits reste prudente : les ressources dont les licences ne sont pas établies restent en lien externe.
- Le commit du 18 novembre corrige explicitement les statuts d'intégration de Lewis et Hugging Face et relie Lewis au FEP et à l'inférence active.

### Lacunes à traiter
1. **Sources sans extraction dédiée (56)** : classifier chaque cas en référence bibliographique simple, ressource d'implémentation, source à extraire, source redondante/supersédée ou source à rejeter. Ne pas imposer une extraction lorsque le rôle documentaire ne le justifie pas.
2. **Dates inconnues (44)** : rechercher les dates sur les pages canoniques, pages d'éditeur, DOI/arXiv ou dépôts officiels ; garder `null` si la date n'est pas vérifiable et noter la limite dans l'historique d'inspection.
3. **Licences inconnues (112)** : distinguer licence du texte, des figures, du code et des données. Ne pas inférer une licence à partir de l'hébergeur ou du type de source.
4. **Scans partiels (119)** : vérifier si le statut reflète encore la dernière inspection ; compléter seulement les dimensions utiles (texte, figures, code/données, commentaires, références, métadonnées, droits). Ne jamais transformer une inspection partielle en scan complet sans preuve.
5. **Concepts vides (11 fiches)** : déterminer si la fiche est un simple pointeur bibliographique, ou si ses tags et pages associées masquent une contribution conceptuelle qui devrait être reliée.
6. **Lignée des preuves** : le modèle distribué décrit dans `docs/source-lineage-architecture.md` reste une architecture cible en migration staged. Ne pas créer de registre parallèle ; préserver `data/sources.yml` jusqu'à ce que le seuil de compatibilité et les validateurs soient satisfaits.
7. **Contrôle des références** : vérifier l'existence de chaque concept, page, domaine et fichier d'extraction référencé ; vérifier aussi que chaque extraction renvoie à une source unique et que les localisateurs identifient réellement le passage inspecté.

## 4. Plan de remédiation proposé

### P0 — intégrité et cohérence mécanique
- Exécuter les validateurs existants du catalogue, des extractions, des concepts, des pages et des graphes.
- Produire un rapport automatique des références orphelines, IDs inconnus, pages absentes, doublons d'identité et extractions sans source.
- Vérifier les 11 listes `concept_ids` vides et les 56 sources sans extraction.
- Contrôler la cohérence entre le dernier scan, le statut de scan résumé et le statut d'intégration.

### P1 — provenance et couverture
- Auditer les sources les plus récentes et les sources qui fondent les pages Understand/Build.
- Compléter les métadonnées vérifiables (dates, versions, révisions, créateurs, éditeurs, identifiants).
- Ajouter ou corriger les liens source → item d'extraction → concept/page/expérience, avec une relation typée et un élément probant précis lorsque le modèle de lignée le permet.
- Identifier explicitement les apports nouveaux, les corroborations indépendantes, les contradictions et les simples reformulations.

### P2 — lisibilité du graphe et exploitation pédagogique
- Vérifier que chaque source a une contribution clairement formulée et une décision d'intégration motivée.
- Distinguer les concepts canoniques, les résultats empiriques, les hypothèses, les analogies et les interprétations éditoriales.
- Faire apparaître les lacunes de couverture (concepts sans sources, sources sans destination, domaines sur/sous-documentés).
- Relier les connaissances retenues aux propriétaires pédagogiques canoniques et aux parcours sans créer de leçons concurrentes.

## 5. Coordination avec les travaux existants

Cet audit ne remplace pas :
- #1208 / #1209 : refonte du panorama LLM sans perte de contenu ;
- #1172 et #1150 : évaluation et inspection média de ressources sur compression et intelligence ;
- #1051 : intégration Microsoft Learn ;
- #1109 : contrat des fiches de synthèse ;
- #584 et #575 : colonne vertébrale computationnelle et distinction génération/scoring/entraînement ;
- #280 / #282 / #368 : convergence et organisation du corpus ;
- #130 : coordination de l'audit de conception pédagogique.

Les corrections de statuts déjà livrées par #1206 doivent être conservées ; ne pas rouvrir ce travail sans nouvel élément.

## 6. Critères de clôture

- [ ] Chaque source possède une décision explicite sur la nécessité d'une extraction.
- [ ] Les métadonnées inconnues sont soit complétées par preuve, soit explicitement laissées inconnues avec une limite documentée.
- [ ] Les tags respectent la taxonomie ; aucun tag ne duplique un concept, un domaine ou un statut.
- [ ] Les concepts et pages référencés existent ; les relations ont un sens explicite et une provenance vérifiable.
- [ ] Les sources et extractions distinguent faits, résultats rapportés, hypothèses, analogies et interprétations.
- [ ] Les graphes conceptuel et computationnel restent distincts et cohérents avec les pages canoniques.
- [ ] Les parcours Understand, Build, Deepen et Practice restent cohérents et bilingues.
- [ ] Les validateurs et tests pertinents passent ; les contrôles rendus et retours apprenants restent séparés des preuves CI.

## Limites de cet audit

Cet état des lieux repose sur la lecture statique des registres, d'un échantillon d'extractions et des commits/issues récents. Il ne prétend pas avoir exécuté localement les tests, reconstruit le site, inspecté les 124 sources externes ni vérifié les 68 extractions une par une. Les nombres sont un instantané de la branche consultée et devront être régénérés par les validateurs.
