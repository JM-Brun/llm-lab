# Audit de navigation et d'ergonomie — 2026-11-09

**Statut :** synthèse source/backlog et plan de validation. Ce document ne prétend pas certifier le rendu publié ni l'efficacité pédagogique.  
**Coordination :** [#130](https://github.com/JM-Brun/llm-lab/issues/130), [#337](https://github.com/JM-Brun/llm-lab/issues/337).  
**Principe :** consolider les décisions et répartir les tâches dans les issues existantes ; ne créer aucun registre, taxonomie, workflow ou moteur de navigation parallèle.

## 1. Conclusion

L'architecture de LLM Lab est assez structurée pour éviter une refonte générale. Les parcours, graphes et navigation ont des responsabilités différentes. Le travail restant porte surtout sur la lisibilité de leurs projections dans le site publié et sur les preuves d'usage qui manquent.

Sources de vérité à préserver :

- parcours conceptuel : `data/guided-route.yml` et `docs/learning-path.md` ;
- parcours d'implémentation : Build path et roadmap #78 ;
- graphe computationnel : registre et vues suivis par #575/#584 ;
- graphe de concepts : `data/concepts.yml` et relations typées ;
- hiérarchie publiée : sidebar Quarto et métadonnées existantes ;
- contrat lecteur : `docs/pedagogical-breadcrumb-and-page-navigation-contract.md` et guides de page/design.

## 2. Modèle de navigation

| Dimension | Question lecteur | Source existante | À ne pas confondre avec |
|---|---|---|---|
| Orientation | Que puis-je apprendre ? | Accueil, panorama | Inventaire des pages |
| Progression | Par où commencer, que suivre ? | Guided route, learning path | Dépendances computationnelles ou Build |
| Localisation | Où suis-je dans le site ? | Sidebar et breadcrumb natifs Quarto | Hiérarchie conceptuelle |
| Contexte pédagogique | Pourquoi cette page est-elle ici ? | Contexte généré depuis le guided route | Breadcrumb de site |
| Exploration | Quelles ressources/notions sont liées ? | Carte des ressources, graphe conceptuel | Parcours obligatoire |
| Action locale | Quelle est la prochaine action utile ? | Liens contextuels | Un « suivant » générique |

Invariants :

1. Un seul breadcrumb de localisation : celui de Quarto.
2. Le contexte pédagogique reste séparé du breadcrumb.
3. Un stepper local décrit un processus, pas la navigation du site.
4. Une relation conceptuelle n'impose pas un ordre de lecture.
5. `suggested_route` ne signifie pas automatiquement prérequis.
6. Understand et Build gardent des progressions propres.
7. Practice & experiment reste transversal.
8. Les appartenances multiples justifiées ne sont pas réduites à un parent artificiel.
9. La parité FR/EN porte sur le sens, les destinations et les objectifs, pas sur une traduction littérale.
10. Source, test automatisé, rendu observé et usage humain sont des niveaux de preuve distincts.

## 3. Diagnostic de la sidebar

Inspection de `site/_quarto.yml` : les sidebars FR/EN utilisent `collapse-level: 1`. Les groupes de la séquence texte → distribution sont des sections sans destination propre. Plusieurs ont déjà une page d'entrée plausible :

| Groupe | Page candidate | Évaluation |
|---|---|---|
| Entrée : texte et tokens / Input: text and tokens | `text-data` | Forte : texte → tokens → IDs → vecteurs initiaux |
| Embeddings, position et contexte / Embeddings, position, and context | `embedding-space` | Forte : lookup et distinction avec états contextualisés |
| Calcul d'un bloc Transformer / Computing a Transformer block | `transformer` | Forte : vue d'ensemble du forward pass et du bloc |
| Logits, probabilités et entropie / Logits, probabilities, and entropy | `logits` | Forte : introduction aux logits |
| Scoring des tokens observés / Observed-target scoring | `vraisemblance` / `likelihood` | À vérifier : vraie page d'entrée ou notion spécialisée ? |
| Loss et gradients / Loss and gradients | `loss` | À vérifier : portée réelle de l'introduction |

Quarto permet une section avec `href` et `contents`. Le motif pourrait rendre le titre de groupe cliquable tout en conservant un contrôle de divulgation distinct. **C'est une hypothèse à tester dans le DOM rendu, pas une fonctionnalité déclarée validée.**

### Pilote recommandé

Piloter uniquement « Entrée : texte et tokens » en FR/EN :

- lier la section à `text-data` ;
- retirer `text-data` des enfants pour éviter le doublon ;
- garder `tokenization-strategies` comme enfant spécialisé ;
- vérifier que lien et disclosure sont deux actions distinctes ;
- ne pas augmenter globalement `collapse-level` ;
- ne pas créer de page d'overview artificielle.

Si Quarto ne fournit pas deux actions accessibles et distinctes, abandonner ce motif plutôt que d'ajouter du JavaScript ad hoc.

Après succès seulement, examiner Embeddings, Transformer et Logits. Scoring et Loss restent à décider séparément selon le rôle réel de leur page candidate.

### Effets induits

La sidebar alimente la carte via `site/tools/build_learning_map.py`. Vérifier donc l'absence de doublon, la stabilité des destinations, la parité FR/EN, le breadcrumb natif et les contextes pédagogiques générés.

## 4. Sémantique des transitions

Les liens doivent exprimer leur intention :

- **Continuer** : prochaine étape centrale du parcours ;
- **Prérequis** : connaissance réellement nécessaire, justifiée explicitement ;
- **Approfondir** : détail ou variante facultative ;
- **Pratiquer** : exercice ou investigation ;
- **Construire** : implémentation, walkthrough ou test ;
- **Explorer** : relation utile sans ordre obligatoire.

Le contrat existant et PR #645 ont déjà intégré les décisions de structure des breadcrumbs/transitions. Ne pas refaire cette conception : vérifier les cas ambigus dans le rendu.

## 5. Orientation locale d'une page

Le lecteur doit pouvoir répondre à trois questions sans accumulation de bandeaux :

1. Où suis-je ? — breadcrumb Quarto.
2. Pourquoi cette page ? — question, portée et objectif.
3. Que puis-je faire ensuite ? — suite centrale et alternative éventuelle, qualifiées.

Le contexte pédagogique n'est affiché que lorsqu'il est défini et défendable. Les pages d'overview, concept, Build, pratique, référence et deep dive conservent leurs besoins propres.

## 6. Carte et graphe : décisions à préserver

- La carte des ressources sert à découvrir l'inventaire et les destinations.
- Le parcours guidé présente une progression limitée et explicite.
- Le graphe conceptuel expose des relations typées sans imposer une séquence.
- Le graphe computationnel décrit les opérations et flux de calcul.

Les décisions de #415/#416/#417 restent applicables. Réutiliser les audits Chromium existants sans les relancer sans régression. Les preuves manquantes portent surtout sur le tactile réel et la revue manuelle avec technologies d'assistance. Les filtres doivent expliquer les relations dont une extrémité est masquée ; les alternatives textuelles et états vides/erreur restent des critères d'ergonomie.

## 7. Protocole de validation par tâches

| ID | Tâche | Preuve recherchée |
|---|---|---|
| N1 | Depuis l'accueil, trouver le parcours recommandé et ouvrir une leçon | Orientation |
| N2 | Depuis un groupe de menu, ouvrir la page d'entrée puis une page spécialisée | Lien et disclosure distincts |
| N3 | Retrouver localisation et contexte pédagogique depuis une leçon | Repères non redondants |
| N4 | Distinguer suite centrale et approfondissement | Sémantique des transitions |
| N5 | Passer de Understand à Build sans confondre les ordres | Articulation des parcours |
| N6 | Explorer une relation puis revenir à la page de départ | Découverte et récupération |
| N7 | Réaliser les actions principales au clavier puis sur tactile réel | Équivalence des interactions |
| N8 | Comprendre la navigation avec un lecteur d'écran | Noms, rôles, états et ordre |

Pour chaque exécution, consigner tâche, langue, page de départ, navigateur/version, viewport/appareil, mode d'interaction, chemin emprunté, hésitations/retours, résultat et défaut reproductible.

La compréhension n'est pas déduite d'un build, d'Axe ou d'une navigation réussie. Le pilote apprenant #447 reste propriétaire de cette preuve.

## 8. Répartition dans le backlog existant

| Issue propriétaire | Livrable |
|---|---|
| [#130](https://github.com/JM-Brun/llm-lab/issues/130) | Coordination et déduplication de l'architecture pédagogique |
| [#337](https://github.com/JM-Brun/llm-lab/issues/337) | Sidebar, carte, crosswalk et navigation publiée FR/EN |
| [#415](https://github.com/JM-Brun/llm-lab/issues/415) | Séparation parcours guidé / carte des ressources |
| [#416](https://github.com/JM-Brun/llm-lab/issues/416) | Sémantique et revue du graphe conceptuel |
| [#417](https://github.com/JM-Brun/llm-lab/issues/417) | Interaction clavier/souris/tactile et robustesse de la carte |
| [#584](https://github.com/JM-Brun/llm-lab/issues/584) | Spine computationnel et contexte des pages |
| [#447](https://github.com/JM-Brun/llm-lab/issues/447) | Compréhension par lecteur indépendant |
| [#329](https://github.com/JM-Brun/llm-lab/issues/329) | Revue du hub d'exercices |
| [#341](https://github.com/JM-Brun/llm-lab/issues/341) | Revue spécifique de l'accueil |
| [#191](https://github.com/JM-Brun/llm-lab/issues/191) | Contraste et design partagé |

### Tâches #337

- [ ] Vérifier le rendu Quarto `section + href + contents` et l'indépendance du lien et du disclosure.
- [ ] Implémenter le pilote FR/EN seulement si les deux actions sont accessibles et distinctes.
- [ ] Vérifier que `text-data` n'apparaît qu'une fois dans le menu et dans la carte.
- [ ] Vérifier la parité FR/EN, le breadcrumb et les destinations.
- [ ] Vérifier la projection de la carte générée et les liens de retour.
- [ ] Étendre à Embeddings, Transformer et Logits uniquement si le pilote est concluant.
- [ ] Examiner séparément Scoring et Loss ; ne pas généraliser sans preuve.
- [ ] Exécuter N1–N6 en FR/EN sur desktop/mobile et consigner les résultats.
- [ ] Coordonner N7–N8 avec #416/#417/#584 dans une session manuelle commune.
- [ ] Rattacher chaque défaut reproductible à son issue propriétaire.

### Tâches humaines coordonnées

- [ ] Une session clavier/lecteur d'écran FR/EN sur sidebar, breadcrumb, contexte pédagogique, carte et graphe.
- [ ] Une session tactile réelle sur sélection/ouverture et navigation dans la carte.
- [ ] Un pilote de compréhension distinct via #447.

## 9. Critères d'acceptation

Le pilote est accepté si le lien ouvre la page attendue, le disclosure reste indépendant, les deux actions sont utilisables au clavier et au tactile, aucune page n'est dupliquée, la carte générée reste cohérente, FR/EN sont équivalents, et le breadcrumb reste exact. La mise en page doit rester utilisable sur petit écran et au zoom.

La revue #337 peut être clôturée lorsque les destinations/crosswalk rendus sont cohérents et que chaque défaut a un propriétaire. Les preuves humaines peuvent rester dans leurs issues dédiées si elles sont explicitement reliées.

## 10. Hors périmètre

Pas de registre, taxonomie ou workflow parallèle ; pas de refonte générale de la sidebar ; pas d'augmentation globale de `collapse-level` pour un problème local ; pas de fusion des graphes/parcours ; pas de réécriture sans défaut reproductible ; pas de revendication d'accessibilité ou d'apprentissage non démontrée.

## 11. État des preuves au 2026-11-09

- **Établi par inspection source :** hiérarchie Quarto, `collapse-level: 1`, pages candidates, responsabilités des structures et issues propriétaires.
- **Déjà vérifié par automatisation/rendu antérieur :** plusieurs cas FR/EN, desktop/mobile, contextes de parcours, interactions clavier du graphe, absence de débordement dans les cas testés et contrôles Axe ciblés. Réutiliser SHA et artefacts existants.
- **Proposé, non validé :** section Quarto avec `href + contents` et généralisation à d'autres groupes.
- **Non démontré :** tactile réel, revue lecteur d'écran sur les composants concernés, amélioration de la compréhension et choix autonome de la prochaine étape.


## 12. Décision du pilote « texte et tokens » — 2026-11-09

La vérification du PAGE-MAP de `tokenization-strategies` révèle une contrainte éditoriale importante : cette page est explicitement `type:deep-dive`, `destination:deepen`, `level:advanced`. Elle ne doit donc pas être déplacée sous Understand uniquement pour remplir le groupe de navigation « Du texte aux identifiants ».

Le pilote retenu est plus conservateur que l'hypothèse initiale :
- supprimer le groupe intermédiaire « Du texte aux identifiants » qui ne contenait qu'une seule page ;
- placer directement `text-data` sous « Comment le modèle calcule sa prédiction » (FR/EN) ;
- conserver `tokenization-strategies` et les autres pages de tokenisation avancée sous Deepen ;
- ne pas dupliquer une page dans deux destinations ;
- laisser Quarto produire le breadcrumb natif à partir de la hiérarchie simplifiée.

Cette variante réduit un niveau de navigation sans mélanger les niveaux pédagogiques et sans ajouter de JavaScript. Elle est appliquée comme pilote source dans la branche `nav/pilot-flatten-text-data-entry`. Son acceptation dépend du rendu Quarto/Chromium : vérifier les destinations, breadcrumbs, carte générée, contexte pédagogique et parité FR/EN. En cas de régression, revenir au groupe initial plutôt que compenser par du code spécifique.

Le test porte sur une simplification de hiérarchie, pas sur la fonctionnalité expérimentale « section cliquable + disclosure ». Cette dernière reste non validée et n'est pas nécessaire pour ce groupe à page unique.
