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

## Limites

- Documentation vivante, non épinglée à une version.
- Audit limité à l'API dense et à la similarité textuelle ; les API SparseEncoder, CrossEncoder, évaluateurs, pertes d'entraînement et détails des modèles ne sont pas couverts.
- Aucun exemple exécuté, aucun score recalculé, aucun benchmark ou test de reproductibilité.
- Aucun statut de licence ou droit de réutilisation supplémentaire n'est établi ici ; aucun extrait long ni figure n'est reproduit.

## Sources internes croisées

- `site/en/cosine-similarity.qmd`
- `site/fr/cosine-similarity.qmd`
- `docs/source-reviews/tokenization-embeddings-source-collection.md`
- `data/sources.yml` — entrée `sentence-transformers-similarity-documentation`

## Suite opérationnelle

Garder la source comme référence. La prochaine revue du lot A doit cibler une source technique pour laquelle une affirmation ou un usage de code précis reste insuffisamment documenté, plutôt que d'ajouter des extraits d'API sans consommateur dans le projet.
