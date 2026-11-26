# Audit — architecture computationnelle et tokenisation : documentation, utilité et exploitabilité

**Date :** 2026-11-26  
**Périmètre :** architecture computationnelle centrale et corpus tokenisation/embeddings  
**Nature :** audit documentaire et de cohérence fondé sur les fichiers de `main` et les issues référencées. Ce document ne remplace pas une revue exhaustive de chaque source, extraction ou page rendue.

## 1. Synthèse

Deux niveaux de maturité différents ressortent.

- **Architecture computationnelle :** le modèle central est formalisé et intégré dans des registres et projections distincts. Il ne faut pas le reconstruire. Les tâches restantes relèvent surtout de validation lecteur, d'accessibilité manuelle et de vérification ciblée.
- **Tokenisation :** le corpus est documenté et partiellement extrait. Le dossier de collection conserve toutefois un instantané dépassé. Le principal travail n'est pas de relancer les scans ni d'extraire toutes les sources, mais de fiabiliser les indicateurs, la traçabilité des items, le sous-graphe conceptuel et son raccordement aux pages/parcours.

L'objectif d'exploitabilité est de naviguer de façon traçable entre source, extraction, idée, concept, page et activité pédagogique, sans confondre ces entités ni inférer une relation à partir d'un simple tag ou d'une proximité éditoriale.

## 2. Architecture computationnelle

### 2.1 Décision canonique

Le modèle est un mécanisme prédictif conditionnel partagé, suivi de branches opérationnelles sœurs :

- génération : sélection d'un token, ajout au contexte, nouvelle prédiction avec paramètres inchangés ;
- scoring d'une cible observée : probabilité/log-probabilité de la cible ;
- évaluation : agrégation des scores sur des données tenues à l'écart, sans mise à jour des paramètres ;
- apprentissage : objectif NLL/cross-entropy, différentiation, gradients et mise à jour des paramètres.

Le graphe computationnel n'est ni le graphe conceptuel ni le parcours pédagogique. Les relations de calcul, les relations sémantiques, les prérequis et les correspondances d'implémentation ont des propriétaires distincts.

### 2.2 Correction structurelle essentielle

Les projections Q/K/V sont calculées à partir des états d'entrée de chaque bloc Transformer. Elles sont des opérations internes répétées dans les blocs et contribuent à produire les états contextualisés suivants ; elles ne viennent pas après des représentations contextualisées finales.

La documentation précise aussi que l'ordre exact résidus/normalisation dépend de l'architecture (Pre-LN/Post-LN) et ne doit pas être présenté comme universel.

### 2.3 État et limites de validation

Les sources canoniques présentes sur `main` sont :

- `docs/canonical-computational-spine.md` ;
- `data/computational-graph.yml` ;
- `data/guided-route.yml` et la documentation de curriculum ;
- les concepts dans `data/concepts.yml` ;
- les pages et vues bilingues générées à partir de ces données.

L'issue #575 consigne les intégrations principales (#577, #578, #581, #582, #586, #589, #593, #594, #596, #598, #600 et #601). L'issue #584 suit les validations lecteur restantes.

**Conclusion :** architecture utile, suffisamment formalisée et déjà exploitable comme référence. Ne pas créer un second graphe, une taxonomie générique ou une seconde navigation. Les contrôles manuels de fil d'Ariane et de lecteur d'écran ne sont pas démontrés par les seuls tests axe/Chromium ; ils restent suivis dans #584. Les tests de rendu ne démontrent pas à eux seuls la compréhension par des apprenants.

## 3. Corpus tokenisation/embeddings

### 3.1 Inventaire à retenir

Le relevé vérifié sur `main` consigné dans #1306 est daté du **21 novembre 2026** :

| Collection | Sources | Fichiers d'extraction | Items atomiques |
|---|---:|---:|---:|
| `tokenization-embeddings` | 32 | 7 | 35 |
| `qkv-attention` | 4 | 4 | 41 |
| `visual-learning-tools` | 6 | 0 | 0 |

