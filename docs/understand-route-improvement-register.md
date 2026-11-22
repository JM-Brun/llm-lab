# Registre des améliorations possibles du parcours Understand

**Statut :** registre d'opportunités et cadre d'audit. Il ne constitue ni une liste de défauts tous confirmés, ni un engagement à tout implémenter.  
**Périmètre :** parcours principal Theory / Understand, pages canoniques FR/EN, vues de découverte, métadonnées et relations vers Deepen, Practice & experiment et Build.  
**État de référence :** dépôt consulté le 22 novembre 2026.

Ce document complète les contrats existants : [learning path](learning-path.md), [content-section mapping](content-section-mapping.md), [page metadata schema](page-metadata-schema.md), [page-template system](page-template-system.md), [reader-experience method](reader-experience-and-editorial-method.md), [page harmonization plan](page-harmonization-plan.md), [information architecture](information-architecture.md), [guided route](../data/guided-route.yml), [computational graph](../data/computational-graph.yml) et [concept registry](../data/concepts.yml). Il ne les remplace pas et ne crée aucune nouvelle source de vérité.

Le but est de rendre les améliorations possibles explicites, de distinguer les acquis des hypothèses et de définir comment décider si une modification apporte réellement quelque chose à l'apprenant.

---

## 1. Principes directeurs

### 1.1 Le critère est le bénéfice apprenant

Un changement doit améliorer au moins une capacité observable :

- construire ou corriger un modèle mental ;
- comprendre une relation entre deux mécanismes ;
- suivre un calcul et interpréter les objets manipulés ;
- transférer un raisonnement à un cas nouveau ;
- retrouver une explication, un exercice ou un approfondissement ;
- choisir le bon niveau de détail sans perdre le fil ;
- expliquer le fonctionnement d'un LLM depuis son entrée jusqu'à ses usages.

La cohérence des fichiers, graphes et métadonnées est nécessaire, mais n'est pas en elle-même un résultat pédagogique.

### 1.2 Trois représentations restent distinctes

1. **Graphe computationnel** : ce qui est calculé, dans quel ordre d'exécution, avec quels objets et paramètres.
2. **Graphe de connaissances** : concepts, définitions, relations conceptuelles, domaines et ressources.
3. **Parcours pédagogique** : ordre de présentation recommandé, niveau d'explication et transitions utiles.

Le parcours est une projection pédagogique des connaissances et mécanismes ; il ne copie pas le graphe de calcul et n'impose pas l'ordre d'exécution comme ordre de lecture. Le document architectural fourni avec la demande insiste sur la convergence des usages autour de la distribution prédictive, sans confondre génération, scoring et apprentissage. Cette distinction est déjà représentée dans le registre computationnel du dépôt : il faut le vérifier et le réutiliser, pas créer un graphe concurrent.

### 1.3 Understand et Build sont deux parcours primaires indépendants

- **Understand** explique ce que fait le modèle, pourquoi et comment l'interpréter.
- **Build** apprend à implémenter, tester et entraîner un petit GPT.
- **Deepen** accueille dérivations, variantes et détails avancés.
- **Practice & experiment** accueille exercices, expériences et auto-évaluations des deux parcours.

Les liens Understand ↔ Build sont contextuels, pas des prérequis obligatoires. Les exercices des leçons restent dans leurs pages dédiées de Practice & experiment ; les leçons principales ne doivent pas accumuler les questions et corrigés.

### 1.4 Améliorer avant d'ajouter

Avant de créer une page, un champ, une taxonomie, une visualisation ou un outil :

1. chercher le contenu et le mécanisme existants ;
2. identifier leur propriétaire canonique ;
3. déterminer si le problème vient du contenu, de la hiérarchie, de la navigation ou du rendu ;
4. préférer une correction locale et réutiliser les contrats existants ;
5. créer une nouvelle structure seulement si un besoin distinct et démontré ne peut être exprimé par l'existant.

### 1.5 Préserver l'information et les nuances

Aucune réorganisation ne doit perdre silencieusement définition, hypothèse, limite, exemple, figure, référence, exercice ou destination utile. Une information avancée déplacée doit rester accessible depuis le point où elle devient utile. Une simplification ne doit pas rendre fausse une affirmation auparavant correctement qualifiée.

---

## 2. État de départ : acquis à préserver

Le dépôt possède déjà une architecture pédagogique et éditoriale substantielle. Il ne faut pas repartir de zéro.

