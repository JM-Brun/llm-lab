# « Comprendre les LLM » — audit du parcours et de la navigation

**Date :** 2026-11-09  
**Périmètre :** architecture pédagogique de haut niveau, parcours guidé et navigation française/anglaise.  
**Nature :** audit des sources du dépôt (Quarto, sidebar, parcours guidé et documents d'architecture). Ce document ne remplace pas une vérification visuelle du site déployé sur plusieurs écrans.

## 1. Objectif de la rubrique

« Comprendre les LLM » doit permettre à un lecteur de construire une représentation mentale cohérente d'un LLM avant d'entrer dans les détails mathématiques ou l'implémentation.

À la fin du parcours principal, le lecteur devrait pouvoir :
1. expliquer ce qu'est un LLM et ce qu'il fait ;
2. suivre le calcul qui transforme un contexte en distribution du prochain token ;
3. distinguer les trois usages de cette distribution : générer un token, attribuer un score à une cible observée, apprendre en ajustant les paramètres ;
4. expliquer pourquoi l'évaluation est nécessaire et en quoi elle diffère de l'entraînement ;
5. savoir où aller pour construire, expérimenter ou approfondir.

La rubrique n'a pas vocation à enseigner tous les détails d'un coup. Elle doit donner une vue d'ensemble exacte, montrer les relations essentielles et offrir des chemins d'approfondissement sans transformer chaque ressource en prérequis.

## 2. Sources examinées

- site/index.qmd : promesse du projet et portes d'entrée.
- site/_quarto.yml : navigation latérale FR/EN.
- site/fr/learning-map.qmd : distinction entre parcours guidé et carte exploratoire.
- data/guided-route.yml : huit étapes et ressources centrales/facultatives.
- docs/learning-path.md : modèle canonique du curriculum.
- docs/computational-curriculum-reorganisation.md : responsabilités des pages et limites Core/Deepen.
- docs/canonical-computational-spine.md : mécanisme prédictif partagé et branches opérationnelles.

L'audit s'appuie sur ces sources. Il ne conclut pas à la qualité visuelle effective des pages déployées : les contrôles responsive, clavier et lecteur d'écran doivent faire l'objet d'une vérification navigateur dédiée.

## 3. État actuel

### 3.1 Les intentions pédagogiques sont bien séparées

L'accueil expose quatre portes d'entrée :
- **Comprendre** : construire une représentation du fonctionnement ;
- **Construire** : implémenter un petit GPT ;
- **S'exercer et expérimenter** : vérifier et manipuler ;
- **Approfondir** : étudier les fondements, variantes et détails techniques.

La carte des ressources ajoute une fonction distincte : explorer les territoires, rubriques, pages et notions canoniques sans imposer un ordre de lecture.

Cette séparation est saine et doit être conservée. Le parcours « Comprendre » n'est ni le parcours Build, ni un catalogue exhaustif des ressources.

### 3.2 Le parcours guidé actuel est pertinent, mais trop détaillé comme résumé d'entrée

Le fichier data/guided-route.yml définit huit étapes :
1. Situer le système.
2. Du texte aux tokens.
3. Des identifiants aux représentations.
4. Comprendre le calcul du Transformer.
5. Des états à la distribution prédictive.
6. Exécuter l'inférence et générer du texte.
7. Attribuer un score aux tokens observés.
8. Apprendre et mettre à jour les paramètres.

Les étapes 2 à 5 décomposent le calcul partagé en sous-étapes utiles. Les étapes 6 à 8 décrivent en revanche des usages distincts de la distribution prédictive. Les huit étapes sont donc une décomposition pédagogique détaillée, pas huit maillons d'une même exécution.

Le titre de la carte annonce « huit étapes » et son texte précise que les pages d'une étape sont complémentaires. C'est exact, mais le lecteur doit encore comprendre pourquoi génération, scoring et apprentissage apparaissent à la suite alors qu'ils ne sont pas des prérequis successifs.

### 3.3 La navigation latérale expose une granularité de référence

La sidebar « Comprendre les LLM » place actuellement :
- le panorama et la génération ;
- le calcul de la prédiction, avec texte/IDs, représentations, Transformer et probabilités ;
- le scoring des tokens observés ;
- la loss et les gradients ;
- les architectures Transformer et les limites des LLM.

Cette navigation est utile comme index des ressources. Elle ne constitue pas encore une représentation évidente du parcours pour un lecteur débutant. En particulier :
- la génération apparaît à la fois dans l'orientation et dans l'étape d'inférence du parcours guidé ;
- les architectures et limites sont mêlées au chemin principal alors que les variantes d'architecture relèvent surtout de l'approfondissement ;
- scoring et apprentissage sont présents, mais leur relation avec le calcul prédictif commun n'est pas immédiatement visible dans les intitulés ;
- la sidebar donne beaucoup de noms de pages avant d'expliquer le petit nombre de questions auxquelles elles répondent.

La duplication de génération peut être une réexposition pédagogique intentionnelle, mais elle doit être identifiée comme telle. Une page canonique ne doit pas apparaître deux fois comme si elle représentait deux notions différentes.

### 3.4 L'accueil porte déjà une synthèse computationnelle dense

Le schéma de la page d'accueil détaille les flux d'inférence, d'apprentissage et d'évaluation. Son contenu est utile et doit être conservé. Sa densité et son vocabulaire sont toutefois plus adaptés à une synthèse architecturale qu'à la première orientation.

Il faut distinguer :
- une vue d'ensemble destinée à répondre rapidement « que fait un LLM ? » ;
- le schéma computationnel détaillé qui explique les opérations et les transitions d'état.

Ne pas supprimer le schéma détaillé : lui donner un emplacement de synthèse ou un accès explicite « Voir le détail du calcul », après une vue simplifiée.

## 4. Modèle pédagogique simplifié recommandé

Le parcours d'entrée devrait être présenté en **trois grandes questions**, suivies de trois branches d'usage. C'est la forme la plus représentative de la proposition du projet sans exposer d'emblée toute sa granularité.

### Question 1 — Qu'est-ce qu'un LLM ?

Le lecteur découvre :
- le modèle, ses paramètres et son contexte ;
- l'idée générale de prédiction du prochain token ;
- un aperçu de génération en boîte noire : un prompt entre, une réponse est produite ;
- le fait que les LLM ne se réduisent ni à une seule architecture ni à une seule tâche.

**Ressource centrale :** llm-overview.

L'aperçu de génération doit rester bref à ce stade. Il peut être illustré dans le panorama sans imposer la page complète de génération comme deuxième ressource obligatoire.

### Question 2 — Comment le modèle produit-il une prédiction ?

Le lecteur suit une seule fois le calcul commun :

    Texte
      → tokens et token IDs
      → embeddings et information positionnelle
      → blocs Transformer
      → états contextualisés finaux
      → logits
      → distribution du prochain token

Les Q/K/V, l'attention, le masque causal, les résidus et le MLP sont expliqués comme des opérations internes aux blocs Transformer. Les Q/K/V ne doivent jamais être placés après les représentations contextualisées finales.

**Ressources centrales :** text-data, embedding-space, positional-encoding, contextualized-representations, transformer, queries-keys-values, scaled-dot-product-attention, causal-masking, logits, probabilites.

Ces ressources détaillent le calcul ; elles ne doivent pas toutes devenir des étapes de même importance dans la représentation d'entrée.

### Question 3 — Que peut-on faire de cette prédiction ?

À partir de la distribution conditionnelle, le lecteur découvre trois usages frères :

| Usage | Question simple | Opération essentielle | Paramètres |
|---|---|---|---|
| **Générer** | Quel token ajouter au contexte ? | Décoder, sélectionner, réinjecter et recommencer | Fixes |
| **Scorer** | Quelle probabilité le modèle attribue-t-il au token réellement observé ? | Lire la probabilité cible et calculer vraisemblance / log-vraisemblance | Fixes |
| **Apprendre** | Comment rendre les cibles observées plus probables ? | Teacher forcing, loss, gradients et mise à jour | Modifiés |

L'évaluation est transversale : elle utilise notamment le scoring sur des données de validation/test et peut aussi examiner des générations. Elle n'est ni une quatrième branche équivalente, ni la dernière étape obligatoire après l'entraînement.

**Ressources centrales :**
- Génération : generation ;
- Scoring : vraisemblance, cross-entropy ;
- Apprentissage : training-examples, cross-entropy, loss, gradients ;
- Évaluation et pratique : evaluation-experimentale, avec un périmètre présenté explicitement.

Le teacher forcing et les exemples décalés appartiennent à la branche apprentissage. Le prefill et le decode appartiennent à l'exécution de l'inférence. Ces notions sont liées mais ne sont pas synonymes.

## 5. Vue synthétique du parcours à présenter au lecteur

La page d'entrée de « Comprendre les LLM » devrait pouvoir être résumée par cette structure :

    COMPRENDRE LES LLM
    │
    ├── 1. Découvrir le système
    │      Qu'est-ce qu'un LLM ? Que fait-il ?
    │
    ├── 2. Comprendre une prédiction
    │      Texte → représentations → Transformer → distribution
    │
    └── 3. Comprendre les usages de la prédiction
           ├── Générer du texte
           ├── Scorer une cible observée
           └── Apprendre en ajustant les paramètres

    En complément, à tout moment :
    - Construire un petit GPT
    - S'exercer et expérimenter
    - Approfondir les notions
    - Explorer la carte et le glossaire

Cette vue est un résumé d'orientation, pas un nouveau graphe computationnel. Elle ne remplace ni data/computational-graph.yml, ni le registre des concepts, ni le parcours guidé détaillé.

## 6. Améliorations recommandées

### P0 — Clarifier la promesse et l'entrée dans le parcours

1. Créer ou réviser une courte page d'entrée « Comprendre les LLM » qui présente les trois questions ci-dessus.
2. Montrer explicitement le résultat attendu : comprendre le calcul d'une prédiction, puis les trois usages de cette prédiction.
3. Distinguer visuellement le parcours conseillé de la carte exploratoire des ressources.
4. Garder le vocabulaire d'entrée simple ; les termes techniques sont introduits au moment où ils deviennent nécessaires.

### P0 — Rendre visible la bifurcation après la distribution

1. Conserver les huit étapes détaillées dans le modèle de parcours si elles restent utiles à la génération de ressources.
2. Dans l'interface, regrouper les étapes 2 à 5 sous une seule grande partie « Comprendre une prédiction ».
3. Présenter génération, scoring et apprentissage comme trois branches, pas comme une suite de prérequis.
4. Signaler l'évaluation comme une pratique transversale sur des données tenues à l'écart.
5. Ne pas faire de la loss ou des gradients un prérequis à la compréhension de la génération.

### P1 — Harmoniser la sidebar sans perdre les ressources

Structure de navigation cible, à considérer comme un regroupement de lecture :

- **Comprendre les LLM**
  - Vue d'ensemble
  - Comment une prédiction est calculée
    - Du texte aux tokens
    - Des tokens aux représentations
    - Le calcul du Transformer
    - Des logits à la distribution
  - Que fait-on de la prédiction ?
    - Générer du texte
    - Scorer des tokens observés
    - Apprendre et ajuster les paramètres
  - Limites et questions ouvertes (aperçu, puis lien vers Approfondir)

- **Construire un petit GPT**
- **S'exercer et expérimenter**
- **Approfondir**
- **Glossaire et histoire**

Les intitulés ci-dessus sont des libellés de navigation, pas une demande de créer une page pour chaque ligne. Réutiliser les pages canoniques et préserver leur contenu. Les variantes d'architectures, détails mathématiques et mécanismes d'efficacité restent accessibles dans Approfondir ; ne pas rendre les pages de référence difficiles à retrouver.

### P1 — Clarifier les liens entre les parcours

- Depuis Comprendre, proposer « Mettre en pratique : construire un petit GPT » au moment où le lecteur a acquis la vue d'ensemble.
- Depuis Build, renvoyer vers l'explication conceptuelle correspondante, sans dupliquer son contenu.
- Depuis Practice, relier chaque exercice aux notions qu'il mobilise et au parcours conceptuel associé.
- Depuis Deepen, indiquer clairement le concept parent et ce que l'approfondissement apporte.
- Le glossaire sert de référence transversale ; il ne constitue pas une étape du parcours.

### P1 — Simplifier la représentation d'accueil

Remplacer la présentation initiale très détaillée par une figure compacte :
1. contexte ;
2. calcul du modèle ;
3. distribution du prochain token ;
4. trois branches génération / scoring / apprentissage.

Ajouter une mention « évaluation transversale ». Garder le schéma computationnel détaillé sur une page de synthèse ou derrière un lien « Voir le détail du calcul ». Préserver tous les liens canoniques du schéma existant.

### P2 — Valider l'expérience de lecture

Tester avec quelques tâches simples, en français et en anglais :
- « Je découvre les LLM : où commencer ? »
- « Je veux comprendre comment le texte devient une prédiction. »
- « Je veux comprendre comment un LLM génère un token. »
- « Je veux comprendre comment le modèle apprend. »
- « Je veux implémenter un petit GPT. »
- « Je veux approfondir l'attention. »

Pour chaque tâche, vérifier le nombre de décisions de navigation, la clarté du prochain pas, les retours possibles vers la vue d'ensemble et l'absence de pages avancées présentées comme obligatoires. Réaliser les contrôles visuels responsive, clavier et lecteur d'écran sur le site rendu.

## 7. Principes à préserver pendant l'évolution

- **Pas de perte d'information :** toute section déplacée ou raccourcie doit avoir une destination documentée.
- **Pas de duplication de concepts :** une page canonique, plusieurs chemins d'accès possibles.
- **Pas de fausse linéarité :** l'ordre pédagogique ne doit pas être confondu avec les dépendances computationnelles.
- **Pas de prérequis artificiels :** scoring et gradients ne sont pas nécessaires pour comprendre l'inférence.
- **Pas de confusion des phases :** prefill/decode pour l'inférence ; teacher forcing et cibles décalées pour l'apprentissage.
- **Pas de sur-ingénierie :** réutiliser les dimensions de métadonnées, les registres, les cartes et les générateurs existants ; ne pas introduire un second modèle de curriculum.
- **Parité FR/EN :** même structure conceptuelle et mêmes intentions, avec des formulations naturelles dans chaque langue.
- **Progressive disclosure :** présenter peu de choix au début, mais garder les détails accessibles.
- **Évaluation honnête :** distinguer vérification du code, optimisation de la loss et généralisation sur données tenues à l'écart.

## 8. Plan de réalisation proposé

1. Valider la structure de haut niveau et les libellés de navigation.
2. Réviser la page d'entrée Comprendre et la vue simplifiée du parcours.
3. Réconcilier data/guided-route.yml avec la présentation en trois questions et les branches, sans casser le générateur actuel.
4. Réorganiser la sidebar FR/EN à partir des responsabilités de pages déjà documentées.
5. Mettre à jour les liens croisés et les cartes générées.
6. Vérifier les métadonnées, les pages canoniques, les liens internes et le rendu Quarto.
7. Faire une revue responsive, clavier et lecteur d'écran avant de considérer l'amélioration terminée.

Ne pas entreprendre une réécriture simultanée de toutes les pages. Commencer par l'orientation et la navigation, puis ajuster les pages uniquement là où un écart réel est constaté.

## 9. Critères d'acceptation

- Un nouveau lecteur identifie en moins d'une minute où commencer et ce qu'il va apprendre.
- Il peut résumer le parcours en trois questions sans connaître les huit étapes techniques.
- Il comprend que le calcul partagé se termine à une distribution conditionnelle.
- Il voit génération, scoring et apprentissage comme trois usages distincts de cette distribution.
- Il ne confond pas évaluation et entraînement.
- Il peut accéder à Build, Practice et Deepen sans que ces parcours soient présentés comme des étapes obligatoires de Comprendre.
- Toutes les ressources actuelles restent accessibles et leur contenu est conservé.
- La navigation FR et EN est conceptuellement cohérente.
- La carte des connaissances reste un outil d'exploration et n'est pas transformée en parcours linéaire.
- Les contrôles de rendu et d'accessibilité sont documentés avec des preuves, pas supposés à partir des seuls fichiers sources.

## 10. Décision recommandée

**Ne pas ajouter davantage d'étapes au parcours.** La prochaine amélioration à fort rendement consiste à réduire la complexité perçue : trois questions pour comprendre, une distribution prédictive comme pivot conceptuel, trois usages frères, et trois parcours complémentaires (Construire, Pratiquer, Approfondir).

Le parcours détaillé à huit étapes et le graphe computationnel restent utiles en arrière-plan. L'interface doit en proposer une projection pédagogique plus simple, fidèle à leur structure et compréhensible dès la première visite.


## 11. Intégration avec les audits et travaux déjà existants — revue du 2026-11-09

Cette section complète l'audit après comparaison avec les audits de parcours, de navigation et de pages déjà présents dans le dépôt. Elle prévaut sur toute recommandation antérieure de ce document qui conduirait à dupliquer un dispositif existant.

### 11.1 Références propriétaires et non-duplication

| Sujet | Référence propriétaire | Rôle de cet audit |
|---|---|---|
| Coordination du design pédagogique global | Issue #130 | Fournir une synthèse de haut niveau et ses décisions, sans créer de roadmap parallèle |
| Ergonomie et navigation | `docs/reviews/navigation-ergonomics-audit-2026-11-09.md`, issue #337 | Vérifier la cohérence du parcours simplifié avec les règles et pilotes de navigation existants |
| Curriculum et dépendances | `docs/learning-path.md`, `data/guided-route.yml`, `docs/learning-path-audit-2026-11-05.md` | Ne pas remplacer ni recopier les huit étapes |
| Revue des pages et transitions | `docs/audits/learning-route-page-review-2026-11-09.md`, `docs/guided-route-page-review-2026-11-09.md` | Ne pas relancer les audits de contenu déjà effectués ; signaler uniquement les écarts de présentation globale |
| Cohérence des motifs de page | `docs/audits/guided-route-pattern-coherence-2026-11-09.md` | Réutiliser les rappels et self-checks existants |
| Graphe computationnel | `docs/canonical-computational-spine.md`, issue #584 | Utiliser le pivot distribution et ses branches sans créer de nouveau graphe |
| Accueil et son rendu | Issue #341 | Confier à cette issue la vérification navigateur du schéma détaillé et des quatre portes d'entrée |
| Validation formative | Issue #447 | Ne pas confondre navigation réussie et compréhension effective |

### 11.2 Vérifications qui changent les recommandations initiales

L'inspection directe des sources actuelles montre que plusieurs suggestions de la section 6 sont **déjà satisfaites** ou doivent être limitées :

1. **Les trois usages de la distribution sont déjà présentés dans le panorama.** `site/fr/llm-overview.qmd` et son équivalent EN contiennent un rappel d'une minute, un schéma partagé avec trois branches, une version mobile et les explications de génération, scoring et apprentissage. Le texte distingue également l'évaluation du scoring.
2. **Prefill/decode et teacher forcing sont déjà introduits dans ce panorama.** Ils sont associés aux branches correctes : phases d'inférence d'une part, politique de contexte en apprentissage d'autre part.
3. **La page d'accueil a déjà quatre destinations lisibles.** Son schéma computationnel détaillé vient après les portes d'entrée et le texte explicatif ; il n'est donc pas affiché comme unique première représentation du système.
4. **La carte sépare déjà explicitement parcours guidé et exploration.** Elle dérive le premier du curriculum et la seconde de la sidebar et des métadonnées.
5. **La sidebar possède déjà des regroupements pour le calcul de la prédiction, le scoring et l'apprentissage.** Une nouvelle hiérarchie proposée sans comparer les pilotes existants serait redondante.

En conséquence, les propositions initiales suivantes sont retirées comme actions immédiates :
- créer une nouvelle page ou un nouveau registre « Comprendre » ;
- ajouter une seconde figure des trois branches dans le panorama ;
- remplacer le parcours guidé à huit étapes par un parcours à trois étapes dans `data/guided-route.yml` ;
- déplacer ou supprimer le schéma détaillé de l'accueil sans défaut de rendu démontré ;
- réorganiser toute la sidebar sur la seule base de la maquette de cet audit.

### 11.3 Projection simplifiée à retenir — sans nouvelle source de données

Les trois questions proposées dans cet audit sont un **résumé éditorial** du parcours existant, et non une nouvelle structure de curriculum :

1. **Qu'est-ce qu'un LLM ?** — déjà porté par l'accueil et `llm-overview`.
2. **Comment calcule-t-il une prédiction ?** — étapes 2 à 5 du guided route, dont les pages centrales sont déjà reliées.
3. **Que fait-on de cette prédiction ?** — étapes 6 à 8, à présenter comme trois usages frères ; l'évaluation reste transversale.

Cette synthèse peut être réutilisée dans des textes d'orientation, des introductions ou des explications orales. Elle ne doit pas générer une deuxième navigation, un deuxième stepper ou une deuxième liste de pages. Le parcours détaillé à huit étapes reste la progression conseillée ; les trois questions en donnent une lecture de niveau supérieur.

### 11.4 Application concrète et propriétaires

| Action | Décision après réconciliation | Propriétaire / preuve |
|---|---|---|
| Accueil : premier écran et schéma détaillé | Conserver la source actuelle ; vérifier le rendu, la lisibilité, les interactions SVG, les labels et le responsive | #341 ; réutiliser les artefacts de navigateur existants |
| Panorama : trois usages | Conserver les schémas desktop/mobile et le rappel existants ; ne pas dupliquer | Revue de source déjà réalisée ; rendu spécifique à intégrer aux contrôles existants |
| Sidebar : groupes de calcul | Suivre le pilote limité de `navigation-ergonomics-audit` : commencer par le groupe texte/tokens avec `text-data` comme destination, seulement si lien et disclosure sont distincts et accessibles | #337 |
| Sidebar : autres groupes | Ne pas généraliser avant validation du pilote ; examiner ensuite embeddings, Transformer et logits ; scoring/loss séparément | #337 |
| Guided route | Garder huit étapes et leurs appartenances multiples intentionnelles (notamment generation et cross-entropy) | `data/guided-route.yml` ; audits de cohérence existants |
| Carte | Conserver la séparation route / exploration et vérifier que la sidebar modifiée ne crée aucun doublon | #337 ; générateur de carte existant |
| Build / Practice / Deepen | Maintenir ces destinations complémentaires ; ne pas les convertir en étapes de Understand | `docs/content-section-mapping.md`, #78 et #130 |
| Validation d'apprentissage | Tester si le lecteur sait reformuler le calcul partagé et distinguer les trois usages ; ne pas inférer ce résultat des tests CI | #447, après les prérequis de rendu indiqués dans cette issue |

### 11.5 Ordre de mise en œuvre révisé

1. **Ne pas modifier les sources canoniques du curriculum ou du graphe** : elles décrivent déjà correctement les relations et les huit étapes.
2. **Réaliser le pilote de sidebar déjà spécifié dans #337**, en commençant par un seul groupe et en respectant le contrat d'accessibilité. Si Quarto ne permet pas deux actions distinctes, ne pas ajouter de JavaScript ad hoc.
3. **Vérifier l'effet de ce pilote sur la carte générée**, les destinations, les contextes pédagogiques et la parité FR/EN.
4. **Achever la revue de l'accueil dans #341**, en réutilisant les preuves existantes et en n'ouvrant des corrections que sur des défauts reproductibles.
5. **Faire une revue de tâches de navigation** N1–N6 décrites dans l'audit ergonomique, puis une session manuelle clavier/tactile/lecteur d'écran pour N7–N8.
6. **Exécuter le pilote apprenant #447** une fois les conditions de rendu/accessibilité satisfaites.

### 11.6 Critère de décision pour toute modification supplémentaire

Avant toute modification de page ou de navigation, répondre à ces questions :
- Quel problème lecteur observable est corrigé ?
- Quelle source canonique possède déjà cette information ?
- La proposition réutilise-t-elle cette source ou crée-t-elle une projection concurrente ?
- Le changement préserve-t-il les appartenances multiples et les différences de granularité ?
- Quel contrôle existant valide le résultat (CI, rendu navigateur, tâche de navigation ou pilote apprenant) ?

Si aucun défaut concret n'est identifié, conserver l'existant. Le principal résultat de cet audit est la clarification de la lecture haut niveau et la priorisation des travaux existants, pas une refonte supplémentaire.
