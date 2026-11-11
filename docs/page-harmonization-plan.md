# Plan de convergence des pages pédagogiques

**Statut :** contrat de coordination et feuille de route ; les décisions existantes restent portées par leurs documents canoniques.  
**Périmètre :** expérience de lecture, composition, en-tête, navigation, fermeture de page et pied de site sur les pages bilingues Understand, Build, Deepen, Practice et Reference.  
**Coordination :** [#368 — template bilingue des leçons](https://github.com/JM-Brun/llm-lab/issues/368), [#282 — pilote et revue des pages](https://github.com/JM-Brun/llm-lab/issues/282), [#280 — convergence progressive du corpus](https://github.com/JM-Brun/llm-lab/issues/280), [#191 — validation du design system](https://github.com/JM-Brun/llm-lab/issues/191), [#337 — revue du parcours et de la navigation rendus](https://github.com/JM-Brun/llm-lab/issues/337).

Ce document rassemble les décisions et l'ordre de travail. **Il ne crée ni nouveau template obligatoire, ni nouvelle taxonomie, ni registre de pages, ni moteur de navigation.** Les contrats spécialisés et les sources de vérité listés ci-dessous prévalent.

## 1. Décision directrice : convergence, pas uniformité

Toutes les pages doivent partager des repères fiables : identité visuelle, hiérarchie typographique, position des éléments de navigation, comportement des composants, qualité des liens, accessibilité et cohérence FR/EN.

En revanche, leur composition dépend de la tâche du lecteur. Une leçon conceptuelle, une visite guidée de code, une collection d'exercices, un panorama et un glossaire ne doivent pas recevoir le même corps de page ni des sections artificielles.

La règle d'arbitrage est la suivante :

1. conserver un élément lorsqu'il répond à une question réelle du lecteur ou porte une information scientifique utile ;
2. déplacer ou fusionner lorsqu'il est pertinent mais mal placé ou redondant ;
3. reformuler lorsqu'il est utile mais difficile à comprendre ou incohérent avec le vocabulaire partagé ;
4. supprimer uniquement après avoir établi qu'il n'apporte ni contenu, ni preuve, ni navigation utile et qu'aucun lien entrant ne dépend de lui.

Une variation justifiée est une réussite du système souple, pas une non-conformité.

## 2. Sources de vérité et responsabilités

| Sujet | Source canonique | Règle de convergence |
|---|---|---|
| Composition et modules pédagogiques | [Flexible page-template system](page-template-system.md) | Modèle souple ; pas de checklist de sections |
| Archétypes et correspondance des types existants | [Page archetype implementation map](site-page-design-system.md) | Réutiliser les tags actuels ; aucun champ archetype parallèle |
| Patrons scientifiques | [Page patterns](page-patterns.md) | Choisir selon la question dominante |
| Walkthroughs, implémentation, vérification et expériences | [Implementation page patterns](implementation-page-patterns.md) | Préserver les contrats d'entrée/sortie, preuves et tests |
| Identité, typographie, espacement, couleurs, responsive et accessibilité | [Visual design system](design-system.md) | Une seule grammaire visuelle partagée |
| Breadcrumbs et transitions pédagogiques | [Pedagogical breadcrumb and page-navigation contract](pedagogical-breadcrumb-and-page-navigation-contract.md) | Quarto et les projections existantes restent canoniques |
| Métadonnées et graphe d'apprentissage | [Page metadata schema](page-metadata-schema.md) | Ne pas exposer les tags techniques comme contenu |
| Placement des contenus et destinations | [Content-section mapping](content-section-mapping.md) | Une responsabilité éditoriale claire par page |
| Ressources facultatives et auto-évaluation | [Learning resource block](learning-resource-block.md) | Bloc replié commun en fin de page, sans vider le corps de ses explications essentielles |
| État des pages effectivement auditées | [Page audit inventory](page-audit-inventory.md) et audits ciblés | Réutiliser les observations ; ne pas créer de deuxième inventaire |

Les responsabilités des issues sont également distinctes : #282 termine le pilote borné et sa revue rendue ; #280 conduit la convergence plus large en réutilisant ces résultats ; #368 coordonne l'anatomie minimale par archétype ; #191 porte la validation visuelle rendue ; #337 porte la revue rendue de la navigation/carte. Ne pas refaire leurs audits en parallèle.

## 3. Anatomie commune : éléments stables, composition variable

### 3.1 Enveloppe du site

Les pages publiées partagent les mêmes éléments de site : navbar globale, sidebar de la langue, surface de lecture, styles de liens et de focus, et pied de site lorsqu'il est fourni par le thème/site.

- La navbar reste courte et orientée vers les intentions stables du lecteur.
- La sidebar reste la navigation détaillée et la source du breadcrumb Quarto.
- La langue et les destinations doivent rester cohérentes entre les deux versions.
- Les contrôles globaux ne doivent pas être recopiés manuellement dans chaque fichier .qmd.

### 3.2 Ouverture et en-tête de page

Ordre de référence, à adapter selon les composants effectivement présents et le type de page :

1. **Breadcrumb natif Quarto** : localisation dans l'architecture publiée.
2. **Titre précis** : nom de l'objet ou de la question, sans métadonnées brutes.
3. **Sous-titre / lead** : ce que la page explique et sa portée, sans répéter un second résumé.
4. **Contexte pédagogique généré**, lorsqu'il existe et est pertinent : étape ou appartenance du parcours, distincte du breadcrumb.
5. **Objectifs et prérequis**, uniquement s'ils aident à décider, apprendre ou vérifier ; réutiliser les composants existants.
6. **Idée essentielle / entrée dans l'explication** : le lecteur doit rapidement comprendre la thèse ou le mécanisme central.

Ne pas afficher systématiquement une rangée de badges, un panneau de métadonnées, une carte d'objectifs ou une section « prérequis ». Le titre, le lead, le contexte et les objectifs ne doivent pas répéter la même information.

Le champ Quarto `description` reste **facultatif** : le filtre `site/filters/meta-description.lua` fournit déjà une description HTML à partir du sous-titre lorsqu'aucune description explicite n'est définie. Ajouter une description propre uniquement lorsqu'elle apporte une formulation de recherche réellement distincte ; ne pas imposer une paraphrase du sous-titre. Le `summary` du bloc `LLM-LAB-PAGE-MAP` répond à un autre usage (résumé de la page dans les vues de découverte) et ne doit pas être confondu avec cette métadonnée HTML.

### 3.3 Corps de page

Le corps partage les mêmes règles de lisibilité et de sémantique, pas une séquence de titres imposée :

- intuition avant formalisation lorsque cela aide à construire le modèle mental ;
- définitions, conventions, dimensions et hypothèses explicites ;
- équations introduites et interprétées ;
- exemples vérifiables, figures et tableaux placés près de l'argument qu'ils éclairent ;
- callouts employés selon leur rôle (note, intuition, avertissement, point essentiel), jamais comme décoration ;
- limites et conditions de validité visibles lorsqu'elles changent l'interprétation ;
- un seul lieu canonique pour le développement substantiel d'un concept, avec des rappels et liens contextualisés ailleurs.

Les schémas locaux décrivent un mécanisme, une transformation ou une comparaison ; ils ne remplacent ni le breadcrumb ni le parcours d'apprentissage.

### 3.4 Fermeture pédagogique de page

La fin du contenu principal doit aider à choisir la prochaine action, sans répéter la sidebar ni créer une liste exhaustive de liens :

- **Continuer** : prochaine étape centrale lorsque la route définit une transition pertinente ;
- **Prérequis** : uniquement si la connaissance est réellement nécessaire ;
- **Construire** : étape ou walkthrough Build correspondant ;
- **Pratiquer** : exercice ou expérience associé ;
- **Approfondir** : développement facultatif ;
- **Explorer** : relation utile sans ordre obligatoire.

N'afficher que les catégories renseignées et utiles. Conserver les liens de progression explicites des walkthroughs Build dans le flux visible lorsqu'ils sont nécessaires pour exécuter la séquence.

### 3.5 Ressources complémentaires et auto-évaluation

Réutiliser le bloc canonique .learning-resources, replié par défaut et placé en fin de page. Il peut accueillir, selon le contenu disponible :

- Explorer en pratique ;
- Pour approfondir ;
- Exercices ;
- Vérifier sa compréhension, avec réponses indépendamment repliées si utile.

Ne pas déplacer dans ce bloc les explications, exemples travaillés, hypothèses ou limites nécessaires pour comprendre le sujet. Ne pas créer de rubrique vide. Le bloc peut être complété progressivement.

### 3.6 Langue et pied de site

Le changement de langue doit être fiable, explicite et situé de façon cohérente. Il ne doit pas être confondu avec la navigation précédente/suivante.

Le sélecteur de langue de la navbar est le contrôle global, disponible sur toutes les pages. Un bloc local `.language-switch` peut offrir un accès direct supplémentaire en fin de contenu ; il est **facultatif selon l'archétype**, mais, lorsqu'il existe, il doit employer la même structure, les mêmes libellés localisés et les liens directs vers la page sœur. Ne pas rendre ce bloc obligatoire sur les pages de référence ou d'activité lorsque la navigation globale suffit. La forme locale canonique est un div Quarto `::: {.language-switch}` contenant le libellé « Langue : » / « Language: » et les deux liens directs ; utiliser des chemins relatifs courts et vérifier les deux sens.

Le pied de site est un composant global de l'enveloppe du site : liens institutionnels, documentation et informations du projet selon le thème existant. Il ne doit pas devenir un deuxième pied de page éditorial répétant les ressources, le breadcrumb ou les transitions locales. Comme la configuration Quarto actuelle définit un pied unique pour les deux langues, son libellé doit être neutre linguistiquement ou être réellement localisé ; une phrase française affichée sur les pages anglaises n'est pas acceptable. Vérifier son comportement sur les pages longues, les pages de référence et les vues mobiles.

## 4. Variantes par famille de pages

Les familles ci-dessous décrivent des comportements par défaut, pas une nouvelle classification de métadonnées. La correspondance stable reste celle de [site-page-design-system.md](site-page-design-system.md).

| Famille / rôle dominant | Repères utiles | À ne pas imposer |
|---|---|---|
| Entrée, panorama, carte du parcours | Question d'orientation, choix de destination, vue d'ensemble et liens de sortie | Objectifs de leçon, auto-évaluation artificielle, précédent/suivant linéaire |
| Leçon conceptuelle | Idée centrale, intuition, définition, mécanisme, exemple, limites, suite | Toutes les rubriques pour chaque concept |
| Deep dive / étude technique | Périmètre précis, hypothèses, formalisation, dérivation, variantes et limites | Une introduction longue ou la répétition du cours central |
| Build / walkthrough | Objectif opérationnel, prérequis d'exécution, étapes, code, contrats, vérifications et liens de progression | Masquer les étapes indispensables dans les ressources facultatives |
| Practice / expérience | Question investiguée, protocole, manipulation, observation, interprétation, limites et reproductibilité | Transformer chaque activité en leçon théorique complète |
| Exercices | Consignes, données, niveaux, indices/corrigés, objectifs de transfert et navigation par thème | Dupliquer sans raison le cours ou ses réponses |
| Référence / glossaire / bibliographie | Accès rapide, structure indexable, définitions et provenance | Un récit pédagogique linéaire, des objectifs génériques ou un stepper |

Une page peut combiner plusieurs patterns si sa tâche le justifie. Si deux tâches exigent chacune une explication substantielle, examiner le découpage éditorial avant d'ajouter des sections à l'infini.

### Contrat minimal par archétype

| Archétype existant (type de métadonnées) | Anatomie attendue par défaut | Éléments conditionnels |
|---|---|---|
| Entrée / panorama (`entry-point`, `system-overview`) | Titre, sous-titre, orientation concise, modèle d'ensemble et destinations explicites | Lead structuré, diagramme, objectifs ou auto-vérification seulement s'ils servent l'orientation |
| Leçon conceptuelle (`concept-lesson`, `concept-bridge`) | Titre, sous-titre, ouverture qui formule l'idée centrale, explication autonome, limites et liens contextuels | Contexte de parcours si la page appartient au registre ; objectifs et bloc de ressources si utiles |
| Approfondissement (`deep-dive`) | Périmètre précis, hypothèses, développement technique et limites | Lead, dérivation longue, navigation vers le concept parent ; pas de breadcrumb guidé par défaut |
| Visite guidée / Build (`guided-build`) | Objectif exécutable, prérequis d'exécution, étapes, résultats attendus et moyens de vérification | Lead, objectifs, liens précédent/suivant visibles si nécessaires à la séquence, ressources complémentaires |
| Practice / exercices / expérience (`exercise-hub`, `exercise-collection`, `experiment-guide`) | Consigne ou question, protocole ou structure d'exercice, critères d'interprétation et limites | Indices, corrigés repliés, ressources ; pas d'objectifs génériques ni de breadcrumb Understand imposés |
| Référence (`glossary`, `historical-reference`, `bibliography`) | Structure de consultation, conventions, entrées et provenance | Introduction brève et liens vers explications canoniques ; pas de parcours linéaire ou d'auto-évaluation artificielle |

Cette table est une règle d'arbitrage, pas une checklist de présence. Le type contrôlé existant reste l'identifiant stable ; le besoin documentaire, le pattern scientifique et les modules de composition ne deviennent pas de nouveaux champs de métadonnées. Le contexte de parcours guidé est dérivé exclusivement des appartenances explicites au registre : il ne se déduit ni de `destination`, ni du chemin du fichier, ni d'un ordre de sidebar.

## 5. Navigation : règles non négociables

Les dimensions suivantes restent séparées :

- **Breadcrumb de site** : .quarto-title-breadcrumbs, généré par Quarto depuis la sidebar.
- **Contexte pédagogique** : projection localisée de data/guided-route.yml, via les partials générés existants.
- **Suggested route** : transitions de lecture déclarées dans les métadonnées ; elles ne signifient pas automatiquement prérequis.
- **Stepper local** : processus, flux de données ou comparaison propre à la page.
- **Sidebar** : navigation détaillée et alternative d'accès.
- **Graphe / carte des ressources** : exploration, pas séquence obligatoire.

Ne pas concaténer ces éléments en une fausse hiérarchie, ni déduire une filiation depuis le chemin du fichier, l'ordre de la sidebar ou la proximité dans un graphe. Les appartenances multiples restent multiples lorsqu'elles sont justifiées. Practice & experiment reste transversal.

## 6. Méthode d'audit et de décision

Réutiliser l'inventaire existant et les audits spécialisés. Pour chaque page ou paire FR/EN, distinguer les dimensions suivantes :

| Dimension | Questions de revue | Statut à consigner |
|---|---|---|
| Rôle et portée | La page répond-elle à une question identifiable ? Son rôle déclaré correspond-il à sa fonction réelle ? | Conforme / écart justifié / à revoir |
| Ouverture | Le titre, le lead et le contexte orientent-ils sans répétition ? | Conforme / amélioration / problème |
| Corps | Les définitions, exemples, équations, figures, limites et références sont-ils au bon endroit ? | Conforme / amélioration / problème |
| Navigation | Breadcrumb, contexte, route, sidebar et liens locaux ont-ils chacun le bon sens ? | Conforme / problème / non applicable |
| Fermeture | La prochaine action est-elle utile, claire et non redondante ? | Conforme / amélioration / non applicable |
| Ressources | Les contenus optionnels et le self-check sont-ils bien regroupés sans perte d'information essentielle ? | Conforme / problème / non applicable |
| Parité FR/EN | Sens, profondeur, exemples, caveats, ancres et destinations sont-ils équivalents ? | Conforme / écart documenté / problème |
| Rendu et accessibilité | Desktop/mobile, clavier, focus, reflow, contraste, tableaux, équations et disclosures sont-ils utilisables ? | Non vérifié / observé / défaut reproductible |
| Preuves | Qu'est-ce qui est validé par source, CI, navigateur ou apprenant ? | Séparer chaque niveau |

Pour chaque écart, classer explicitement :

- défaut affectant la compréhension, l'orientation, l'accessibilité ou la maintenance ;
- variation légitime liée à la famille de page ;
- préférence stylistique de faible priorité.

Prioriser par impact lecteur, nombre de pages concernées, coût et risque de régression. Les jugements éditoriaux restent humains ; seuls les invariants objectifs et stables sont candidats à une validation automatisée.

## 7. Lots de réalisation

### Lot A — Consolider le contrat et l'échantillon

- [ ] Réutiliser le pilote et les cinq paires déjà identifiées sous #282 ; ne pas les ré-auditer sans nouvelle question ou changement de rendu.
- [ ] Confirmer les décisions de composition et les écarts justifiés par famille.
- [ ] Vérifier la cohérence entre ce plan et les guides canoniques ; résoudre les éventuelles contradictions à la source.

### Lot B — Valider l'enveloppe commune

- [ ] Examiner navbar, sidebar, breadcrumb, titre, lead, contexte pédagogique, switch de langue et pied de site dans le rendu publié.
- [ ] Vérifier largeur de lecture, marges, hiérarchie des titres, rythme vertical, liens, tableaux, équations, code, figures et callouts.
- [ ] Tester clavier, focus visible, zoom/reflow, viewport étroit et préférences de contraste pertinentes.
- [ ] Consigner pages, langue, navigateur, viewport, résultats et captures disponibles dans les issues de revue existantes.

### Lot C — Piloter les variantes

- [ ] Choisir une page représentative par famille utile, en réutilisant les pages déjà auditées.
- [ ] Corriger uniquement les défauts observés ; conserver les différences éditoriales qui ont une raison.
- [ ] Comparer les rendus avant/après en FR et EN.
- [ ] Vérifier que les ancres publiques, références, liens entrants et identifiants stables survivent aux déplacements.

### Lot D — Généraliser par lots bornés

- [ ] Étendre les corrections à partir des constats, par famille ou composant partagé.
- [ ] Éviter les réécritures globales, remplacements regex risqués et changements de toutes les pages dans une seule PR.
- [ ] Réutiliser les composants et partials existants ; ne créer une abstraction qu'après avoir démontré plusieurs usages stables.
- [ ] Mettre à jour les guides canoniques seulement lorsqu'un constat justifie une règle durable.

## 8. Validation et critères d'acceptation

La validation doit distinguer :

1. **Source** : contenu, métadonnées, liens et composants correctement structurés.
2. **Automatisation** : tests, contrôles de liens, génération des données et rendu Quarto réussis.
3. **Rendu observé** : pages réellement inspectées sur desktop et mobile, dans les deux langues.
4. **Accessibilité** : résultats automatisés et contrôles manuels rapportés séparément.
5. **Apprentissage** : retours d'apprenants ou évaluation indépendante ; ne pas inférer l'efficacité depuis un rendu ou une CI verte.

Critères d'acceptation de la convergence :

- chaque page a un rôle clair et une composition adaptée ;
- les composants partagés ont un comportement et une présentation cohérents ;
- la navigation reste sémantiquement distincte et sans doublon ;
- la parité FR/EN porte sur le sens, la profondeur et les destinations ;
- aucun contenu scientifique utile, caveat, exemple, référence ou preuve n'est perdu ;
- les exceptions utiles sont documentées plutôt que supprimées ;
- les contrôles techniques passent et le rendu réellement inspecté est consigné ;
- aucun registre, taxonomie, template rigide ou système de navigation parallèle n'a été introduit.

## 9. Prochaine séquence concrète

La suite doit rester dans les issues existantes :

1. terminer la revue rendue du pilote sous #282 ;
2. utiliser ses résultats pour ajuster le contrat de template sous #368 ;
3. poursuivre la convergence du corpus sous #280 à partir de l'inventaire existant ;
4. valider les composants et tokens dans le rendu sous #191 ;
5. vérifier la navigation publiée et la carte sous #337.

**Premier objectif opérationnel :** établir une comparaison rendue, bilingue et responsive de l'enveloppe commune sur un petit échantillon représentatif avant toute modification globale des pages.
