# Transfert des pratiques de gestion des connaissances de Society Lab vers LLM Lab

**Date :** 2026-11-18  
**Statut :** analyse comparative et recommandations ; aucune migration ni implémentation technique n'est déclarée achevée.  
**Périmètre :** sources, ingestion, métadonnées, extraction, provenance, concepts, relations, graphes, synthèse, validation et passage à l'échelle.

## 1. Synthèse exécutive

Society Lab et LLM Lab partagent des exigences de gestion rigoureuse des connaissances, mais leurs modèles métier sont différents.

- **Society Lab** organise et confronte des connaissances scientifiques, économiques, sociales et politiques : sources, études, jeux de données, affirmations, hypothèses, concepts, mécanismes, méthodes, analyses et dossiers.
- **LLM Lab** construit une compréhension technique et pédagogique des modèles de langage : sources, versions, inspections, extractions, concepts, formalismes, algorithmes, implémentations, tests, expériences, résultats, pages, exercices et parcours.

Le transfert pertinent porte donc sur les **principes de gouvernance**, pas sur la copie des schémas. LLM Lab possède déjà une architecture documentaire avancée : registres canoniques distincts, concepts bilingues, ressources, provenance des sources, extractions, graphes et parcours pédagogiques. La priorité est de consolider cette architecture, de réduire l'écart entre contrats et données réelles et de rendre les contrôles plus systématiques. Il ne faut créer ni second pipeline, ni deuxième ontologie, ni graphe concurrent.

**Décision recommandée :** adopter les pratiques de traçabilité, de mémoire des décisions, de validation des relations et de gestion explicite des inconnues ; conserver les objets, vocabulaires et propriétaires propres à LLM Lab.

## 2. Périmètre et méthode

Cette comparaison est une analyse documentaire fondée sur les contrats et audits disponibles dans les deux dépôts au 18 novembre 2026. Pour LLM Lab, elle confronte notamment le README, l'architecture informationnelle, l'architecture de provenance, l'audit transversal, le workflow d'intégration, le protocole de validation, le schéma du catalogue et la roadmap. Pour Society Lab, elle s'appuie sur les documents d'architecture, métadonnées, ingestion, graphe, types de relations et audit du pipeline.

Ce n'est pas un audit exhaustif ligne par ligne, une exécution locale de tous les validateurs ou une vérification indépendante de chaque enregistrement. Les statistiques Society Lab citées plus bas sont celles rapportées par son audit, non des mesures de LLM Lab.

## 3. Architecture LLM Lab à préserver

Le principe architectural actuel est : **une source canonique par type d'information, puis des vues dérivées**.

| Objet | Propriétaire canonique | Rôle |
|---|---|---|
| Contenu pédagogique | `site/**/*.qmd` | Explications, exemples, équations et références |
| Identité et métadonnées des pages | Bloc `LLM-LAB-PAGE-MAP`, schéma page | Identité et relations éditoriales |
| Catalogue des sources | `data/sources.yml`, migration distribuée spécifiée | Identité bibliographique et facettes |
| Historique d'inspection | `scan_history`, cible `data/source-scans/` | Événements d'inspection append-only |
| Provenance | Cible `data/source-lineage/` | Relations directionnelles source-artifact |
| Extractions | `data/extractions/` | Items atomiques localisés et disposition éditoriale |
| Domaines | `data/domains.yml` | Familles de connaissances contrôlées |
| Concepts | `data/concepts.yml` | Entités stables, bilingues et relations sémantiques |
| Ressources non-page | `data/resources.yml` | Artefacts réutilisables identifiés |
| Parcours guidé | `data/guided-route.yml` | Progression de lecture, non ontologie |
| Graphe historique | `data/history-pilot.yml` | Événements et relations historiques spécialisés |
| Projections | Générateurs et données dérivées | Cartes et vues de consultation |

Les distinctions structurantes sont essentielles :

