# Audit transversal des processus de connaissance

**Date de l'audit :** 2026-11-18  
**Périmètre :** découverte et inscription des sources, inspection, extraction, métadonnées, synthèse, concepts et relations, intégration pédagogique, validation et maintenance.  
**Nature :** audit documentaire et architectural fondé sur les contrats du dépôt et les preuves GitHub disponibles ; ce document ne prétend pas avoir exécuté localement tous les validateurs ni inspecté individuellement les 124 sources.

## 1. Verdict exécutif

LLM Lab dispose déjà d'un processus de recherche et d'intégration des connaissances remarquablement explicite. Les étapes, les unités d'analyse, les distinctions de provenance, les décisions éditoriales et les limites de validation sont largement documentées. L'architecture est bien pensée : elle sépare les sources, les inspections, les extractions, les graphes locaux aux sources, le graphe conceptuel canonique, les ressources et les parcours pédagogiques.

**Le principal défaut n'est pas l'absence de méthode : c'est l'écart entre une architecture cible distribuée et le fonctionnement actuel du catalogue centralisé, ainsi que la couverture inégale de la traçabilité sémantique.** Il faut consolider et faire respecter les contrats existants, pas créer un deuxième pipeline ou une nouvelle ontologie.

| Dimension | Évaluation | Motif |
|---|---|---|
| Découpage des processus | Solide | Workflow normatif en étapes et gates indépendants |
| Identité et provenance des sources | Solide dans le contrat | IDs stables, déduplication par identifiants durables, versions et historique d'inspection |
| Métadonnées | Bien spécifiées, couverture incomplète | Champs typés et inconnues explicites ; dates/licences encore souvent inconnues |
| Extraction | Solide dans le contrat | Items atomiques, locateurs, voix, preuve, confiance, hypothèses, limites et dispositions |
| Synthèse multi-sources | Solide dans la méthode | Convergence, complémentarité, contradiction et indépendance sont distinguées |
| Concepts et relations | Architecture solide, sémantique à approfondir | Registre canonique bilingue et relations typées ; couverture et provenance au niveau des arêtes encore incomplètes |
| Intégration pédagogique | Bien gouvernée | Propriétaires canoniques, décisions explicites, non-régression, parité FR/EN et séparation des parcours |
| Validation automatique | Bonne base | Validateurs, tests, CI et rapport de couverture ; ils ne prouvent ni vérité scientifique ni efficacité pédagogique |
| Scalabilité opérationnelle | À améliorer | `data/sources.yml` reste le catalogue d'écriture central ; la migration distribuée est une architecture cible |
| Découvrabilité documentaire | À améliorer | Les documents normatifs existent mais ne sont pas tous exposés depuis les points d'entrée les plus visibles |

## 2. Architecture et responsabilités déjà correctement séparées

Les documents suivants constituent le corpus normatif existant :

- [Information architecture and metadata governance](information-architecture.md) : source de vérité, propriétaires, projections et sémantique des graphes.
- [Source catalogue and extraction data contract](source-catalogue-schema.md) : identités, classifications, métadonnées, extractions et vocabulaires.
- [Source lineage architecture](source-lineage-architecture.md) : modèle cible distribué et migration progressive.
- [External-source to learning-system integration workflow](workflows/source-to-learning-system-integration.md) : processus opératoire de l'inscription à la publication.
- [Source-to-knowledge validation protocol](workflows/source-to-knowledge-validation.md) : contrôle de la qualité du produit de connaissance et de la méthode.
- [Source synthesis method](source-synthesis-method.md) : méthode de synthèse.
- Les templates de [registration](workflows/templates/source-registration-template.yml), [extraction](workflows/templates/source-extraction-template.yml), [review](workflows/templates/source-review-template.md), [comparaison multi-sources](workflows/templates/multi-source-comparison-template.md) et [audit des médias](workflows/templates/visual-asset-audit-template.md).

Les objets ne doivent pas être fusionnés :

1. source externe et version ;
2. événement d'inspection ;
3. item d'extraction localisé ;
4. graphe et parcours reconstruits propres à la source ;
5. concept canonique et relation sémantique ;
6. page ou ressource du projet ;
7. parcours pédagogique du projet ;
8. preuve de validation et observation d'apprenant.

