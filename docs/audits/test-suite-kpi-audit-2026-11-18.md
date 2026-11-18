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

Lecture historique de l'audit initial : 8 protégés et 3 partiels sur 11 candidats. Les lacunes ont depuis reçu des tests dans la branche PR #1275 (voir sections 10 et 11). Ce ratio historique ne doit pas être réutilisé comme valeur courante. **Aucun score ENG-02 n'est publié** : le périmètre critique complet n'a pas été approuvé et la sensibilité des assertions aux défauts n'a pas encore été vérifiée par mutations.

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

## 8. Limites de l'audit initial

- Les six fichiers initiaux ont été inspectés sur le commit de référence indiqué ; le dépôt n'a pas pu être cloné dans l'environnement de travail.
- À cette étape initiale, aucun test, lint, type-check, benchmark ou mutation n'avait été exécuté. Les résultats ultérieurs sont consignés séparément en sections 10 et 11.
- Les constats de comportement numérique initiaux étaient des risques déduits du code ; les tests de caractérisation ajoutés fixent maintenant plusieurs contrats, sous réserve de validation sur le dernier SHA.
- Le nombre de tests, le taux de couverture de lignes et le présent échantillon ne constituent pas le dénominateur ENG-02.

## 9. Fichiers audités

- [tests/unit/test_attention.py](../../tests/unit/test_attention.py) · [attention.py](../../src/llm_lab/foundations/attention.py)
- [tests/unit/test_losses.py](../../tests/unit/test_losses.py) · [losses.py](../../src/llm_lab/foundations/losses.py)
- [tests/unit/test_gpt_ops.py](../../tests/unit/test_gpt_ops.py) · [gpt_ops.py](../../src/llm_lab/foundations/gpt_ops.py)
- [Contrat KPI](../project-kpis.md) · [CI](../../.github/workflows/ci.yml)


## 10. Second review: TransformerBlock and assembled GPT

The next audit pass reviewed `tests/unit/test_transformer_block.py`,
`src/llm_lab/foundations/transformer_block.py`, `tests/unit/test_gpt.py`,
and `src/llm_lab/foundations/gpt.py` on `main`.

### Existing protections retained

- TransformerBlock: forward shape and finite outputs; 3D input contract; head-count divisibility; depth-scaled initialization applied only to the two residual-output projections.
- GPT: output shape and finite logits; invalid rank, dtype, empty inputs, context overflow and token range; same-seed reproducibility and different-seed divergence; prefix invariance; independently derived parameter-count formula.

### High-value additions in the PR branch

- TransformerBlock residual composition: replace the two sublayer functions with deterministic outputs and assert that both are added to the residual stream. This isolates the pre-LN residual wiring from the numerical behavior of attention and the MLP.
- GPT batch independence: assert that an input sequence produces identical logits alone and as one item in a batch. This detects accidental cross-example mixing.
- Loss batch-mean numerical boundary: two individually large but representable per-example losses must average to a finite value without overflowing an intermediate sum.

These additions are in the branch but have not yet been confirmed by a new CI run. They are candidate invariant protections, not a measured ENG-02 score.

### Remaining gaps worth considering later

- TransformerBlock: test that the MLP preserves the batch/sequence dimensions and returns the configured embedding width; current full-forward coverage provides indirect protection, so a separate test is justified only if it adds a distinct failure signal.
- GPT: test the position-embedding contribution or exact embedding-to-logit wiring only if a small deterministic test can isolate it without duplicating the end-to-end prefix and shape tests.
- Mutation pilot: deliberately break one residual addition, introduce cross-batch mixing, remove causal masking, and alter the loss reduction. Record the exact failing assertion for each mutation. Restore the source after each mutation and do not commit intentionally broken code.

### Updated validation status

The first run on the earlier implementation commit `c35b7b50985946c6175ab0f848b98d0793faf7b9` passed the complete pytest job in approximately 58 seconds, Quarto and secret scanning. Ruff formatting passed, but Ruff lint failed on one `SIM117` nested-context finding. That finding was corrected in `b180b2a`.

