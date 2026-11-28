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
| P1.1 — Understand continuity | **Partial.** The predictive distribution → observed-target likelihood → cross-entropy → batch loss → gradients → training loop path, inference → context-use boundary, and text-input → representations boundary have been checked in FR/EN. The new prediction → scoring transition has the correct likelihood destination; the likelihood Practice exercise explicitly contrasts generated and observed prefixes. The text-input slice revealed a remaining Practice-placement migration. Evidence: the 2026-11-24 route audit in docs/page-audit-inventory.md. | Continue with the other unverified stage boundaries; do not infer that the whole nine-stage route is closed. |
| P1.2 — Understand / Build / Deepen / Practice boundaries | **Partial.** Dedicated Practice companions exist across the inspected groups, but the text-data lesson still contains one practical task in its supplementary panel, and some pages do not expose the companion link under a consistent Practice heading. The training-loop code remains an optional, collapsed lookup-table experiment, clearly distinguished from the full GPT implementation in Build. | Continue the same check on the remaining core pages; retain optional code only where its role and scope are explicit. |
| P1.3 — Lesson-to-Practice links | **Partial.** Probability, likelihood, cross-entropy, loss, gradients, training-loop, text-data, embedding-space, positional-encoding and contextualized-representations all have FR/EN Practice companions. Link placement is inconsistent on some representation pages; the focused migration is recorded in the latest inventory entry. The scaled-attention companion is handled separately by #1604. | Verify the remaining Understand pages and ensure old anchors remain valid after future migrations. |
| P1.4 — FR/EN parity | **Partial.** The inspected route slices have matching objectives, exercise content and destinations. A missing English likelihood → cross-entropy link was found and corrected in PR #1609; the text-input/representations pages also have consistent FR/EN roles, with navigation placement to harmonize. | Continue semantic parity checks beyond this slice; matching page counts alone are insufficient. |
| P1.5 — Generated projections | **Integrated.** #1604 and #1606 are merged. Their final-head CI and Quarto/browser checks passed; the map freshness tests and bilingual route-transition checks passed. | Reconcile maps and generated route/context fragments again after both merges. |
| P1.6 — Computational graph versus lessons | **Integrated for this branch.** The direct prediction → scoring relation is merged as an explanatory transition, not a new prerequisite or serial stage. The likelihood lesson preserves the observed-prefix/fixed-parameter semantics, and the final route-projection and Quarto checks passed. | After #1606 merges, inspect the final graph and generated reader projections together; keep evaluation distinct from training. |
| P1.7 — Transformer details | **Partial.** Reused the existing Transformer, Q/K/V, scaled-attention and causal-mask scientific audits; inspected the article-level hand-off and FR/EN Practice ownership. The core route is coherent. A structural migration now gives Transformer and causal masking explicit link-only Practice sections and moves Q/K/V deepening, Build walkthroughs, FlashAttention and API/reference-code material under Further exploration. Evidence: the 2026-11-25 article-level audit in docs/page-audit-inventory.md and the focused content PR. | Validate the final PR head in Quarto and browser review; continue only with the remaining unverified stage boundaries. Do not re-derive the existing equations. |

### Next bounded audit

The text-input → representations migration is implemented in #1611. Its final-head CI and Quarto/browser checks must pass before it is treated as integrated; the initial browser run exposed a localized French collection-anchor assumption, now corrected in the browser-review contract without weakening the visible-link requirement.

The representations → computation boundary is now audited at article level in FR/EN. The focused migration gives Transformer and causal masking explicit link-only Practice sections, and places the Q/K/V deep dive, the optional Build walkthrough, FlashAttention and API/reference-code material under Further exploration. Existing explanations, equations, figures, citations, anchors and graph relations are retained. The scientific source audits are reused rather than repeated.

After this migration is validated, continue with the next unverified stage boundary from docs/page-audit-inventory.md. Do not reopen the already audited scoring/loss, gradient/training-loop, inference/context-use or text-input/representations groups without a concrete regression.

**Evidence boundary:** successful CI and browser checks validate technical and rendered-page contracts, not comprehension. Manual screen-reader/native-breadcrumb review and the independent learner pilot owned by #447 remain separate work.


## Progress snapshot — 2026-11-25 (Build contract audit)

