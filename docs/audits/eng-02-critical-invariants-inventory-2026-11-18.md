# ENG-02 — Inventaire des invariants critiques GPT

**Version :** 0.2 — 2026-11-18  
**Référence inspectée :** `71f87f8d633e1a7a4fdcf1ac82b29bda181b307d`  
**Statut :** périmètre de dix domaines approuvé ; inventaire candidat ; dénominateur non approuvé ; ENG-02 = **not measured**.

## 1. Objet et règle de comptage

L'inventaire transforme le périmètre approuvé en propriétés comportementales distinctes, chacune reliée à une preuve de test. Il ne compte ni fonctions, ni cas paramétrés, ni lignes couvertes, ni méthodes de test.

Une propriété est comptée une seule fois, même si plusieurs tests l'étayent. Deux propriétés sont séparées lorsqu'une mutation plausible peut en casser une sans casser l'autre. Les validations homogènes sont regroupées ; elles ne sont pas comptées une fois par valeur invalide.

Le tableau contient **48 lignes de regroupement initiales**, et non 48 invariants indépendants démontrés. La revue de granularité a identifié plusieurs lignes qui agrègent des propriétés séparables par mutation. Le nombre 48 est donc retiré comme proposition de dénominateur ; il ne doit pas être utilisé pour calculer ENG-02. Les lignes « partiel » ne peuvent pas être comptées au numérateur strict.

## 2. Inventaire initial — 48 lignes regroupées (version à décomposer)

Les statuts sont issus d'une lecture statique des sources et tests. « Protégé » signifie qu'une assertion pertinente a été repérée ; cela ne prouve pas sa sensibilité à une mutation.