| Élément | État connu dans les sources consultées | Conséquence |
|---|---|---|
| Parcours Understand | 9 étapes dans le registre guidé | Auditer transitions et compréhension avant de changer nombre ou ordre |
| Contrats de leçons | 20 leçons centrales recensées dans l'audit du 20 novembre | Améliorer les contrats existants, ne pas créer un second inventaire |
| Distinctions transversales | 11 distinctions reliées à des exercices communs à plusieurs étapes | Vérifier leur utilité sans dupliquer les exercices |
| Carte et plan de révision | Carte conceptuelle, étapes, ressources, questions et résultats FR/EN | Contrôler leur lisibilité et cohérence avec le parcours textuel |
| Graphe computationnel | Registre dédié dans data/computational-graph.yml | Réutiliser les objets et opérations existants |
| Registre de concepts | data/concepts.yml avec définitions bilingues, importance, domaines et ressources | Améliorer qualité des relations, pas créer une ontologie parallèle |
| Métadonnées de pages | Contrat LLM-LAB-PAGE-MAP v1 et vocabulaire contrôlé | Corriger valeurs et usages ; ne pas exposer les champs techniques |
| Gabarits et archétypes | Templates souples et familles de pages existants | Converger sur une expérience cohérente sans uniformiser toutes les pages |
| Exercices | Pages dédiées dans Practice & experiment | Maintenir la séparation explication / accumulation d'exercices |
| Bilinguisme | Pages, registres et navigation FR/EN | Vérifier la parité sémantique et fonctionnelle, pas seulement la présence de fichiers |
| Validation | Builds, liens, audits éditoriaux et vérifications rendues ciblées | Compléter par des tests d'usage et d'apprentissage |

Références de cet état : learning-path.md, understand-path-overview.md, audits/understand-lesson-contracts-2026-11-20.md, content-section-mapping.md, page-metadata-schema.md et project-status.md. Ces constats sont datés : vérifier les évolutions ultérieures avant toute action.

---

## 3. Registre des améliorations possibles

Les pistes sont des hypothèses à examiner. **À auditer** signifie que le besoin ou son étendue doit être confirmé avant modification. **Conditionnel** signifie que l'amélioration n'est pertinente que si un cas d'usage réel la justifie.

### A. Contenu scientifique et modèle mental

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| C01 | Vérifier que le fil rouge relie texte, tokens, IDs, embeddings, états, blocs, logits et distribution | Suivre la transformation d'un même objet plutôt que mémoriser des pages isolées | Un exemple est traçable entre étapes ; chaque changement de représentation est nommé | P0 |
| C02 | Maintenir la distinction entre ordre de lecture et ordre réel du calcul | Éviter de croire que les états contextualisés finaux précèdent les Q/K/V qui contribuent à les produire | Les pages disent que Q/K/V sont calculés dans les blocs à partir de leurs états d'entrée, même si leur étude vient plus tard | P0 |
| C03 | Vérifier la chaîne interne d'un bloc Transformer | Relier projections, scores, masque, normalisation, agrégation, projection, résidus, normalisation et MLP | Le schéma suit une convention explicite et ne saute aucune transformation déterminante | P0 |
| C04 | Renforcer les distinctions token / ID / embedding / état caché / logit / probabilité / token sélectionné | Éviter les confusions entre objets de types et rôles différents | Des questions de discrimination et de transfert détectent les confusions ; terminologie stable | P0 |
| C05 | Vérifier la cohérence entre contexte, préfixe, position prédite et cible observée | Comprendre génération, scoring et teacher forcing | L'apprenant identifie le préfixe conditionnant chaque prédiction et sa cible | P0 |
| C06 | Consolider pθ(xₜ \| x<ₜ) et ses trois usages | Ne pas présenter trois mécanismes prédictifs indépendants | Les branches partent de la même distribution ; leurs actions et effets sur les paramètres sont distingués | P0 |
| C07 | Vérifier logits versus probabilités | Ne pas traiter des scores non normalisés comme des probabilités | Exemple sur softmax, décalage constant des logits et non-négativité/somme à un des probabilités | P1 |
| C08 | Clarifier les deux axes de softmax dans les tenseurs multi-positions | Ne pas confondre normalisation sur vocabulaire et sur positions | Axes, dimensions et objets normalisés sont indiqués | P0 |
| C09 | Vérifier distribution prédictive, entropie et surprisal | Interpréter incertitude et score d'un événement sans confondre les quantités | Exemple numérique commun permettant de calculer et comparer les notions | P1 |
| C10 | Clarifier likelihood, log-likelihood, NLL, cross-entropy et loss agrégée | Distinguer quantité, signe et granularité | Chaque page indique unité (token, séquence, batch), signe, réduction et convention | P0 |
| C11 | Vérifier perplexité et limites d'interprétation | Ne pas la présenter comme taux d'erreur ou qualité universelle | Interprétation conditionnée au tokenizer, corpus, segmentation et protocole | P1 |
| C12 | Consolider teacher forcing, décalage entrée/cible, causalité et masques | Comprendre le passage de la prédiction à l'apprentissage | L'apprenant reconstruit paires entrée/cible et explique ce que chaque masque autorise | P0 |
| C13 | Clarifier gradients, rétropropagation, optimiseur et mise à jour des paramètres | Éviter de croire que forward ou gradient modifie directement les poids | L'ordre loss → backward → gradients → optimizer step est expliqué avec ses conditions | P0 |
| C14 | Vérifier préentraînement, fine-tuning, instruction tuning et ICL | Distinguer changement des poids et changement du contexte | Comparaison de ce qui change, reste fixe, des données et de l'objectif | P1 |
| C15 | Vérifier partage des poids entrée/sortie, biais et conventions d'architecture | Ne pas présenter une variante comme universelle | Les affirmations sont qualifiées selon architecture ou modèle | P2 |
| C16 | Rendre visibles les hypothèses du modèle pédagogique de référence | Ne pas généraliser automatiquement le GPT decoder-only à tous les LLM | Les simplifications importantes sont nommées lorsqu'elles affectent l'interprétation | P1 |
| C17 | Distinguer mécanisme et qualité linguistique | Ne pas confondre démonstration mécanique et modèle utile | Le site distingue poids aléatoires, paramètres appris et qualité des sorties | P1 |
| C18 | Consolider les limites : hallucination, calibration, connaissance, contexte, biais et évaluation | Ne pas assimiler prédiction à vérité ou raisonnement garanti | Limites reliées aux mécanismes concernés, sans généralisation abusive | P1 |