Le relevé global associé indique 142 sources, 100 fichiers d'extraction et 520 items atomiques. Au relevé du 21 novembre, 44 sources avaient une décision de collection explicite (42 appartenances non vides et 2 listes explicitement vides) et 98 restaient indécises. Ces chiffres ne doivent pas être présentés comme un comptage au 26 novembre sans nouveau rapport.

Le dossier `docs/source-reviews/tokenization-embeddings-source-collection.md` porte encore un instantané du 19 novembre (139/96/489 et 25/0/0 pour tokenization-embeddings). Cet en-tête est périmé au regard du relevé ultérieur #1306 et doit être réconcilié.

### 3.2 Interprétation correcte

Un enregistrement source, un fichier d'extraction et un item atomique sont trois unités différentes. La présence d'une source au catalogue ne signifie ni qu'elle a été intégralement inspectée, ni qu'une extraction est nécessaire, ni qu'une affirmation de page est prouvée.

Les extractions doivent être jointes au catalogue par `extraction.source_id -> source.id -> source.collections`. Les appartenances ne doivent pas être inférées à partir des tags, thèmes, concept IDs, titres, noms de fichiers, citations ou proximité dans un dossier.

Le travail de couverture/provenance #1211 doit rester distinct du travail de décision d'appartenance aux collections #1306. Les 42 sources sans fichier d'extraction au relevé du 21 novembre constituent une file de triage source par source, pas un quota d'extractions. Le rapport de localisateurs connu dans #1211 porte encore sur 96 fichiers / 489 items ; il ne démontre donc pas la qualité des localisateurs des 100 fichiers / 520 items du relevé plus récent.

### 3.3 Valeur du corpus

La collection apporte une combinaison utile de ressources pédagogiques, documentation, implémentations et recherche expérimentale. Elle permet de traiter les algorithmes, les choix d'implémentation, les coûts et les disparités linguistiques, sans réduire la tokenisation à un tutoriel BPE.

Les distinctions à préserver comprennent notamment :

- BPE historique de compression, BPE sous-mots en NLP et byte-level BPE ;
- apprentissage du vocabulaire versus encodage d'un texte ;
- token, occurrence, chaîne de token et Token ID ;
- caractère Unicode, point de code et octet UTF-8 ;
- normalisation, pré-tokenisation, segmentation, post-traitement et décodage ;
- métriques de compression/fertilité versus qualité en aval ;
- observations expérimentales versus interprétation causale.

Les limites d'inspection de chaque source restent celles des dossiers de revue ; ce document ne rehausse pas une revue partielle en revue intégrale.

## 4. Modèle conceptuel et pages

### 4.1 Concepts candidats

Le registre `data/concepts.yml` possède déjà les concepts de token et de représentations/embeddings, mais la modélisation canonique de la famille tokenizer reste à examiner. Les candidats à arbitrer sont notamment :

- tokenizer, tokenisation, vocabulaire, Token ID ;
- normalisation et pré-tokenisation ;
- subword tokenization, BPE, WordPiece, Unigram ;
- token spécial, encodage/décodage ;
- entraînement et compatibilité du tokenizer ;
- offsets et fertilité des tokens ;
- évaluation et tokenisation multilingue.

Cette liste est un inventaire de candidats, pas une instruction de créer une entrée par terme. Chaque candidat doit être évalué : concept autonome, spécialisation, opération du graphe computationnel, attribut ou simple terme de vocabulaire.

### 4.2 Pipeline et parcours

Le pipeline pédagogique utile est : texte brut → normalisation éventuelle → pré-tokenisation éventuelle → segmentation selon le modèle et son vocabulaire → post-traitement/tokens spéciaux → Token IDs. L'apprentissage du tokenizer (construction du vocabulaire/règles) est un processus distinct de l'encodage d'un texte avec un tokenizer entraîné.

Plusieurs parcours peuvent être projetés sur les mêmes connaissances :
- comprendre les unités et la motivation de la tokenisation ;
- construire un tokenizer et inspecter chaque étape ;
- comparer BPE, WordPiece et Unigram ;
- évaluer les compromis de longueur, coût, couverture, robustesse et équité multilingue.

