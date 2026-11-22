# Audit ciblé — documentation Sentence Transformers (similarité) — 19 novembre 2026

## Décision

**Conserver comme référence technique ; ne pas créer d'extraction dédiée.**

La documentation précise les contrats API de Sentence Transformers, mais la contribution conceptuelle pertinente est déjà intégrée aux pages bilingues sur la similarité cosinus et au dossier transversal. Les détails supplémentaires sont des choix d'API et de backend, sans appel concret ni besoin de reproduction identifié dans le projet.

## Source et périmètre

- ID catalogue : `sentence-transformers-similarity-documentation`.
- URL canonique : https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
- Documentation consultée le 19 novembre 2026 : page STS, référence des fonctions de similarité et API `SentenceTransformer`.
- Source vivante : aucune version ou révision immuable n'a été établie.

## Contrats techniques observés

- La page STS encode des textes via `SentenceTransformer.encode`, puis appelle `SentenceTransformer.similarity` pour produire une matrice de scores entre toutes les paires des deux ensembles.
- La métrique de l'instance est exposée par `similarity_fn_name`. Les choix documentés pour `SentenceTransformer` comprennent cosine, dot product, distance euclidienne négative et distance Manhattan négative.
- `similarity_pairwise` calcule les scores des paires alignées (i avec i), à distinguer du calcul all-pairs qui produit une matrice.
- La documentation précise que le produit scalaire sur des embeddings normalisés est équivalent au cosinus ; choisir dot peut éviter une renormalisation répétée dans ce cas.
- La référence utilitaire actuelle expose également des variantes MaxSim/MeanMaxSim associées à des modèles multi-vecteurs ; elles ne doivent pas être confondues avec le contrat de l'API dense `SentenceTransformer.similarity`.
- L'API `SentenceTransformer` indique plusieurs backends d'inférence (torch, ONNX, OpenVINO) et une valeur de similarité configurable. Ce sont des détails dépendants de la version et du modèle.

Les exemples de la documentation utilisent des modèles précis et leurs scores illustratifs. Ils ne constituent pas des résultats généraux ni un benchmark indépendant.

## Comparaison avec le projet

Les pages `site/en/cosine-similarity.qmd` et `site/fr/cosine-similarity.qmd` couvrent déjà :
- la différence entre similarité géométrique et équivalence sémantique ;
- le rôle de la normalisation et la perte d'information portée par la norme ;
- le fait que certains modèles sont entraînés/recommandés pour dot product et d'autres pour cosine ;
- l'équivalence entre produit scalaire et cosinus pour des vecteurs normalisés ;
- les alternatives euclidienne et produit scalaire dans le protocole de comparaison ;
- la nécessité de mesurer les performances sur une tâche et un jeu représentatifs.

Le dossier `tokenization-embeddings-source-collection.md` cite explicitement Sentence Transformers pour les métriques disponibles et leur portée, et indique de ne pas transformer la page en catalogue exhaustif d'API.

## Pourquoi aucune extraction

1. Les éléments de fond utiles à l'apprentissage sont déjà couverts dans les deux langues.
2. La distinction all-pairs / pairwise est un contrat d'API, mais aucun exemple du projet ne dépend actuellement de cette API.
3. Les backends et variantes multi-vecteurs relèvent de domaines plus spécialisés, hors du périmètre de la page actuelle.
4. Une extraction supplémentaire dupliquerait des descriptions de métriques sans apporter de preuve scientifique ou de mécanisme nouveau.

**Disposition :** référence technique maintenue ; couverture conceptuelle existante ; pas d'extraction. Réouvrir si le projet adopte Sentence Transformers dans un exemple exécutable, un atelier de retrieval, ou une comparaison de modèles qui exige de documenter le contrat all-pairs/pairwise et le backend.

## Limites du relevé du 19 novembre