| ID | Domaine | Invariant comportemental | Tests/assertions repérés | État statique |
|---|---|---|---|---|
| ATT-01 | Attention | Masque causal et absence d'influence du futur | test_causal_mask_structure; test_scaled_dot_product_attention_causal_invariance | Protégé |
| ATT-02 | Attention | Softmax normalisé sur l'axe demandé et invariant à une translation constante | test_softmax_with_temperature_properties; test_wrong_softmax_axis_fails_per_query_normalization_invariant | Protégé |
| ATT-03 | Attention | Température : concentration basse/haute et validation | test_softmax_with_temperature_properties; test_softmax_rejects_nonfinite_temperature | Protégé |
| ATT-04 | Attention | Stabilité des extrêmes et rejet des logits, scores et masques invalides | tests extreme, overflowed_scores, invalid_mask_entries, fully_masked_attention_row | Protégé |
| ATT-05 | Attention | Scores mis à l'échelle, clés autorisées, somme pondérée et formes | test_scaled_dot_product_attention_matches_hand_computable_weighted_sum; test_attention_weights_normalize_only_over_allowed_keys; test_scaled_dot_product_attention_shapes_and_invariants | Protégé |
| LOSS-01 | Losses | Valeur analytique de la cross-entropy depuis logits bruts | test_cross_entropy_matches_known_value | Protégé |
| LOSS-02 | Losses | Gradient correct par différences finies et somme nulle par ligne | test_gradient_matches_central_finite_differences; test_gradient_rows_sum_to_zero | Protégé |
| LOSS-03 | Losses | Réduction batch par moyenne sans débordement intermédiaire | test_cross_entropy_averages_large_finite_losses_without_sum_overflow | Protégé |
| LOSS-04 | Losses | Invariance aux translations par ligne et comportement des extrêmes float64 | tests rowwise_constant_shift, extreme_opposite_sign, unrepresentable_extreme | Protégé |
| LOSS-05 | Losses | Validation des logits/cibles et non-mutation des entrées | tests invalid_inputs (loss/gradient); test_loss_and_gradient_do_not_mutate_logits | Protégé |
| OPS-01 | GPT ops | Projection linéaire : poids transposé, biais et dimensions de tête arbitraires | test_linear_matches_manual_matmul_and_broadcasts_bias; test_linear_supports_arbitrary_leading_dimensions | Protégé |
| OPS-02 | GPT ops | LayerNorm normalise le dernier axe puis applique gamma/beta | test_layer_norm_normalizes_then_rescales_last_axis; test_layer_norm_with_identity_affine_yields_roughly_unit_variance | Protégé |
| OPS-03 | GPT ops | Epsilon ajouté à la variance avant racine ; variance nulle finie | test_layer_norm_constant_rows_remain_finite_and_normalize_to_zero; test_layer_norm_epsilon_is_added_to_variance_before_sqrt | Protégé |
| OPS-04 | GPT ops | GELU conforme à l'approximation de référence et nulle en zéro | test_gelu_is_zero_at_zero_and_close_to_exact_erf_definition | Protégé |
| OPS-05 | GPT ops | Initialisation : formes, biais nul, RNG reproductible et échelle statistique | tests init_linear, seeded_rng, init_matrix | Protégé |
| BLOCK-01 | TransformerBlock | Forward préserve forme batch/séquence/embedding et reste fini | test_block_forward_preserves_shape_and_stays_finite; validation 3D et têtes | Partiel |
| BLOCK-02 | TransformerBlock | Chaque sous-couche est ajoutée une fois au flux résiduel | test_block_forward_adds_both_sublayers_to_the_residual_stream | Protégé |
| BLOCK-03 | TransformerBlock | Initialisation GPT-2 mise à l'échelle uniquement sur projections de sortie résiduelle | test_gpt2_scaled_initialization_applies_only_to_residual_output_projections | Protégé |
| GPT-01 | GPT | Forme des logits (batch, séquence, vocabulaire) et valeurs finies | test_forward_returns_expected_logit_shape | Protégé |
| GPT-02 | GPT | Validation rang/type, dimensions vides, contexte et bornes token | test_forward_validation_errors | Protégé |
| GPT-03 | GPT | Les logits du préfixe sont indépendants des tokens futurs | test_prefix_invariance_future_tokens_do_not_change_earlier_logits | Protégé |
| GPT-04 | GPT | Indépendance des exemples au sein d'un batch | test_batch_items_are_independent | Protégé |
| GPT-05 | GPT | Initialisation reproductible à graine identique | test_same_seed_reproduces_identical_logits | Protégé |
| GPT-06 | GPT | Nombre de paramètres conforme à une formule indépendante | test_num_parameters_matches_configuration_formula | Protégé |
| TRAIN-01 | Training examples | Chaque cible est le token suivant l'entrée, pas une copie | test_every_target_is_the_next_token_in_the_stream; test_targets_are_shifted_not_copied | Protégé |
| TRAIN-02 | Training examples | Nombre et chevauchement des fenêtres conformes à context/stride | tests window_count, stride_equal_to_context_length, smaller_stride, worked_example | Protégé |
| TRAIN-03 | Training examples | Séquences courtes et paramètres/formes/types invalides rejetés | test_invalid_inputs_raise_value_error | Assertion repérée (revérifiée statiquement) |
| TRAIN-04 | Training examples | Construction déterministe sans mutation du flux source | test_output_is_deterministic_and_stream_is_not_mutated | Protégé |
| FILTER-01 | Decoding filters | Top-k garde exactement k candidats et renormalise | test_top_k_keeps_exactly_k_renormalized_candidates; identity when k >= vocab | Protégé |
| FILTER-02 | Decoding filters | Top-p garde le plus petit noyau atteignant le seuil, token de franchissement inclus | test_top_p_includes_the_token_that_crosses_the_threshold; test_top_p_nucleus_size_adapts_to_distribution_shape | Protégé |
| FILTER-03 | Decoding filters | Égalités départagées de façon déterministe par indice | test_top_k_breaks_ties_by_lowest_index_deterministically; test_top_p_breaks_ties_by_lowest_index | Protégé |
| FILTER-04 | Decoding filters | Seuils/distributions invalides rejetés et entrée non mutée | tests invalid_distributions, top_k_invalid_k, top_p_invalid_p, filters_do_not_mutate_the_input | Assertion repérée (revérifiée statiquement) |
| GEN-01 | Generation | Greedy choisit l'argmax du dernier pas et construit la chaîne autoregressive | test_generate_greedy_is_deterministic_and_matches_manual_argmax_chain | Protégé |
| GEN-02 | Generation | Échantillonnage reproductible avec RNG seedé | test_generate_sampled_tokens_are_reproducible_with_seeded_rng | Protégé |
| GEN-03 | Generation | Chaque pas transmet au modèle uniquement la dernière fenêtre de contexte | test_generate_slides_the_context_window | Partiel : sortie vérifiée, pas les fenêtres réellement transmises |
| GEN-04 | Generation | Ordre température → top-k → top-p et effets de troncature | tests temperature_before_filtering, sampling_with_truncation, top_k_one, tight_top_p | Protégé |
| GEN-05 | Generation | Paramètres invalides rejetés même en greedy ; zéro token préserve le prompt | tests validation_errors, rejects_non_integer_token_counts, without_new_tokens, rejects_nonfinite_temperature | Protégé |
| EMB-01 | Embedding inspection | Lookup préserve ordre/doublons des IDs et renvoie une copie | test_lookup_preserves_id_order_and_duplicates | Protégé |
| EMB-02 | Embedding inspection | Matrice/IDs invalides (forme, type, non-finis, bornes) rejetés | test_lookup_rejects_invalid_matrix_or_ids | Protégé |
| EMB-03 | Embedding inspection | Top-k cosine renvoie IDs et scores en ordre décroissant | test_cosine_top_k_returns_ids_and_descending_scores | Protégé |
| EMB-04 | Embedding inspection | Égalités stables par ID et exclusion de soi contrôlée | tests excludes_self_and_breaks_ties_by_id; can_include_self_explicitly | Protégé |
| EMB-05 | Embedding inspection | Requête cosine définie et candidats de norme nulle exclus | tests rejects_undefined_or_invalid_requests; excludes_zero_norm_candidates; cosine_top_k_is_stable_for_very_large_and_small_finite_rows; cosine_top_k_accepts_numpy_integer_k | Assertion repérée (revérifiée statiquement) |
| WEIGHT-01 | GPT-2 weights | Embeddings de tokens et tête de sortie liées selon le contrat | test_copies_embeddings_and_ties_output_head_to_token_table | Protégé |
| WEIGHT-02 | GPT-2 weights | QKV fusionné découpé Q/K/V et transposé correctement | test_splits_fused_qkv_and_transposes_conv1d_weights | Protégé |
| WEIGHT-03 | GPT-2 weights | Projections attention/MLP mappées selon conventions et formes | test_splits_fused_qkv_and_transposes_conv1d_weights; test_gpt2_small_config_matches_published_dimensions | Protégé |
| WEIGHT-04 | GPT-2 weights | Préfixes HF et buffers de masque gérés sans collision silencieuse | test_accepts_transformer_prefix_tied_head_and_mask_buffers; test_rejects_prefixed_and_unprefixed_parameter_collision | Assertion repérée (revérifiée statiquement) |
| WEIGHT-05 | GPT-2 weights | Tête non liée, clés manquantes/inattendues et formes incorrectes rejetées | tests rejects_untied_output_head, rejects_missing_parameter, rejects_unexpected_parameter, rejects_shape_that_does_not_match_config | Protégé |
| WEIGHT-06 | GPT-2 weights | Copies float64 indépendantes et validation complète avant assignation | tests loaded_parameters_are_independent_float64_copies; rejects_missing_parameter_without_modifying_model; rejects_nonreal_nonfinite_or_unrepresentable_tensor | Assertion repérée (revérifiée statiquement) |