Cette séparation évite notamment de transformer une séquence d'article en prérequis, un tag en concept, une citation en corroboration indépendante ou une association source-concept en preuve d'une relation scientifique.

## 3. Évaluation par étape

### 3.1 Découverte, sélection et identité

**Acquis**

- L'identité repose sur des IDs stables et des identifiants externes durables (DOI, URL canonique, dépôt et révision), pas sur le titre seul.
- Les éditions, versions, miroirs et révisions matériellement différentes peuvent rester distincts et être reliés.
- Les sources peuvent être classées avant inspection ; la sélection et l'inspection sont des états différents.
- Le processus demande de rechercher les doublons avant toute inscription.

**À renforcer**

- Documenter un critère minimal de sélection et de priorité (question de recherche, type de contribution attendu, autorité adaptée à l'usage, coût d'inspection, risque de dépendance aux sources déjà présentes).
- Enregistrer les sources écartées ou différées uniquement lorsque leur réapparition probable justifie une trace ; ne pas transformer chaque URL découverte en entrée durable.
- Pour les sources web mutables, privilégier la révision ou le snapshot quand ils existent. Une URL canonique seule n'identifie pas toujours le contenu effectivement inspecté.

### 3.2 Inspection et ingestion

**Acquis**

- Le workflow distingue accès direct, API, texte indexé, miroir et dépôt.
- La couverture est décomposée : texte auteur, figures/médias, code/données, commentaires, ressources liées, métadonnées et droits.
- Les parties inaccessibles ou non inspectées restent explicites ; un extrait indexé n'est pas présenté comme une lecture directe.
- L'historique d'inspection est conçu comme append-only ; une correction doit superséder un événement plutôt que l'effacer.

**À renforcer**

- Définir un petit contrat commun de capture des artefacts (empreinte/hash si disponible, date de récupération, version/révision, méthode, type MIME/format, locator stable et état d'accès). Ne le rendre obligatoire que lorsque la reproductibilité ou la volatilité de la source le justifie.
- Définir des règles de conservation et de sécurité pour les snapshots : droits, secrets, données personnelles, contenu non redistribuable et taille des fichiers. Le dépôt ne doit pas devenir un miroir intégral des sources.
- Clarifier les critères qui font passer une composante de `partial` à `complete`, et `not-applicable` à `not-inspected`. Le statut global ne doit pas masquer les dimensions manquantes.

### 3.3 Extraction et reconstruction pédagogique

**Acquis**

- L'unité de décision est l'item atomique, non l'article entier.
- Chaque item comporte un identifiant local à la source, un résumé/paraphrase, un locator, un type de preuve, un niveau de confiance, un périmètre, des hypothèses et des limites.
- Les voix de l'auteur, des commentateurs, des mainteneurs et de l'éditeur sont distinguées.
- Les éléments inférés sont marqués comme tels.
- Pour les sources pédagogiques, le graphe local et le parcours d'enseignement sont séparés du graphe conceptuel et du parcours du projet.
- Les contributions redondantes, rejetées ou différées doivent rester représentées lorsqu'elles éclairent la décision.

**À renforcer**

- Formaliser les règles de granularité avec quelques fixtures contrastées : affirmation composée à scinder, formule avec hypothèses, figure seulement légendée, code non exécuté, commentaire communautaire, résultat rapporté sans protocole.
- Exiger un locator vérifiable et une frontière de preuve pour chaque item retenu ; pour les pages web mouvantes, le locator devrait inclure section/heading et snapshot ou date d'accès.
- Prévoir un état explicite `not-applicable` pour le modèle pédagogique des sources non-instructionnelles, au lieu de forcer une reconstruction artificielle.

### 3.4 Métadonnées

**Acquis**

- Les champs importants sont typés : type, langue BCP 47, dates, version/révision, licence, droits de réutilisation, niveau, contributions, audiences, statuts, domaines, tags et IDs de concepts.
- Les tags sont des facettes de recherche ; ils ne remplacent ni concepts, ni domaines, ni champs bibliographiques.
- Les valeurs inconnues restent inconnues. Une URL publique ou un dépôt public ne prouve pas une licence.
- Les dimensions `scan_status`, `integration_status` et la disposition de chaque item sont indépendantes.

**Risque résiduel**

Le contrat décrit les champs, mais ne définit pas encore un mécanisme uniforme de provenance **champ par champ** pour les métadonnées sensibles ou volatiles (date de publication, date de mise à jour, version, licence, identité du créateur). L'historique de scan général ne permet pas toujours de retrouver quelle preuve justifie une valeur particulière.

**Recommandation**

Introduire, après examen d'exemples réels, une provenance de métadonnée ciblée : valeur, locator ou URL justificative, date de vérification, méthode et statut (déclaré par l'éditeur, vérifié sur la source canonique, inféré, inconnu). Ne pas créer une structure lourde pour chaque champ trivial ; commencer par les dates, versions et droits. Toute évolution doit être ajoutée au schéma et aux fixtures, sans remplir rétroactivement les inconnues par supposition.