### B. Progression pédagogique et transitions

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| P01 | Tester la nécessité et l'utilité de chaque étape | Éviter une étape correcte mais redondante ou mal placée | L'apprenant explique la question de l'étape et ce qu'elle prépare | P0 |
| P02 | Expliciter les transitions plutôt que multiplier les prérequis | Donner une raison de poursuivre sans créer un DAG rigide | Chaque transition répond à « acquis ? », « manque ? », « pourquoi la suite ? » | P0 |
| P03 | Contrôler les retours en arrière nécessaires | Détecter un concept introduit trop tôt ou insuffisamment préparé | Les retours d'un pilote sont relevés et classés ; une refonte exige un motif récurrent | P1 |
| P04 | Vérifier l'équilibre entre aperçu et explication détaillée | Montrer tôt le système global sans noyer le débutant | L'overview permet de raconter le système brièvement ; les leçons portent les explications substantielles | P0 |
| P05 | Vérifier que les notions importantes sont introduites avant leur première utilisation exigeante | Éviter les prérequis silencieux | Les usages anticipés reçoivent une intuition suffisante et un lien canonique | P0 |
| P06 | Identifier les prérequis mathématiques strictement nécessaires | Éviter un cursus mathématique préalable disproportionné | Chaque prérequis est justifié par une tâche de compréhension ; le reste reste facultatif | P1 |
| P07 | Renforcer les transitions prédiction → scoring et training | Comprendre comment une cible observée remplace le token choisi, puis pourquoi la loss introduit les gradients | L'apprenant explique les changements de contexte, d'objectif et d'action | P0 |
| P08 | Distinguer boucle de génération et boucle d'entraînement | Ne pas confondre dynamique d'inférence et optimisation | Schémas séparés ; paramètres fixes en inférence, mis à jour par l'optimiseur en training | P0 |
| P09 | Vérifier l'intégration de prefill et decode | Comprendre l'exécution réelle de génération | L'apprenant distingue traitement initial du prompt et pas de décodage ; KV cache présenté comme optimisation facultative | P1 |
| P10 | Distinguer ICL, context engineering, RAG, mémoire et fine-tuning | Ne pas traiter ces mécanismes comme synonymes | L'apprenant distingue rôle du modèle, application, récupération, contexte et paramètres | P0 |
| P11 | Tester le passage théorie → Build sans dépendance obligatoire | Faciliter le transfert vers le code sans rendre Understand incomplet | Les liens Build annoncent ce qu'ils permettent de construire ou vérifier | P1 |
| P12 | Vérifier la place des pages d'architecture, d'histoire et de limites | Enrichir sans interrompre le fil central | Le statut essentiel, complémentaire ou facultatif est compréhensible | P1 |
| P13 | Ajouter des synthèses uniquement lorsqu'une relation nouvelle doit être consolidée | Éviter les récapitulatifs répétitifs | La synthèse relie des concepts, elle ne répète pas les introductions | P2 |
| P14 | Vérifier charge cognitive et longueur des étapes | Prévenir les ruptures et la fatigue | Temps, retours, fatigue et points de rupture observés ; pas de durée arbitraire imposée | P1 |