- PR #1611 is merged: text-input → representations Practice ownership is normalized in FR/EN; its Python CI and full Quarto/browser review passed.
- PR #1613 is merged: representations → Transformer/Q/K/V/attention/causal-mask Practice and Further exploration boundaries are normalized; its final-head Python CI and full Quarto/browser review passed.
- The next bounded audit now follows the existing 2026-11-08 Build-tour inventory recommendation: compare each guided code tour with its actual source and unit tests.
- The first configuration-tour pass found a real contract mismatch: `GPTConfig` claimed positive integer dimensions but accepted positive floats at construction, and it deferred invalid seed errors to NumPy's RNG. A focused correction is under validation on branch `audit/build-config-validation-contract`, including FR/EN page and Practice alignment. It is not integrated until final-head CI and Quarto/browser checks pass.
- Remaining Build audit scope: `gpt_ops.py` → `transformer_block.py` → `gpt.py` → `generate.py`, including their code excerpts, tests, exercises and stated implementation limits. Do not repeat the earlier scientific or architecture audits; check only source-to-page consistency and uncovered test contracts.
- Manual screen-reader/native-breadcrumb review and the independent learner pilot under #447 remain separate evidence and are not closed by automated checks.


## Progress snapshot — 2026-11-25 (Build operations and model audit)

- The GPT configuration audit and correction are merged in PR #1614. Runtime integer validation, seed validation, tests, FR/EN tour and Practice alignment, generated map projection and browser self-check contract all passed final CI and Quarto/browser review.
- The operations / Transformer block / assembled GPT audit is carried forward on branch `audit/build-ops-model-precision-v2` after #1614 changed the shared generated-map files. It corrects the LayerNorm epsilon nuance, GELU error bound, GPT worked parameter count (6,386), prefix-invariance evidence scope, and duplicate exercise numbering. Its source/test suite passed; final Quarto/browser checks are running on the rebased content.
- The generation-tour correction is merged in PR #1617: `top_k` and `temperature` now receive fail-fast runtime validation; regression tests and the FR/EN walkthrough agree with the contract.
- All five guided Build tours have now been compared against implementation, tests, FR/EN explanations and Practice companions. PR #1618 carries the operations/block/model corrections and is awaiting final Quarto/browser checks. Once it merges, mark this bounded source-to-page audit complete; do not repeat the already-validated Transformer/QKV/attention scientific audit.
- Next independent evidence: manual screen-reader/native-breadcrumb and accessibility review, then the learner pilot under #447. Automated browser checks do not close either item.


## Next bounded Practice audit — training-example transfer (2026-11-25)

The previous recommendation to author BPE/window/leakage exercises is superseded: the bilingual Text data collection already contains TR-D (shifted windows), TR-E (BPE merge trace) and TR-F (split/tokenizer leakage). Their calculations and FR/EN solutions were independently checked in this pass; no correction or duplication is warranted. TR-A–TR-C remain the existing representation/lookup/context sequence. These labels are inventory shorthand; the pages use descriptive stable anchors.

The next content task is narrower: expand the existing FR/EN Practice companions for **training examples** with one or two transfer scenarios covering document-boundary/packing policy and padding/loss reduction. The current four self-checks already cover input-target shift, teacher forcing/causality, attention-vs-loss masks and logits axes. The lesson itself explains packing, EOS/boundary markers, cross-document attention, dynamic padding, and the distinction between attention and loss masks; the companion does not yet ask learners to apply these decisions to a concrete packed/padded batch.

**Implementation boundary:** keep `sliding_input_target_pairs` as the narrow window constructor. Its source and tests match the documented contract; it does not implement packing, padding, collators or loss masks. Do not add those features or tests until a concrete pipeline contract is selected. Exercises should remain conceptual and use the existing worked examples.

**Acceptance criteria for the next PR:**
1. FR/EN companions add the same task structure and equivalent worked reasoning, with stable descriptive anchors.
2. Learners distinguish the EOS/boundary marker from the cross-document attention policy and from target alignment.
3. Learners construct attention-valid positions and loss-valid targets separately, calculate a stated valid-token reduction, and diagnose the case where an attention mask is present but PAD labels still enter the loss.
4. No duplication of TR-D window-count arithmetic or TR-F leakage/split protocols.
5. The existing Quarto/browser workflow validates both companions, links, math, disclosures, mobile layout and keyboard activation; no new workflow is created.

