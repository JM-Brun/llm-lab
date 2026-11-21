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

| Ordre | Travail restant | Résultat à consigner |
| --- | --- | --- |
| 1 | Vérifier en FR et EN les trajets panorama → comparaison → étape, carte → leçon → fiche et plan → exercice → retour. Tester sur écran large et étroit, au clavier, et à la souris ou au toucher selon la carte. [#337](https://github.com/JM-Brun/llm-lab/issues/337) · [#417](https://github.com/JM-Brun/llm-lab/issues/417) | Indiquer le navigateur, la langue, la largeur et le mode d’entrée. Vérifier l’arrivée sur la bonne section, la visibilité du focus et l’ouverture puis le repli des formules et corrigés. Donner une reproduction de chaque défaut. |
| 2 | Vérifier la portée des signatures formelles du plan. Examiner d’abord le cas additif $E+P$ et l’emplacement de RoPE, les deux axes de normalisation et la distinction entre gradient et pas de l’optimiseur. [Registre du parcours](../data/guided-route.yml) | Pour chaque signature, retrouver dans la leçon les hypothèses du calcul, l’objet qu’il transforme et l’exercice qui permet de vérifier la distinction. Corriger la formulation là où les deux lectures divergent. |
| 3 | Mener le pilote indépendant du texte à l’attention. [Protocole](learner-validation-pilot.md) · [#447](https://github.com/JM-Brun/llm-lab/issues/447) | Comparer les réponses avant et après la lecture, puis évaluer séparément le transfert sur un cas inédit. Consigner les observations anonymisées et les notions ou pages que la personne a dû revoir. |
| 4 | Piloter le transfert sur les étapes aval. Les [formes A/B et le cas inédit de validation](audits/learning-path-learner-evaluation.md#prediction-use-pilot) sont prêts. | Relever les réponses et le raisonnement, en particulier l’origine du préfixe, la pondération par cible valide et le rôle des paramètres pendant la validation. Examiner aussi si les formes A/B suscitent des difficultés comparables. |
| 5 | Corriger les problèmes constatés. | Rejouer la tâche qui a fait apparaître le problème. Une difficulté récurrente due à un prérequis enseigné trop tard justifie de revoir l’ordre. Pour une confusion circonscrite ou un mauvais repérage, revoir la fiche, l’explication ou le lien concerné. |

Le [comparatif des approches d’apprentissage](source-reviews/learning-path-comparison-2026-11-05.md#which-learning-approach-serves-which-outcome) a relevé un prérequis local. Le rappel de softmax apparaît à son premier usage dans le calcul de l’attention. Trois fiches bilingues donnent accès aux exercices existants sur l’état contextualisé, les deux axes de normalisation et la perte d’une cible. Le [pilote à une position causale](learner-validation-pilot.md#causal-position-and-observed-target) indique quoi observer pour décider d’une correction locale ou d’une adaptation de l’ordre.

Sur les étapes aval, cinq fiches bilingues relient leur question de rappel aux exercices sur le préfixe, les cibles valides, la mise à jour ou le classement des checkpoints. Le [comparatif des scripts d’entraînement](source-reviews/learning-path-comparison-2026-11-05.md#from-scoring-to-training-and-validation) documente notamment les conditions sous lesquelles une moyenne par lot et une moyenne par cible répondent à la même question.

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