### C. Structure et squelette des pages

Le système de templates est volontairement souple. Ces pistes ne constituent pas un gabarit rigide à appliquer à chaque page.

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| S01 | Vérifier que le titre nomme l'objet ou la question | S'orienter immédiatement | Titre précis, distinct du nom de section et compréhensible hors contexte | P1 |
| S02 | Orienter l'ouverture vers le problème scientifique | Éviter le méta-discours générique | Les premières lignes expliquent problème, idée centrale ou phénomène | P0 |
| S03 | Faire apparaître l'intuition avant la formalisation lorsque pertinent | Construire le modèle mental avant la notation | Intuition correcte et reliée explicitement à la définition | P1 |
| S04 | Introduire chaque notation avant son emploi | Éviter symboles non définis ou ambigus | Sens, domaine, dimension et convention explicités si nécessaires | P0 |
| S05 | Interpréter les équations, pas seulement les afficher | Transformer la formule en explication | Termes et opérations reliés à leur sens et à un cas concret | P0 |
| S06 | Harmoniser conventions de tenseurs et dimensions entre pages liées | Réduire les changements de notation | Conventions explicites et cohérentes ; différences signalées | P1 |
| S07 | Placer un exemple calculé près du mécanisme | Rendre le mécanisme vérifiable | Exemple petit, résultat contrôlable et interprétation fournie | P0 |
| S08 | Réutiliser une famille d'exemples entre pages lorsque cela aide | Faciliter les transitions | Continuité utile sans répétition artificielle | P1 |
| S09 | Distinguer intuition, définition, propriété, hypothèse et limite | Éviter qu'une analogie soit prise pour une définition | Statut des affirmations clair ; limites des analogies explicites | P1 |
| S10 | Déplacer les développements avancés hors du premier parcours sans les perdre | Préserver le rythme et la profondeur | Qualifications essentielles conservées ; lien Deepen contextuel et fonctionnel | P0 |
| S11 | Vérifier la clôture de page | Aider à choisir la prochaine action | Seules les actions utiles sont proposées : continuer, pratiquer, construire, approfondir, explorer | P1 |
| S12 | Réduire les sections qui décrivent le site plutôt que le sujet | Éliminer le méta-discours sans valeur | Test de suppression éditoriale appliqué aux introductions et conclusions | P1 |
| S13 | Éviter sections vides ou répétées imposées par un template | Préserver la souplesse | Chaque section répond à une question propre à la page | P1 |
| S14 | Contrôler densité des callouts | Éviter fragmentation et perte de hiérarchie | Chaque encadré a une fonction distincte et non redondante | P2 |
| S15 | Préserver références, figures, légendes et crédits lors des déplacements | Ne pas perdre provenance et valeur pédagogique | Provenance, droits et source vérifiables pour chaque figure | P0 |

### D. Forme, visualisations et ergonomie

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| F01 | Vérifier lisibilité des schémas à leur taille réelle | Éviter les diagrammes illisibles | Textes, flèches et légendes lisibles sur mobile et desktop | P0 |
| F02 | Choisir des visualisations qui expliquent une transformation ou comparaison | Éviter l'illustration décorative | Chaque visuel répond à une question et se comprend sans narration orale | P1 |
| F03 | Stabiliser couleurs et formes sémantiques | Réduire l'effort de décodage | Catégories constantes ; aucune information portée par la couleur seule | P1 |
| F04 | Vérifier textes alternatifs et légendes | Rendre les figures accessibles et compréhensibles hors contexte | Alternative informative, légende précise, figure reliée au texte | P0 |
| F05 | Limiter schémas redondants et Mermaid par défaut | Choisir le format le plus lisible | Comparer diagramme, figure, tableau, animation et texte selon le besoin | P2 |
| F06 | Ajouter des interactions seulement si elles servent une manipulation intellectuelle | Éviter interactivité décorative | L'apprenant fait varier une entrée, prédit et interprète ; alternative statique disponible | P1 |
| F07 | Vérifier tableaux, équations et code sur petit écran | Éviter débordements et perte de contenu | Pas de débordement imprévu à 390 px | P0 |
| F08 | Réduire les repères de navigation concurrents | Préserver la hiérarchie | Breadcrumb, contexte du parcours et navigation locale ont des rôles distincts | P0 |
| F09 | Contrôler contraste, focus, états interactifs et ordre clavier | Ne pas dépendre de la souris | Parcours clavier complet, focus visible et critères d'accessibilité vérifiés | P0 |
| F10 | Contrôler poids et chargement des figures/widgets | Éviter dégradation de l'expérience | Chargement observé, alternative statique et dégradation gracieuse | P2 |
| F11 | Rendre les exemples de code lisibles et copiables | Faciliter le transfert vers Build | Langage, formatage, contexte, sortie attendue et lien vers code complet | P1 |
| F12 | Vérifier les droits des figures externes avant de les remplacer ou supprimer | Éviter perte pédagogique et attribution insuffisante | Provenance, droits, licence et alternative documentés avant décision | P0 |

