# Parcours principal — travail restant et critères de clôture

**État de référence : 2026-11-24**  
**Périmètre :** parcours principal Understand, transitions vers Practice, articulation du graphe computationnel et validations éditoriales FR/EN.

Ce document est le plan d'exécution courant. Il complète le registre architectural `docs/canonical-computational-spine.md` et l'inventaire des audits `docs/page-audit-inventory.md`. Il ne remplace ni ces sources ni les issues qui portent les chantiers transverses.

## 1. Décision d'architecture à préserver

Le parcours principal doit être lisible comme un livre, mais il ne doit pas transformer le calcul d'un LLM en une succession mathématiquement fausse.

Le noyau partagé est :

```text
contexte → forward pass → logits → distribution conditionnelle
```

Cette distribution ouvre trois usages distincts :

- **Génération / inférence** : sélectionner ou échantillonner un token, le réinjecter dans le contexte, puis recommencer avec des paramètres fixes.
- **Scoring d'une cible observée** : lire la probabilité du token de référence avec le préfixe observé, puis construire une vraisemblance ; aucun token n'est sélectionné et aucun paramètre n'est mis à jour.
- **Apprentissage** : agréger les pénalités des cibles observées en une loss, calculer les gradients, puis mettre à jour les paramètres.

Le graphe computationnel décrit les opérations et leurs relations typées. Le parcours guidé décrit un ordre pédagogique. Le graphe de concepts décrit les relations de connaissance. Le parcours Build décrit la réalisation logicielle. Ces représentations doivent se référencer, mais ne doivent pas être fusionnées.

Dans le détail du Transformer, Q/K/V restent des projections des états d'entrée de chaque bloc, à l'intérieur de ce bloc. Elles ne constituent pas une étape située après les représentations contextualisées finales.

**Conséquence éditoriale :** conserver un fil principal concis et intelligible ; placer les exercices et questions dans leurs pages Practice dédiées ; relier les approfondissements et les implémentations sans les injecter dans le fil Understand.

## 2. État des changements récents