Subsequent commits add the corrected context-manager test, a batch-mean numerical boundary test, the TransformerBlock residual test and GPT batch-independence test. The GitHub Actions API did not report a new run for the latest commits at the time of this audit update. Therefore the initial pytest success does not validate these later additions, and lint/type-check on the corrected head remain unconfirmed.


## 11. CI follow-up and formatting correction

A workflow run was subsequently created for the expanded head
`737e93aec3be4a9577970bf801eca056e9f50224`:

- Full test job: passed.
- Quarto site: passed.
- Secret scanning: passed.
- Python quality job: failed at `ruff format --check .`, before lint and type checking.
- Exact finding: one extra blank line before
  `test_cross_entropy_averages_large_finite_losses_without_sum_overflow`
  in `tests/unit/test_losses.py`. No semantic or lint failure was reported in that run because those later checks were skipped.

The whitespace was corrected in commit `133fe837c54101219899c3e04d2756ea3d7e8f83`.
A new Actions run for that exact commit was not yet visible when this update was written.
Do not treat the correction as validated until formatting, lint, type checking and
the full workflow complete successfully.

The test job on the expanded head is independent evidence that the new tests
present at that SHA passed as part of the full suite. The formatting-only failure
does not invalidate that test result, but it does prevent declaring the PR green.


A subsequent source review found that the first whitespace-only follow-up (`133fe83`) had removed the wrong blank line: it left only one blank line between the large-loss test and the next test definition. The formatter finding therefore remained unresolved despite the commit message. This was corrected explicitly in `8eacc07a0584a114f050bc684a14b2efe1679de9` by restoring the required separation. The current PR head is later than the last observed workflow run; no CI validation for this exact correction is available yet. This correction supersedes the earlier claim that `133fe83` had resolved formatting.



## 12. Validation complète de la branche propre #1277

**État vérifié le 2026-11-18 — commit testé :** `68f9bc205699a40a21a378bd6902dd4b0b7ca0f4`.

Les workflows GitHub Actions associés à ce SHA sont terminés avec succès :

| Contrôle | Run / job | Résultat |
|---|---|---|
| Python quality and domain checks | CI run `44365219499`, job `135017010363` | **success** |
| Test suite | CI run `44365219499`, job `135017012033` | **success** |
| Quarto site & browser audit | run `44365219545`, job `135017011048` | **success** |
| Secret scanning | run `44365219836` | **success** |

Détail de la suite de tests :

- Commande : `uv run pytest -n 2 --dist loadscope --durations=20`.
- Environnement : Linux, Python 3.12.16, pytest 9.2.0, deux workers.
- Résultat : **673 passed in 79.48s**.
- Couverture : **98.19 %** (554 statements, 10 missed).
- Les modules `attention.py`, `losses.py`, `gpt.py`, `gpt_ops.py` et `transformer_block.py` affichent chacun 100 % de couverture de lignes dans ce rapport. Cela ne prouve pas à lui seul la couverture des invariants.
- Le seuil global existant de 90 % est atteint.

Détail qualité :

- `ruff format --check .` : success.
- Ruff lint : success.
- Type check : success.
- Les validations catalogue/extractions, graphe de métadonnées, ressources pédagogiques, registre de concepts bilingue, dataset historique et fragments associés passent également.

Détail Quarto :

- Rendu complet du site : success.
- Contrôles des contrôles de learning map, export du graphe de connaissances, parité de la timeline et liens locaux : success.
- Certains contrôles de navigateur et rendus incrémentaux ont été ignorés car le scope de cette PR ne les déclenchait pas ; le workflow Quarto global reste en succès.

Les deux jobs opt-in « full-corpus extraction locator inventory » et « concept-registry scale benchmark » ont été ignorés. Ils ne doivent pas être décrits comme exécutés.

### Interprétation de la durée

La suite actuelle dure 79.48 s sur deux workers. Le précédent point de comparaison mentionné dans ce rapport était 57.14 s pour 661 tests sur un autre SHA et un autre run. L'écart brut est de +22.34 s (+39.1 %) pour +12 tests ; il ne permet pas d'attribuer le surcoût aux seuls tests ajoutés, car l'environnement, le cache, la charge du runner et les autres tests peuvent varier. Conserver cette mesure comme observation, pas comme preuve de régression. Pour une comparaison causale, relancer les deux versions dans des conditions identiques ou comparer plusieurs runs appariés.

