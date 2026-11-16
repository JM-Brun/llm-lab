# Revue de source — Mingdi Fan, “Compression Is Intelligence”

**Source :** [PhilArchive, MINCII-3](https://philarchive.org/archive/MINCII-3) · [historique des versions](https://philarchive.org/versions/MINCII-3) · [extraction structurée](../../data/extractions/fan-compression-intelligence-2026.yml)

**Référence affichée dans le PDF :** Mingdi Fan, “Compression Is Intelligence: The Common Ground of Positive Subjectivity and Negative Subjectivity — With a Discussion on the Nature of Intelligence”, prépublication PhilArchive, identifiant MINCII-3. L’historique PhilArchive indique un dépôt de la version archivée le 17 mai 2026. Le PDF complet (9 sections, références comprises) a été consulté le 16 novembre 2026.

**Statut :** texte intégral inspecté ; références principales identifiées ; pas de reproduction des expériences des travaux cités. Aucun droit de republication du texte, des figures ou des tableaux n'a été établi : lien et reformulation seulement.

## 1. Question et thèse de l'auteur

Comment des systèmes très différents — humains et modèles de langage — peuvent-ils être qualifiés d'intelligents ? Fan propose de les comprendre comme deux stratégies de « compression effective » des régularités du monde :

- **Subjectivité positive :** compression narrative de l'expérience en un centre relativement unifié, le « je ». La sélection est fortement contrainte par le corps, l'évolution, la mortalité, la mémoire et les besoins d'action ; elle privilégierait les structures causales et les régularités pertinentes.
- **Subjectivité négative :** compression probabiliste du langage en une distribution conditionnelle. L'objectif de pré-entraînement par cross-entropy réduit l'erreur prédictive et peut retenir des régularités structurées comme des régularités statistiques plus superficielles.
- **Subjectivité grise / grey-body-ness :** position intermédiaire proposée pour des systèmes dont les objectifs de compression pourraient combiner modélisation probabiliste globale et sélection plus structurée à l'échelle des tâches, particulièrement en cas d'interaction sensorimotrice.

La thèse centrale est que l'intelligence ne requiert pas nécessairement subjectivité, conscience, intentionnalité ou ancrage sémantique. Fan distingue l'efficacité **fonctionnelle** (réussir une tâche de compression et généraliser) de l'efficacité **structurelle** (représentations parcimonieuses et recombinables), puis réserve le terme « compréhension » à la seconde.

## 2. Architecture argumentative du texte

| Partie | Fonction | Idée centrale |
|---|---|---|
| §1 | Cadrage | La théorie de Shannon mesure la quantité d'information, pas la qualité sémantique ou structurelle des régularités |
| §2 | Généalogie | Théorie algorithmique de l'information, complexité effective, épiplexité, apprentissage profond, neurosciences et algèbre |
| §3 | Stratégie A | La mémoire et le récit autobiographique compressent l'expérience en nœuds et chaînes causales |
| §4 | Stratégie B | Le modèle de langage ajuste une distribution pour réduire la cross-entropy et capter des régularités de séquences |
| §5 | Comparaison | Les deux stratégies sont différentes sans que l'une soit simplement une version déficiente de l'autre |
| §6 | Définitions | Intelligence, compréhension, subjectivité, conscience et intentionnalité sont dissociées |
| §7 | Prédictions | Quatre propositions empiriquement testables sont avancées |
| §8 | Extension | Une stratégie mixte et conditionnelle est proposée pour la subjectivité grise |
| §9 | Conclusion | Les deux stratégies appartiennent à une même famille de compression effective |

## 3. Apports utiles à LLM Lab

1. **Une distinction structurante entre compression prédictive et compression sélective.** Elle prolonge les ressources déjà présentes sur la prédiction du prochain token, la cross-entropy et le codage arithmétique, en posant une question différente : quelles régularités un système conserve-t-il et à quelles contraintes répond cette sélection ?
2. **Une passerelle entre information et représentation.** La source relie l'objectif probabiliste à la question de la structure interne, sans se limiter à la longueur de code.
3. **Une distinction pédagogique entre performance et parcimonie.** Réussir une tâche et disposer d'une représentation compacte, réutilisable et recombinable ne sont pas la même propriété.
4. **Des prédictions falsifiables à discuter.** Effets du raisonnement explicite, qualité/curation des données, débruitage, découverte autonome de définitions et comparaison des représentations pré-entraînées et alignées.
5. **Une occasion d'enseigner la frontière entre résultat formel, analogie et hypothèse ontologique.** C'est probablement la contribution pédagogique la plus précieuse pour un laboratoire d'expérimentation.

## 4. Audit scientifique et limites

### 4.1 Shannon n'est pas réfuté

La théorie de Shannon répond à un problème précis : les limites de codage pour une source probabiliste. Elle ne prétend pas mesurer la signification, la compréhension ou la qualité des modèles internes. Dire qu'elle ne tranche pas une question sémantique ou ontologique ne constitue donc pas une limitation de son résultat dans son domaine propre.

### 4.2 Épiplexité : ne pas remplacer la définition formelle par l'intuition

Fan mobilise l'épiplexité de Finzi et al. (2026) pour caractériser l'information structurée accessible sous contraintes de calcul. Le travail primaire définit l'épiplexité comme la longueur du programme optimal \(P^*\) qui minimise un MDL à temps borné ; l'entropie à temps borné correspond au coût résiduel attendu des données sous ce programme. La quantité dépend donc de la classe de programmes, du budget de calcul et de l'observateur. Finzi et al. précisent également que l'épiplexité est une mesure d'information et non une garantie de généralisation OOD pour une tâche donnée. Le papier de Fan emploie ensuite parfois « contenu d'information structurée » comme raccourci intuitif : ce raccourci ne doit pas remplacer la définition.

Le préprint arXiv:2601.03220 a une version révisée déposée le 16 mars 2026 ; le dossier cite le même identifiant arXiv, mais la date et la version effectivement consultée doivent rester explicites. L'épiplexité est un cadre récent, dépendant de choix formels et de ressources de calcul ; elle ne doit pas être présentée comme une mesure universelle déjà stabilisée.

### 4.3 Cross-entropy ne signifie pas « apprendre indistinctement tout le bruit »

L'objectif de cross-entropy ne comporte pas en lui-même un terme explicite « structure versus bruit ». Mais cela ne signifie pas qu'un LLM encode tout motif prédictible sans sélection : architecture, biais inductifs, régularisation, données, optimisation, capacité finie, déduplication, curation et post-entraînement modifient ce qui est appris et retenu. La formule de Fan est une opposition heuristique, pas une description exhaustive de l'apprentissage profond réel.

### 4.4 L'analogie entre récits humains et distributions de LLM reste une hypothèse de niveau supérieur

Le récit autobiographique, la mémoire épisodique, l'action incarnée et l'ajustement d'une distribution de tokens sont des mécanismes hétérogènes. Les assimiler à deux « algorithmes de compression » peut être fécond pour penser, mais ne constitue pas une équivalence computationnelle démontrée. Le cerveau ne poursuit pas littéralement une fonction d'objectif unique d'épiplexité.

### 4.5 La correspondance algébrique An/Fn n'est pas une preuve sur les réseaux neuronaux

Aksenov et al. établissent des résultats formels sur des monoïdes libres commutatifs et non commutatifs, puis confrontent leurs prédictions à une analyse empirique du graphe de dépendances de MathLib/Lean 4. Ils indiquent eux-mêmes ne pas identifier précisément le « macro set » qui correspondrait aux abstractions mathématiques humaines. Fan transpose ensuite cette structure vers la cognition humaine, les paramètres neuronaux et les lois d'échelle des LLM. Ce second transfert est analogique : les paramètres d'un réseau ne sont pas des macros indépendantes d'un monoïde libre. Les théorèmes et les observations MathLib ne démontrent donc pas que les LLM sont structurellement incapables de comprendre, ni que leurs rendements doivent être linéaires pour la raison proposée.

### 4.6 « Compréhension » : définition stipulative et contestable

Le texte définit la compréhension par l'efficacité structurelle et la recombinaison parcimonieuse, en s'appuyant sur l'analogie An/Fn. Cette définition peut servir d'hypothèse opérationnelle, mais elle ne recouvre pas automatiquement toutes les conceptions philosophiques, linguistiques et cognitives de la compréhension. Les conclusions « intelligent mais sans compréhension » dépendent directement de cette stipulation.

### 4.7 Les quatre prédictions ne sont pas des résultats expérimentaux

- **CoT et lois d'échelle :** une déviation de loi de puissance n'établirait pas à elle seule un changement de stratégie. Il faut contrôler données, budget de calcul, longueur de sortie, contamination, post-entraînement, architecture et définition de la loss.
- **FineWeb-Edu :** des performances supérieures sur certains benchmarks ne prouvent pas que l'épiplexité en est la cause. Curation, qualité, distribution, filtrage, composition et protocole peuvent varier ensemble.
- **Débruitage :** le compromis proposé entre raisonnement et rappel factuel est une prédiction testable, pas une loi générale ; il faut définir le bruit et maintenir constants les budgets et les distributions d'évaluation.
- **Découverte de définitions :** la métrique T0 et le transfert entre systèmes formels doivent être définis de manière reproductible avant toute conclusion sur un « goût mathématique ».

### 4.8 Alignement et incarnation

L'affirmation selon laquelle RLHF/DPO déplaceraient l'objectif vers l'épiplexité est une interprétation proposée par l'auteur. DPO, RLHF et entraînement constitutionnel n'ont pas une unique fonction objective interchangeable ; leurs effets doivent être mesurés, et une préférence pour des réponses jugées cohérentes ne prouve pas l'acquisition de représentations causales. De même, traiter des données multimodales ou sensorimotrices ne suffit pas à démontrer un ancrage phénoménologique ou une expérience subjective.

## 5. Ce qu'il faut retenir — et ne pas enseigner comme fait

**À retenir :**
- La cross-entropy et le surprisal décrivent une performance prédictive ; ils ne caractérisent pas à eux seuls la structure, la parcimonie ou l'ancrage d'une représentation.
- Les contraintes de ressources et les objectifs d'apprentissage influencent les régularités conservées.
- Il est utile de séparer réussite fonctionnelle, généralisation, réutilisation de représentations, compréhension et expérience subjective.
- Une hypothèse sur l'intelligence doit produire des critères opérationnels et des expériences susceptibles de la réfuter.

**À ne pas présenter comme résultats établis :**
- « L'intelligence est la compression » comme définition scientifique consensuelle.
- « Les humains maximisent l'épiplexité » et « les LLM ne font que compresser le bruit » comme faits établis.
- La correspondance An/Fn comme modèle mathématique démontré des réseaux neuronaux.
- L'absence de compréhension des LLM comme conséquence nécessaire d'une loi algébrique.
- L'alignement comme preuve de déplacement mesuré vers l'épiplexité, ou l'incarnation comme preuve d'expérience subjective.

## 6. Décision d'intégration

**Décision : intégrer comme essai théorique et cadre d'hypothèses, avec un statut critique explicite ; ne pas en faire une leçon canonique ni ajouter des concepts ontologiques au graphe canonique à ce stade.**

| Destination | Décision |
|---|---|
| Fiche de révision compression | Ajouter une courte carte « objectif prédictif / sélection structurelle » et les garde-fous |
| Entropie et cross-entropy | Réutiliser les définitions existantes ; ajouter un renvoi, sans dupliquer les leçons |
| Généralisation et qualité des données | Relier aux pages existantes et aux expériences sur décalage de distribution |
| Compréhension / limites des LLM | Renvoi critique seulement ; conserver les distinctions opérationnelles |
| Graphe canonique | Aucun nouvel identifiant pour « subjectivité positive/négative/grise » ou « intelligence par compression » avant opérationnalisation et revue indépendante |
| Expérience | Ajouter un jouet sur structure séquentielle, modèle de prédiction et contrôle par permutation ; ne pas le baptiser mesure d'épiplexité |

## 7. Expérience pédagogique proposée

Construire un corpus synthétique où une règle génératrice simple produit des séquences longues, puis comparer :

1. un modèle unigramme (ignore l'ordre) ;
2. un modèle bigramme (capture des dépendances locales) ;
3. une variante avec motifs fréquents mais non informatifs ;
4. une variante permutée conservant les fréquences marginales mais détruisant une partie des dépendances.

Mesurer cross-entropy en bits/token sur un jeu de test tenu à l'écart, avec plusieurs graines et des contrôles de taille. Faire varier séparément le bruit et la quantité de données. L'expérience montre ce qu'un objectif prédictif peut exploiter dans des régularités séquentielles ; elle ne mesure ni l'épiplexité formelle, ni la compréhension, ni la subjectivité.

**Question de réflexion :** si deux modèles ont une cross-entropy similaire, quelles mesures supplémentaires permettraient de comparer la parcimonie, le transfert et la recombinaison de leurs représentations ?

## 8. Synthèse opérationnelle

Cette source est utile parce qu'elle déplace la discussion de « combien un modèle prédit-il bien ? » vers « quelles structures son apprentissage lui permet-il de conserver et de réutiliser ? ». Son cadre est stimulant, mais ses conclusions philosophiques reposent sur plusieurs ponts analogiques et des hypothèses qui restent à tester. LLM Lab doit donc enseigner la distinction entre mesures informationnelles, critères de structure, résultats expérimentaux et interprétations ontologiques.

## Références clés citées par la source et vérifications primaires

- [Finzi et al. (2026), *From Entropy to Epiplexity*, arXiv:2601.03220](https://arxiv.org/abs/2601.03220) : résumé, définition et portée de l'épiplexité vérifiés dans le texte arXiv (version révisée du 16 mars 2026). Le papier souligne explicitement que la mesure n'est pas une garantie de généralisation OOD sur une tâche spécifique.
- [Aksenov et al. (2026), *Compression Is All You Need: Modeling Mathematics*, arXiv:2603.20396](https://arxiv.org/abs/2603.20396) : introduction, résultats de monoïdes et analyse MathLib consultés. Les auteurs reconnaissent que l'identification d'un macro set précis dans MathLib reste un problème ouvert.
- Shannon (1948), *A Mathematical Theory of Communication*.
- Gell-Mann & Lloyd (1996), *Information Measures, Effective Complexity, and Total Information*.
- Finzi et al. (2026), *From Entropy to Epiplexity*, arXiv:2601.03220.
- Delétang et al. (2023), *Language Modeling Is Compression*, arXiv:2309.10668.
- Aksenov, Bodnia, Freedman & Mulligan (2026), *Compression Is All You Need: Modeling Mathematics*, arXiv:2603.20396.
- Kaplan et al. (2020), *Scaling Laws for Neural Language Models*, arXiv:2001.08361.
- Penedo et al. (2024), *The FineWeb Datasets*, arXiv:2406.17557.

## Référence

Fan, Mingdi (2026). “Compression Is Intelligence: The Common Ground of Positive Subjectivity and Negative Subjectivity — With a Discussion on the Nature of Intelligence.” PhilArchive preprint, MINCII-3. https://philarchive.org/archive/MINCII-3