## 3. Limites de la preuve statique

- Un test présent ne prouve pas qu'une mutation plausible serait détectée.
- Une assertion peut être indirecte ou ne pas distinguer des comportements voisins.
- Les tests d'intégration/parité GPT-2 constituent une preuve distincte ; ne pas présumer qu'ils ont été exécutés parce que les tests unitaires passent.
- Les états partiels/lacunes doivent être explicitement conservés, pas masqués par la couverture de lignes.

## 4. Règle de calcul proposée

Après approbation humaine :
- **Dénominateur** : nombre d'invariants retenus dans la version approuvée.
- **Numérateur strict** : invariants reliés à une assertion exécutable dont la sensibilité est démontrée par mutation ciblée ou preuve indépendante équivalente.
- Une propriété partiellement testée n'est pas comptée au numérateur.
- Une mutation non pertinente ou impossible doit être justifiée, pas utilisée pour gonfler ou réduire artificiellement le score.

Formule proposée :

`ENG-02 = invariants avec preuve de test sensible / invariants approuvés`

Cette mesure est plus exigeante que la simple présence d'un test. Elle ne confond pas couverture de lignes, présence d'un test et résistance aux défauts.

## 5. Décisions attendues pour approbation

1. Valider les 48 lignes comme unités distinctes, ou demander des regroupements/séparations motivés.
2. Confirmer que validations d'entrée, non-mutation, reproductibilité et compatibilité des checkpoints appartiennent au périmètre critique pédagogique.
3. Confirmer que les invariants partiels restent au dénominateur et sont exclus du numérateur strict.
4. Confirmer une pondération uniforme, ou décider si les invariants de contrat API doivent peser différemment des invariants mathématiques centraux. La proposition actuelle ne pondère pas.
5. Faire la campagne de mutations manuelles prévue, puis étendre uniquement aux invariants où une mutation plausible et discriminante existe.

**Décision conservée :** les dix domaines sont approuvés par le mainteneur. Le nombre de 48 est proposé, pas approuvé. ENG-02 reste **not measured** jusqu'à approbation de l'inventaire et preuves de sensibilité suffisantes.


## 6. Revue de granularité — 2026-11-18

La revue méthodologique du 18 novembre conclut que la méthode générale est pertinente, mais que les **48 lignes ne constituent pas encore des unités de comptage suffisamment indépendantes**. Le dénominateur de 48 est retiré. Il ne faut ni le figer ni chercher à préserver ce nombre.

### Décompositions requises

