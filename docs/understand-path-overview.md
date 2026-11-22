# Parcours « Comprendre les LLM » — synthèse et audit de navigation

**Statut :** note d'audit éditorial et proposition d'évolution  
**Date :** 2026-11-13  
**Périmètre :** point d'entrée français, panorama LLM, navigation latérale, parcours guidé et carte des ressources.

Cette note est fondée sur les sources du dépôt : `site/index.qmd`, `site/fr/learning-map.qmd`, `site/fr/llm-overview.qmd`, `site/fr/generation.qmd`, `data/guided-route.yml`, `docs/learning-path.md`, `docs/content-section-mapping.md` et `docs/information-architecture.md`. Il s'agit d'un audit éditorial des sources, pas encore d'une validation visuelle desktop/mobile ou d'un test utilisateur.

<a id="understand-route-follow-up"></a>

## État et travail restant au 21 novembre 2026

Le parcours « Comprendre » compte **9 étapes, 20 leçons avec leur contrat et leur fiche de révision, et 11 distinctions travaillées dans des exercices communs à plusieurs étapes**. La carte montre l’enchaînement des concepts. Le plan de révision précise la question et le résultat de chaque étape et ouvre l’écriture formelle à la demande. [Registre du parcours](../data/guided-route.yml) · [Carte](../site/fr/learning-map.qmd#conceptual-route) · [Plan de révision FR](../site/fr/review-path.qmd) · [EN](../site/en/review-path.qmd)

Les changements intégrés couvrent l’entrée positionnelle, les deux axes de softmax, la projection des états finaux vers les probabilités, les retours des exercices vers les étapes et le choix du préfixe selon qu’on génère ou qu’on score une continuation observée. La comparaison de ces usages est accessible depuis le panorama. [#1452](https://github.com/JM-Brun/llm-lab/pull/1452) · [#1453](https://github.com/JM-Brun/llm-lab/pull/1453) · [#1454](https://github.com/JM-Brun/llm-lab/pull/1454) · [#1455](https://github.com/JM-Brun/llm-lab/pull/1455) · [#1456](https://github.com/JM-Brun/llm-lab/pull/1456)

Ce lot complète les retours depuis les corrigés sur les états finaux et sur le choix du préfixe. Le premier renvoie vers Calcul et Prédiction, le second vers Inférence et Scoring. Il relie aussi les leçons sur la loss et la boucle d’entraînement à un cas où deux méthodes d’agrégation de la loss de validation classent deux checkpoints dans un ordre différent. [Exercice sur les états finaux](../site/fr/exercises/logits.qmd#ex-final-state-to-next-token) · [Exercice sur le préfixe](../site/fr/exercises/vraisemblance.qmd#ex-generation-versus-scoring) · [Exercice sur la loss de validation](../site/fr/exercises/loss.qmd#ex-validation-loss-by-token)

Depuis ces premières corrections, les leçons réorganisées suivent davantage les exemples existants. Les représentations et le contexte ont été revus dans [#1470](https://github.com/JM-Brun/llm-lab/pull/1470), les renvois depuis les fiches aval dans [#1472](https://github.com/JM-Brun/llm-lab/pull/1472), puis la chaîne des logits à la validation dans [#1473](https://github.com/JM-Brun/llm-lab/pull/1473).

Le lot [#1474](https://github.com/JM-Brun/llm-lab/pull/1474) réorganise l’entrée du parcours et relie la leçon et la fiche sur les positions au même [exercice corrigé sur l’entrée du premier bloc](../site/fr/exercises/text-data.qmd#ex-token-to-block-input). Les deux occurrences y partagent un ID et un plongement. Les vecteurs de position distincts donnent deux entrées différentes dans le cas additif. Le corrigé renvoie vers la même étape du [plan](../site/fr/review-path.qmd#representations). Les encodages relatifs, les illustrations, les preuves et les ressources restent dans la [leçon sur les positions](../site/fr/positional-encoding.qmd). Le [suivi détaillé des leçons](audits/understand-lesson-contracts-2026-11-20.md) indique où retrouver chaque bloc déplacé.

### Reprise après les réorganisations

Le [relevé de conservation](audits/understand-lesson-contracts-2026-11-20.md#conservation-après-les-réorganisations-de-première-lecture) donne les destinations des exemples, formules, réserves et références du lot intégré jusqu’à `6e17382`. Depuis le plan FR/EN, le lecteur peut ouvrir l’exercice transversal en fin de parcours, puis revenir à l’étape Entraînement. Le plan et la carte pointent vers l’exercice et le corrigé de la leçon.

**Contrôle au clavier sur le site publié, 21 novembre 2026.** Dans Chrome (1363 × 936 pixels), depuis l’étape Entraînement, Entrée ouvre le volet d’écriture formelle et Espace le referme. En FR et EN, Entrée mène ensuite à l’exercice sur le token visible en entrée et ignoré comme cible. Le corrigé est initialement replié, s’ouvre avec Entrée et se referme avec Espace. Le lien de retour ramène à l’ancre Entraînement. L’essai porte sur ce trajet publié. Le nouvel aller-retour vers l’exercice final est vérifié sur le HTML de la branche. [Retour FR](https://jm-brun.github.io/llm-lab/fr/review-path.html#training) · [Retour EN](https://jm-brun.github.io/llm-lab/en/review-path.html#training)

Les déplacements dans le Transformer et le masque causal sont détaillés dans le [relevé de préservation](audits/understand-lesson-contracts-2026-11-20.md#préservation-du-contenu-dans-le-transformer-et-le-masque-causal). Les essais dans le navigateur couvrent les trajets du panorama au plan et de la carte à la fiche, l’aller-retour depuis l’exercice final, les corrigés repliés et les renvois des exercices sur le masque, les deux axes de softmax et la validation. L’exercice de comparaison de checkpoints donne maintenant accès directement à l’étape Entraînement. Les observations ci-dessous restent à recueillir pour décider des prochains changements.

### Trajets vérifiés dans le site rendu

Chromium 153, en FR et EN, à 390 et 1 280 px. Les liens ont été activés au clavier, sauf le départ de la carte guidée vers la leçon à 1 280 px, testé à la souris. Les volets testés ont été ouverts puis refermés au clavier.

- Panorama → comparaison des usages → Scoring. L’écriture formelle s’ouvre dans l’étape atteinte.
- Carte guidée → leçon sur les positions → fiche → exercice des deux occurrences → étape Représentations.
- Plan, étape Calcul → exercice des deux softmax → étape Prédiction.
- Plan, étape Entraînement → fiche de la boucle d’entraînement → exercice des checkpoints → étape Entraînement. Le nouveau lien figure après le corrigé.

### Navigation au clavier et retour depuis la carte

Sur le rendu local du 21 novembre 2026, Chromium 141 a été utilisé en FR et EN à 390 et 1 440 px de large. Le test démarre au premier Tab, emprunte le lien d’évitement et continue par Tab, Entrée, Espace et Échap. Les trajets du plan vers l’exercice final, la comparaison des checkpoints et les deux softmax atteignent leurs ancres de retour. Les réponses et l’écriture formelle s’ouvrent et se replient au clavier. Après le retour de l’exercice final, le Tab suivant reste dans l’étape Entraînement. Le même départ au premier Tab permet de passer du panorama à la comparaison des usages, puis au volet formel de Scoring. Depuis la carte guidée, le trajet passe par la leçon sur les positions, l’exercice sur l’entrée du premier bloc et le retour à Représentations.

Dans la carte, Échap rend le focus au territoire ou au concept dont le contrôle vient d’être recréé. À 390 px, le trajet tactile émulé sélectionne une leçon dans un territoire, ouvre la leçon, puis restaure la sélection et le panneau au retour du navigateur. La sélection est aussi retrouvée après rechargement de l’URL. L’audit automatique vérifie le contraste dans la vue des notions et dans la vue d’un territoire avec une page sélectionnée. Les compteurs et les titres du panneau de détails ont été assombris après le signalement d’un contraste insuffisant.

### Entrer dans le parcours et comprendre le transfert

| Contenu | Destination FR/EN |
| --- | --- |
| Pré-entraînement, transfert, compression prédictive et ses limites | Le [panorama FR](../site/fr/llm-overview.qmd#transformers-changed) et le [panorama EN](../site/en/llm-overview.qmd#transformers-changed) présentent les mêmes explications dans le prolongement du pré-entraînement. Le tableau sur l’emplacement des informations suit, puis le passage du modèle à l’assistant précède les critères de choix. |
| Dépendance entre deux tours de génération | Le corrigé de la question sur le calcul prédictif réunit la réinjection du token et le caractère séquentiel de la boucle. La question sur le transfert reprend le cas des avis positifs ou négatifs de la [page d’exercices FR](../site/fr/exercises/llm-overview.qmd) et [EN](../site/en/exercises/llm-overview.qmd). Elle distingue l’acquis du pré-entraînement, le rôle des exemples en contexte et l’évaluation sur des avis tenus à l’écart. |
| Écriture de la prédiction, commandes de la carte et ressources | La formule est accessible depuis le [squelette FR](../site/fr/learning-map.qmd#conceptual-route) et le [squelette EN](../site/en/learning-map.qmd#conceptual-route). Le volet d’aide se trouve à côté de la carte. Les deux volets utilisent des commandes natives. Les ressources du panorama suivent l’auto-évaluation et le lien vers la tokenisation figure dans l’explication et dans la navigation de fin de leçon. |

La comparaison prend `eebc737` comme référence. Les neuf sections du panorama et leurs ancres, les figures et leurs textes alternatifs, les tableaux, la formule et les destinations des liens existants sont conservés en FR et EN. Le [passage sur la composition du contexte](../site/fr/learning-map.qmd#parcours-théorique-understand) et ses deux liens restent dans la synthèse en six mouvements. La carte donne un accès direct à la liste des neuf étapes et au point d’entrée de l’exploration des ressources.

La comparaison du HTML de la carte et du panorama a retrouvé 152 ancres éditoriales et 374 destinations de lien, décomptées par page, ainsi que les six figures et leurs textes alternatifs, les tableaux et les expressions mathématiques. Dans Chromium 141, les deux raccourcis de la carte, les volets, le corrigé et le passage du panorama à la tokenisation ont été vérifiés au clavier en FR et EN à 390 et 1 280 px, avec et sans JavaScript.

### Du panorama aux premiers plongements

Dans la [leçon FR](../site/fr/text-data.qmd#tokenizer-output) et la [leçon EN](../site/en/text-data.qmd#tokenizer-output), les deux IDs de l’exemple court sont visibles dès la première lecture. Le résultat vient de la trace GPT-2 existante sur `hello world`. Le texte repère l’espace initial du deuxième token et précise le caractère synthétique des plongements de la trace. La trace revient au même point dans la leçon.

Le [premier exercice de lookup](../site/fr/exercises/text-data.qmd#ex-text-to-embedding-lookup) suit la chaîne texte → IDs → lignes de la table. L’exercice sur la position et l’entrée du premier bloc reste dans les ressources complémentaires. Les deux exemples narratifs, le script reproductible, les conséquences de la segmentation et les détails sur la préparation du corpus restent à leur emplacement. La carte conserve les six mouvements d’orientation de [#1482](https://github.com/JM-Brun/llm-lab/pull/1482), dont la conception et l’exploitation du contexte.

La trace GPT-2 a été exécutée en FR et EN. Le rendu a été parcouru au clavier de la carte jusqu’aux plongements, avec un aller-retour vers la trace et un accès direct à l’exercice de lookup. Les deux langues ont été testées dans Chromium à 390 et 1 280 px.


### Du lookup au préfixe accessible

La leçon sur les [plongements FR](../site/fr/embedding-space.qmd#lookup) et [EN](../site/en/embedding-space.qmd#lookup) reprend le cas de l’exercice où l’ID 17 apparaît aux positions 0 et 3. Lire deux fois la ligne 17 donne le même vecteur. La [leçon sur la position](../site/fr/positional-encoding.qmd) s’appuie sur ces deux occurrences pour faire calculer les entrées distinctes du premier bloc dans le cas additif. La [leçon sur la contextualisation](../site/fr/contextualized-representations.qmd) fixe ensuite le rang et demande de distinguer un changement dans le préfixe accessible d’un changement après le token courant.

Les versions FR et EN expliquent qu’un même token garde son ID dans un vocabulaire donné, tandis que le découpage du texte peut produire des tokens différents. La position agit selon l’architecture. Le masque causal fixe les positions visibles par chaque requête.

La comparaison à `56e1cdf` retrouve les titres et ancres, les figures et leurs textes alternatifs, les équations affichées, les destinations existantes et les ressources complémentaires des six pages. Les exercices et leurs corrigés restent identiques. Les trajets vers les trois exercices et l’ouverture des corrigés au clavier ont été vérifiés dans Chromium en FR et EN à 390 et 1 280 px.

### Première lecture et transfert, du Panorama à la position

Le Panorama place les deux tours et l’explorateur dans la même section. La définition de la surprise et le calcul de vraisemblance restent accessibles dans un volet de la section sur les trois usages. Le rappel sur le découpage réel se trouve au raccord [Panorama → Texte](../site/fr/text-data.qmd#tokenizer-output). Les probabilités illustratives du Panorama et les sorties GPT‑2 de la trace conservent leur provenance respective.

Les leçons FR/EN donnent les quatre lectures de la table pour la séquence jouet, puis réutilisent ses occurrences aux rangs 0 et 3 dans le cas additif. La [comparaison positionnelle](../site/fr/positional-encoding.qmd#position-permutation) fixe le rang et l’ID de B entre `ABC` et `CBA`. Le [cas de transfert](../site/fr/exercises/positional-encoding.qmd#ex-positional-mask-transfer) garde B en dernier dans `ACB` et `CAB`, pour vérifier les limites de l’effet du seul masque dans une couche. La preuve d’équivariance, les SVG et les limites d’extrapolation restent accessibles depuis la leçon.

Le bandeau généré conserve le numéro d’étape et ajoute le rang de la page uniquement dans les étapes à plusieurs leçons. La hiérarchie documentaire de la carte reste à examiner dans [#1492](https://github.com/JM-Brun/llm-lab/issues/1492), [#1493](https://github.com/JM-Brun/llm-lab/issues/1493) et [#1499](https://github.com/JM-Brun/llm-lab/issues/1499). Le [pilote indépendant #447](https://github.com/JM-Brun/llm-lab/issues/447) peut maintenant demander au lecteur de justifier successivement la ligne lue, le point d’insertion de la position et le préfixe accessible.

### Travail restant

| Ordre | Travail restant | Résultat à consigner |
| --- | --- | --- |
| 1 | Mener le [pilote texte → attention](learner-validation-pilot.md) avec un lecteur indépendant. Partir d’une occurrence, relever la ligne lue et le point d’insertion de la position, puis proposer le [cas causal](learner-validation-pilot.md#causal-position-and-observed-target). [#447](https://github.com/JM-Brun/llm-lab/issues/447) · [#483](https://github.com/JM-Brun/llm-lab/issues/483) | Comparer les réponses avant et après lecture, puis évaluer le transfert sur un cas inédit. Distinguer une difficulté à trouver le contenu d’une erreur sur la visibilité, la cible ou la pénalité. Consigner la langue, l’appareil, les pages revisitées et les aides fournies. |
| 2 | Mener le [pilote aval](audits/learning-path-learner-evaluation.md#prediction-use-pilot) sur la génération, le scoring et l’entraînement. Utiliser les formes A/B et le cas inédit de validation. | Consigner les choix de préfixe et de cible, la pondération par cible valide et les paramètres qui changent. Comparer aussi la difficulté des deux formes. L’exercice public sert à la répétition et les variantes du protocole au transfert. |
| 3 | Tester la carte sur appareil tactile réel et avec lecteur d’écran, dans les deux langues. Rejouer la sélection, le retour et les volets sur les trajets ci-dessus. [#337](https://github.com/JM-Brun/llm-lab/issues/337) · [#417](https://github.com/JM-Brun/llm-lab/issues/417) | Noter navigateur, dispositif, langue et largeur. Contrôler le focus, l’annonce de l’état des volets, la lecture des formules et l’arrivée sur l’ancre. Donner un trajet de reproduction pour chaque défaut. |
| 4 | Traiter les difficultés observées. Rejouer le trajet ou le calcul après chaque correction. | Corriger le lien, l’intitulé ou le rappel quand il suffit à reprendre le calcul. Envisager de déplacer une leçon si un manque de prérequis persiste. Consigner la destination FR/EN des exemples, preuves, code et références. |

Pour le [pilote du panorama](https://github.com/JM-Brun/llm-lab/issues/1208), mesurer le temps de première lecture et demander au lecteur de distinguer ce que le modèle réutilise de ce que les exemples lui fournissent. Utiliser un cas différent de la question corrigée du panorama et relever si le lecteur propose une évaluation sur de nouvelles entrées sans aide.

La [revue des signatures formelles](audits/understand-lesson-contracts-2026-11-20.md#vérification-des-quatre-cas-formels-du-plan) fixe le résultat attendu pour le cas additif et RoPE, les deux axes de softmax et la distinction entre gradient et pas d’optimiseur. Elle sert de référence pour lire les réponses des pilotes.

Le [comparatif des approches d’apprentissage](source-reviews/learning-path-comparison-2026-11-05.md#which-learning-approach-serves-which-outcome) a relevé un prérequis local. Le rappel de softmax apparaît à son premier usage dans le calcul de l’attention. Trois fiches bilingues donnent accès aux exercices existants sur l’état contextualisé, les deux axes de normalisation et la perte d’une cible. Le [pilote à une position causale](learner-validation-pilot.md#causal-position-and-observed-target) indique quoi observer pour décider d’une correction locale ou d’une adaptation de l’ordre.

Sur les étapes aval, cinq fiches bilingues relient leur question de rappel aux exercices sur le préfixe, les cibles valides, la mise à jour ou le classement des checkpoints. Le [comparatif des scripts d’entraînement](source-reviews/learning-path-comparison-2026-11-05.md#from-scoring-to-training-and-validation) documente notamment les conditions sous lesquelles une moyenne par lot et une moyenne par cible répondent à la même question.

Pour suivre la conservation lors d’un déplacement, prendre la dernière version de `main` comme référence et relever la destination des exemples, hypothèses, figures, équations, corrigés et références propres à chaque leçon. Comparer aussi les ancres et les liens affichés en FR et EN, en ouvrant les volets qui accueillent du contenu déplacé. Une correction d’interface se vérifie en rejouant le trajet correspondant. Les résultats des pilotes apprenants restent à recueillir.

### De la distribution à la génération, puis au scoring

Le fil rouge reprend le trajet guidé [Probabilités](../site/fr/probabilites.qmd#running-example-next-token) → [Entropie](../site/fr/entropy.qmd) → [Génération](../site/fr/generation.qmd#la-boucle-sur-un-exemple) → [Apprentissage en contexte](../site/fr/in-context-learning.qmd) → [Ingénierie du contexte](../site/fr/context-engineering.qmd) → [Vraisemblance](../site/fr/vraisemblance.qmd). Le trajet [EN](../site/en/entropy.qmd) suit le même ordre. Le lien vers l’entropie rejoint le calcul de température. Le [cas du token choisi et de la cible observée](../site/fr/cross-entropy.qmd#chosen-token-vs-target) rejoint l’explication de la surprise. La carte exploratoire conserve le trajet direct Entropie → Vraisemblance pour étudier la surprise et le scoring. Les liens correspondants restent accessibles dans le corps et les ressources de la leçon.

La génération reprend la distribution à quatre candidats, puis change le préfixe pour le deuxième tour. L’[exercice sur les deux préfixes](../site/fr/exercises/vraisemblance.qmd#ex-generation-versus-scoring) garde son tableau, ses questions et son corrigé. La leçon d’ingénierie du contexte pose la question avant de renvoyer à l’exercice, qui contient les valeurs et le résultat. Les formules, figures, ancres de section, exemples et références des leçons restent en place. Pour le pilote aval, relever quel préfixe le lecteur choisit pour chacun des deux calculs avant d’ouvrir le corrigé.

### De la perte locale à la mise à jour

Le calcul de la [loss FR](../site/fr/loss.qmd#de-la-perte-locale-à-la-loss-du-batch) et [EN](../site/en/loss.qmd#from-local-penalty-to-batch-loss) ouvre l’exemple du gradient à la première cible. L’exemple isole la pénalité locale de 0,511 nat. La loss de 0,476 nat par token repose sur les trois cibles de la continuation illustrative. La formule du gradient de la moyenne et le cas des positions ignorées restent dans le volet de la leçon sur les gradients.

Le [pas d’entraînement FR](../site/fr/training-loop.qmd#rejouer-un-pas-sur-le-premier-token) et [EN](../site/en/training-loop.qmd#replay-one-step-on-the-first-token) est accessible depuis la leçon sur les gradients après le calcul de mise à jour. Il précède les explications sur les lots, les époques et l’initialisation. Le calcul SGD de la tête de sortie, les deux exercices de transfert et les réserves sur la validation sont conservés. Pendant le [pilote aval](audits/learning-path-learner-evaluation.md#prediction-use-pilot), relever à quel moment le lecteur fait changer les paramètres et s’il précise la quantité qu’il dérive.

L’ordre actuel sert de référence pour ces vérifications. Les sections ci-dessous conservent l’audit éditorial initial.

## 1. Ce que le parcours doit faire comprendre

Le parcours doit construire une représentation mentale progressive du système, et non faire mémoriser une liste de composants. À son terme, le lecteur doit pouvoir expliquer :

1. ce qu'est un LLM et ce que signifie prédire le prochain token ;
2. comment un texte devient une entrée exploitable par le modèle ;
3. comment cette entrée devient une représentation numérique puis contextuelle ;
4. comment le Transformer transforme ces représentations ;
5. comment le calcul aboutit à une distribution de probabilité sur le prochain token ;
6. comment le modèle exploite les instructions et exemples du contexte sans mise à jour des paramètres, et comment le système prépare ce contexte ;
7. ce que l'on peut faire de la distribution : générer, scorer une cible observée ou apprendre en ajustant les paramètres.

Le fil directeur est une question : **comment un modèle transforme-t-il un contexte en prédiction, et comment cette prédiction est-elle utilisée ?**

Trois représentations doivent rester distinctes :

- **Parcours pédagogique :** dans quel ordre est-il préférable d'apprendre ?
- **Graphe de connaissances :** quels concepts sont reliés, et par quelles relations ?
- **Graphe computationnel :** quelles opérations le modèle réalise-t-il et comment s'enchaînent-elles ?

Le parcours est une projection pédagogique des connaissances, pas une transcription de l'architecture technique. La génération, le scoring et l'apprentissage partagent un calcul prédictif, mais sont trois usages distincts et non trois étapes d'une seule boucle d'exécution.

## 2. Le parcours simplifié à présenter au lecteur

Cette synthèse en six mouvements est la couche d'orientation. Elle ne remplace pas les neuf étapes canoniques de `data/guided-route.yml`.

### 1 — Situer : qu'est-ce qu'un LLM ?

Un LLM exploite un contexte pour attribuer des probabilités aux continuations possibles. Le projet prend le GPT autorégressif comme exemple concret, sans prétendre que tous les LLM ont la même architecture ou le même objectif.

**À retenir :** LLM, GPT et Transformer ne sont pas synonymes ; architecture, apprentissage des paramètres et utilisation du modèle sont trois questions différentes.

Page : [Panorama : qu'est-ce qu'un LLM ?](../site/fr/llm-overview.qmd).

### 2 — Observer : comment produit-il du texte ?

Suivre d'abord une génération complète comme une boîte noire :

`contexte → distribution du prochain token → sélection → nouveau contexte → répétition`

Le modèle calcule une distribution ; une règle de décodage sélectionne un token ; le token est réinjecté dans le contexte. Les paramètres restent fixes pendant l'inférence ordinaire.

Page : [Générer du texte](../site/fr/generation.qmd), d'abord comme aperçu du système.

### 3 — Expliquer le calcul : que reçoit et que calcule le modèle ?

Ouvrir progressivement la boîte en quatre mouvements :

- **Texte → tokens → identifiants :** le texte est segmenté et représenté par des IDs.
- **Identifiants → représentations :** les IDs donnent accès à des vecteurs ; l'information positionnelle est ajoutée ; les couches produisent des représentations contextualisées.
- **Transformer les représentations :** les blocs Transformer appliquent notamment les projections Q/K/V, l'attention, le masque causal, les connexions résiduelles, la normalisation et les MLP.
- **États → prédiction :** les états finaux sont projetés en logits puis en distribution de probabilité sur le vocabulaire.

**Point de vigilance :** Q/K/V sont calculés à l'intérieur de chaque bloc Transformer, à partir de ses états d'entrée. Ils ne viennent pas après les représentations contextualisées finales.

Pages centrales : [Texte et données](../site/fr/text-data.qmd), [Embeddings](../site/fr/embedding-space.qmd), [Représentations contextualisées](../site/fr/contextualized-representations.qmd), [Transformer](../site/fr/transformer.qmd), [Q/K/V](../site/fr/queries-keys-values.qmd), [Attention](../site/fr/scaled-dot-product-attention.qmd), [Masque causal](../site/fr/causal-masking.qmd), [Logits](../site/fr/logits.qmd), [Probabilités](../site/fr/probabilites.qmd).

### 4 — Concevoir et exploiter le contexte : que fournit-on au modèle ?

L'**apprentissage en contexte** (*in-context learning*, ICL) décrit comment le modèle adapte ses réponses aux instructions et démonstrations présentes dans son contexte, sans mettre à jour ses paramètres. L'**ingénierie du contexte** (*context engineering*) désigne le travail du système qui sélectionne, récupère, structure, actualise et sécurise les informations transmises au modèle.

Ces notions sont liées mais différentes : ICL décrit un comportement du modèle ; context engineering décrit une pratique de conception du système. Le prompt engineering en est une partie, tandis que RAG et mémoire sont des mécanismes qui peuvent alimenter le contexte sans se confondre avec lui.

Pages centrales : [Apprentissage en contexte](../site/fr/in-context-learning.qmd), [Ingénierie du contexte](../site/fr/context-engineering.qmd). Exercices : [ICL](../site/fr/exercises/in-context-learning.qmd), [context engineering](../site/fr/exercises/context-engineering.qmd).

### 5 — Comprendre les usages : que fait-on de la prédiction ?

La distribution prédictive ouvre trois branches sœurs :

- **Générer :** sélectionner un token, l'ajouter au contexte et recommencer. Le *prefill* traite le prompt initial ; le *decode* poursuit la génération token par token.
- **Scorer :** mesurer la probabilité attribuée à un token ou à une séquence observée, sans sélectionner de token et sans mettre à jour les paramètres.
- **Apprendre :** comparer les prédictions aux cibles observées, agréger une loss, calculer des gradients et mettre à jour les paramètres. Le *teacher forcing* utilise le préfixe observé ; il ne désigne pas le *prefill*.

L'évaluation est transversale : elle mesure le comportement du modèle sur des données et selon un protocole définis. Ce n'est pas une quatrième branche d'exécution.

Pages centrales : [Génération](../site/fr/generation.qmd), [Vraisemblance](../site/fr/vraisemblance.qmd), [Cross-entropie](../site/fr/cross-entropy.qmd), [Loss](../site/fr/loss.qmd), [Gradients](../site/fr/gradients.qmd), [Évaluation expérimentale](../site/fr/evaluation-experimentale.qmd).

### 6 — Explorer selon son besoin

Après cette vue d'ensemble, le lecteur choisit librement :

- **Construire :** implémenter et vérifier un petit GPT avec le parcours Build indépendant ;
- **Pratiquer :** exercices, calculs, manipulations et expériences ;
- **Approfondir :** dérivations, géométrie, variantes d'attention, architectures et limites ;
- **Consulter :** glossaire, histoire et références.

Ces destinations complètent le parcours sans devenir des étapes obligatoires supplémentaires.

### Schéma de synthèse

```text
COMPRENDRE UN LLM

Situer le système
      ↓
Observer une génération complète (boîte noire)
      ↓
Expliquer le calcul
Texte → tokens → représentations → Transformer → distribution
      ↓
Concevoir et exploiter le contexte
      ├── ICL : exploiter les exemples sans mise à jour des paramètres
      └── Context engineering : préparer et gérer les informations
      ↓
Comprendre les usages de la prédiction
      ├── Générer : sélectionner et réinjecter
      ├── Scorer : évaluer une cible observée
      └── Apprendre : loss → gradients → paramètres
      ↓
Explorer : construire · pratiquer · approfondir · consulter
```

Ce schéma est un résumé de lecture. Il ne remplace ni le registre des neuf étapes, ni le graphe computationnel, ni la carte des concepts.

## 3. Audit de l'existant

### Points solides

- Le point d'entrée distingue déjà les deux parcours principaux et indépendants : Understand et Build.
- Le panorama commence par le système global et distingue LLM, GPT et Transformer.
- La génération est volontairement présentée tôt comme aperçu « boîte noire », puis reprise plus en détail. Cette répétition a une justification pédagogique : voir le phénomène avant d'en étudier les mécanismes.
- Le parcours guidé distingue le calcul prédictif des usages génération, scoring et apprentissage.
- `guided-route.yml` centralise les neuf étapes et leurs objectifs bilingues ; les pages facultatives ne sont pas des prérequis.
- La carte distingue pages, concepts et relations, au lieu de réduire tout le contenu à une arborescence unique.
- Build, Practice et Deepen ont des destinations distinctes.

### Frictions observées dans les sources

1. **La carte cumule plusieurs fonctions.** Elle présente le parcours guidé, les territoires, rubriques, pages, notions canoniques, filtres et vues interactives. C'est utile pour explorer, mais beaucoup à traiter pour quelqu'un qui veut seulement savoir par où commencer.
2. **La vue courte n'est pas assez immédiatement distincte de la vue exhaustive.** Neuf étapes et la carte détaillée arrivent rapidement, alors que le lecteur a d'abord besoin de retenir quelques idées structurantes.
3. **La double présence de la génération peut sembler redondante.** Son rôle d'aperçu puis de reprise détaillée doit être explicitement annoncé.
4. **La navigation latérale est profonde.** Les sous-sections aident à retrouver les pages, mais peuvent faire croire que chaque page est un chapitre obligatoire ou que l'arborescence représente exactement le calcul.
5. **Les étapes détaillées mélangent plusieurs granularités.** Les neuf étapes conviennent au guidage, mais les intitulés de haut niveau doivent rester formulés en questions et résultats compréhensibles.
6. **Les branches scoring et apprentissage sont moins visibles dans la navigation que la chaîne de calcul.** Leur distinction mérite d'être présentée dans une synthèse simple, sans les transformer en étapes de génération.
7. **La carte et la sidebar peuvent être prises pour deux parcours concurrents.** Leur rôle respectif doit être rappelé au point de choix.

## 4. Améliorations proposées

### P0 — Clarifier l'orientation, sans changer le curriculum

1. Ajouter au début de la page « Parcours guidé et carte des ressources » la synthèse en cinq mouvements : Situer, Observer, Expliquer le calcul, Comprendre les usages, Explorer.
2. Présenter les trois grandes questions : qu'est-ce qu'un LLM ? comment calcule-t-il une prédiction ? que fait-on de cette prédiction ?
3. Expliciter la double fonction de la page Génération : **aperçu du système** après le panorama, puis **explication détaillée** à l'étape inférence.
4. Rappeler que la sidebar sert à retrouver les ressources, le parcours guidé à proposer un ordre de lecture, et la carte à explorer les relations.

### P1 — Réduire la charge cognitive de la carte

1. Faire apparaître la synthèse courte avant les étapes détaillées, puis les vues exploratoires.
2. Conserver les vues Territoires / Rubriques / Pages / Notions, mais les présenter comme des outils de consultation, pas comme des étapes supplémentaires.
3. Dans les libellés, privilégier les questions et résultats attendus ; garder les inventaires de notions dans les objectifs détaillés ou les pages.
4. Distinguer les ressources centrales et facultatives sans ajouter une nouvelle taxonomie ni un nouveau registre.

### P2 — Harmoniser la navigation et les retours

1. Vérifier que les intitulés de sidebar décrivent des questions ou ensembles cohérents, et non une prétendue séquence exacte des opérations.
2. Ajouter des liens de retour sobres vers la synthèse depuis les pages centrales, sans répéter un gros bloc de navigation partout.
3. Dans les pages génération, scoring et apprentissage, rappeler les trois usages frères avec des liens croisés, sans dupliquer leurs explications.
4. Réaliser une revue visuelle desktop/mobile et clavier de la carte et de la sidebar après les modifications.

## 5. Garde-fous

- Conserver `data/guided-route.yml` comme source des étapes.
- Ne pas fusionner Understand et Build.
- Ne pas transformer la carte des connaissances en séquence linéaire.
- Ne pas faire des pages Deepen des prérequis implicites.
- Ne pas déplacer les explications canoniques dans la page d'orientation : elle doit orienter, pas répéter les leçons.
- Ne pas supprimer les détails, exemples ou références lors d'une simplification de la navigation.
- Ne pas introduire une nouvelle taxonomie si les rôles actuels suffisent.

## 6. Ordre de réalisation

1. Valider la synthèse en cinq mouvements et son vocabulaire.
2. L'intégrer à la page de carte comme couche d'orientation.
3. Ajuster les libellés qui créent une ambiguïté entre aperçu et reprise détaillée de la génération.
4. Vérifier les liens et la parité FR/EN.
5. Effectuer la revue responsive, clavier et lecteur d'écran.
6. Après cette validation seulement, décider si certains intitulés de sidebar doivent être raccourcis ou regroupés.

**Critère de réussite :** un nouveau lecteur doit pouvoir, en moins d'une minute, répondre à « par où commencer ? », décrire le fil général du fonctionnement d'un LLM et comprendre qu'il peut ensuite choisir de construire, pratiquer ou approfondir sans lire toutes les pages.
