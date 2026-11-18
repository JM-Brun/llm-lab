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