### E. Navigation et découverte

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| N01 | Rendre le point d'entrée et la prochaine action évidents | Éviter que le débutant doive comprendre l'architecture du dépôt | Accès clair depuis l'accueil à Understand, Build, Practice et Deepen | P0 |
| N02 | Vérifier cohérence carte, route guidée, sidebar et review path | Éviter des représentations contradictoires | Même étapes, pages et rôles ; usages propres à chaque vue explicités | P0 |
| N03 | Distinguer breadcrumb, contexte du parcours et suggestions précédente/suivante | Éviter doublons et confusion | Chaque repère répond à une question différente | P0 |
| N04 | Réduire les choix simultanés sur les pages d'entrée | Faciliter la décision | Options essentielles visibles ; branches secondaires accessibles sans rivaliser | P1 |
| N05 | Vérifier accès leçon ↔ page d'exercices dédiée | Rendre la pratique trouvable sans encombrer le cours | Lien contextualisé, bon exercice et retour vers le concept | P0 |
| N06 | Vérifier retour depuis corrigés et exercices transversaux | Éviter les culs-de-sac | Le retour mène à la bonne étape ou ancre | P1 |
| N07 | Donner aux liens des libellés informatifs | Rendre la destination prévisible | Le lien annonce la question ou le mécanisme cible | P1 |
| N08 | Vérifier découverte par concept et synonymes utiles | Retrouver une notion sans connaître le titre de page | Les concepts canoniques conduisent à la bonne explication | P2 |
| N09 | Vérifier pages isolées ou orphelines | Rendre le contenu utile découvrable | Chaque ressource importante a un accès justifié ; pas de liens artificiels | P1 |
| N10 | Vérifier liens FR/EN et changement de langue | Préserver le contexte de lecture | La page équivalente et, si possible, l'ancre correspondante sont ouvertes | P0 |
| N11 | Rendre le caractère facultatif des ressources évident | Ne pas faire passer l'exploration pour un prérequis | Le rôle core/optional est compréhensible sans exposer les codes internes | P1 |

### F. Métadonnées, taxonomies et sémantique

Le contrat existant est la référence. Ces pistes visent l'exactitude et l'exploitation des données, pas l'ajout automatique de champs.

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| M01 | Auditer type, destination, topic, level, language et status | Éviter des filtres, cartes et vues erronés | Valeurs permises et cohérentes avec rôle et langue | P0 |
| M02 | Vérifier parité des tags FR/EN | Former une même unité éditoriale bilingue | Même topic, destination, niveau et type ; IDs propres à la langue | P0 |
| M03 | Vérifier scope, purpose et summary selon leurs sémantiques | Éviter les paraphrases interchangeables | Scope = frontière ; purpose = capacité ; summary = contenu trouvé, si utile | P1 |
| M04 | Vérifier suggested_route.previous/next | Éviter les prérequis implicites | Transition pédagogique recommandée, jamais hiérarchie conceptuelle | P0 |
| M05 | Vérifier hierarchy.parents/children | Garder une hiérarchie conceptuelle valide | Inclusion/décomposition réelle ; dépendances de calcul dans le graphe computationnel | P0 |
| M06 | Vérifier related et la réciprocité utile | Éviter les relations contextuelles perdues | Connexion expliquée et découvrable, sans hiérarchie artificielle | P1 |
| M07 | Vérifier importance et domaines des concepts | Donner un sens stable à la centralité et aux catégories | Valeurs justifiées et cohérentes avec domaines et concepts canoniques | P1 |
| M08 | Vérifier que les identifiants techniques ne sont jamais visibles | Séparer métadonnées et contenu apprenant | Aucun tag type:, destination:, topic:, level:, language:, status: ni ID interne affiché | P0 |
| M09 | Traiter les termes scientifiques comme concepts, non comme tags décoratifs | Éviter nuages de tags et taxonomies parallèles | Définitions et relations viennent du registre de concepts ; emphase en contexte | P1 |
| M10 | Vérifier ancres, identifiants et références après réorganisation | Éviter liens cassés et vues orphelines | Liens, fragments, générateurs et cartes résolvent leurs cibles | P0 |
| M11 | Justifier tout champ supplémentaire avant extension du schéma | Limiter coût de maintenance | Cas d'usage, propriétaire, vocabulaire, migration et validation démontrés | P1 |

