# Cahier de reprise — audit ENG-02 et validations GPT — 2026-11-18 (suite)

## État vérifié de la branche de travail

### PR #1287 — validation des paramètres

URL : https://github.com/JM-Brun/llm-lab/pull/1287

- Toujours ouverte, en brouillon, base `main`, non fusionnée.
- Head vérifié après les derniers commits : `bf3f806c5eac163397ae2a477917dbe69ce0eef8`.
- La revue a signalé qu'un entier Python arbitrairement grand (`10**100`) peut faire lever `TypeError` dans `np.isfinite`.
- Correction appliquée : suppression de l'appel `np.isfinite` redondant dans les deux validations `top_p`. Le test de plage `0.0 < p <= 1.0` rejette déjà NaN, les infinis et les valeurs hors intervalle, sans conversion flottante susceptible de déborder.
- Tests ajoutés pour `10**100` dans `top_p_filter` et `generate`.
- Les workflows associés au nouveau head étaient en attente au dernier contrôle : CI run `44381381047` (pending) et secret scanning `44381381211` (queued). Quarto n'apparaissait pas encore dans la liste des runs associés à ce head ; vérifier à nouveau.
- Aucun pytest local n'a été exécuté. Ne pas fusionner avant le résultat des checks sur le head exact et une revue de la PR.

## Audit statique GPT-2 — constat détaillé

Fichiers examinés :
- `src/llm_lab/foundations/gpt2_weights.py`
- `tests/unit/test_gpt2_weights.py`

### Risque WEIGHT-A — collision de noms

`_parameter_tensors` retire `transformer.` avec une compréhension de dictionnaire. Si le checkpoint contient simultanément `wte.weight` et `transformer.wte.weight`, les deux clés deviennent `wte.weight` et l'une écrase l'autre selon l'ordre d'itération.

**Correction attendue :** construire le dictionnaire normalisé explicitement et lever `ValueError` lorsqu'une clé normalisée existe déjà. Ne pas fusionner les deux valeurs, même si elles sont égales : l'entrée est ambiguë et l'ordre ne doit jamais décider du poids chargé.

**Tests attendus :** collision avec valeurs différentes et collision avec valeurs identiques ; dans les deux cas, erreur explicite avant toute modification du modèle. Vérifier aussi que les checkpoints entièrement préfixés et entièrement non préfixés restent acceptés.

### Risque WEIGHT-B — tenseurs non réels ou non finis

La fonction locale `take` convertit directement avec `np.array(..., dtype=np.float64)`. Des valeurs complexes peuvent être converties avec perte (avertissement/discard de la partie imaginaire) ; NaN et infinis peuvent entrer dans le modèle sans rejet explicite.

**Correction attendue :** avant conversion, exiger un tableau de type entier ou flottant réel (rejeter notamment complexe, booléen et object), puis vérifier la finitude. Après conversion float64, vérifier encore la finitude afin de détecter les entiers ou flottants trop grands pour float64. Lever `ValueError` avec le nom du paramètre. La vérification doit concerner chaque tenseur appris, y compris `lm_head.weight` s'il est fourni, mais les buffers de masque connus restent exclus comme aujourd'hui.

**Tests attendus :** NaN, +inf, -inf, complexe, dtype object et valeur entière/float trop grande pour float64, sur au moins un paramètre tardif. Garder un test positif pour les types flottants et entiers usuels.

### Risque WEIGHT-C — atomicité insuffisamment démontrée

Le test `test_rejects_missing_parameter_without_modifying_model` ne compare que `model.token_embedding`. Il ne prouve donc pas que les autres paramètres sont inchangés.

**Correction attendue :** créer une fonction de test qui copie tous les tableaux de paramètres du modèle et de chacun de ses blocs avant le chargement. Provoquer une erreur tardive (par exemple supprimer le dernier biais MLP du dernier bloc, ou fournir une valeur invalide sur ce paramètre), puis comparer l'intégralité de l'état après l'exception. Ne pas se limiter à une erreur précoce.

### Ordre recommandé

1. Collision de clés et tests.
2. Validation des tenseurs et tests.
3. Atomicité complète et test d'échec tardif.
4. Relire le diff complet pour vérifier que les trois protections précèdent toute assignation.
5. Ouvrir une PR distincte, fondée sur le `main` courant, et attendre CI/Quarto/secret scanning.

## Audit embedding_inspection — prochaine étape