| Ligne initiale | Propriétés à distinguer | Motif |
|---|---|---|
| ATT-02 | Normalisation/axe du softmax ; invariance par translation des logits | Deux propriétés mathématiques distinctes |
| ATT-03 | Effet de la température sur la concentration ; validation du paramètre température | Comportement numérique et contrat d'entrée indépendants |
| ATT-04 | Stabilité numérique des extrêmes ; validation des logits/scores/masques et lignes entièrement masquées | Stabilité et rejet d'entrées sont des contrats distincts |
| ATT-05 | Formule et mise à l'échelle des scores ; respect du masque ; somme pondérée ; contrat de formes | Comportements pouvant être rompus séparément |
| LOSS-05 | Validation logits/cibles ; absence de mutation des entrées | Contrat d'entrée et effet de bord indépendants |
| OPS-05 | Formes/biais de l'initialisation ; reproductibilité RNG ; échelle/distribution statistique | Contrats indépendants |
| GPT-02 | Rang/type ; dimensions vides ; longueur de contexte ; bornes des token IDs | Classes de validation à séparer si les mutations sont indépendantes |
| TRAIN-03 | Séquences trop courtes ; type/valeur de context_length ; type/valeur de stride | Préconditions et frontières de type distinctes |
| FILTER-04 | Validation top-k ; validation top-p ; validation des distributions ; non-mutation | Contrats non interchangeables |
| GEN-05 | Validation du nombre de tokens ; validation des paramètres de sampling ; validation même en greedy ; max_new_tokens=0 | Chemins de validation et comportement fonctionnel distincts |
| EMB-05 | Définition du cosinus ; exclusion des normes nulles ; stabilité aux amplitudes extrêmes ; type de k | Propriétés mathématiques, numériques et API distinctes |
| WEIGHT-06 | Copie indépendante des tenseurs ; validation avant assignation ; atomicité de l'état du modèle | Une copie correcte ne prouve pas l'atomicité transactionnelle |

Cette liste fixe les **axes de décomposition**, pas un nouveau décompte final. Certaines lignes initiales non citées peuvent encore nécessiter une séparation après inspection de l'implémentation et des assertions. À l'inverse, deux assertions qui vérifient la même propriété ne doivent pas créer deux unités.

### Règle de révision du dénominateur

Pour chaque unité révisée, documenter :
1. l'énoncé atomique de la propriété ;
2. la frontière du contrat et les exclusions ;
3. une mutation plausible qui la viole sans nécessairement violer les unités voisines, ou une justification explicite de non-mutabilité ;
4. le chemin du code, le test et l'assertion discriminante ;
5. l'état de preuve (non audité, assertion repérée, sensibilité démontrée).

Séparer aussi les **invariants fonctionnels/mathématiques** des **contrats d'API et effets de bord** dans le tableau, puis demander une décision explicite sur leur inclusion et leur poids. La pondération uniforme reste une hypothèse, pas une décision.

### Décision

- Périmètre de dix domaines : approuvé antérieurement.
- Inventaire de 48 lignes : index de départ utile, mais **non approuvé et retiré comme dénominateur**.
- Nouveau dénominateur : non établi ; ne pas publier de pourcentage.
- ENG-02 : **not measured**.
- Mutations manuelles : toujours non exécutées ; la revue statique ne les remplace.


## 7. Pilote de mutations — protocole discriminant (préparation)

Les cinq mutations ci-dessous sont définies comme un premier pilote ciblé. Cette section documente les mutations attendues et leurs tests sentinelles ; **elle ne prétend pas qu'elles ont été exécutées**. Le résultat de chacune doit être renseigné uniquement après exécution sur un environnement de test, puis restauration vérifiée du code.