| Élément | État au 24-11-2026 | Décision |
|---|---|---|
| PR [#1602](https://github.com/JM-Brun/llm-lab/pull/1602) — consolidation Entropie | Fusionnée | Considérer le contenu comme intégré. Les liens du Panorama et les relations de carte avaient été corrigés. |
| PR [#1603](https://github.com/JM-Brun/llm-lab/pull/1603) — première migration Practice Attention | Fermée, remplacée | Ne pas la reprendre ; son successeur est #1604. |
| PR [#1604](https://github.com/JM-Brun/llm-lab/pull/1604) — page Practice dédiée à l'attention à produit scalaire | Ouverte, fusionnable, CI en échec ; Quarto annulé au dernier contrôle | Corriger les artefacts de carte bilingues périmés, puis refaire tous les contrôles. |
| PR [#1606](https://github.com/JM-Brun/llm-lab/pull/1606) — transition distribution prédictive → scoring | Ouverte, fusionnable, CI en échec ; Quarto réussi au dernier contrôle | Adapter le test de contrat des transitions au troisième lien typé, sans supprimer la relation pédagogique. |
| Issue [#575](https://github.com/JM-Brun/llm-lab/issues/575) | Fermée comme décision architecturale terminée | Ne pas la rouvrir pour des tâches éditoriales ou de validation. |
| Issue [#584](https://github.com/JM-Brun/llm-lab/issues/584) | Ouverte | Conserver les validations lecteur, accessibilité et intégration résiduelles ici. |

### 2.1 PR #1604 — migration des exercices Attention

Le contenu déplacé est le bon périmètre : l'exercice « mélange pondéré ou sélection ? » rejoint la page Practice dédiée à l'attention à produit scalaire ; l'ancien ancrage reste une redirection éditoriale afin de préserver les liens existants. L'exercice multi-têtes reste dans la collection générale, car il porte sur l'implémentation du bloc multi-têtes et non sur le calcul mono-tête.

**Échec CI observé :**

- Contrôles de qualité et validation de domaine : succès.
- Tests : **816 réussis, 2 échoués, 1 ignoré**.
- Quarto : exécution annulée ; il faut la relancer après correction.
- Les deux échecs sont `test_tracked_interactive_map_matches_renderer[fr]` et `[en]`.
- Les fichiers suivis `site/includes/generated-map-data-fr.qmd` et `site/includes/generated-map-data-en.qmd` ne contiennent pas les relations Entropie → fiche de révision sur la compression et → expérience de théorie de l'information attendues par le générateur.

**Travail requis :**

1. Régénérer les deux projections depuis les données canoniques présentes sur le head courant, avec la commande indiquée par le test :  
   `uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python site/tools/build_learning_map.py`
2. Vérifier que la génération ne retire aucune relation ajoutée par la consolidation Entropie #1602.
3. Vérifier les liens de la page Practice FR/EN vers la collection approfondie et le maintien de l'ancien ancrage.
4. Relancer les tests Python, le rendu Quarto, les contrôles de liens et l'audit Chromium existant.
5. Inspecter les captures FR/EN et les résultats d'accessibilité avant fusion.

Ne pas corriger le test de fraîcheur en le désactivant ou en réduisant ses assertions : les projections doivent correspondre au générateur.

### 2.2 PR #1606 — transition vers le scoring

La relation ajoutée exprime que la distribution prédictive commune peut être utilisée pour scorer une cible observée. Elle ne crée ni nouvelle étape dans le parcours linéaire ni prérequis entre génération et scoring.

**Échec CI observé :**

- Contrôles de qualité et validation de domaine : succès.
- Tests : **817 réussis, 1 échoué, 1 ignoré**.
- Quarto : succès sur le head contrôlé.
- L'échec est `test_route_document_uses_the_strict_transition_schema` dans `tests/knowledge/test_guided_route_transitions.py`.
- Le test attend exactement deux transitions ; le registre en contient maintenant trois, dont la nouvelle transition `predictive-distribution-to-observed-scoring`.

**Travail requis :**

1. Examiner le test et le contrat Pydantic de `GuidedRouteTransition`.
2. Remplacer l'hypothèse fragile « exactement deux transitions » par des assertions sur le schéma strict et les invariants utiles : identifiants uniques, références de stages valides, pages FR/EN valides, direction et champs obligatoires.
3. Ajouter une assertion explicite sur la présence et la sémantique de `predictive-distribution-to-observed-scoring`.
4. Vérifier que la transition est projetée dans le contexte de lecture de `fr/vraisemblance` et `en/likelihood`, sans devenir un prérequis du parcours.
5. Régénérer les projections dérivées si le générateur l'exige, puis relancer Python, Quarto, liens et audit Chromium.

Ne pas supprimer la transition pour satisfaire l'ancien nombre attendu. Ne pas transformer cette relation en dépendance de parcours.

## 3. Travail restant, ordonné par dépendances

### P0 — Débloquer et intégrer les deux PR

- [ ] **P0.1 — #1604 :** régénérer les cartes FR/EN depuis les données canoniques ; vérifier les relations Entropie ; obtenir une CI verte.
- [ ] **P0.2 — #1606 :** rendre le test de contrat des transitions indépendant d'un nombre codé en dur ; tester explicitement la nouvelle relation ; obtenir une CI verte.
- [ ] **P0.3 — #1604 et #1606 :** attendre le rendu Quarto et l'audit navigateur finaux ; inspecter les artefacts ; fusionner seulement après succès.
- [ ] **P0.4 — Réconciliation :** après fusion, vérifier que les deux changements coexistent sur `main` et que les cartes, fragments de contexte et liens bilingues sont à jour.

### P1 — Terminer la vérification du parcours principal

Cette étape est un audit ciblé des pages et transitions, pas une nouvelle refonte de l'architecture.

- [ ] **P1.1 — Vérifier la continuité Understand :** pour chaque transition centrale, confirmer que la page précédente prépare effectivement la suivante, que les notions nécessaires sont définies ou reliées et qu'aucune étape facultative ne semble obligatoire.
- [ ] **P1.2 — Vérifier les frontières entre niveaux :** les leçons Understand expliquent les mécanismes ; Build traite l'implémentation ; Deepen porte les formalismes et variantes avancés ; Practice porte les questions, exercices, corrigés et tâches de transfert.
- [ ] **P1.3 — Vérifier les liens de sortie des leçons :** chaque leçon centrale doit proposer un accès clair à sa page Practice dédiée lorsqu'elle existe. Les liens ne doivent pas multiplier les renvois redondants vers le catalogue générique.
- [ ] **P1.4 — Vérifier FR/EN :** mêmes objectifs, mêmes étapes, mêmes exercices essentiels et mêmes relations, avec une terminologie localisée cohérente.
- [ ] **P1.5 — Vérifier les projections générées :** cartes de connaissances, fragments de contexte guidé et vues du graphe doivent être régénérés depuis leurs sources canoniques. Ne pas éditer manuellement un artefact généré pour masquer un décalage.
- [ ] **P1.6 — Vérifier le graphe computationnel contre les leçons :** distribution partagée, génération, scoring, évaluation à paramètres fixes et entraînement doivent garder des sémantiques distinctes. Le préfixe généré et le préfixe observé ne doivent pas être confondus.
- [ ] **P1.7 — Vérifier les détails Transformer :** Q/K/V proviennent des états d'entrée de chaque bloc ; masque causal et masque de loss ont des rôles différents ; les variantes Pre-LN/Post-LN ne sont pas présentées comme une règle universelle.

Réutiliser `docs/page-audit-inventory.md` et les audits déjà enregistrés. Ne pas recommencer les vérifications de source déjà validées sans régression concrète. Ajouter une entrée datée à l'inventaire pour chaque nouveau groupe audité, avec pages, critères, preuves, anomalies et décisions.

### P2 — Validation lecteur et accessibilité manuelles

Ces vérifications ne sont pas remplaçables par les tests automatiques, les captures ou un score axe.

- [ ] **P2.1 — Lecteur d'écran FR :** parcourir le panorama et un échantillon représentatif des pages Understand, Practice et Build avec un lecteur d'écran réel ; noter ordre de lecture, titres, liens, annonces des schémas et changements de langue.
- [ ] **P2.2 — Lecteur d'écran EN :** réaliser le même contrôle en anglais ; relever les écarts de libellés et de navigation.
- [ ] **P2.3 — Fil d'Ariane natif :** vérifier visuellement et au clavier l'ascendance, les libellés localisés, l'ordre, la destination et l'absence de doublon avec les autres repères de navigation.
- [ ] **P2.4 — Touch/mobile :** vérifier sur appareil ou émulation tactile les zones interactives, les menus, les cartes et les liens de progression.
- [ ] **P2.5 — Tracer les preuves :** noter environnement, pages, opérations effectuées, résultat, défauts et limites. Un contrôle non réalisé doit rester explicitement « non vérifié ».

### P3 — Validation pédagogique indépendante

- [ ] **P3.1 — Réutiliser le protocole de l'issue [#447](https://github.com/JM-Brun/llm-lab/issues/447)** pour tester si un lecteur peut expliquer le calcul partagé puis distinguer génération, scoring et apprentissage.
- [ ] **P3.2 — Tester la navigation sans guidage :** demander à un lecteur de trouver la suite logique, la page Practice et un approfondissement à partir d'une leçon.
- [ ] **P3.3 — Relever les confusions réelles :** par exemple probabilité de la cible vs entropie de la distribution, masque causal vs masque de loss, teacher forcing vs préfixe généré, prefill vs decode.
- [ ] **P3.4 — Ne modifier le parcours qu'à partir de résultats observés :** documenter le problème, sa fréquence et la correction retenue. Ne pas ajouter de cartes, de transitions ou de JavaScript « au cas où ».

Le protocole et les résultats de validation pédagogique restent sous la responsabilité de #447 ; ce document ne transfère pas leur périmètre.

## 4. Critères de clôture

Le travail sur le parcours principal pourra être considéré comme stabilisé lorsque les conditions suivantes seront toutes satisfaites :

1. Les PR #1604 et #1606 sont fusionnées après validation complète de leur head final.
2. Les sources canoniques et leurs projections FR/EN sont cohérentes et les tests de fraîcheur passent.
3. Le parcours Understand est continu et compréhensible sans absorber Build, Deepen ou Practice.
4. Les leçons centrales donnent un accès non ambigu à leurs pages d'exercices dédiées.
5. Les distinctions calculatoires du registre architectural sont respectées dans les pages et leurs schémas.
6. Les validations automatiques de rendu, liens, responsive, clavier et axe sont vertes sur les heads finaux.
7. Les contrôles manuels lecteur d'écran et fil d'Ariane sont documentés ; les limites restantes sont explicitement transférées à leur issue propriétaire.
8. Les résultats de validation pédagogique sont enregistrés dans #447 ; les changements qui en découlent sont traçables.

## 5. Hors périmètre — ne pas relancer sans preuve nouvelle

- Reconcevoir le noyau computationnel déjà défini dans #575.
- Créer un second registre ou un nouveau système de navigation.
- Convertir automatiquement toutes les relations du graphe computationnel en prérequis pédagogiques.
- Fusionner génération, scoring et apprentissage en une boucle d'exécution unique.
- Ajouter une page d'exercices distincte pour chaque notion sans vérifier qu'elle apporte une vraie valeur ; privilégier les pages Practice thématiques cohérentes.
- Refaire les audits scientifiques, responsive ou de navigation déjà validés sans régression reproductible.
- Ajouter une nouvelle suite de tests navigateur ou un workflow GitHub Actions parallèle : réutiliser les mécanismes existants.

## 6. Mise à jour du statut

À chaque évolution significative, mettre à jour ce document et l'issue #584 avec :

- le commit ou le head de PR vérifié ;
- les contrôles réellement exécutés et leur résultat ;
- les artefacts consultés ;
- les points non vérifiés ;
- la prochaine action concrète et son issue/PR propriétaire.

Une PR fusionnée ne vaut pas preuve de validation lecteur. Une CI verte ne vaut pas preuve de compréhension pédagogique. Ces niveaux de preuve doivent rester séparés.


## Progress snapshot — 2026-11-24

This snapshot records only work completed after the execution plan was merged in PR #1607. It does not close a P1 item globally unless all of its pages and criteria have been checked.

| Work item | Progress from the current audit | Remaining scope |
|---|---|---|
| P1.1 — Understand continuity | **Partial.** The path predictive distribution → observed-target likelihood → cross-entropy → batch loss → gradients → training loop has been checked in FR/EN. The new prediction → scoring transition has the correct likelihood destination; the likelihood Practice exercise explicitly contrasts generated and observed prefixes. Evidence: the 2026-11-24 route audit in docs/page-audit-inventory.md. | Continue with the other unverified stage boundaries; do not infer that the whole nine-stage route is closed. |
| P1.2 — Understand / Build / Deepen / Practice boundaries | **Partial.** The inspected core lessons keep their questions in dedicated Practice companions. The training-loop code remains an optional, collapsed lookup-table experiment, clearly distinguished from the full GPT implementation in Build. | Continue the same check on the remaining core pages; retain optional code only where its role and scope are explicit. |
| P1.3 — Lesson-to-Practice links | **Partial.** The probability, likelihood, cross-entropy, loss, gradients and training-loop lesson pairs expose dedicated FR/EN Practice destinations. The scaled-attention companion is handled separately by #1604. | Verify the remaining Understand pages and ensure old anchors remain valid after future migrations. |
| P1.4 — FR/EN parity | **Partial.** The inspected route slice has matching objectives, exercises and destinations. A missing English likelihood → cross-entropy link was found and corrected in PR #1609. | Continue semantic parity checks beyond this slice; matching page counts alone are insufficient. |
| P1.5 — Generated projections | **In progress.** #1604 and #1606 are being validated on their corrected heads; the map freshness tests and route-projection checks must pass before their changes are integrated. | Reconcile maps and generated route/context fragments again after both merges. |
| P1.6 — Computational graph versus lessons | **Partial.** The direct prediction → scoring relation is now explicitly represented by #1606 as an explanatory transition, not a new prerequisite or serial stage. The inspected likelihood lesson preserves the observed-prefix/fixed-parameter semantics. | After #1606 merges, inspect the final graph and generated reader projections together; keep evaluation distinct from training. |
| P1.7 — Transformer details | **Not revisited in this pass.** Existing Q/K/V, causal-mask, positional-encoding and tensor-shape audit records remain authoritative. | Reopen only if a concrete regression or unresolved item in the inventory requires it. |

### Next bounded audit

The inference → context-use boundary is now audited in FR/EN: generation → in-context learning → context engineering. The audit found no need for a new page, route edge or diagram; the existing generation timeline and conditional context-engineering diagram remain in the earlier visual inventory. Continue from the remaining unverified boundaries rather than reopening completed Q/K/V, attention, positional-encoding, likelihood, cross-entropy or gradient derivations. The next bounded candidate is text input → representations: inspect the hand-off from text/data and token IDs to embedding lookup and positional information, focusing on page ownership, Practice destinations, FR/EN parity and route continuity. Reuse the existing source/math audit evidence; do not repeat derivations.

**Evidence boundary:** the 2026-11-24 source and executable checks do not substitute for the final-head browser review of #1604/#1606, manual screen-reader/native-breadcrumb work, or the independent learner pilot owned by #447.