Fichiers :
- `src/llm_lab/foundations/embedding_inspection.py`
- `tests/unit/test_embedding_inspection.py`

Constats statiques :
- `cosine_top_k` accepte uniquement les `int` Python pour `k`, alors que les contrats voisins acceptent les entiers NumPy. Décider et documenter le contrat ; recommandation : accepter `np.integer`, rejeter booléens Python et NumPy.
- `np.linalg.norm` peut déborder sur des vecteurs finis de grande amplitude ; le contrôle de finitude des entrées ne garantit donc pas des normes finies.
- Une normalisation robuste par mise à l'échelle doit éviter de former directement la somme des carrés. Vérifier également le calcul du produit scalaire et la stabilité des résultats.
- Tests à ajouter : invariance du cosinus sous multiplication par une très grande et une très petite constante positive, avec des entrées qui restent représentables ; maintien des résultats ordinaires et des égalités déterministes.

Ne pas modifier le comportement pour les entrées usuelles sans test de référence. Si le domaine numérique est volontairement borné, préférer un contrat explicite à une complexité inutile.

## ENG-02 — état et méthode

- Périmètre approuvé : dix domaines GPT (attention, losses, GPT operations, TransformerBlock, GPT, training examples, decoding filters, generation, embedding inspection, GPT-2 weights).
- Le dénominateur historique de 48 lignes agrégées est retiré ; il ne doit pas être réutilisé.
- ENG-02 reste **not measured**.
- La présence statique d'une assertion ne suffit pas à qualifier un invariant de protégé : il faut une assertion discriminante et une sensibilité démontrée par mutation ou preuve équivalente.
- Décomposer les axes ATT-02/03/04/05, LOSS-05, OPS-05, GPT-02, TRAIN-03, FILTER-04, GEN-05, EMB-05 et WEIGHT-06 en propriétés atomiques, sans doublons.
- Pour chaque ligne retenue : propriété atomique, périmètre/exclusions, mutation discriminante, fichier/test/assertion, état de preuve, type (invariant fonctionnel/mathématique ou contrat API/effet de bord).
- Faire approuver inclusion, dénominateur et pondération avant tout calcul. Ne pas assimiler nombre de tests, couverture de lignes et nombre d'invariants.

## Mutations manuelles — toujours non exécutées

Les cinq mutations MUT-01 à MUT-05 restent à réaliser dans un clone local ou un environnement de développement autorisé :
1. addition résiduelle ;
2. indépendance des éléments du batch ;
3. masque causal ;
4. placement de l'epsilon LayerNorm ;
5. réduction de la cross-entropy.

Pour chaque mutation : noter SHA de départ, diff exact, commande ciblée, exit code, assertion échouée ou absence de détection, restauration, puis confirmer `git diff --exit-code`. Ne jamais committer une mutation volontaire.

## Limites et validation

Les modifications effectuées via l'API GitHub ne constituent pas une exécution locale. Aucun pytest local n'est revendiqué. Les résultats GitHub Actions doivent être associés au SHA exact, et les jobs opt-in ignorés doivent rester explicitement hors des conclusions.

## Séquence de reprise

1. Recontrôler PR #1287, son head et tous les workflows ; corriger toute régression avant fusion.
2. Implémenter WEIGHT-A, WEIGHT-B et WEIGHT-C dans une PR séparée.
3. Auditer et corriger la stabilité numérique de `cosine_top_k`, puis décider le contrat `np.integer` de `k`.
4. Reprendre la décomposition atomique de l'inventaire ENG-02.
5. Exécuter MUT-01 à MUT-05 dans un environnement local/CI approprié et consigner les preuves.
6. Faire approuver le dénominateur avant de calculer ENG-02 ; sinon conserver `not measured`.
7. Mettre à jour ce cahier avec les SHA, checks et décisions réellement observés.

## Critères de clôture

- [ ] PR #1287 validée sur son head final et fusionnée explicitement.
- [ ] Collisions préfixe/non-préfixe rejetées.
- [ ] Tenseurs non réels/non finis rejetés avant assignation.
- [ ] Test d'atomicité couvrant tous les paramètres après erreur tardive.
- [ ] Calcul des cosinus stable sur le domaine numérique retenu.
- [ ] Cinq mutations manuelles exécutées et restaurées.
- [ ] Inventaire atomique approuvé ; ENG-02 calculé ou laissé « not measured » avec justification.
