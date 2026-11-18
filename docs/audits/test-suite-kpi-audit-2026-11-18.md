# Audit concret des tests — attention, losses et gpt_ops

**Date :** 2026-11-18  
**Commit audité :** `d11902853567b50f4ede8fa3b8816731a77987e8` (`main`)  
**Statut :** audit statique des six fichiers ; aucune exécution de tests, lint, typage ou benchmark n'est revendiquée.

## 1. Synthèse

| Domaine | État des protections existantes | Priorité |
|---|---|---|
| `attention` | Très bonne base : propriétés mathématiques, causalité, masques, stabilité numérique et validations | P2 : compléter quelques frontières, sans doublons |
| `losses` | Bonne base : référence, différences finies, invariants du gradient et validation | P1 : caractériser les logits finis extrêmes de signes opposés |
| `gpt_ops` | Bonne base sur les formules nominales, formes et reproductibilité | P1 : cas de variance nulle et rôle d'`eps` |

Le besoin est d'améliorer la protection des invariants, pas d'augmenter le nombre de tests. L'échantillon ne suffit pas à calculer ENG-02 : le dénominateur doit être revu et approuvé sur le périmètre critique complet.

## 2. Attention

### Déjà protégé

- **Masque causal :** forme, triangle inférieur et diagonale à zéro, futur à `-inf`, longueurs nulles/négatives rejetées.
- **Softmax :** normalisation, invariance par translation, limites de température haute/basse.
- **Stabilité numérique :** logits extrêmes, logits proches de grande amplitude, température non finie, scores débordants.
- **Masques :** entrées NaN/+inf rejetées, biais additif fini accepté, clés interdites à poids nul.
- **Ligne entièrement masquée :** sortie et poids nuls sans warning, convention explicitement testée.
- **Calcul d'attention :** référence calculable à la main, dimensions Q/K/V distinctes, sortie pondérée.
- **Causalité fonctionnelle :** modifier un token futur ne doit pas modifier les sorties antérieures.
- **Validation :** dimensions, séquences, formes, masques et entrées non finies.

### Gaps justifiés

1. Paramétrer le test de causalité sur plusieurs positions de coupure (actuellement le dernier token est perturbé et les trois sorties précédentes sont contrôlées).
2. Remplacer `np.random.seed` / `np.random.randn` par un `np.random.default_rng(seed)` local afin de ne pas modifier l'état aléatoire global.
3. Ajouter une frontière de type à `causal_mask` seulement si le contrat doit refuser explicitement flottants et booléens : le docstring annonce un entier, mais les tests ne couvrent que zéro et les valeurs négatives.
4. Confirmer le rejet d'une forme de masque broadcastable mais différente de `(T_q, T_k)`, puisque l'implémentation exige une correspondance exacte.

**À ne pas faire :** dupliquer les tests nominaux de softmax ou de causalité, déjà bien couverts.

## 3. Losses

### Déjà protégé

- Valeur de cross-entropy comparée à une référence analytique.
- Gradient comparé à des différences finies centrales sur un petit tableau.
- Invariance de la loss à un décalage constant par ligne.
- Somme des gradients nulle par ligne.
- Non-mutation des logits.
- Cas invalides paramétrés : rang/tailles vides, batch incohérent, indices hors plage, cible non entière, logits NaN/inf — pour loss et gradient.
- Stabilité pour des logits de grande amplitude commune.

### Gap prioritaire : extrêmes opposés

`losses.py` soustrait le maximum de chaque ligne, ce qui stabilise les cas usuels. Mais des logits tous finis et de signes opposés proches des limites float64 (ex. `[1e308, -1e308]`) peuvent faire déborder cette soustraction vers `-inf`. La validation accepte les entrées finies ; le calcul doit donc caractériser ce cas au lieu de laisser apparaître silencieusement un résultat non fini.

**Action :**
- Ajouter des tests de caractérisation pour `cross_entropy_from_logits` et `cross_entropy_gradient` sous `np.errstate(over="raise", invalid="raise")`.
- Décider du contrat : prise en charge robuste de toutes les entrées float64 finies, ou rejet explicite des cas hors domaine numérique par `ValueError`.
- Garder les différences finies sur un cas bien conditionné ; ne pas les utiliser pour valider les extrêmes.

Secondaire : tester le cas batch de taille 1 et classe unique (loss et gradient nuls) si ce cas est autorisé.

## 4. GPT ops

### Déjà protégé

- `linear` : produit matriciel manuel, diffusion du biais, forme de sortie sur entrée `(B,T,in)`.
- `layer_norm` : normalisation du dernier axe puis affine, moyenne nulle et variance proche de 1.
- `gelu` : zéro en zéro et comparaison à la définition exacte par erf.
- Initialisation : dimensions, biais nul, reproductibilité avec générateur seedé.
- Initialisation matricielle : moyenne et écart-type empiriques plausibles sur 60 000 tirages.

### Gaps justifiés

1. **Layer norm constante :** vérifier qu'une ligne de variance nulle reste finie avec `eps`, et donne zéro avant transformation affine.
2. **Epsilon configurable :** vérifier sur un petit vecteur que `eps` est ajouté à la variance avant la racine.
3. **Linear :** ajouter un exemple 2D ou 1D si cela clarifie le contrat annoncé `(..., in_features)`; le test actuel ne couvre que trois dimensions.
4. **Test statistique d'initialisation :** le conserver tant qu'il ne pèse pas dans la durée mesurée ; il est déterministe avec sa graine, mais n'est pas un benchmark.