### G. Bilinguisme et terminologie

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| L01 | Auditer parité conceptuelle FR/EN, pas seulement présence des fichiers | Éviter nuances ou exemples manquants | Claims, hypothèses, limites, figures, exercices et références équivalents | P0 |
| L02 | Stabiliser termes techniques canoniques et traductions | Améliorer cohérence, liens et recherche | Glossaire et concept registry utilisés ; variantes justifiées | P1 |
| L03 | Contrôler équations et conventions dans les deux langues | Préserver le sens scientifique | Définitions et hypothèses identiques ; différences de présentation signalées | P0 |
| L04 | Vérifier que les exemples traduits conservent leur sens | Éviter exemples dépendant de la langue ou du tokenizer | Adaptation ou limites explicites | P1 |
| L05 | Vérifier navigation linguistique des pages et exercices | Éviter perte de contexte | Liens croisés valides ; absence de traduction signalée honnêtement | P1 |

### H. Exercices, auto-évaluation et transfert

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| E01 | Vérifier couverture des objectifs par les exercices existants | Ne pas confondre explication et compréhension vérifiée | Chaque objectif essentiel a une activité pertinente ou une absence justifiée | P0 |
| E02 | Varier rappel, calcul, interprétation, prédiction et transfert | Dépasser la simple restitution de définitions | Activités couvrant plusieurs opérations intellectuelles | P1 |
| E03 | Ajouter des cas contrefactuels là où ils discriminent les modèles mentaux | Tester la compréhension du mécanisme | L'apprenant prédit ce qui change et reste invariant, puis justifie | P0 |
| E04 | Vérifier que les corrigés expliquent le raisonnement | Corriger la conception, pas seulement donner une réponse | Étapes, hypothèses et erreurs plausibles expliquées | P1 |
| E05 | Vérifier progression de difficulté | Éviter exercices trop difficiles ou triviaux | Niveau aligné sur l'étape et prérequis annoncés naturellement | P1 |
| E06 | Contrôler exercices transversaux | Renforcer une distinction sans répétition inutile | Chaque association multi-étape a une raison et une consigne cohérente | P1 |
| E07 | Maintenir la séparation cours / exercices | Faire grandir la pratique sans polluer le parcours | Leçon liée à sa page dédiée ; questions et corrigés restent dans Practice | P0 |
| E08 | Vérifier exercices de reconstruction de bout en bout | Tester le modèle mental intégré | L'apprenant reconstruit entrée → distribution → trois usages | P1 |
| E09 | Vérifier indices gradués et solutions volontaires | Soutenir l'auto-correction | Indices utiles ; solution complète ouverte à la demande | P2 |
| E10 | Vérifier calculs des visualisations interactives indépendamment | Éviter d'enseigner une erreur | Résultats comparés à un calcul de référence ; hypothèses affichées | P0 |

### I. Validation et qualité de preuve

| ID | Amélioration possible | Bénéfice attendu | Critère de vérification | Priorité |
|---|---|---|---|---|
| V01 | Exécuter le pilote complet avec un novice réel | Détecter les difficultés spontanées | Protocole, contexte, version du site et observations consignés | P0 |
| V02 | Conserver les premières réponses avant indices/corrigés | Distinguer compréhension autonome et assistée | Réponse initiale, aide, réponse finale et confiance séparées | P0 |
| V03 | Tester reconstruction des transitions, pas seulement définitions | Vérifier le modèle mental intégré | L'apprenant explique les objets transmis d'une étape à l'autre | P0 |
| V04 | Distinguer erreur scientifique, prérequis, rédaction, navigation, interaction et accessibilité | Corriger la bonne couche | Cause hypothétique et niveau de confiance consignés | P0 |
| V05 | Répéter auprès de profils différents avant généralisation | Éviter de surinterpréter un seul participant | Profils et limites décrits ; conclusions proportionnées | P1 |
| V06 | Effectuer revue visuelle desktop/mobile et clavier | Vérifier le rendu réel | Trajets documentés en FR/EN, tailles représentatives et clavier | P0 |
| V07 | Vérifier liens externes, citations et droits | Maintenir fiabilité et provenance | Sources retrouvables, références exactes et droits signalés | P1 |
| V08 | Automatiser seulement les invariants stables | Éviter scripts et workflows fragiles | Tests ciblés sur schémas, destinations, parité, liens et visibilité | P1 |
| V09 | Vérifier les régressions après refonte | Éviter de casser une autre route | Build, liens, ancres, clavier et pages liées vérifiés | P0 |
| V10 | Distinguer présence, qualité et maîtrise | Ne pas confondre publication et apprentissage | Statuts séparés : disponible, techniquement validé, pédagogiquement observé | P0 |

---

## 4. Priorisation consolidée

