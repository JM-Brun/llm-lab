# Cahier de reprise — invariants critiques et KPIs

**Date de mise à jour :** 2026-11-18  
**Dépôt :** `JM-Brun/llm-lab`  
**Branche de travail :** `test/critical-invariants-audit-clean`  
**PR :** [#1277](https://github.com/JM-Brun/llm-lab/pull/1277)

Ce document est le point d'entrée opérationnel d'une future session. Il sépare les faits validés, les analyses statiques et les tâches non exécutées.

## 1. État validé

### Dernier SHA avec CI complète

Le SHA `d4ea580bd403c5b60984e56ebc3fdb2a994b90d9` a les résultats suivants :

| Contrôle | Run | Résultat |
|---|---:|---|
| CI Python quality/domain checks | `44375498268` | success |
| Suite pytest | `44375498268` | success |
| Quarto site & browser audit | `44375498283` | success |
| Secret scanning | `44375498160` | success |

Les résultats détaillés de la suite (673 tests, 98.19 % de couverture, 79.48 s sur deux workers) et les limites d'interprétation figurent dans [l'audit de la suite](test-suite-kpi-audit-2026-11-18.md#12-validation-complète-de-la-branche-propre-1277).

Les jobs opt-in « full-corpus extraction locator inventory » et « concept-registry scale benchmark » ont été ignorés. Aucun résultat ne doit leur être attribué.

### État de la PR au dernier contrôle

PR #1277 ouverte, en brouillon, fusionnable, non fusionnée, base `main`. Le SHA validé est également le head de branche à cet instant. Re-vérifier l'état avant toute action, car GitHub peut avoir reçu de nouveaux commits depuis cette note.

## 2. Ce qui a été effectivement livré

La PR porte des protections ciblées sur :
- stabilité numérique de la cross-entropy pour logits extrêmes et rejet des pertes non représentables ;
- gradients de cross-entropy et réduction de batch ;
- causalité de l'attention, générateurs aléatoires locaux et validation du type de longueur du masque ;
- LayerNorm à variance nulle et placement de l'epsilon ;
- projection linéaire sur entrée 2D ;
- addition des deux branches résiduelles du TransformerBlock ;
- indépendance des exemples dans le batch GPT.

Ces tests restent dans les modules pytest existants. Aucun second job pytest, aucune dépendance de mutation et aucun workflow de mutation n'ont été ajoutés.

## 3. Limites connues de l'environnement de travail

Les API GitHub disponibles permettent de lire et modifier les fichiers, les PR et les résultats Actions. Elles ne fournissent pas d'exécution arbitraire de commandes dans un clone du dépôt. Le clone local a échoué précédemment faute de résolution DNS vers GitHub.

**En conséquence, le pilote de mutations décrit ci-dessous n'a pas été exécuté.** Les propositions de mutations sont un protocole de reprise, pas des résultats. Pour les exécuter, utiliser un clone local ou un environnement CI de développement autorisé, avec une copie de travail propre.

## 4. Première tâche — pilote manuel de mutations

Objectif : vérifier qu'une assertion détecte une faute plausible, et pas seulement que la ligne de code est couverte.

### Préparation

```bash
git fetch origin
git switch test/critical-invariants-audit-clean
git pull --ff-only
git status --short
```

Le statut doit être propre avant de commencer. Sauvegarder le SHA initial :

```bash
git rev-parse HEAD
```

Exécuter une seule mutation à la fois. Après chaque mutation :
1. lancer le test ciblé ;
2. enregistrer le code de sortie et le nom du test/assertion qui échoue ;
3. restaurer le fichier (`git restore -- <fichier>`) ;
4. vérifier `git diff --exit-code` avant la mutation suivante.

Ne jamais committer une mutation volontaire.

### Matrice de mutations

| ID | Mutation contrôlée | Test ciblé initial | Signal attendu |
|---|---|---|---|
| MUT-01 | Dans `TransformerBlock.forward`, retirer l'ajout du résultat attention au flux résiduel ou celui du MLP, une seule branche à la fois | `tests/unit/test_transformer_block.py::test_block_forward_adds_both_sublayers_to_the_residual_stream` | Assertion exacte sur `x + 1.5` en échec |
| MUT-02 | Introduire un couplage entre éléments du batch dans le chemin GPT (par ex. ajouter une statistique calculée sur l'axe batch dans une copie temporaire de travail) | `tests/unit/test_gpt.py::test_batch_items_are_independent` | Les logits du premier exemple diffèrent entre calcul isolé et batch |
| MUT-03 | Neutraliser temporairement le masque causal dans l'attention multi-tête | `tests/unit/test_gpt.py::test_prefix_invariance_future_tokens_do_not_change_earlier_logits` et les tests causaux de `tests/unit/test_attention.py` | Une perturbation future modifie une sortie antérieure |
| MUT-04 | Retirer temporairement `eps` du dénominateur de LayerNorm ou le placer hors de la racine | Tests epsilon et variance nulle de `tests/unit/test_gpt_ops.py` | Référence numérique différente ou sortie non finie sur variance nulle |
| MUT-05 | Modifier temporairement la réduction de la loss (somme au lieu de moyenne, ou moyenne incorrecte des exemples) | `tests/unit/test_losses.py::test_cross_entropy_averages_large_finite_losses_without_sum_overflow` et tests de référence de loss | Valeur numérique différente ou overflow détecté |

Commandes ciblées après chaque mutation :

```bash
uv run pytest -q tests/unit/test_transformer_block.py
uv run pytest -q tests/unit/test_gpt.py
uv run pytest -q tests/unit/test_attention.py
uv run pytest -q tests/unit/test_gpt_ops.py
uv run pytest -q tests/unit/test_losses.py
```

**Attention à MUT-03 :** le test GPT prefix-invariance est un détecteur de bout en bout ; il faut aussi exécuter les tests directs d'attention pour localiser précisément la protection. Une mutation qui ne fait pas échouer le test ciblé doit être analysée : test insuffisant, mutation équivalente ou mauvaise localisation. Ne pas forcer une conclusion positive.

Pour chaque cas, consigner : diff exact de la mutation, SHA de départ, commande, exit code, nom et message de l'assertion, résultat détecté/non détecté, restauration confirmée.

## 5. Deuxième tâche — étendre l'inventaire critique

L'inspection statique initiale de cette session a confirmé l'existence des modules et tests ci-dessous. Cela ne constitue pas une revue exhaustive de leurs assertions.

| Domaine | Implémentation | Tests existants repérés | Questions d'audit à traiter |
|---|---|---|---|
| Exemples d'entraînement | `src/llm_lab/foundations/training_examples.py` | `tests/unit/test_training_examples.py` | Décalage exact input/target, formule du nombre de fenêtres, stride, dernière cible complète, absence de mutation, types et frontières |
| Filtres de décodage | `src/llm_lab/foundations/decoding_filters.py` | `tests/unit/test_decoding_filters.py` | top-k exact, top-p inclut le token de franchissement, égalités stables, normalisation, distribution dégénérée, valeurs de p/k invalides |
| Génération | `src/llm_lab/foundations/generate.py` | `tests/unit/test_generate.py` | argmax greedy, RNG obligatoire et reproductible, ordre température → top-k → top-p, fenêtre glissante, max_new_tokens nul, validation |
| Inspection embeddings | `src/llm_lab/foundations/embedding_inspection.py` | `tests/unit/test_embedding_inspection.py` | identité des token IDs, ordre/duplicats, cosinus, zéro-normes, stabilité des ties, copie/non-mutation |
| Chargement GPT-2 | `src/llm_lab/foundations/gpt2_weights.py` | `tests/unit/test_gpt2_weights.py` | split QKV, transpositions Conv1D, embeddings/head liés, clés manquantes/inattendues, atomicité (aucune mutation partielle), copie des tenseurs |

Pour chaque domaine :
1. lire le module complet et le fichier de tests complet ;
2. distinguer les contrats documentés des comportements accidentels ;
3. associer chaque invariant à au moins une assertion discriminante ;
4. repérer les cas déjà couverts pour éviter les doublons ;
5. ajouter un test seulement si le risque et le signal distinct sont démontrés.

Ne pas élargir automatiquement l'inventaire à toutes les fonctions utilitaires. Définir d'abord le périmètre pédagogique critique du KPI.

## 6. Troisième tâche — rendre ENG-02 mesurable

ENG-02 = Critical Invariant Coverage. Conserver le statut **not measured** tant que les éléments suivants ne sont pas validés.

- Périmètre explicite (modules/fonctionnalités inclus et exclus).
- Registre d'invariants sans doublons ; chaque ligne formule une propriété vérifiable, pas une fonctionnalité vague.
- Dénominateur approuvé par revue humaine.
- Numérateur limité aux invariants ayant un test et une assertion pertinente.
- Sensibilité vérifiée par mutation ou justification documentée équivalente.
- Traçabilité vers chemin de test, nom d'assertion, commit et date de revue.

Formule possible après approbation :

`ENG-02 = invariants critiques protégés / invariants critiques retenus × 100`

Ne pas mélanger couverture de lignes, nombre de tests, nombre de propriétés et couverture des invariants. Si le dénominateur est incomplet, ne pas publier de pourcentage.

## 7. Quatrième tâche — mesurer le coût CI

Point de mesure observé : 673 tests, 98.19 % de couverture, 79.48 s, deux workers, SHA `d4ea580`.

Le run antérieur à 661 tests et 57.14 s n'est pas un témoin contrôlé. L'écart brut ne permet pas d'attribuer un coût aux douze tests supplémentaires. Pour une comparaison utile :
- utiliser le même type de runner, la même version Python/dépendances et le même nombre de workers ;
- faire plusieurs runs par révision ;
- comparer médiane et dispersion ;
- distinguer temps total du job, temps pytest et temps de setup ;
- ne modifier la CI qu'en réponse à un coût mesuré.

Conserver les tests rapides dans la suite existante. Ne pas créer une deuxième invocation pytest.

## 8. Cinquième tâche — décision sur l'outillage mutation

Ne pas ajouter de framework de mutation tout de suite. Décision après MUT-01 à MUT-05 :
- si le pilote manuel révèle des trous utiles, évaluer un outil sur une liste blanche réduite ;
- mesurer runtime, mutations équivalentes, reproductibilité et lisibilité du rapport ;
- si adopté, commencer par un workflow manuel/planifié non bloquant ;
- n'introduire un seuil bloquant qu'après plusieurs exécutions stables et une revue du bruit.

## 9. Séquence de reprise condensée

1. Vérifier le SHA de la branche, la PR et les checks.
2. Exécuter MUT-01 à MUT-05 en local, restaurer chaque fichier, consigner les preuves.
3. Étendre l'audit aux cinq domaines du tableau §5, sans dupliquer les protections existantes.
4. Faire approuver le périmètre et le dénominateur ENG-02.
5. Calculer ENG-02 ou maintenir explicitement « not measured ».
6. Faire une mesure CI appariée avant toute optimisation.
7. Mettre à jour ce cahier et l'audit de tests, puis relancer CI/Quarto/secret scanning sur le nouveau SHA.
8. Faire relire la PR #1277 ; fusion manuelle uniquement après validation explicite.

## 10. Critères de clôture

- [ ] Les cinq mutations ont un résultat réel, reproductible et restauré.
- [ ] L'inventaire des cinq domaines du §5 est audité et les lacunes sont qualifiées.
- [ ] Le périmètre et le dénominateur ENG-02 sont approuvés.
- [ ] Chaque invariant compté est relié à une assertion probante.
- [ ] ENG-02 est calculé ou demeure « not measured » avec une raison explicite.
- [ ] Le coût CI est comparé sur des runs appariés.
- [ ] Les changements éventuels sont validés sur le SHA courant.
- [ ] La PR #1277 est revue et fusionnée explicitement, ou ses blocages sont consignés.

## 11. Documents liés

- [Audit de la suite de tests](test-suite-kpi-audit-2026-11-18.md)
- [KPIs du projet](../project-kpis.md)
- [PR #1277](https://github.com/JM-Brun/llm-lab/pull/1277)


## 12. Audit statique des cinq domaines complémentaires — 2026-11-18

Revue des cinq modules et de leurs fichiers de tests sur le HEAD
`bad9fc2b0e676d872158d569048d9cf8f0cac278`. Il s'agit d'une lecture du code
et des assertions, pas d'une exécution pytest ni d'une validation par mutation.

| Domaine | Protections déjà visibles | Lacunes / points à clarifier | Priorité |
|---|---|---|---|
| Exemples d'entraînement | Décalage input/target, formule du nombre de fenêtres, stride, chevauchement, dernière cible complète, déterminisme et non-mutation du flux | `context_length` et `stride` ne valident que `< 1` : les booléens passent et les flottants positifs peuvent provoquer un `TypeError` plus loin au lieu du `ValueError` annoncé. Ajouter des cas booléen/flottant/entier NumPy et vérifier les types au point d'entrée | Haute |
| Filtres de décodage | top-k exact et renormalisé, égalités stables, top-p inclut le token de franchissement, seuil exact, p=1, distributions invalides, non-mutation | `top_p_filter` accepte `True` comme `p=1.0` ; décider explicitement si booléen est invalide et tester. Le chemin top-k a déjà une validation stricte, y compris entiers NumPy | Moyenne |
| Génération | Chaîne greedy, reproductibilité RNG, ordre température → top-k → top-p, fenêtre de contexte, prompt invalide, zéro nouveau token, bornes top-k/top-p/température | Le test de fenêtre glissante vérifie surtout la forme et les bornes des tokens, pas les fenêtres réellement transmises au modèle après dépassement du contexte. Ajouter un faux modèle qui enregistre les entrées. Pas d'assertion explicite de non-mutation du prompt. `top_p=True` est accepté comme 1.0 | Haute |
| Inspection embeddings | Ordre et doublons des IDs, copie des lignes, similarités décroissantes, exclusion de soi, ties stables, candidats nuls exclus, requête nulle rejetée | `cosine_top_k` rejette `np.int64(k)` alors que le contrat dit entier positif et que d'autres API acceptent les entiers NumPy. Les normes calculées directement peuvent déborder sur des vecteurs finis de grande amplitude ; tester l'invariance d'échelle ou borner/documenter le domaine | Moyenne |
| Chargement GPT-2 | Copie/transposition des projections, split QKV, head lié en valeur, préfixe HF et buffers, clés manquantes/inattendues, formes, copie float64, absence d'assignation avant validation complète | Pas de rejet explicite des tenseurs non finis/non réels avant conversion float64. Les alias préfixés et non préfixés d'une même clé peuvent se remplacer silencieusement dans `_parameter_tensors`. Le test d'atomicité ne compare qu'un paramètre après erreur : vérifier l'état complet du modèle après un échec tardif | Haute |

### Conclusion de périmètre

- Les cinq domaines disposent d'une base de tests substantielle ; aucune raison
  de dupliquer les cas déjà présents.
- Les lacunes du tableau sont des candidats à tests ciblés, pas des défauts
  démontrés par exécution. Ne pas les compter comme violations détectées.
- Le périmètre proposé pour la revue ENG-02 comprend les cinq domaines déjà
  traités (`attention`, `losses`, `gpt_ops`, `TransformerBlock`, `GPT`)
  et ces cinq domaines complémentaires. L'inventaire doit rester limité aux
  invariants pédagogiques et fonctionnels explicitement documentés dans ces
  modules ; les fonctions auxiliaires non critiques et les détails de
  présentation sont exclus.
- Aucun dénominateur chiffré n'est approuvé dans cette session : les propriétés
  doivent d'abord être dédoublonnées, reliées à une assertion précise et
  soumises à validation humaine. ENG-02 reste **not measured**.

## 13. Comparaison des durées pytest sur le HEAD courant

Le run CI `44376545387` valide le HEAD `bad9fc2` : 673 tests réussis,
98.19 % de couverture de lignes, commande
`uv run pytest -n 2 --dist loadscope --durations=20`, Python 3.12.16,
pytest 9.2.0, deux workers. Le job pytest rapporte **81.58 s**.

Trois observations disponibles avec le même OS Linux, Python, pytest,
commande et nombre de workers :

| SHA | Run CI | Tests | Durée pytest |
|---|---:|---:|---:|
| `68f9bc205699a40a21a378bd6902dd4b0b7ca0f4` | `44365219499` | 673 | 79.48 s |
| `d4ea580bd403c5b60984e56ebc3fdb2a994b90d9` | `44375498268` | 673 | 73.57 s |
| `bad9fc2b0e676d872158d569048d9cf8f0cac278` | `44376545387` | 673 | 81.58 s |

Médiane : **79.48 s** ; étendue : **8.01 s**. Les trois observations sont
comparables sur les paramètres visibles, mais l'échantillon reste trop petit
pour conclure à une régression ou attribuer les écarts aux changements de code.
Les deux derniers SHA sont des mises à jour documentaires par rapport au code
de tests déjà validé. Ne pas modifier la CI sur cette seule base.

### État de validation au moment de cette revue

- CI sur `bad9fc2` : succès (qualité/domain checks et 673 tests).
- Secret scanning sur `bad9fc2` : succès.
- Quarto sur `bad9fc2` : encore en cours au dernier relevé ; résultat à
  confirmer avant de considérer le SHA entièrement validé.
- Les jobs opt-in d'inventaire complet des locateurs et de benchmark du registre
  restent ignorés ; aucun résultat ne leur est attribué.
- Aucune des cinq mutations manuelles n'a été exécutée dans un clone local.
- Aucune revue humaine n'est enregistrée sur la PR ; elle reste en brouillon.



## 14. Inventaire ENG-02 — périmètre approuvé et décompte candidat

Le mainteneur a approuvé le périmètre de dix domaines GPT. Un inventaire initial de **48 lignes regroupées** a été créé, puis sa granularité a été revue : ces lignes ne sont pas 48 invariants indépendants dans
[ENG-02 — inventaire des invariants critiques](eng-02-critical-invariants-inventory-2026-11-18.md).

Le nombre 48 est retiré comme proposition de dénominateur : plusieurs lignes agrègent des propriétés indépendantes. La décomposition et la séparation des contrats API des invariants fonctionnels restent à effectuer. Les statuts « protégé » sont des constats statiques de présence
d'assertions, non une preuve de sensibilité à une mutation. Les lignes partielles
restent au dénominateur proposé et sont exclues du numérateur strict.

L'inventaire documente notamment les lacunes candidates suivantes :
- validation de types pour `context_length` / `stride` ;
- rejet explicite de `top_p=True` ;
- vérification des fenêtres réellement transmises par `generate` ;
- stabilité de cosine sur amplitudes extrêmes et prise en charge éventuelle de
  `np.int64(k)` ;
- collisions de noms préfixés/non préfixés et atomicité complète du chargement
  GPT-2.

**ENG-02 reste not measured.** Les cinq mutations manuelles n'ont toujours pas
été exécutées. Prochaine étape : revue du tableau de 48 lignes, puis mutation
pilote dans un clone local et liaison de chaque résultat à l'ID concerné.


## 15. Revue de granularité ENG-02 — 2026-11-18

La revue méthodologique de la PR #1281 a validé la méthode générale, mais pas le dénominateur de 48. Les lignes ATT-02/03/04/05, LOSS-05, OPS-05, GPT-02, TRAIN-03, FILTER-04, GEN-05, EMB-05 et WEIGHT-06 doivent être décomposées selon les propriétés indépendantes et mutations discriminantes décrites dans l'inventaire §6.

**Décision de mesure :** ne pas utiliser 48 comme dénominateur, ne pas calculer de pourcentage, et conserver ENG-02 à **not measured**. La revue est statique ; elle n'a pas exécuté pytest ni les cinq mutations.

### État CI de la PR documentaire #1281

Le commit documentaire `e3504f9f2b2a46036ce7a102afbb3a51c812375f` a obtenu des résultats Actions complets :
- CI : succès (suite de tests et contrôles qualité/domaines) — run `44378806764`.
- Quarto : succès — run `44378806979`.
- Secret scanning : succès — run `44378806676`.

Dans le job CI, les deux jobs opt-in (inventaire complet des locateurs et benchmark de montée en charge) ont été ignorés. Ces résultats valident ce commit documentaire, pas les mutations manuelles ni la sensibilité des tests.

### Reprise

1. Recomposer les invariants atomiques en repartant des douze axes de décomposition de l'inventaire §6.
2. Vérifier les unités restantes afin d'éviter les agrégats cachés et les doublons.
3. Distinguer explicitement invariants fonctionnels/mathématiques et contrats d'API/effets de bord ; faire approuver leur inclusion et pondération.
4. Ajouter une colonne « mutation discriminante / raison de non-mutabilité ».
5. Geler une version du dénominateur seulement après revue ; exécuter ensuite les mutations et établir le numérateur strict.