| Mutation | Défaut injecté (un seul changement) | Test sentinelle principal | Signal attendu | État |
|---|---|---|---|---|
| MUT-01 — addition résiduelle | Supprimer l'addition de l'attention ou du MLP au flux résiduel dans `TransformerBlock.forward` | `test_block_forward_adds_both_sublayers_to_the_residual_stream` | Échec de l'égalité exacte avec `x + 1.5` lorsque les deux sous-couches sont remplacées par des constantes | À exécuter |
| MUT-02 — indépendance du batch | Introduire une dépendance entre exemples (par exemple une réduction/normalisation accidentelle sur l'axe batch) | `test_batch_items_are_independent` | Les logits du premier exemple évalué seul diffèrent de ceux du même exemple dans un batch plus grand | À exécuter |
| MUT-03 — masque causal | Inverser la polarité du triangle causal ou laisser accessibles des clés futures | `test_causal_mask_structure` et `test_scaled_dot_product_attention_causal_invariance` | La structure du masque ou l'invariance des sorties antérieures est violée | À exécuter |
| MUT-04 — epsilon LayerNorm | Calculer `sqrt(variance) + eps` au lieu de `sqrt(variance + eps)` | `test_layer_norm_epsilon_is_added_to_variance_before_sqrt` | La valeur de sortie ne correspond plus à la référence analytique avec `eps=0.25` | À exécuter |
| MUT-05 — réduction cross-entropy | Remplacer la moyenne sur le batch par une somme (ou sommer avant de diviser de façon à provoquer un débordement intermédiaire) | `test_cross_entropy_averages_large_finite_losses_without_sum_overflow` | La valeur n'est plus la moyenne attendue, ou le calcul déclenche un débordement/rejet | À exécuter |

### Enregistrement obligatoire par mutation

Pour chaque exécution, consigner : SHA propre de départ ; patch exact ; commande pytest ciblée ; code de sortie ; test/assertion qui échoue ; vérification qu'aucun test sans rapport n'explique l'échec ; restauration ; puis `git diff --exit-code` et vérification du SHA propre. Une mutation survivante doit être analysée : soit l'assertion est insuffisante, soit la mutation ne représente pas un défaut observable dans le contrat. Ne jamais committer une mutation volontaire sur une branche de travail.

### Limites d'interprétation

- Un test sentinelle nommé ici est un candidat justifié par lecture statique, pas encore une preuve de sensibilité.
- MUT-03 doit être évaluée à la fois au niveau du masque et au niveau de l'attention ; un seul résultat ne prouve pas automatiquement les deux propriétés.
- MUT-05 cible spécifiquement la réduction batch. La vérification par différences finies peut rester cohérente si loss et gradient subissent la même erreur d'échelle ; elle ne remplace donc pas le test de moyenne.
- Les cinq résultats ne suffisent pas à approuver le dénominateur global : ils valident seulement cinq correspondances ciblées dans l'inventaire.


## 8. Première correspondance atomique — lot pilote

Cette table précise les unités candidates derrière le pilote. Les identifiants sont des repères de travail, **pas un dénominateur approuvé**. Les unités voisines restent séparées lorsqu'une mutation peut violer l'une sans violer l'autre.

| ID candidat | Propriété atomique | Implémentation | Assertion sentinelle | Mutation discriminante |
|---|---|---|---|---|
| BLOCK-02a | La sortie de la sous-couche attention est ajoutée au flux résiduel | `src/llm_lab/foundations/transformer_block.py::TransformerBlock.forward` | `tests/unit/test_transformer_block.py::test_block_forward_adds_both_sublayers_to_the_residual_stream` | Omettre uniquement `x + attention_output` |
| BLOCK-02b | La sortie de la sous-couche MLP est ajoutée au flux résiduel après l'attention | `src/llm_lab/foundations/transformer_block.py::TransformerBlock.forward` | Même test sentinelle ; la constante MLP vaut `-0.5` | Omettre uniquement l'addition de la sortie MLP |
| GPT-04 | Un exemple du batch ne dépend pas des autres exemples | `src/llm_lab/foundations/gpt.py::GPT.forward` | `tests/unit/test_gpt.py::test_batch_items_are_independent` | Introduire une opération qui mélange les éléments du batch |
| ATT-01a | Le masque causal représente les positions futures comme interdites | `src/llm_lab/foundations/attention.py::causal_mask` | `tests/unit/test_attention.py::test_causal_mask_structure` | Inverser le triangle autorisé/interdit |
| ATT-01b | Les sorties antérieures de l'attention ne dépendent pas des clés/valeurs futures | `src/llm_lab/foundations/attention.py::scaled_dot_product_attention` | `tests/unit/test_attention.py::test_scaled_dot_product_attention_causal_invariance` | Ignorer le masque causal dans le calcul des poids |
| OPS-03a | L'epsilon est ajouté à la variance avant la racine carrée | `src/llm_lab/foundations/gpt_ops.py::layer_norm` | `tests/unit/test_gpt_ops.py::test_layer_norm_epsilon_is_added_to_variance_before_sqrt` | Déplacer l'addition de l'epsilon après la racine |
| LOSS-03a | La cross-entropy est réduite par moyenne sur le batch, et non par somme | `src/llm_lab/foundations/losses.py::cross_entropy_from_logits` | `tests/unit/test_losses.py::test_cross_entropy_averages_large_finite_losses_without_sum_overflow` | Remplacer la moyenne par une somme |
| LOSS-03b | La réduction de pertes finies proches de la limite float64 évite un débordement intermédiaire | `src/llm_lab/foundations/losses.py::cross_entropy_from_logits` | Même test sentinelle | Sommer les pertes avant division, de façon à provoquer un overflow intermédiaire |

Commandes ciblées prévues, à exécuter séparément pour chaque mutation :

- `pytest -q tests/unit/test_transformer_block.py::test_block_forward_adds_both_sublayers_to_the_residual_stream`
- `pytest -q tests/unit/test_gpt.py::test_batch_items_are_independent`
- `pytest -q tests/unit/test_attention.py::test_causal_mask_structure tests/unit/test_attention.py::test_scaled_dot_product_attention_causal_invariance`
- `pytest -q tests/unit/test_gpt_ops.py::test_layer_norm_epsilon_is_added_to_variance_before_sqrt`
- `pytest -q tests/unit/test_losses.py::test_cross_entropy_averages_large_finite_losses_without_sum_overflow`

La même assertion peut étayer plusieurs unités candidates si elle détecte séparément chacune des mutations définies. La preuve doit toutefois être consignée mutation par mutation ; une exécution réussie du test sur le code non muté n'établit pas sa sensibilité.


## 9. Recontrôle statique ciblé — 2026-11-18

Une relecture directe des implémentations et tests sur `main` (référence `cb7e3c859591b954188bb435a7b888ae2949875f`) corrige trois constats devenus obsolètes dans l'inventaire initial. Il s'agit d'une inspection du code et des assertions, **pas d'une exécution de pytest ni d'une preuve de sensibilité aux mutations**.

| Invariant | Vérification de l'implémentation | Vérification des tests | Correction de l'état statique |
|---|---|---|---|
| TRAIN-03 | `sliding_input_target_pairs` rejette explicitement booléens, flottants et valeurs inférieures à 1 pour `context_length` et `stride`; valide aussi dimension/type du flux et longueur minimale | `test_invalid_inputs_raise_value_error` paramètre notamment `True`, `False`, flottants Python et NumPy, valeurs nulles/négatives, flux multidimensionnel, flux flottant et séquence trop courte | L'ancienne lacune « booléens/flottants positifs non testés » est obsolète ; assertion repérée |
| FILTER-04 | `top_k_filter` rejette booléens et types/valeurs invalides de `k`; `top_p_filter` rejette booléens, valeurs non finies et seuils hors de (0, 1]; le validateur commun rejette distributions invalides | Tests dédiés top-k/top-p, distributions invalides et non-mutation ; `True`, `False` et `np.bool_(True)` sont explicitement paramétrés comme seuils top-p invalides | L'ancienne lacune « p=True accepté » est obsolète ; assertion repérée |
| EMB-05 | `cosine_top_k` met à l'échelle chaque ligne avant le calcul de norme, exclut les lignes nulles et accepte les entiers NumPy pour `k` | Tests pour amplitudes `1e308` et `1e-300`, candidats de norme nulle, requête nulle, égalités et `np.int64(k)` | Les deux lacunes signalées sont couvertes statiquement ; assertion repérée |

### Conséquence pour ENG-02

- Ces trois lignes ne doivent plus être décrites comme présentant les lacunes précises indiquées dans la première version de l'inventaire.
- Leur état peut passer de « partiel » à « assertion repérée » au sens de la taxonomie statique du document.
- Elles ne passent **pas** au statut « sensibilité démontrée » : aucune mutation discriminante de ces propriétés n'a été exécutée.
- Les autres lacunes mentionnées dans les sections précédentes restent à vérifier une par une ; cette revue ciblée ne vaut pas audit exhaustif des dix domaines.
- ENG-02 demeure **not measured** et aucun dénominateur n'est proposé par cette mise à jour.


## 10. Recontrôle statique ciblé — chargement GPT-2 et génération (2026-11-18)

Inspection directe des implémentations et tests de `main` après intégration de #1301. Cette section ne rapporte aucune exécution locale de pytest et aucune mutation exécutée.

| Invariant / axe | Code et assertions observés | Conclusion statique |
|---|---|---|
| WEIGHT-04 — normalisation des préfixes | `_parameter_tensors` retire le préfixe `transformer.`, ignore les buffers `.attn.bias` / `.attn.masked_bias` et rejette les doublons après normalisation. Les tests couvrent le cas préfixé valide avec tête liée et buffers, ainsi que la collision préfixé/non préfixé | La lacune précédemment signalée est couverte ; « assertion repérée » |
| WEIGHT-06 — validation avant assignation | `load_gpt2_state_dict` collecte toutes les valeurs dans `updates`, vérifie les paramètres manquants/inattendus, formes, types réels et finitude/représentabilité avant la boucle finale de `setattr`. Les tests prennent un snapshot de tous les paramètres NumPy du modèle avant rejet d'un paramètre manquant et d'un tenseur invalide | L'atomicité n'est pas limitée à un attribut dans les tests actuels ; « assertion repérée » pour les cas de rejet couverts. La sensibilité mutationnelle reste inconnue |
| GEN-03 — fenêtre réellement transmise | `generate` calcule `window = context[-context_length:]` à chaque itération et passe `window[None, :]` à `model.forward`. Le test actuel vérifie la longueur finale et les bornes des tokens, mais n'intercepte pas les arguments réellement transmis à `forward` | Reste « partiel ». Test discriminant recommandé : remplacer/intercepter `model.forward`, enregistrer chaque entrée, puis vérifier pour chaque pas la fenêtre exacte attendue, sa taille maximale et l'inclusion du token nouvellement généré |
| BLOCK-01 — forme et finitude | `forward` compose les branches et le test vérifie séparément `out.shape == x.shape` et `np.all(np.isfinite(out))` | Deux propriétés candidates à séparer dans la prochaine matrice atomique : préservation de forme et finitude de sortie. Elles ne deviennent pas deux unités approuvées sans mutations discriminantes |

### Mise à jour de la décomposition candidate

- `WEIGHT-04` et `WEIGHT-06` ne doivent plus conserver leurs anciennes lacunes statiques telles quelles ; les assertions pertinentes sont maintenant repérées dans la suite actuelle.
- `GEN-03` reste partiel : l'implémentation paraît correcte, mais le test ne vérifie pas la fenêtre passée au modèle. La recommandation de test est précise et directement falsifiable.
- `BLOCK-01` doit être décomposé en deux candidats, sans créer artificiellement un nouveau total approuvé.
- Aucun de ces constats ne démontre la sensibilité aux mutations. ENG-02 reste **not measured** ; le dénominateur reste non approuvé.

## 8. Décomposition atomique ciblée — ATTENTION et LOSSES (2026-11-18)

Cette décomposition est une **proposition de granularité**, pas une approbation du dénominateur. Les suffixes alphabétiques identifient des propriétés candidates séparables ; ils ne constituent pas un nouveau total ENG-02. Les états ci-dessous restent statiques tant que les mutations discriminantes ne sont pas exécutées.

### ATTENTION — propriétés candidates

| ID candidat | Propriété atomique | Assertion/test existant à rattacher | Mutation discriminante candidate |
|---|---|---|---|
| ATT-01a | `causal_mask(n)` produit zéro sur la diagonale et sous la diagonale, puis `-inf` strictement au-dessus | `test_causal_mask_structure` | Inverser la triangularité ou rendre une position future autorisée ; l'égalité élément par élément doit échouer |
| ATT-01b | L'attention causale ne laisse pas les clés/valeurs futures influencer les sorties antérieures | `test_scaled_dot_product_attention_causal_invariance` | Neutraliser le masque dans le calcul d'attention ; la perturbation des positions futures doit modifier une sortie antérieure |
| ATT-02a | Le softmax normalise indépendamment chaque tranche le long de l'axe demandé | `test_softmax_with_temperature_properties`, `test_wrong_softmax_axis_fails_per_query_normalization_invariant` | Remplacer l'axe de normalisation par un axe voisin ; les sommes attendues par tranche ne valent plus 1 |
| ATT-02b | Ajouter une constante à tous les logits d'une tranche ne change pas ses probabilités | `test_softmax_with_temperature_properties` | Supprimer la soustraction du maximum ou introduire un décalage dépendant de la valeur absolue ; comparer les probabilités avant/après translation |
| ATT-03a | À logits non uniformes fixés, une température basse concentre la distribution et une température élevée l'aplatit | `test_softmax_with_temperature_properties` | Ignorer la température ou multiplier au lieu de diviser les logits ; les distributions froide/chaude cessent de satisfaire les références |
| ATT-03b | Une température non finie ou non strictement positive est rejetée | `test_softmax_with_temperature_invalid`, `test_softmax_rejects_nonfinite_temperature` | Supprimer la validation de température ; au moins une entrée invalide doit ne plus lever `ValueError` |
| ATT-04a | Les logits finis extrêmes restent traités de façon numériquement stable lorsque le résultat mathématique est représentable | `test_softmax_extreme_finite_logits_stays_normalized`, tests des logits extrêmes proches | Réintroduire une exponentiation non stabilisée ou une soustraction qui déborde ; les tests sous `np.errstate` doivent échouer |
| ATT-04b | Les logits non finis sont rejetés par le softmax | `test_softmax_with_temperature_invalid` | Retirer le contrôle de finitude ; NaN/infini ne provoque plus le rejet attendu |
| ATT-04c | Les entrées de masque NaN/+inf sont rejetées, tandis qu'une ligne entièrement masquée suit la convention zéro explicitement documentée | `test_attention_rejects_invalid_mask_entries`, `test_fully_masked_attention_row_returns_zeros_without_warning` | Accepter NaN/+inf ou remplacer la branche de ligne entièrement masquée par une division par zéro ; les tests correspondants échouent |
| ATT-05a | Les scores QK sont divisés par \(\sqrt{d_k}\) avant softmax | `test_scaled_dot_product_attention_matches_hand_computable_weighted_sum` | Supprimer le facteur d'échelle ; les poids et la somme pondérée divergent de la référence analytique |
| ATT-05b | Les positions interdites par le masque reçoivent un poids nul et ne contribuent pas à la normalisation | `test_attention_weights_normalize_only_over_allowed_keys` | Ignorer le masque ou le traiter avec une polarité inversée ; le poids de la clé interdite devient non nul |
| ATT-05c | La sortie est la somme pondérée des vecteurs valeurs avec les poids effectivement calculés | `test_scaled_dot_product_attention_matches_hand_computable_weighted_sum`, `test_attention_weights_normalize_only_over_allowed_keys` | Remplacer l'agrégation pondérée par une somme non pondérée ou utiliser un axe erroné ; la référence manuelle échoue |
| ATT-05d | Les dimensions de sortie et de poids respectent respectivement \((T_q,d_v)\) et \((T_q,T_k)\) | `test_scaled_dot_product_attention_shapes_and_invariants` | Transposer la sortie ou les poids, ou réduire un axe ; les formes exactes échouent |

Précisions de frontière :
- ATT-01a porte sur la construction du masque ; ATT-01b porte sur son effet causal dans le calcul d'attention. Ne pas les fusionner au seul motif qu'ils concernent le même mécanisme.
- ATT-04a est une propriété numérique sur des résultats représentables ; ATT-04b/04c relèvent du contrat d'entrée et de la convention explicite des lignes entièrement masquées.
- ATT-05a/b/c/d séparent formule des scores, application du masque, agrégation des valeurs et contrat de formes. Une seule mutation ne doit pas être supposée casser les quatre propriétés.

### LOSSES — propriétés candidates

| ID candidat | Propriété atomique | Assertion/test existant à rattacher | Mutation discriminante candidate |
|---|---|---|---|
| LOSS-01a | La cross-entropy calculée depuis les logits bruts correspond à la valeur analytique attendue | `test_cross_entropy_matches_known_value` | Calculer la perte sur logits normalisés de façon incorrecte ou inverser la classe cible ; la valeur analytique échoue |
| LOSS-02a | Le gradient par rapport aux logits correspond à la dérivée numérique de la loss moyenne | `test_gradient_matches_central_finite_differences` | Inverser le signe du gradient ou omettre la division par batch ; les différences finies divergent |
| LOSS-02b | La somme des composantes du gradient est nulle pour chaque exemple | `test_gradient_rows_sum_to_zero` | Omettre la soustraction de 1 sur la classe cible ou altérer une probabilité ; la somme par ligne n'est plus nulle |
| LOSS-03a | La réduction de la loss est la moyenne des pertes individuelles du batch, et non leur somme | `test_cross_entropy_matches_known_value` (batch 1, donc non discriminant pour la réduction) ; renforcer par un cas multi-exemples à valeurs non extrêmes | Remplacer la moyenne par une somme ; un test multi-exemples doit distinguer les deux résultats |
| LOSS-03b | La réduction moyenne évite un débordement intermédiaire lorsque la moyenne finale est représentable | `test_cross_entropy_averages_large_finite_losses_without_sum_overflow` | Sommer les pertes brutes avant division ; le test sous `np.errstate(over="raise")` doit échouer |
| LOSS-04a | La loss est invariante à une translation constante indépendante de chaque ligne de logits | `test_cross_entropy_is_invariant_to_rowwise_constant_shift` | Omettre la normalisation log-sum-exp stable ou introduire une dépendance à l'offset absolu ; la comparaison échoue |
| LOSS-04b | Les cas extrêmes float64 représentables produisent une loss/gradient fini et les cas non représentables sont rejetés | `test_extreme_opposite_sign_logits_have_finite_gradient`, `test_extreme_opposite_sign_logits_have_zero_loss_for_maximum_target`, `test_unrepresentable_extreme_cross_entropy_is_rejected` | Réintroduire une soustraction/exponentiation instable ou supprimer le rejet des résultats non représentables ; les tests de frontière échouent |
| LOSS-05a | Les logits et cibles qui violent le contrat de rang, forme, type, finitude ou bornes sont rejetés | `test_invalid_inputs_raise_value_error`, `test_gradient_invalid_inputs_raise_value_error` | Supprimer une classe de validation ; conserver un cas paramétré ciblant précisément cette classe |
| LOSS-05b | Les fonctions de loss et de gradient ne modifient pas le tableau de logits fourni par l'appelant | `test_loss_and_gradient_do_not_mutate_logits` | Modifier les logits en place pendant la stabilisation ou la construction des probabilités ; le snapshot avant/après diffère |

**Lacune à traiter avant de qualifier LOSS-03a de protégé :** le test analytique actuel utilise un batch de taille 1 et ne distingue donc pas moyenne et somme. Ajouter un cas multi-exemples simple avec pertes différentes et une moyenne calculable à la main. Ne pas confondre ce futur test avec le test d'overflow, qui vérifie une propriété numérique distincte.

### Règles de consolidation

1. Les identifiants suffixés sont des unités candidates à discuter ; ils ne sont ni approuvés ni comptés dans un dénominateur.
2. Les tests cités établissent seulement la présence d'assertions repérées. Les mutations indiquées sont des expériences proposées, pas des résultats.
3. Lorsqu'un même test soutient deux propriétés, vérifier qu'il contient bien deux assertions indépendantes et qu'une mutation peut en faire échouer une sans nécessairement faire échouer l'autre.
4. Pour chaque candidat, confirmer le contrat public, l'implémentation, la localisation précise de l'assertion et l'effet observable avant de le conserver.
5. Les contrats API (validation, formes, non-mutation) doivent rester identifiés séparément des propriétés mathématiques/fonctionnelles jusqu'à décision explicite sur leur inclusion et leur pondération.

**État après cette décomposition :** ATTENTION et LOSSES sont structurés en propriétés candidates plus fines ; la revue n'est pas exhaustive, aucun dénominateur n'est proposé, aucune mutation n'est exécutée ici et ENG-02 reste **not measured**.