Les priorités organisent l'investigation ; elles n'impliquent pas de tout réaliser.

### P0 — Justesse et obstacles fondamentaux

1. Cohérence scientifique du fil rouge et des types d'objets.
2. Distinction ordre computationnel / ordre pédagogique.
3. Chaîne commune prédiction → génération, scoring et apprentissage.
4. Distinction préfixe, cible observée, token sélectionné et paramètres.
5. Teacher forcing, masques, loss, gradients et mise à jour.
6. Transitions entre étapes et absence de prérequis implicites.
7. Métadonnées exactes, non visibles et bilingues.
8. Navigation de base, liens d'exercices, retour et changement de langue.
9. Lisibilité équations/figures/interactions sur mobile et au clavier.
10. Préservation des références et contenus pendant les refontes.
11. Pilote apprenant réel et revue rendue, sans prétendre qu'ils ont déjà eu lieu.

### P1 — Efficacité pédagogique

- Qualité des exemples et continuité du fil rouge.
- Intuition, notation, dimensions et interprétation des équations.
- Distinctions ICL / context engineering / RAG / fine-tuning.
- Hypothèses et limites du GPT de référence.
- Progression de difficulté et transfert des exercices.
- Cohérence terminologique et parité FR/EN.
- Découverte par concept et liens contextuels.
- Cohérence des figures et conventions visuelles.

### P2 — Améliorations conditionnelles

- Interactions et visualisations avancées.
- Synthèses supplémentaires.
- Recherche sémantique et filtres de découverte.
- Optimisations de performance des ressources.
- Variantes architecturales et détails non essentiels au premier parcours.

Ne pas promouvoir une piste P2 en P0 parce qu'elle est techniquement intéressante ou facile à automatiser.

---

## 5. Contrats de qualité pour toute modification

### 5.1 Contrat pédagogique

- Quel problème de compréhension ou de navigation est visé ?
- Pour quel profil ou quelle étape ?
- Quelle capacité l'apprenant devrait-il acquérir ou exercer ?
- Pourquoi le contenu ou la navigation actuelle ne suffit-il pas ?
- Comment vérifier le bénéfice ?

### 5.2 Contrat scientifique

- Quelle affirmation ou relation est modifiée ?
- Quelles hypothèses, conventions et limites s'appliquent ?
- Quelle source ou démonstration la soutient ?
- Le changement reste-t-il vrai dans le périmètre annoncé ?
- Les pages voisines utilisent-elles les mêmes objets et notations ?

### 5.3 Contrat éditorial et structurel

- Quelle page est propriétaire du contenu ?
- Le changement relève-t-il de Understand, Build, Deepen ou Practice ?
- Est-ce une explication canonique, un rappel, une synthèse ou un lien ?
- Quel contenu est conservé, déplacé, fusionné ou retiré ?
- Les pages FR et EN sont-elles mises à jour ensemble ?

### 5.4 Contrat de métadonnées

- Les champs existants suffisent-ils ?
- Les valeurs respectent-elles page-metadata-schema.md ?
- Les relations sont-elles du bon type ?
- Les identifiants et tags restent-ils non visibles ?
- Les générateurs et vues dérivées restent-ils cohérents ?

### 5.5 Contrat de validation

- Build et contrôles de liens passent-ils ?
- Pages rendues lisibles en FR et EN ?
- Clavier et petits écrans vérifiés pour les éléments concernés ?
- Changement testé sur une tâche apprenant si le problème est pédagogique ?
- Limites de validation explicitement indiquées ?

---

## 6. Méthode d'audit recommandée

Ne pas auditer toutes les pages dans une passe superficielle. Réutiliser les audits et issues existants.

### Lot 1 — Architecture et transitions

Comparer guided-route.yml, learning-path.md, carte, review path, sidebar et métadonnées. Examiner chaque transition des neuf étapes et les trois usages du prédicteur. Réutiliser #130, #575, #971 et les audits de novembre.

**Livrable :** tableau des transitions avec rôle, acquis, question suivante, page canonique et preuve.

### Lot 2 — Audit de fond par familles de pages

Traiter des groupes cohérents : entrée et texte ; représentations et position ; Transformer, Q/K/V et masques ; logits, probabilités et entropie ; génération et contexte ; scoring ; loss, gradients et training loop.

Pour chaque groupe : justesse, portée des affirmations, exemples, notations, frontières de responsabilité, contenu à préserver, liens vers exercices et approfondissements.

**Livrable :** écarts confirmés et corrections proposées, pas une réécriture systématique.

### Lot 3 — Squelette, rédaction et forme

Comparer ouverture, sections, exemples, figures, limites et clôtures. Évaluer densité, répétitions, méta-discours, callouts et visualisations. Vérifier rendu desktop/mobile/clavier.