1. Une page n'est pas un concept ; un titre de section n'est pas un nœud d'ontologie.
2. Un tag est une facette de recherche, pas une relation sémantique.
3. Une source, une inspection, une extraction, un concept et une ressource ont des identités et cycles de vie distincts.
4. Une citation bibliographique n'est pas une corroboration indépendante.
5. Le graphe local reconstruit d'une source n'est pas le graphe conceptuel canonique.
6. Le graphe de pages, le graphe conceptuel et le parcours pédagogique ont des sémantiques différentes.
7. Les graphes lecteur sont des projections, pas des sources d'édition concurrentes.

L'architecture cible de provenance est déjà spécifiée sous forme distribuée par source : identité, événements d'inspection, relations de lineage et extractions, avec index global généré. Cette migration ne doit pas être déclarée achevée avant les gates de compatibilité, de migration des consommateurs et de CI.

## 4. Apports transférables de Society Lab

### 4.1 Typage explicite des objets

Society Lab distingue notamment SOURCE, STUDY, DATASET, CLAIM, HYPOTHESIS, CONCEPT, MECHANISM, METHOD, ANALYSIS, DOSSIER et DOMAIN. Il faut retenir le principe, pas importer les types tels quels.

Pour LLM Lab, les objets pertinents comprennent source, version, inspection, item d'extraction, concept, définition, équation/formalisme, algorithme, implémentation, test, expérience, résultat, page pédagogique, exercice et ressource.

Ne pas transformer automatiquement une phrase extraite en concept, un exemple en preuve, un test logiciel en validation scientifique ou une page en entité théorique.

### 4.2 Métadonnées typées et inconnues explicites

Les métadonnées doivent être minimales, typées et propres à l'objet. Identifiants, versions, dates, langue, domaines, licences, références et statuts ne doivent pas être mélangés dans des tags libres.

Une valeur inconnue doit rester inconnue. Une URL publique ne prouve pas une licence ; une date de consultation ne prouve pas une date de publication ; la mention d'une expérience ne prouve pas sa reproduction.

La piste la plus utile, déjà identifiée dans LLM Lab, est une provenance ciblée champ par champ pour les métadonnées sensibles ou volatiles (dates, versions, droits/licences, identité du créateur) : valeur, locator/preuve, date et méthode de vérification, statut (déclaré, vérifié, inféré, inconnu). Ne pas imposer cette enveloppe à chaque champ trivial.

### 4.3 Ingestion comme processus auditable

Rendre visibles les décisions et transitions :
1. découverte et cadrage par une question ;
2. déduplication par DOI, URL canonique, dépôt/révision ou autre identifiant durable ;
3. qualification de la source et du rôle attendu ;
4. inspection avec périmètre, version, méthode d'accès et limites ;
5. extraction d'items atomiques avec locateurs vérifiables ;
6. synthèse et mise en relation sans inférer depuis la seule proximité ;
7. revue, validation et disposition éditoriale ;
8. intégration aux registres canoniques et aux pages ;
9. contrôles de rendu, parité FR/EN, liens, CI et maintenance.

Distinguer les états de sélection, accès, inspection, extraction et intégration. Un statut global unique masque les dimensions incomplètes.

### 4.4 Manifestes de lots et mémoire des décisions

Pour une campagne multi-sources, un manifeste léger peut conserver : identifiant du lot, question/requête, critères d'inclusion/exclusion, candidats, décisions, doublons, raisons, responsable et état de clôture.

Décisions possibles : sélectionné, doublon, exclu, différé, inaccessible. Conserver les rejets/reportés lorsqu'ils sont susceptibles d'être réexaminés ou expliquent une décision importante ; ne pas enregistrer chaque URL découverte.

La mémoire des décisions relie ancienne et nouvelle formulation, motif, preuves, objets/pages affectés, contrôles réalisés et actions de retrait/conservation. Elle évite de perdre le raisonnement derrière les évolutions de schéma, de concepts et de synthèses.

### 4.5 Relations typées, directionnelles et justifiées

Les relations doivent porter une sémantique explicite, un sens, une justification, une portée et, lorsqu'elles sont probantes, un locator. Il faut distinguer les relations conceptuelles, documentaires, pédagogiques et expérimentales.

