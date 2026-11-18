# ENG-02 — Inventaire des invariants critiques GPT

**Version :** 0.1 — 2026-11-18  
**Référence inspectée :** `71f87f8d633e1a7a4fdcf1ac82b29bda181b307d`  
**Statut :** périmètre de dix domaines approuvé ; inventaire candidat ; dénominateur non approuvé ; ENG-02 = **not measured**.

## 1. Objet et règle de comptage

L'inventaire transforme le périmètre approuvé en propriétés comportementales distinctes, chacune reliée à une preuve de test. Il ne compte ni fonctions, ni cas paramétrés, ni lignes couvertes, ni méthodes de test.

Une propriété est comptée une seule fois, même si plusieurs tests l'étayent. Deux propriétés sont séparées lorsqu'une mutation plausible peut en casser une sans casser l'autre. Les validations homogènes sont regroupées ; elles ne sont pas comptées une fois par valeur invalide.

Le tableau contient **48 invariants candidats**. Ce nombre est un inventaire de travail, pas le dénominateur officiel : regroupements, exclusions et criticité doivent être relus et approuvés. Les lignes « partiel » restent au dénominateur proposé, mais ne sont pas réputées couvertes au numérateur.

## 2. Inventaire candidat (48)

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
| TRAIN-03 | Training examples | Séquences courtes et paramètres/formes/types invalides rejetés | test_invalid_inputs_raise_value_error | Partiel : booléens/flottants positifs context/stride non testés |
| TRAIN-04 | Training examples | Construction déterministe sans mutation du flux source | test_output_is_deterministic_and_stream_is_not_mutated | Protégé |
| FILTER-01 | Decoding filters | Top-k garde exactement k candidats et renormalise | test_top_k_keeps_exactly_k_renormalized_candidates; identity when k >= vocab | Protégé |
| FILTER-02 | Decoding filters | Top-p garde le plus petit noyau atteignant le seuil, token de franchissement inclus | test_top_p_includes_the_token_that_crosses_the_threshold; test_top_p_nucleus_size_adapts_to_distribution_shape | Protégé |
| FILTER-03 | Decoding filters | Égalités départagées de façon déterministe par indice | test_top_k_breaks_ties_by_lowest_index_deterministically; test_top_p_breaks_ties_by_lowest_index | Protégé |
| FILTER-04 | Decoding filters | Seuils/distributions invalides rejetés et entrée non mutée | tests invalid_distributions, top_k_invalid_k, top_p_invalid_p, filters_do_not_mutate_the_input | Partiel : p=True accepté comme 1.0 |
| GEN-01 | Generation | Greedy choisit l'argmax du dernier pas et construit la chaîne autoregressive | test_generate_greedy_is_deterministic_and_matches_manual_argmax_chain | Protégé |
| GEN-02 | Generation | Échantillonnage reproductible avec RNG seedé | test_generate_sampled_tokens_are_reproducible_with_seeded_rng | Protégé |
| GEN-03 | Generation | Chaque pas transmet au modèle uniquement la dernière fenêtre de contexte | test_generate_slides_the_context_window | Partiel : sortie vérifiée, pas les fenêtres réellement transmises |
| GEN-04 | Generation | Ordre température → top-k → top-p et effets de troncature | tests temperature_before_filtering, sampling_with_truncation, top_k_one, tight_top_p | Protégé |
| GEN-05 | Generation | Paramètres invalides rejetés même en greedy ; zéro token préserve le prompt | tests validation_errors, rejects_non_integer_token_counts, without_new_tokens, rejects_nonfinite_temperature | Protégé |
| EMB-01 | Embedding inspection | Lookup préserve ordre/doublons des IDs et renvoie une copie | test_lookup_preserves_id_order_and_duplicates | Protégé |
| EMB-02 | Embedding inspection | Matrice/IDs invalides (forme, type, non-finis, bornes) rejetés | test_lookup_rejects_invalid_matrix_or_ids | Protégé |
| EMB-03 | Embedding inspection | Top-k cosine renvoie IDs et scores en ordre décroissant | test_cosine_top_k_returns_ids_and_descending_scores | Protégé |
| EMB-04 | Embedding inspection | Égalités stables par ID et exclusion de soi contrôlée | tests excludes_self_and_breaks_ties_by_id; can_include_self_explicitly | Protégé |
| EMB-05 | Embedding inspection | Requête cosine définie et candidats de norme nulle exclus | tests rejects_undefined_or_invalid_requests; excludes_zero_norm_candidates | Partiel : amplitude extrême et np.int64(k) non couverts |
| WEIGHT-01 | GPT-2 weights | Embeddings de tokens et tête de sortie liées selon le contrat | test_copies_embeddings_and_ties_output_head_to_token_table | Protégé |
| WEIGHT-02 | GPT-2 weights | QKV fusionné découpé Q/K/V et transposé correctement | test_splits_fused_qkv_and_transposes_conv1d_weights | Protégé |
| WEIGHT-03 | GPT-2 weights | Projections attention/MLP mappées selon conventions et formes | test_splits_fused_qkv_and_transposes_conv1d_weights; test_gpt2_small_config_matches_published_dimensions | Protégé |
| WEIGHT-04 | GPT-2 weights | Préfixes HF et buffers de masque gérés sans collision silencieuse | test_accepts_transformer_prefix_tied_head_and_mask_buffers | Partiel : collision préfixé/non préfixé non testée |
| WEIGHT-05 | GPT-2 weights | Tête non liée, clés manquantes/inattendues et formes incorrectes rejetées | tests rejects_untied_output_head, rejects_missing_parameter, rejects_unexpected_parameter, rejects_shape_that_does_not_match_config | Protégé |
| WEIGHT-06 | GPT-2 weights | Copies float64 indépendantes et validation complète avant assignation | tests loaded_parameters_are_independent_float64_copies; rejects_missing_parameter_without_modifying_model | Partiel : atomicité comparée sur un seul attribut |

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