Les fonctions n'annoncent pas de contrat de validation des formes/paramètres : ne pas traiter l'absence de tests d'erreur comme un défaut sans décider d'abord du contrat.

## 5. Cartographie ENG-02 — candidats de première revue

| ID provisoire | Invariant | Protection actuelle | État |
|---|---|---|---|
| ATT-01 | Masquage causal et absence d'influence du futur | Structure + perturbation | Protégé |
| ATT-02 | Normalisation softmax et invariance par translation | Propriétés + références | Protégé |
| ATT-03 | Stabilité softmax, scores et masques | Cas extrêmes et entrées invalides | Protégé |
| ATT-04 | Calcul d'attention et pondération des valeurs | Référence à la main | Protégé |
| LOSS-01 | Cross-entropy stable et conforme | Valeur connue + décalage commun | Partiel : extrêmes opposés |
| LOSS-02 | Gradient correct | Différences finies + somme nulle | Protégé sur cas bien conditionné |
| LOSS-03 | Validation des logits/cibles | Cas paramétrés sur les deux API | Protégé |
| GPTOPS-01 | Projection linéaire et biais | Produit matriciel manuel | Protégé |
| GPTOPS-02 | Layer norm, axe, affine et epsilon | Référence + variance | Partiel : variance nulle / epsilon |
| GPTOPS-03 | GELU conforme à l'approximation | Référence erf | Protégé |
| GPTOPS-04 | Initialisation reproductible | Seed, formes, biais nul | Protégé |

Lecture de travail : 8 protégés et 3 partiels sur 11 candidats. **Ce ratio 8/11 n'est pas une mesure ENG-02 publiable** : l'inventaire est partiel et la sensibilité des assertions aux défauts n'a pas été vérifiée. Un test ne compte que si son assertion peut effectivement détecter la violation.

## 6. Actions et ordre recommandé

### P1 — lacunes à forte valeur
- [ ] Ajouter les tests de caractérisation des logits extrêmes opposés dans `test_losses.py`.
- [ ] Décider/documenter le comportement attendu aux limites float64.
- [ ] Ajouter le cas de layer norm à variance nulle dans `test_gpt_ops.py`.
- [ ] Ajouter un test du rôle de l'`eps` configurable.

### P2 — renforcement ciblé
- [ ] Paramétrer la perturbation causale sur plusieurs positions.
- [ ] Remplacer l'aléatoire global dans `test_attention.py` par des générateurs locaux.
- [ ] Trancher le contrat de type de `causal_mask`.
- [ ] Ajouter un cas d'entrée 2D à `linear` si utile à la clarté du contrat.

### P3 — sensibilité des assertions
- [ ] Effectuer des mutations locales : inverser le masque, retirer `sqrt(d_k)`, changer l'axe softmax, supprimer `eps`, retirer la soustraction de la cible au gradient.
- [ ] Vérifier que le test associé échoue pour chaque mutation.
- [ ] Évaluer un outil de mutation uniquement après ce pilote manuel ; aucun framework ni job CI n'est justifié à ce stade.

### Validation d'intégration
- [ ] Exécuter les trois modules isolément, puis la suite pytest complète.
- [ ] Relever les durées avant/après sur le même runner et commit.
- [ ] Vérifier Ruff et mypy selon la CI existante.
- [ ] Faire approuver le dénominateur ENG-02 ; lier chaque invariant retenu à son assertion.
- [ ] Mettre à jour `docs/project-kpis.md` avec le mapping validé et une première valeur mesurée.

## 7. CI : décision

La CI actuelle exécute déjà la suite pytest complète avec deux workers (`pytest -n 2 --dist loadscope --durations=20`). Les nouveaux tests déterministes et minuscules doivent rejoindre les modules existants : **pas de seconde invocation pytest, pas de job dédié**. Les mutations restent manuelles/advisory au début ; un job planifié ou manuel ne sera envisagé qu'après mesure du coût et du bruit.

## 8. Limites de cet audit

- Les six fichiers ont été inspectés sur le commit indiqué ; le dépôt n'a pas pu être cloné dans l'environnement de travail.
- Aucun test, lint, type-check, benchmark ou mutation n'a été exécuté dans cette session.
- Les constats de comportement numérique sont des risques déduits du code ; les tests de caractérisation doivent confirmer le résultat et fixer le contrat.
- Le nombre de tests, le taux de couverture de lignes et le présent échantillon ne constituent pas le dénominateur ENG-02.

## 9. Fichiers audités

- [tests/unit/test_attention.py](../../tests/unit/test_attention.py) · [attention.py](../../src/llm_lab/foundations/attention.py)
- [tests/unit/test_losses.py](../../tests/unit/test_losses.py) · [losses.py](../../src/llm_lab/foundations/losses.py)
- [tests/unit/test_gpt_ops.py](../../tests/unit/test_gpt_ops.py) · [gpt_ops.py](../../src/llm_lab/foundations/gpt_ops.py)
- [Contrat KPI](../project-kpis.md) · [CI](../../.github/workflows/ci.yml)