### Statut des conclusions

- Les ajouts de tests de cette branche sont validés par la suite complète et les contrôles qualité.
- La couverture de lignes à 98.19 % n'est **pas** une mesure ENG-02.
- Aucune mutation volontaire n'a encore été exécutée ; la sensibilité des assertions n'est donc pas établie.
- Le dénominateur ENG-02 n'est toujours pas approuvé : ne publier aucun score de couverture des invariants.
- Les workflows sont verts sur le SHA ci-dessus. Toute modification ultérieure de documentation crée un nouveau SHA et ne bénéficie pas automatiquement de cette preuve CI ; il faut distinguer le SHA validé du SHA documentaire courant.

## 13. Cahier de reprise — prochaines sessions

Ordre d'exécution recommandé :

1. **Mutation pilote manuelle (priorité immédiate).** Dans un clone local, exécuter une mutation à la fois sur une copie de travail, lancer uniquement le test ciblé, noter le test/assertion qui échoue, puis restaurer le fichier avant la mutation suivante. Cas minimaux :
   - retirer l'addition résiduelle attention dans `TransformerBlock` ;
   - introduire un mélange entre exemples du batch dans GPT ;
   - désactiver le masque causal dans l'attention ;
   - retirer ou déplacer l'epsilon de LayerNorm ;
   - modifier la réduction de cross-entropy / moyenne du batch.
   Résultat attendu : matrice mutation → test ciblé → détectée (oui/non) → diagnostic. Ne jamais committer une mutation volontaire.

2. **Étendre l'inventaire critique au périmètre GPT pédagogique.** Examiner `training_examples` (décalage entrée/cible, fenêtres, stride, séquences courtes), `generate` et `decoding_filters` (arrêt, déterminisme, top-k/top-p, validité des probabilités), puis `embedding_inspection` et `gpt2_weights` (bornes, dimensions, complétude et parité indépendante). Pour chaque invariant, noter le contrat, le test existant, l'assertion probante et les limites.

3. **Approuver le dénominateur ENG-02.** Établir une liste courte mais exhaustive sur le périmètre explicitement déclaré ; distinguer invariant critique, propriété secondaire et simple validation d'entrée. Exiger une revue humaine de chaque élément et une correspondance vers une assertion exécutable. Ne compter un invariant comme protégé que si le test détecte une violation plausible.

4. **Calculer ENG-02 seulement après revue.** Publier numérateur, dénominateur, périmètre, révision de l'inventaire, commit, chemins de tests et mutations associées. En cas d'incertitude ou d'inventaire incomplet, conserver le statut « not measured ».

5. **Mesurer le coût CI correctement.** Le point actuel est 673 tests, 98.19 %, 79.48 s, deux workers, sur le SHA validé ci-dessus. Ne pas conclure à une régression à partir du seul écart avec 661 tests / 57.14 s. Recueillir plusieurs mesures appariées avant d'ajuster le pipeline.

6. **Décider ensuite de l'outillage de mutation.** N'ajouter ni dépendance ni workflow tant que le pilote manuel ne montre pas un bénéfice concret. Si pertinent, tester un outil sur une liste blanche d'un ou deux modules, mesurer runtime et équivalences, puis envisager un workflow manuel/planifié non bloquant.

7. **Revalider la branche après toute modification.** Le SHA `68f9bc205699a40a21a378bd6902dd4b0b7ca0f4` est le dernier SHA avec preuve CI complète consignée ici. Vérifier le head actuel de la PR, relancer les workflows après changement de code ou de configuration, et ne pas confondre succès d'un ancien SHA avec validation du nouveau.

### Critères de clôture

- [ ] Matrice des mutations renseignée avec des résultats réellement observés.
- [ ] Inventaire critique complet du périmètre déclaré et revu.
- [ ] Chaque invariant compté lié à un test et à une assertion détectant une violation.
- [ ] Dénominateur ENG-02 approuvé et reproductible.
- [ ] Mesure ENG-02 calculée, ou statut « not measured » maintenu avec justification.
- [ ] Mesures CI comparables et interprétées sans attribution abusive.
- [ ] PR #1277 revue puis fusionnée explicitement ; aucun merge automatique implicite.