### 3.5 Synthèse et arbitrage multi-sources

**Acquis**

- La méthode distingue preuve primaire, interprétation secondaire, contribution pédagogique, preuve de projet et observation apprenant.
- La répétition n'est pas confondue avec une corroboration indépendante ; la dépendance des citations doit être examinée.
- Les désaccords sont conservés et arbitrés, pas moyennés.
- Nouveauté et complémentarité sont évaluées séparément.
- Les décisions d'intégration utilisent un vocabulaire contrôlé et une justification par item.
- Le processus teste une intégration bornée avant de conclure qu'une source pédagogique n'apporte rien.

**À renforcer**

- Maintenir une matrice de contributions/affirmations qui pointe vers les IDs d'extraction et les locateurs, plutôt qu'une synthèse uniquement narrative.
- Distinguer explicitement « source qui rapporte un résultat », « source qui reproduit le résultat » et « équipe du projet qui a reproduit le résultat ».
- Pour les affirmations sensibles ou controversées, conserver la chaîne de dépendance des citations et le protocole exact ; ne pas compter plusieurs tutoriels dérivés d'un même papier comme plusieurs preuves indépendantes.

### 3.6 Concepts, domaines et relations

**Acquis**

- `data/concepts.yml` est le registre canonique bilingue des concepts ; `data/domains.yml` définit les domaines ; `data/resources.yml` gère les ressources non-page.
- Les relations sont typées et directionnelles ; les règles de symétrie et d'acyclicité sont limitées aux types qui le nécessitent.
- Les graphes de pages, de concepts, de ressources, les relations historiques et les parcours restent distincts.
- Les générateurs produisent des projections ; les sorties générées ne doivent pas devenir des sources d'édition.

**Limites importantes**