- Documentation vivante, non épinglée à une version.
- Audit limité à l'API dense et à la similarité textuelle ; les API SparseEncoder, CrossEncoder, évaluateurs, pertes d'entraînement et détails des modèles ne sont pas couverts.
- Aucun exemple exécuté, aucun score recalculé, aucun benchmark ou test de reproductibilité.
- Aucun statut de licence ou droit de réutilisation supplémentaire n'est établi ici ; aucun extrait long ni figure n'est reproduit.

## Sources internes croisées

- `site/en/cosine-similarity.qmd`
- `site/fr/cosine-similarity.qmd`
- `docs/source-reviews/tokenization-embeddings-source-collection.md`
- `data/sources.yml` — entrée `sentence-transformers-similarity-documentation`

## Audit du projet et vérification sur la version 6.3.0 — 22 novembre 2026

La référence publique reste une documentation vivante. Le complément de code et les essais portent sur la version `6.3.0`, commit `cddcaee3405a5efde83c1d98f89c6ebd6733dab6`. Exécution hors ligne avec Python 3.12.14, Torch `2.9.1+cpu`, Transformers `5.24.0`, Tokenizers `0.23.3` et SciPy `1.18.1`. Les vecteurs de test sont construits à la main avec `StaticEmbedding`. Le modèle multilingual E5 fournit un exemple de configuration lu à une révision fixée. Ses poids n'ont pas été exécutés. [Release 6.3.0](https://github.com/huggingface/sentence-transformers/releases/tag/v6.3.0) · [Source de l'API dense épinglée](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/model.py) · [Configuration E5 épinglée](https://huggingface.co/intfloat/multilingual-e5-small/tree/614241f622f53c4eeff9890bdc4f31cfecc418b3)

| Chemin dans la documentation et les exemples | Point à retenir | Destination dans LLM Lab |
| --- | --- | --- |
| Représenter un texte avec le pipeline modulaire | Le pooling agrège les états de tokens. Le masquage, le pooling et la normalisation dépendent du pipeline. La configuration E5 inspectée enchaîne Transformer, moyenne masquée de dimension 384 et normalisation. | Construction des vecteurs dans le dossier sur les embeddings ([FR](../../site/fr/embeddings-deep-dive.qmd), [EN](../../site/en/embeddings-deep-dive.qmd)). |
| Configurer l'encodage pour la tâche | Dans cette version, `encode_query()` cherche le prompt `query`. `encode_document()` cherche `document`, `passage`, puis `corpus`. Les méthodes fixent aussi le rôle pour un éventuel routeur. La carte E5 prescrit des préfixes explicites et l'arbre inspecté ne contient pas de `config_sentence_transformers.json` qui les déclare. | Référence d'implémentation facultative pour documenter le modèle et l'encodage requête–document lors d'une expérience de recherche. |
| Utiliser une tâche pour choisir les exemples et la loss | Les paires annotées permettent de comparer des scores à des labels. Avec des positifs et des négatifs du batch, vérifier les faux négatifs liés aux doublons et aux paraphrases. La loss d'apprentissage et le score de classement se configurent à deux étapes du protocole. | Dossier sur les embeddings pour la formation des représentations. Le document de recherche reste la destination d'évaluation du classement. |
| Calculer des scores ou classer un corpus | `similarity` produit la matrice complète. `similarity_pairwise` aligne deux listes. La recherche requête–corpus peut être suivie d'un cross-encoder qui score ensemble chaque requête et candidat de la liste. | Similarité cosinus pour les métriques, recherche documentaire pour la génération et le reclassement des candidats. |
| Évaluer selon le résultat attendu | L'évaluateur STS compare des scores de paires annotées par Pearson ou Spearman. L'évaluateur de recherche classe le corpus par requête puis rapporte notamment Recall@k, MRR et nDCG. Consigner les jeux, la langue, les jugements de pertinence et la coupure `k`. | Garder les deux évaluations distinctes dans le protocole existant de la leçon sur le cosinus. |

[Pooling à la révision inspectée](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/modules/pooling.py) · [Loss à négatifs dans le batch](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/losses/multiple_negatives_ranking.py) · [Exemple recherche et reclassement](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/examples/sentence_transformer/applications/retrieve_rerank/README.md) · [Carte E5](https://huggingface.co/intfloat/multilingual-e5-small/blob/614241f622f53c4eeff9890bdc4f31cfecc418b3/README.md)

Sentence-BERT motive le calcul séparé de vecteurs comparables pour éviter un encodage conjoint de chaque paire. E5 illustre un entraînement contrastif sur des paires faiblement supervisées. MTEB compare plusieurs familles de tâches de manière à rendre les limites d'une évaluation STS seule observables. Les jeux et résultats de ces travaux gardent leur périmètre empirique. [Sentence-BERT](https://aclanthology.org/D19-1410/) · [E5](https://arxiv.org/abs/2212.03533v2) · [MTEB](https://arxiv.org/abs/2210.07316v3)

### Contre-exemple exécutable sans checkpoint

On attribue aux deux requêtes les vecteurs `q₁ = (1, 0)` et `q₂ = (0, 1)`. Les trois documents ont les vecteurs `A = (0.90, 0.95)`, `B = (0.80, 0.70)` et `C = (0.20, 0.80)`. Un mot par entrée suffit pour les reproduire avec un tokenizer WordLevel et `StaticEmbedding`. La métrique est le produit scalaire sur ces vecteurs, sans normalisation. Les paires STS annotées `(q₁, A)`, `(q₁, C)` et `(q₂, C)` reçoivent les labels `[4, 1, 3]`. Pour la recherche, seul A est pertinent pour `q₁` et seul C est pertinent pour `q₂`.

| Requête | A | B | C | Rang du document pertinent |
| --- | ---: | ---: | ---: | ---: |
| `q₁` | 0,90 | 0,80 | 0,20 | 1 |
| `q₂` | 0,95 | 0,70 | 0,80 | 2 |

Les deux évaluateurs de la bibliothèque, appelés sur les mêmes représentations, donnent **Spearman = 1**, **Recall@1 = 0,50**, **Recall@2 = 1**, **MRR@2 = 0,75** et **nDCG@2 ≈ 0,8155**. La paire `(q₂, A)`, qui devance la cible de recherche, est absente du petit jeu STS. Le résultat constitue un contre-exemple contrôlé. La question à reprendre dans le protocole existant est « Quel ordre est correct dans le jeu de paires, et quel document est perdu si le moteur retourne un seul résultat ? » [Évaluateur STS](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/evaluation/embedding_similarity.py) · [Évaluateur de recherche](https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/evaluation/information_retrieval.py)

Contrôles complémentaires avec la même version. Avec deux états `(1,3)`, `(3,1)` et une ligne de padding `(99,99)` masquée, le pooling moyenne donne `(2,2)`. Le module Normalize donne ensuite un vecteur de norme un. Avec un modèle statique local sans prompt ni routeur, `encode_query("x")` et `encode_document("x")` rendent le même vecteur `(1,1)`. Avec des poids de jetons `query=(3,0)`, `document=(1,3)`, `passage=(1,5)` et des préfixes fournis à la configuration, ils rendent `(2,0.5)` et `(1,2)`. La sélection explicite de `passage` donne `(1,3)`.

**Décision.** Garder la documentation comme référence d'API et l'exemple comme preuve dans l'audit. Réutiliser les leçons bilingues sur les embeddings, le cosinus et la recherche documentaire. Les chiffres synthétiques vérifient les contrats d'encodage et de métrique. Le cosinus est la métrique par défaut observée lorsque l'instance synthétique laisse sa configuration de similarité vide. Une comparaison de qualité entre un encodeur générique et E5 demanderait des modèles épinglés, des paires annotées et des jugements de recherche propres à la tâche. [Issue #775](https://github.com/JM-Brun/llm-lab/issues/775)

## Suite opérationnelle

Garder la source comme référence. La prochaine revue du lot A doit cibler une source technique pour laquelle une affirmation ou un usage de code précis reste insuffisamment documenté, plutôt que d'ajouter des extraits d'API sans consommateur dans le projet.