Le graphe de concepts doit exprimer les relations sémantiques ; le graphe computationnel, les opérations et données ; les parcours, un ordre pédagogique justifié. Aucun de ces graphes ne doit être forcé à devenir une séquence totale.

### 4.3 Responsabilité éditoriale des pages

Le découpage existant reste pertinent :
- `text-data` : passage du texte aux IDs et embeddings ;
- `tokenization-strategies` : mécanismes et familles de segmentation ;
- `tokenizer-design-evaluation` : compromis et résultats expérimentaux ;
- `corpus-preparation` : préparation documentaire et ajustement du tokenizer.

Il faut vérifier la couverture et les liens FR/EN, sans créer une page par algorithme ni déplacer toute l'analyse scientifique dans l'introduction.

## 5. Plan d'action et propriétaires

| Priorité | Action | Propriétaire / coordination |
|---|---|---|
| P0 | Réconcilier l'instantané du dossier tokenisation avec #1306 (21 nov.), en gardant les dates et périmètres explicites | #1319, avec #1306 |
| P0 | Mettre à jour l'audit des localisateurs pour les 100 fichiers / 520 items, ou publier un nouveau périmètre vérifié | #1211 |
| P1 | Auditer les 7 extractions de la collection : provenance, localisateurs, types d'idées, limites, claims et disposition d'intégration | #1319 et #1211 |
| P1 | Arbitrer les concepts candidats et construire le sous-graphe tokenisation avec relations typées, sans doublonner les opérations du graphe computationnel | #1319, en coordination avec #416 et #1233 |
| P1 | Vérifier le raccordement concepts ↔ pages FR/EN et les quatre responsabilités éditoriales | #1319, #114 |
| P2 | Dériver et vérifier les parcours Understand / Build / Deepen / Practice à partir des dépendances justifiées | #130, #225, #584 selon le périmètre |
| P2 | Valider l'expérience rendue, l'accessibilité manuelle et l'utilité auprès d'apprenants | #584 et issues éditoriales concernées |

## 6. Garde-fous

- Ne pas relancer des scans déjà effectués sans lacune de preuve précise.
- Ne pas extraire systématiquement toutes les sources ni chercher à augmenter artificiellement les compteurs.
- Ne pas créer un concept canonique par terme technique sans justification.
- Ne pas confondre source, claim, concept, nœud computationnel, page et activité.
- Ne pas déduire une relation de prérequis depuis l'ordre des pages ou une relation de preuve depuis une citation.
- Ne pas introduire de registre universel, de pipeline parallèle, de workflow par concept ou d'action CI supplémentaire.
- Préserver les ressources visuelles existantes ; les questions de droits suivent #156 et ne justifient aucune suppression unilatérale.
- Toute validation doit préciser son périmètre, son commit, ses commandes et ce qu'elle ne démontre pas.

## 7. Critères de clôture

L'audit tokenisation pourra être considéré comme opérationnel lorsque :
1. le dossier affiche un instantané cohérent avec le dernier rapport validé, daté et reproductible ;
2. les 7 extractions de la collection ont été examinées sans supposer que le nombre est un objectif ;
3. les concepts candidats ont une décision documentée (créer, fusionner, spécialiser, traiter comme opération/attribut ou différer) ;
4. le sous-graphe est validé et n'empiète pas sur le graphe computationnel ;
5. chaque concept retenu est relié aux pages FR/EN qui l'expliquent réellement ;
6. les parcours sont justifiés par les dépendances et les objectifs pédagogiques ;
7. les contrôles structurels, provenance, contenu, rendu et accessibilité sont rapportés séparément.

**Conclusion :** l'architecture computationnelle est une base stabilisée à exploiter ; la tokenisation constitue un pilote pertinent pour vérifier la continuité de la chaîne documentaire et conceptuelle. Le prochain gain de qualité vient de la réconciliation et de la traçabilité, pas d'une nouvelle architecture.