- Une association `source.concept_ids` indique une pertinence, pas la preuve d'une définition ni d'une arête conceptuelle.
- La documentation d'architecture indique explicitement que l'export JSON-LD ne revendique pas encore une provenance claim-level complète.
- Les arêtes conceptuelles n'ont pas encore une couverture systématique d'évidence/locator au niveau de chaque relation. La couche de source lineage cible peut fournir cette traçabilité, mais son déploiement doit être vérifié séparément.
- Les contraintes de domaine/portée, famille, inverse, transitivité et éligibilité comme dépendance d'apprentissage restent un sujet d'arbitrage suivi notamment dans [#512](https://github.com/JM-Brun/llm-lab/issues/512), à coordonner avec les propriétaires du graphe existant.

**Recommandation**

Prioriser la provenance des arêtes qui portent une affirmation scientifique ou une dépendance, pas les liens de simple découverte. Une relation doit pouvoir répondre à : qui l'affirme, sur quelle preuve/locator, dans quel contexte, avec quelle confiance et quelles limites ? Les associations de navigation ou de classification n'ont pas besoin du même niveau de preuve.

### 3.7 Intégration pédagogique et bilingue

**Acquis**

- Les pages canoniques ont des propriétaires ; les nouvelles pages ne sont pas la réponse par défaut.
- Les modifications apprenant sont bilingues et conservent les réserves scientifiques.
- Les quatre destinations Understand, Build, Deepen et Practice ont des rôles distincts.
- La route Understand reste dans son registre canonique ; le graphe de concepts ne devient pas une route concurrente.
- Les contenus déplacés doivent conserver leurs exemples, figures, références, légendes et qualifications.

**Point de vigilance**

La qualité du processus dépend de la mise à jour simultanée des pages propriétaires, des concepts, des sources, des métadonnées, des projections générées, des références, des exercices et des liens. Une checklist de changement doit identifier les artefacts affectés, mais éviter d'imposer des modifications inutiles à tous les registres à chaque nouvelle source.

### 3.8 Validation et mesure de qualité

**Acquis**

- Les validateurs structurels, tests, CI, rendu Quarto et contrôles de liens sont distincts de la revue scientifique, de la revue navigateur/accessibilité et de la validation par apprenants.
- Le rapport de couverture des sources permet de transformer des écarts en files de revue, sans les corriger automatiquement.
- Les rapports de CI sont liés à un commit précis ; un résultat ancien ne valide pas un nouveau HEAD.

**Limites**

- Un schéma valide ne prouve pas la fidélité de l'extraction.
- Un locator présent ne prouve pas que l'interprétation est juste.
- Une relation résolue ne prouve pas que sa sémantique est correcte.
- Une synthèse cohérente ne prouve pas qu'elle est exhaustive.
- Un rendu réussi ne prouve pas l'accessibilité, la qualité visuelle ou l'apprentissage.
- Les statuts de licence et les droits doivent être revus humainement à partir de preuves explicites.

## 4. Scalabilité : état actuel et architecture cible

La documentation [source lineage architecture](source-lineage-architecture.md) propose une évolution proportionnée : fichiers par source, événements d'inspection append-only, fichiers de lineage par source, extractions séparées, puis index de compatibilité généré. Elle prévoit inventaire des lecteurs/écrivains, migration sans perte, validation en parallèle, migration des consommateurs, CI et rollback.

**Cette architecture est une cible, pas un état acquis.** Le contrat du catalogue indique encore que `data/sources.yml` est l'emplacement canonique actuel ; la migration distribuée ne doit pas être présentée comme terminée avant que tous les lecteurs, écrivains, tests, workflows et skills aient été migrés.

La stratégie recommandée est donc :

1. Conserver le catalogue actuel tant que la migration n'a pas passé ses gates.
2. Mesurer les conflits de fusion, temps de validation et coûts de maintenance avant de décider du découpage.
3. Inventorier tous les lecteurs/écrivains, y compris scripts, tests, workflows et skills.
4. Définir les schémas versionnés pour sources, événements et arêtes avant le convertisseur.
5. Migrer sans perte et produire un index de compatibilité déterministe.
6. Comparer ancien catalogue et projection, puis faire lire les nouveaux chemins aux consommateurs.
7. Ne basculer les écritures qu'après validation complète et documenter le rollback.
8. Garder YAML et les validateurs Python tant que le volume et les usages ne justifient pas une base de données.

Ne pas distribuer les fichiers simplement pour « faire scalable » : la migration n'est utile que si elle réduit réellement les conflits et permet des changements indépendants sans multiplier les incohérences.

## 5. État de preuve observé au 18 novembre 2026

Le rapport de couverture exécuté sur le catalogue dans le cadre de PR #1214 fournit un snapshot de 124 sources, 68 extractions et 378 items, avec 102 concepts. Il signale notamment 56 sources sans extraction, 29 de ces sources étant marquées `integrated`, 11 sans lien conceptuel, 6 sans destination pédagogique, 18 concepts sans source associée, 44 dates inconnues et 114 statuts de licence inconnus. Il ne rapporte aucune référence d'extraction vers une source inconnue, aucune référence de concept inconnue et aucune incohérence entre statut de scan et historique.

Ces chiffres doivent être lus comme des alertes de revue, non comme des objectifs. Une source sans extraction peut être une référence bibliographique ou une ressource d'implémentation ; un concept sans source catalogue peut être un fondamental défini par le projet ; un statut inconnu peut être la seule valeur honnête.

La PR #1219 sur l'extraction Neuronpedia documente un cas utile de traçabilité au niveau des items : six items localisés, graphe source-local, hypothèses et limites explicites, sans assimiler observations d'activation, explications générées, attribution approximative et causalité établie. Sa description rapporte 621 tests passés et un rendu Quarto réussi sur son HEAD. Cela valide cette modification et les contrôles exécutés, pas la qualité de tout le corpus.

## 6. Priorités recommandées

**Mise à jour après revue du contrat d'extraction — 2026-11-18**

La comparaison du validateur réel avec le template et le README des extractions a révélé un écart entre les champs suggérés et les champs effectivement imposés. La correction documentaire est proposée dans [PR #1223](https://github.com/JM-Brun/llm-lab/pull/1223) : propriété du scan conservée au niveau source, graphe source-local explicitement extensible, exemple README corrigé et aide éditoriale distinguée du contrat CI.

Le renforcement raisonné du validateur est suivi séparément dans [#1226](https://github.com/JM-Brun/llm-lab/issues/1226). Il faudra établir une matrice champ/propriétaire/obligation/validation/fixtures/compatibilité, puis distinguer erreurs d'intégrité et avertissements de qualité. Ne pas rendre obligatoires les dates/licences inconnues ni imposer une taxonomie fermée sans preuve corpus.

La provenance des valeurs sensibles de métadonnées (dates, versions, droits) est étudiée dans [#1225](https://github.com/JM-Brun/llm-lab/issues/1225). Elle reste distincte de la provenance des affirmations et relations conceptuelles suivie dans [#512](https://github.com/JM-Brun/llm-lab/issues/512).


### P0 — Fiabiliser la traçabilité et les statuts

1. Poursuivre [#1211](https://github.com/JM-Brun/llm-lab/issues/1211) : traiter les alertes du rapport une par une, avec décisions justifiées et sans remplissage automatique.
2. Vérifier particulièrement les sources `integrated` sans extraction dédiée : documenter si l'intégration est bibliographique, par référence, via une synthèse, ou si le statut doit être corrigé.
3. Revoir les relations conceptuelles importantes et les liens source-concept à partir des items réellement inspectés.
4. Garder les inconnues de date, version et licence tant qu'aucune preuve fiable ne permet de les résoudre.

### P1 — Fermer l'écart entre contrat et implémentation

1. Inventorier les lecteurs/écrivains et mesurer les coûts réels du catalogue monolithique avant la migration distribuée.
2. Vérifier que chaque étape normative possède un validateur ou un contrôle humain clairement identifié ; documenter les étapes qui restent manuelles.
3. Ajouter des fixtures de qualité d'extraction et de provenance de métadonnées, pas seulement des fixtures de syntaxe/références.
4. Coordonner la sémantique avancée des relations avec [#512](https://github.com/JM-Brun/llm-lab/issues/512) et le propriétaire du graphe ; ne pas créer une seconde issue concurrente.
5. Vérifier la couverture de la provenance au niveau des arêtes conceptuelles et des affirmations, sans prétendre que le JSON-LD actuel la garantit.

### P2 — Améliorer l'ergonomie et l'observabilité

1. Publier un résumé de couverture lisible et daté depuis CI, si le comportement de PR #1214 est conservé ; préciser son commit et les limites du rapport.
2. Mesurer l'effort d'ajout incrémental d'une source sur plusieurs types de sources, y compris une source multimédia ; ne pas conclure à la scalabilité sur le seul nombre de fichiers.
3. Documenter des seuils de déclenchement pour rescanner une source (nouvelle version, URL déplacée, correction importante, changement de droits, nouveau résultat contradictoire).
4. Rendre les workflows normatifs accessibles depuis README, CONTRIBUTING et l'index d'architecture.

## 7. Décision d'architecture

**À préserver :** les registres canoniques existants, les relations typées, les statuts indépendants, les extractions atomiques, les graphes locaux aux sources, le graphe conceptuel, les ressources et les parcours séparés.

**À ne pas créer :** un nouveau registre de sources, une nouvelle ontologie, un deuxième parcours, un graphe global non typé, une extraction obligatoire pour chaque entrée bibliographique, ou une automatisation qui infère des licences, des concepts ou des corroborations.

**À faire évoluer :** la traçabilité champ par champ des métadonnées sensibles, la provenance des arêtes conceptuelles, les contrôles de qualité de l'extraction, l'observabilité du pipeline et la migration distribuée lorsque son bénéfice est démontré.

## 8. Découverte inter-domaines et mémoire des décisions

L'audit du cycle source → connaissance ne suffit pas, à lui seul, à garantir que le corpus permette de découvrir des relations entre plusieurs centaines de sujets. Le graphe conceptuel existant décrit des relations typées entre concepts ; il ne doit pas être confondu avec un graphe exhaustif de toutes les sources, pages, ressources, expériences et décisions.

Le suivi transversal est désormais explicité dans [#1233 — découverte inter-domaines et traçabilité des décisions](https://github.com/JM-Brun/llm-lab/issues/1233), en coordination avec #512 (interopérabilité et provenance des affirmations), #416 (sémantique du graphe conceptuel) et #1211 (réconciliation du corpus).

Les exigences structurantes sont les suivantes :

- **Un modèle multi-structures, pas un registre parallèle :** relier les identifiants canoniques existants (source/version, item extrait, concept, domaine, page, ressource, expérience, nœud computationnel, décision) sans recopier leurs définitions.
- **Des relations qualifiées par leur fonction :** distinguer assertion sémantique, preuve, contradiction, corroboration indépendante, citation bibliographique, classification, navigation, représentation, dépendance d'implémentation et relation pédagogique.
- **Des chemins de preuve explicables :** une relation fondée sur une source doit pouvoir remonter à l'item extrait, au locator, à la version inspectée et aux limites de l'inspection. Une relation conceptuelle directe peut conserver une rationale explicite lorsque la preuve bibliographique n'est pas le bon fondement.
- **Des suggestions non promues automatiquement :** cooccurrence, tags partagés, proximité de pages ou citation commune peuvent proposer une piste de recherche, jamais prouver une relation. Les candidats doivent exposer leur raison et passer une revue avant d'intégrer le graphe canonique.
- **Une mémoire des décisions proportionnée :** conserver Git, issues, PR et rationales existantes comme historique primaire ; ne structurer que les décisions durables qui doivent être retrouvées depuis les entités affectées. Enregistrer alternatives, motifs, portée, preuves, statut et conditions de réexamen.
- **Des projections exploratoires séparées des parcours :** les requêtes de découverte peuvent traverser domaines et concepts, mais ne deviennent ni un nouvel ordre d'apprentissage ni une seconde navigation pédagogique.
- **Une scalabilité mesurée :** tester génération incrémentale, invalidation sélective, coût de validation et conflits à 1k/5k/10k sources avant de choisir une base de données ou un moteur de graphe. YAML reste le format canonique tant qu'une mesure ne justifie pas autre chose.

Les premières requêtes de référence doivent couvrir au minimum : ponts entre domaines, explications concurrentes, corroborations/contradictions indépendantes, pages ou concepts insuffisamment étayés, chemin complet vers la preuve et décisions qui affectent une page. Chaque résultat devra afficher le chemin et ses limites, pas seulement un score de similarité.

## 9. Limites de cet audit

- Audit documentaire et examen des contrats et états GitHub disponibles ; les commandes de validation n'ont pas toutes été réexécutées localement pendant cet audit.
- Le rapport de couverture est un instantané lié à un commit de PR, pas un décompte garanti du HEAD actuel de `main`.
- Les statuts de PR/CI sont volatils ; consulter leurs HEAD et workflows avant toute fusion ou clôture.
- Aucun examen exhaustif des 124 sources, des 378 items, des 102 concepts ou de toutes les arêtes n'est revendiqué.
- Aucune validation indépendante de la vérité scientifique, de la conformité juridique ou de l'efficacité pédagogique n'est revendiquée.

## 9. Sources internes

- [Information architecture](information-architecture.md)
- [Source catalogue schema](source-catalogue-schema.md)
- [Source lineage architecture](source-lineage-architecture.md)
- [Source integration workflow](workflows/source-to-learning-system-integration.md)
- [Source-to-knowledge validation protocol](workflows/source-to-knowledge-validation.md)
- [Source synthesis method](source-synthesis-method.md)
- [Knowledge graph implementation audit](knowledge-graph-implementation-audit.md)
- [Source coverage report](source-coverage-report.md)
- [Issue #1211 — provenance coverage and canonical graph reconciliation](https://github.com/JM-Brun/llm-lab/issues/1211)
- [Issue #512 — knowledge-structure interoperability and relation semantics](https://github.com/JM-Brun/llm-lab/issues/512)