Exemples de distinctions utiles (noms indicatifs, pas une demande d'ajout immédiat au schéma) :

- `DEFINES` : définit un concept dans un périmètre donné ;
- `FORMALIZES` : formalise mathématiquement ;
- `DERIVES_FROM` : découle d'une dérivation explicite ;
- `IMPLEMENTS` : implémente une méthode ;
- `USES` : utilise une méthode ou un artefact ;
- `TESTS` : vérifie un comportement logiciel défini ;
- `VALIDATES` : apporte une validation selon un protocole et un périmètre ;
- `ILLUSTRATES` : illustre sans valider ;
- `PREREQUISITE_OF` : dépendance pédagogique ou technique justifiée ;
- `CONTRADICTS`, `EXTENDS`, `CITES` : relations à définir précisément.

Les vocabulaires existants restent la référence jusqu'à une décision explicite. Ne pas imposer un DAG au graphe entier : les contraintes de cycle dépendent de la relation. Une citation n'est pas une corroboration indépendante ; `ILLUSTRATES`, `TESTS` et `VALIDATES` ne sont pas interchangeables.

### 4.6 Validation structurelle distincte de la validation scientifique

Les validateurs peuvent contrôler schémas, références, IDs, relations, justifications, doublons et projections. Ils ne prouvent pas à eux seuls la vérité scientifique, l'indépendance des sources ou la compréhension d'un apprenant.

Conserver des niveaux distincts :
- validité structurelle et intégrité référentielle ;
- qualité et localisation de la preuve documentaire ;
- correction mathématique/algorithmique ;
- comportement logiciel testé ;
- résultat expérimental reproductible ;
- qualité pédagogique et transfert de compréhension.

Un statut `validated` doit être interprété relativement au type d'objet et au protocole, jamais comme un score universel de vérité.

## 5. Quatre vues analytiques, un même système canonique

On peut distinguer quatre dimensions fonctionnelles sans créer quatre bases indépendantes :

| Vue | Objets et relations | Question |
|---|---|---|
| Scientifique et conceptuelle | Concepts, définitions, formalismes, relations sémantiques | Quels objets théoriques sont liés, et comment ? |
| Sources et preuves | Sources, versions, inspections, extractions, locateurs, lineage | D'où vient cette affirmation ? |
| Implémentations et expériences | Code, algorithmes, tests, configurations, résultats | Comment l'idée est-elle réalisée et éprouvée ? |
| Pédagogique | Pages, ressources, exercices, parcours, prérequis | Comment construire la compréhension ? |

Ce sont des **projections complémentaires sur des objets canoniques communs**. Elles se croisent par des IDs stables et des liens typés, sans recopier les définitions. Une proximité visuelle, un lien de navigation ou des tags communs ne prouvent jamais une relation scientifique.

## 5 bis. Inventaire complet des graphes et structures reliées

Les quatre vues du tableau précédent sont des **familles analytiques**, pas un inventaire exhaustif. Le dépôt contient plusieurs graphes, modèles et projections dont les vocabulaires et finalités doivent rester distincts. L'inventaire opérationnel à prendre comme contrat de compatibilité est le suivant :

| Structure | Propriétaire canonique | Sémantique à préserver |
|---|---|---|
| Graphe conceptuel | `data/concepts.yml` + `data/domains.yml` | Concepts canoniques bilingues, relations sémantiques typées et appartenance multi-domaines |
| Graphe computationnel | `data/computational-graph.yml` | Nœuds data/opération/contrôle/politique, flux typés, branches opérationnelles, boucles et retours explicites |
| Graphe de pages/navigation | Blocs `LLM-LAB-PAGE-MAP` | Hiérarchie éditoriale, liens associés et navigation locale |
| Parcours Understand | `data/guided-route.yml` | Étapes et transitions pédagogiques justifiées |
| Build path | Leçons d'implémentation, jalons et preuves de code existants | Dépendances de construction, implémentation et inspection |
| Généalogie historique | `data/history-pilot.yml` | Événements de recherche, publications, versions de modèles et écosystème avec relations historiques sourcées |
| Graphes pédagogiques locaux aux sources | `data/extractions/<source-id>.yml` | Nœuds `src-` propres à une source et séquence pédagogique reconstruite |
| Provenance et lineage | Cible `data/source-lineage/`, scans et extractions | Relations source/version/inspection/item/locator et décisions d'intégration |
| Associations de ressources | `data/resources.yml`, associations des concepts et métadonnées de pages | Liens entre concepts, ressources réutilisables et pages |
| Projections d'interopérabilité | Exports JSON-LD, SKOS, Schema.org et PROV-O | Exports déterministes ; PROV-O actuel au niveau dataset/artefact, pas une provenance scientifique complète au niveau claim |
| Sous-graphes générés | Générateurs de learning map, Mermaid computationnel et JSON-LD | Vues dérivées de leur propriétaire canonique, jamais éditées manuellement |

Les quatre familles analytiques sont donc des regroupements de consultation : scientifique/conceptuelle (notamment graphe conceptuel et généalogie), preuve (lineage et provenance), implémentation (computationnel et Build) et pédagogique (pages, route et graphes locaux). Les associations de ressources et les exports d'interopérabilité traversent ces familles sans les fusionner.

### Ponts typés entre structures

Les ponts doivent référencer les IDs existants, sans copier les définitions des nœuds ni fusionner les vocabulaires. Exemples :
- un nœud computationnel est expliqué par une page ;
- un événement historique implique ou précède un concept, sans déduire automatiquement une causalité ;
- un item d'extraction étaye une affirmation ou une définition dans un périmètre explicite ;
- un jalon Build implémente ou inspecte un nœud computationnel ;
- un concept canonique est mis en correspondance avec un nœud pédagogique local, sans promotion automatique de ce dernier.

Chaque pont précise sa catégorie (assertion sémantique, preuve, navigation, classification, représentation, implémentation ou pédagogie), sa direction, ses endpoints canoniques, sa justification et ses exigences de preuve. Une chronologie ne démontre pas une causalité ; l'ordre des pages ne crée pas un prérequis ; une citation ne prouve pas une affirmation ; un nœud local à une source ne devient pas automatiquement un concept canonique.

Cinq parcours de traversée doivent servir de tests d'intégration : concept → computation → implémentation → page Build ; concept → événement historique → sources ; page → concept → extraction → locator ; concept multi-domaine → pont inter-domaines ; modèle pédagogique local à une source → concepts canoniques, sans promotion automatique.

## 6. Chaîne de traçabilité recommandée

`SOURCE` → `SOURCE_VERSION` → `INSPECTION_EVENT` → `EXTRACTION_ITEM` → `KNOWLEDGE_OBJECT` → `IMPLEMENTATION / TEST / EXPERIMENT` → `PEDAGOGICAL_REPRESENTATION`

Chaque transition doit être explicite et typée. Toutes les étapes ne sont pas obligatoires pour chaque source. Une source peut contribuer à une définition sans implémentation ; un test peut vérifier un invariant logiciel sans constituer une expérience scientifique ; une page peut synthétiser plusieurs extractions.

Pour une affirmation importante, le lecteur doit pouvoir remonter à l'objet, la relation et sa justification, l'item extrait, son locator, la version inspectée, les limites de l'inspection et les validations réalisées. La granularité est proportionnée au risque et à l'importance : pas de règle mécanique « une source par phrase ».

## 7. État observé et limites

### LLM Lab

Les documents du dépôt attestent déjà une architecture informationnelle, des schémas de sources/extractions, un workflow d'intégration, un protocole de validation, une architecture cible de provenance distribuée, des registres distincts domaines/concepts/ressources et des graphes aux sémantiques différenciées.

L'audit transversal du 18 novembre 2026 identifie néanmoins des écarts : catalogue source encore centralisé tant que la migration n'est pas terminée ; provenance champ par champ non uniforme ; granularité d'extraction à éprouver par fixtures ; critères de complétude d'inspection à clarifier ; couverture de la preuve sur les relations à renforcer ; découvrabilité des contrats normatifs à améliorer. Ce sont des constats documentaires à traiter et vérifier par les issues propriétaires, non une affirmation que tous les validateurs ont été exécutés ici.

### Society Lab — chiffres rapportés par son audit

Le rapport consulté indique 214 sources, 59 études, 14 datasets, 83 claims, 22 hypothèses, 25 dossiers, 15 concepts et 596 relations initiales ; sept doublons de triplets auraient été consolidés, ramenant le total à 589. Il rapporte une couverture inégale : URL pour 214/214 sources, licence pour 1/214, vérification par source pour 28/83 claims, provenance explicite pour 26/83 claims, historique de révision pour 3/83 claims et financement/conflits pour 0/59 études.

Ces chiffres illustrent l'écart possible entre modèle défini et couverture opérationnelle. Ils ne sont ni des métriques LLM Lab ni une validation indépendante de Society Lab. Le rapport mentionne aussi des limites sur la matérialisation des manifestes, la déduplication bibliographique/conceptuelle, la cohérence fiches-graphe, les benchmarks de montée en charge et l'épreuve des mécanismes sur des cas réels.

## 8. Recommandations pour LLM Lab

### À adopter
1. Provenance vérifiable au niveau des items extraits et, pour certains champs sensibles, au niveau du champ.
2. Mémoire des décisions de sélection, fusion, renommage, dépréciation et révision.
3. Manifestes légers pour les campagnes multi-sources.
4. Relations typées, directionnelles et justifiées, avec contraintes de cycle spécifiques.
5. États indépendants pour accès, inspection, extraction, revue, intégration et publication.
6. Rapports de couverture montrant inconnues et objets orphelins.
7. Fixtures adversariales pour granularité, locateurs, voix, références et relations.
8. Tests de cohérence entre registres, projections, pages FR/EN, code, expériences et rapports.

### À ne pas adopter
- Importer les types métier Society Lab sans besoin démontré.
- Créer une seconde ontologie, un catalogue concurrent ou un registre central de relations.
- Transformer chaque mention en arête.
- Inférer des relations depuis tags, ordre des sections ou proximité visuelle.
- Transformer les états de workflow en scores de vérité.
- Stocker des snapshots complets sans règles de droits, sécurité et conservation.
- Introduire une base spécialisée avant d'avoir mesuré les limites du modèle Git/YAML.
- Rendre le dépôt public dépendant d'une base privée ou d'un autre dépôt.

## 9. Contrôles qualité et passage à l'échelle

Rapports à calculer depuis les registres canoniques, séparément par type d'objet :

- sources sans identifiant durable, version ou date d'inspection ;
- métadonnées sensibles sans preuve/méthode de vérification ;
- extractions retenues sans locator ou frontière de preuve ;
- relations sans justification, type inconnu ou cible inexistante ;
- concepts sans définition canonique ou source pertinente ;
- pages/ressources référençant des concepts obsolètes ;
- doublons d'identité, d'extraction ou de triplets ;
- projections obsolètes ou non déterministes ;
- expériences sans configuration, graine, baseline, métriques, coûts ou limites lorsque pertinents ;
- asymétries FR/EN de claims, réserves, exemples et références ;
- sources, concepts, ressources ou pages orphelins ;
- temps de génération/validation/recherche/rendu, taille des fichiers et conflits de fusion.

Ne pas fixer de seuils arbitraires avant d'avoir une baseline. Mesurer d'abord les volumes et temps actuels, puis tester des scénarios synthétiques x10 et x100. Préciser ce que chaque benchmark mesure : génération, validation, recherche, rendu, revue humaine ou maintenance collaborative.

## 10. Plan de travail et issues existantes

Réutiliser les issues ouvertes plutôt que créer des doublons :

| Travail | Suivi existant |
|---|---|
| Audit de couverture de provenance et réconciliation du graphe canonique | [#1211](https://github.com/JM-Brun/llm-lab/issues/1211) |
| Provenance champ par champ pour dates, versions et droits | [#1225](https://github.com/JM-Brun/llm-lab/issues/1225) |
| Réconcilier contrat d'extraction et couverture du validateur | [#1226](https://github.com/JM-Brun/llm-lab/issues/1226) |
| Découverte inter-domaines fondée sur les preuves et traçabilité des décisions | [#1233](https://github.com/JM-Brun/llm-lab/issues/1233) |
| Pilote attention / théorie de l'information / compression | [#1237](https://github.com/JM-Brun/llm-lab/issues/1237) |

Suites à rattacher aux issues propriétaires après vérification de périmètre : migration distribuée et gates de compatibilité ; fixtures d'inspection/extraction/relations ; critères de complétude ; tests de cohérence des projections ; benchmarks x10/x100 ; indexation des contrats documentaires. Ne pas ouvrir de tickets redondants.

Le pilote attention / information theory / compression met à l'épreuve les liens entre mathématiques, calcul, interprétation, implémentation, histoire et pédagogie. Il doit distinguer analogie, équivalence formelle, causalité, dépendance d'implémentation et choix pédagogique. Chaque passerelle doit être argumentée sur un exemple réel et accompagnée de ses limites.

## 10 bis. Premier pilote scientifique : attention, théorie de l'information et compression

L'issue [#1237](https://github.com/JM-Brun/llm-lab/issues/1237) est le premier test réel de cette architecture. Il faut commencer par réconcilier les contenus, IDs, extractions, expériences, locateurs et pages bilingues déjà présents, et non réingérer ou dupliquer les ressources.

Matériel existant à réutiliser :
- concepts/pages d'attention : self-attention, attention-score, attention-weight, Q/K/V et scaled dot-product attention ;
- concepts/pages d'information : entropie, cross-entropy, KL, information mutuelle et V-information ;
- synthèses : [information theory and LLMs](source-syntheses/information-theory-and-llms-2026-11.md), [two meanings of compression](source-syntheses/compression-two-meanings-2026-11.md), [model compression](source-syntheses/model-compression-2026-11.md) ;
- expériences : `experiments/information-theory/attention_kl_vs_mutual_information.py`, `compression.py`, `run.py`, le dossier `experiments/information-theory-llm/` et `experiments/sequence-compression/` ;
- extractions de Vaswani et al., FlashAttention et sources d'information theory, ainsi que les graphes computationnel et historique, en conservant leurs modèles séparés.

### Passerelles à accepter avec leur portée

1. **Softmax → distribution catégorielle.** Pour une requête donnée et un ensemble de clés visibles fixé, les poids softmax sont non négatifs et normalisés ; ils définissent une distribution catégorielle. L'entropie de Shannon de cette distribution est donc bien définie. Sa valeur caractérise la concentration des poids pour cette requête/tête/couche/entrée et ce masque ; elle ne mesure pas à elle seule l'information sémantique, l'information stockée dans les valeurs ou l'importance causale.
2. **Attention → calcul → FlashAttention.** Le calcul d'attention met en œuvre scores, masque, softmax et somme pondérée des valeurs. FlashAttention réorganise le calcul exact (à la précision flottante près) avec tuilage et softmax en ligne pour réduire les transferts HBM et éviter de matérialiser toute la matrice. C'est une relation d'implémentation et d'IO, pas une preuve de compression informationnelle.
3. **Modèle autorégressif → coût de codage prédictif.** La factorisation de la probabilité d'une séquence en probabilités conditionnelles relie le NLL à une longueur de code idéale ; la cross-entropy donne le coût idéal moyen sous inadéquation du modèle. Une expérience de codage sans perte exige toutefois un encodeur/décodeur déterministe, un modèle et tokenizer partagés, des conventions de précision et un test de reconstruction exacte. Un modèle génératif n'est pas à lui seul un codec.
4. **Compression de modèle et mémoire d'exécution.** Séparer au moins le codage prédictif de données, la compression du checkpoint (quantification, pruning, distillation) et la mémoire runtime (KV cache, activations, buffers, trafic HBM). Taille du checkpoint, qualité prédictive, mémoire de travail, latence, débit et bits/token sont des mesures différentes.
5. **Rate-distortion, information bottleneck et MDL.** N'ajouter un pont qu'avec des sources primaires inspectées et les variables, distorsion/perte, classe de modèles et hypothèses explicitement définies. Ne pas qualifier l'attention d'information bottleneck par simple analogie avec une représentation pondérée.

### Contre-exemples à conserver dans le benchmark

- Entropie des poids d'attention ≠ information mutuelle.
- FlashAttention ≠ compression informationnelle, sans revendication de codage distincte.
- Quantification d'un checkpoint ≠ codage source du corpus d'entraînement.
- Quantification du KV cache → réduction potentielle de mémoire runtime, pas compression du checkpoint.
- Poids d'attention diffus ou concentrés ≠ pertinence sémantique ou importance causale démontrée.

Le benchmark doit inclure cas positifs, négatifs et ambigus, locateurs exacts, hypothèses, limites, statut épistémique, notes d'indépendance des sources et explications FR/EN. Mesurer la précision sur un jeu de candidats revu manuellement avant de présenter des liens suggérés comme connaissances validées. Chaque passerelle acceptée doit être traçable jusqu'à source/version + item d'extraction + locator, ou déclarer explicitement le manque de preuve.

## 11. Critères d'acceptation

- Chaque type d'information a un propriétaire canonique explicite.
- Les IDs et références inter-registres sont validés automatiquement.
- Les relations ont une sémantique, un sens, une justification et une preuve lorsque nécessaire.
- Les inconnues et limites d'inspection sont conservées.
- Les projections sont déterministes et régénérables.
- Les décisions importantes sont traçables.
- Les contrôles FR/EN et les liens pages-concepts-sources-ressources sont testés.
- Les performances sont mesurées avant toute évolution technologique.
- Validations structurelle, scientifique, logicielle, expérimentale et pédagogique restent distinctes.
- Le projet public demeure autonome et compréhensible sans dépendance à Society Lab.

## 12. Références

### LLM Lab
- [README](../README.md)
- [Information architecture and metadata governance](information-architecture.md)
- [Source lineage architecture](source-lineage-architecture.md)
- [Audit transversal des processus de connaissance](source-process-audit.md)
- [Source catalogue and extraction data contract](source-catalogue-schema.md)
- [Workflow d'intégration source → système d'apprentissage](workflows/source-to-learning-system-integration.md)
- [Protocole de validation source → connaissance](workflows/source-to-knowledge-validation.md)
- [Roadmap](roadmap.md)

### Society Lab
- [Architecture](https://github.com/JM-Brun/society-lab/blob/main/docs/architecture.md)
- [Métadonnées et nommage](https://github.com/JM-Brun/society-lab/blob/main/docs/metadata-and-naming.md)
- [Protocole d'ingestion](https://github.com/JM-Brun/society-lab/blob/main/docs/ingestion-protocol.md)
- [Graphe de connaissances](https://github.com/JM-Brun/society-lab/blob/main/knowledge/GRAPH.md)
- [Types de relations](https://github.com/JM-Brun/society-lab/blob/main/knowledge/RELATION_TYPES.yml)
- [Audit du pipeline — novembre 2026](https://github.com/JM-Brun/society-lab/blob/main/docs/audit-ingestion-knowledge-pipeline-2026-11.md)
- [Framework inter-domaines](https://github.com/JM-Brun/society-lab/blob/main/docs/cross-domain-knowledge-framework.md)

### Références complémentaires
- [SOMEF — Software Metadata Extraction Framework](https://doi.org/10.1162/qss_a_00167), à évaluer pour la description de logiciels et artefacts scientifiques.
- [kg-metadata](https://github.com/MaastrichtU-IDS/kg-metadata), ressource sur les métadonnées de graphes et la validation ; ne justifie pas à elle seule une migration RDF/SHACL.