The source-level findings and remaining tasks are recorded in [the audit report](audits/training-example-practice-gaps-2026-11-25.md) and the [page audit inventory](page-audit-inventory.md). Manual accessibility work remains under #483; learner validation remains gated under #447. CI and rendered checks do not establish comprehension.

**Dependency not yet integrated:** the CA-A lesson/companion migration is still open in #1622 and #1623. Their Quarto/browser jobs passed, but their Test suite jobs were cancelled and need a successful final-head rerun before merge. Keep the causal-masking ownership item open until then; this training-example audit is a separate next slice.


## Progress snapshot — 2026-11-25 (training-example Practice transfer)

- The bounded follow-up identified by the 2026-11-25 audit is implemented in PR [#1625](https://github.com/JM-Brun/llm-lab/pull/1625): the FR/EN training-examples Practice companions retain their four existing checks and add two transfer scenarios for packed document boundaries and padded-batch loss reduction.
- The packing exercise makes the three separate decisions explicit: target shift, cross-document attention visibility, and whether the first token after a boundary contributes to loss. It avoids implying that EOS itself blocks attention.
- The padding exercise constructs attention and loss masks separately and checks the valid-token mean (0.625) against the naive padded-position mean (1.2).
- The lesson pages, guided route, graph registries, generated maps and `sliding_input_target_pairs` implementation remain unchanged. The exercises do not claim to implement a packer or collator.
- The scope and pedagogical decisions are documented in `docs/audits/training-example-practice-transfer-2026-11-25.md`.
- **Status:** PR open; the final-head Quarto/browser audit is queued. Do not treat the change as integrated until the final CI and rendered checks pass and the artifacts have been inspected. Manual screen-reader review and learner validation remain separate evidence.


## Progress snapshot — 2026-11-25 (Q/K/V evidence and CA-A ownership)

- #1618, #1619 and #1620 are merged. The five guided Build tours are source/page/test-audited; the current Q/K/V pages have post-merge Chromium evidence and the current GitHub Pages artifact has been inspected. #483 remains open only for manual full-keyboard, touch and screen-reader checks; #447 remains gated.
- The CA-A causal-mask/prefix-invariance exercise was found in the shared Attention collection even though the causal-masking lesson linked to a dedicated Practice companion. The companion held only a short check. PR #1622 is merged after its Python CI, Quarto/browser review and secret scanning passed. PR #1626 moves CA-A into the dedicated companion, preserves the old collection anchors as link-only aliases, aligns the lesson's test-scope claims with the existing full-GPT test, and reconciles the roadmap status. No new implementation or test framework is needed.
- After CA-A integration, the next exercise gap to inspect is the text-data transfer sequence: BPE merge tracing, shifted windows and leakage/document-boundary handling. The existing TR-A/B/C and training-example material must be compared first; do not duplicate their representation/shape activities.
- Do not repeat the validated scoring/loss, gradient/training-loop, inference/context-use, text-input/representations, or Transformer/QKV/attention scientific audits. Reuse their evidence and only correct reproducible regressions.


## Fil rouge narratif et clin d'œil culturel — audit du 2026-11-26

Le contrat éditorial, l'état source-level FR/EN, la carte d'utilisation par étape Understand et les travaux restants sont consignés dans [running-example-and-editorial-easter-egg.md](running-example-and-editorial-easter-egg.md).

Décision : conserver le fil rouge comme support de raisonnement récurrent mais facultatif. Les exemples français et anglais peuvent être localisés différemment ; leur parité est conceptuelle et computationnelle, pas littérale. Ne pas forcer le clin d'œil dans chaque page, dans les exemples spécialisés d'ICL/context engineering ou dans les fixtures Build.

Le travail restant est borné : contrôler le rendu publié après déploiement, compléter éventuellement une expérience ICL à paramètres fixes et poursuivre la vérification des traces numériques FR/EN. La leçon de tokenisation prend désormais le préfixe du fil rouge comme matériau principal, y compris pour la comparaison de tokenizers et la trace de lookup ; le contraste d'espace initial dans Deepen réutilise également `situation` / ` situation`. L'intégration dans Build reste différée et appartient à [#924](https://github.com/JM-Brun/llm-lab/issues/924). Aucun nouveau registre, graphe, workflow ou parcours n'est requis.



## Reconciliation — 2026-11-28 (current main-route backlog)

This section supersedes stale snapshots above where their PR states or next actions have changed. It does not close the broader issues; it records the current execution order and the evidence boundary.

### Integrated since the previous snapshot

- [x] **Scoring transition and map projections:** PRs [#1604](https://github.com/JM-Brun/llm-lab/pull/1604) and [#1606](https://github.com/JM-Brun/llm-lab/pull/1606) are merged. The old P0 checklist for these PRs is historical; do not rerun or repair their former CI failures absent a reproducible regression on main.
- [x] **Understand/Practice migrations:** PRs [#1810](https://github.com/JM-Brun/llm-lab/pull/1810), [#1811](https://github.com/JM-Brun/llm-lab/pull/1811) and [#1813](https://github.com/JM-Brun/llm-lab/pull/1813) are merged. Training-example alignment/debugging, the SGD exercise, decoding temperature prediction and bilingual self-assessment disclosures are integrated. Their earlier pending-validation descriptions are superseded by the merged state.
- [x] **Understand destination evidence:** PR [#1814](https://github.com/JM-Brun/llm-lab/pull/1814) is merged. Batches 1–7 provide source→claim→FR/EN destination evidence for all 20 canonical Understand lessons.
- [x] **Nine-stage route hand-off:** PR [#1821](https://github.com/JM-Brun/llm-lab/pull/1821) is merged. The integration plan now names the current nine stages and distinguishes pedagogical order from computational dependencies.
- [ ] **Concept-bridge Practice link:** [PR #1824](https://github.com/JM-Brun/llm-lab/pull/1824) is open. It gives the separate `language-representation` bridge a shared Practice destination with `text-data`; the superseded #1820 branch is closed.
- [x] **Source-level intellectual-contribution inventory:** the 20 canonical Understand lessons are covered in [the consolidated #1739 matrix](source-syntheses/understand-route-intellectual-contributions-index-2026-11.md). This is source-level coverage, not proof that every contribution has a current bilingual published destination.

### Current open work and ownership

| Workstream | Verified state | Next action / owner |
|---|---|---|
| Dedicated Practice inventory — [#1512](https://github.com/JM-Brun/llm-lab/issues/1512) | 51 companion pages per language plus one catalogue page are on main. PRs #1810/#1811/#1813 are merged. PR #1814 also integrated the 20/20 Understand destination-evidence matrix. [#1824](https://github.com/JM-Brun/llm-lab/pull/1824) is open: it adds a shared FR/EN Practice destination for the `language-representation` bridge and `text-data`, without creating another exercise page. | Validate the final #1824 head (map freshness, CI, Quarto and browser artifact), then review/merge. Continue the full lesson→companion inventory; page counts alone do not prove semantic parity or that every assessment prompt has moved. |
| Intellectual contribution and destination evidence — [#1739](https://github.com/JM-Brun/llm-lab/issues/1739) | Source-level contribution and destination evidence are integrated for **20/20 canonical Understand lessons** through merged PR #1814 and batches 1–7. The published `language-representation` concept bridge is an additional route destination, not part of this 20-lesson denominator; its Practice hand-off is tracked separately in #1512 / PR #1824. | No further source inventory is required unless a lesson changes. Remaining gates: deployed FR/EN anchor/link verification, rendered transition review, manual accessibility and independent learner validation. Reuse existing source audits; do not repeat scientific reviews. |
| Understand route structure and duration — [#1208](https://github.com/JM-Brun/llm-lab/issues/1208), [#280](https://github.com/JM-Brun/llm-lab/issues/280) | The 20-lesson / 9-chapter migration ledger exists. Content pilots and browser coverage have advanced; PR #1803 is merged. The current issue still requires the exhaustive conservation matrix and rendered reading-time / learner checks. | Continue section-level source→destination reconciliation before shortening or splitting any lesson. Measure required rendered path in FR/EN; do not split by word count or duplicate canonical concepts. Keep this redesign distinct from the existing nine-stage route registry until the migration map is approved. |
| Computational-spine integration — [#584](https://github.com/JM-Brun/llm-lab/issues/584) | The shared model and generated route architecture are integrated. PR #1821 reconciles the nine-stage route in the integration plan. PR #1824 addresses the missing Practice hand-off for the separate `language-representation` bridge. Remaining work is manual screen-reader review, lesson-level breadcrumb semantics and bounded rendered checks; automated Axe/DOM evidence is not a substitute. | Coordinate manual FR/EN screen-reader and breadcrumb review with #988 for shared navigation. Transfer graph-edge review to #416 and learner comprehension to #447; do not duplicate their audits. |
| Foundations architecture — [#1732](https://github.com/JM-Brun/llm-lab/issues/1732) | Open architectural proposal; no parallel registry or independent curriculum should be created. | Keep as a cross-cutting design decision. Before implementation, map candidate formal material to existing Understand/Build/Deepen/Practice owners and confirm that Foundations adds a genuinely distinct learning outcome. |
| Common misconceptions — [#1633](https://github.com/JM-Brun/llm-lab/issues/1633) | Evidence-backed coverage proposal is open; no validated global registry yet. | Continue the six-case pilot and reuse existing lessons/Practice destinations. Do not create a slogan-based “myths” course or another per-concept workflow. |

### Completed and integrated — prediction-stage destination evidence

The prediction-stage audit in [batch 4](source-syntheses/understand-destination-evidence-batch-4-2026-11.md) was the first increment of this work. Its interim 13/20 count was superseded by batches 5–7; merged PR #1814 now carries the complete 20/20 canonical lesson matrix. Deployed anchor verification, accessibility and learner validation remain separate.

### Completed and integrated — generation and context-use destination evidence

Generation is documented in [batch 5](source-syntheses/understand-destination-evidence-batch-5-2026-11.md); ICL and context engineering are documented in [batch 6](source-syntheses/understand-destination-evidence-batch-6-2026-11.md). These batches reuse the existing source audits, verify FR/EN lesson and Practice destinations, and preserve the boundaries between inference, prompt-conditioned behavior and application-level context construction. Merged PR #1814 integrates the source-level evidence; no lesson change or new route stage was justified.

### Completed and integrated — all 20 destination-evidence records

The four scoring/training lessons are documented in [batch 7](source-syntheses/understand-destination-evidence-batch-7-2026-11.md). Together, batches 1–7 provide source-level destination evidence for all 20 canonical Understand lessons; merged PR #1814 integrates the matrix and evidence hand-off. No further source-ingestion or contribution-inventory campaign is required for #1739 unless a page changes.

### Next execution batch — rendered route and learner validation

1. Verify generated FR/EN anchors and local links on the deployed Quarto site for the 20 canonical lessons and the separate `language-representation` bridge, including the shared Practice hub and the documented Loss FR/EN heading difference.
2. Inspect the complete prediction → inference/scoring → training branches in rendered order. Check that the three uses of the shared predictive distribution remain visible and are not presented as one mandatory linear execution chain.
3. Run representative desktop/mobile and keyboard checks, then manual screen-reader review for the central route, generated maps and breadcrumb transitions. Reuse shared-navigation evidence rather than creating duplicate audits.
4. Conduct the learner review owned by #447: ask learners to reconstruct generation, scoring and training from the shared model and explain the role of context, targets, loss and updates. Record observed confusion before changing route order or adding pages.

### Revised priority order

1. **P0 — #1824 final-head validation:** complete repository-wide map freshness, CI, Quarto render and browser audit; review the final diff before merge. Do not merge while generated-map checks fail.
2. **P1 — #1739 rendered and learner evidence:** the 20/20 source-to-destination matrix is integrated. Remaining work is deployed-anchor/transition verification, accessibility and learner validation; do not start another source inventory.
3. **P1 — #1512 full bilingual Practice inventory:** continue after #1824; preserve worked explanations and only move genuinely learner-directed assessment/experimentation. The concept bridge uses an explicitly justified shared hub rather than a new page.
4. **P1 — #1208/#280 lesson migration:** continue conservation and duration evidence in parallel, but do not modify the guided route until the section-level destination map is approved.
5. **P2 — #584 manual accessibility:** schedule actual FR/EN assistive-technology and touch checks; reuse shared-navigation evidence from #988.
6. **P2 — #447 learner validation:** remains gated by #483; after accessibility review, test route reconstruction and branch distinctions and use observed confusion to justify any route change.

**Decision rule:** improve the main route through demonstrated continuity, explicit learning outcomes, complete bilingual destination evidence and reduced cognitive load. Do not add a stage, page, graph edge, metadata field or navigation widget merely because it appears structurally convenient.