**Livrable :** corrections communes seulement si un motif récurrent est démontré ; sinon corrections locales.

### Lot 4 — Métadonnées et graphes

Auditer tags et champs, relations suggested_route / hierarchy / related, cohérence pages-concepts-domaines-nœuds computationnels, pages orphelines, liens cassés et identifiants exposés.

**Livrable :** anomalies de données et corrections ciblées, sans extension de schéma par défaut.

### Lot 5 — Exercices et validation apprenant

Cartographier objectifs et exercices ; vérifier rappel, calcul, interprétation, prédiction et transfert ; exécuter le protocole de parcours complet ; distinguer observations et interprétations.

**Livrable :** compte rendu du pilote, propositions hiérarchisées et limites de preuve.

---

## 7. Tableau de suivi

Ce tableau pilote le registre. Il ne remplace ni les issues GitHub ni les inventaires de pages.

| Axe | État initial | Prochaine preuve utile | Règle de décision |
|---|---|---|---|
| Contenu scientifique | Audits de fond et graphe computationnel existants | Vérifier transitions et contre-exemples | Corriger les erreurs ou ambiguïtés démontrées |
| Progression | 9 étapes structurées | Parcours novice sans coaching | Ne pas réordonner sur intuition seule |
| Squelette | Templates souples et contrats | Audit comparatif de groupes de pages | Corriger motifs récurrents, préserver exceptions utiles |
| Forme | Design system et contrôles rendus partiels | Revue desktop/mobile/clavier | Pas d'ornement sans gain de compréhension |
| Navigation | Carte, sidebar, review path et liens contextuels | Trajets réels FR/EN | Une fonction claire par repère |
| Métadonnées | Schéma et registres contrôlés | Audit d'intégrité et de visibilité | Réutiliser le schéma avant extension |
| Exercices | Pages dédiées et distinctions transversales | Couverture objectifs/exercices et pilote | Modifier seulement si manque constaté |
| Bilinguisme | Structure FR/EN en place | Revue de parité sémantique et fonctionnelle | Même savoir, exemples adaptés si nécessaire |
| Preuve d'apprentissage | Protocoles écrits, pilote complet à exécuter | Session réelle et compte rendu | Ne pas confondre build, lecture experte et maîtrise |

---

## 8. Hors périmètre et garde-fous

Ce registre ne justifie pas, à lui seul :

- une refonte générale de navigation ou une dixième étape ;
- un nouveau système de templates ou une taxonomie parallèle ;
- un champ de métadonnées supplémentaire ;
- un nouveau graphe ou une nouvelle source de vérité ;
- une page de synthèse pour chaque concept ;
- un workflow GitHub par notion ou par page ;
- des exercices dupliqués dans les leçons ;
- une visualisation interactive pour chaque mécanisme ;
- une réécriture des pages validées sans anomalie reproductible.

Les améliorations propres à Build, à l'ingestion des sources, aux références ou à l'architecture générale restent dans leurs documents et issues propriétaires. Ce registre note seulement leurs effets sur l'expérience Understand lorsqu'ils sont pertinents.

---

## 9. Références et coordination

- [Learning path](learning-path.md) — ordre conceptuel et séparation Understand / Build.
- [Guided route](../data/guided-route.yml) — source machine-readable des neuf étapes.
- [Understand path overview](understand-path-overview.md) — état, navigation et vérifications rendues.
- [Audit des contrats des leçons du 20 novembre](audits/understand-lesson-contracts-2026-11-20.md) — conservation et frontières par leçon.
- [Content-section mapping](content-section-mapping.md) — responsabilité des pages.
- [Page metadata schema](page-metadata-schema.md) — vocabulaire et relations des métadonnées.
- [Flexible page-template system](page-template-system.md) — composition souple des pages.
- [Reader experience and editorial method](reader-experience-and-editorial-method.md) — progression, densité et préservation.
- [Information architecture](information-architecture.md) — propriétaires canoniques et projections.
- [Computational graph](../data/computational-graph.yml) — objets et opérations de calcul.
- [Concept registry](../data/concepts.yml) — définitions et relations conceptuelles.
- [#130](https://github.com/JM-Brun/llm-lab/issues/130), [#575](https://github.com/JM-Brun/llm-lab/issues/575), [#971](https://github.com/JM-Brun/llm-lab/issues/971), [#447](https://github.com/JM-Brun/llm-lab/issues/447) — coordination et validation existantes.

**Règle de maintenance :** mettre à jour ce registre lorsqu'un audit confirme, invalide ou clôt une piste structurante. Les issues GitHub restent la source du statut opérationnel. Ne pas recopier ici l'historique détaillé des PR ni transformer chaque ligne en issue indépendante.
