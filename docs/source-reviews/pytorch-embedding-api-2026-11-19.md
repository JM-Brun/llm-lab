# Audit ciblé — API PyTorch `torch.nn.Embedding` — 19 novembre 2026

## Décision

**Conserver comme référence technique ; ne pas créer d'extraction dédiée à ce stade.**

La source `pytorch-embedding-api` documente le contrat d'une API PyTorch précise. Elle est utile pour comprendre une implémentation PyTorch, mais elle ne constitue pas une preuve que le projet utilise cette API. Les explications générales de lookup et de matrice de plongements sont déjà présentes dans les pages bilingues consacrées aux embeddings. Les options propres à PyTorch ne sont pas utilisées par le chemin GPT NumPy inspecté.

## Source et périmètre consulté

- Source catalogue : `pytorch-embedding-api`.
- URL canonique : https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html
- Version affichée : documentation stable, page vivante ; aucune révision immuable ni date de publication vérifiée.
- Contrat consulté : table de lookup de taille fixe ; indices entiers en entrée ; poids de forme `(num_embeddings, embedding_dim)` ; sortie de forme `(*, embedding_dim)`.
- Options examinées : `padding_idx`, `max_norm`, `norm_type`, `scale_grad_by_freq`, `sparse`, `from_pretrained` et `freeze`.

## Comparaison avec le contenu du projet

Les pages `en/embedding-space` et `fr/embedding-space` expliquent déjà :
- qu'un ID de token sert d'indice/adresse pour sélectionner une ligne ;
- que la matrice contient une ligne par ID et un vecteur de dimension (d) par ligne ;
- que le vecteur initial n'est pas un état contextualisé ;
- que deux occurrences d'un même ID sélectionnent la même ligne initiale.

Le chemin GPT assemblé dans `src/llm_lab/foundations/gpt.py` est explicitement NumPy :
- `token_embedding` et `position_embedding` sont des matrices NumPy ;
- `token_embedding[ids]` effectue le lookup par indexation avancée ;
- les embeddings de tokens et de positions sont additionnés avant les blocs Transformer ;
- le module documente une branche d'inférence seulement, sans rétropropagation ni optimiseur.

La dépendance PyTorch est optionnelle dans le groupe `ml`. L'inspection ciblée antérieure du GPT, des blocs, des opérations et des tests n'avait identifié aucun appel direct à `torch.nn.Embedding`, `nn.Embedding`, `F.embedding` ou `torch.embedding`. Cette conclusion reste bornée aux fichiers inspectés : elle ne vaut pas scan exhaustif de tous les fichiers du dépôt.

## Ce que la source permet d'affirmer

1. `torch.nn.Embedding` est une table de lookup indexée par des tenseurs entiers.
2. Pour une entrée de forme `(*)`, la sortie ajoute une dimension `embedding_dim`, soit `(*, H)`.
3. `padding_idx` exclut la ligne correspondante des gradients ; une instance nouvellement créée initialise normalement cette ligne à zéro, mais elle peut être modifiée explicitement.
4. `max_norm` peut modifier les poids en place pendant le forward.
5. `sparse=True` produit des gradients clairsemés pour la matrice, avec une compatibilité d'optimiseurs limitée.
6. `from_pretrained` construit le module depuis une matrice de poids fournie ; le gel est activé par défaut.

Ces points sont des propriétés du contrat PyTorch documenté, pas des propriétés universelles de toute opération de lookup ni des garanties de l'implémentation NumPy du projet.

## Pourquoi aucune extraction

- Le mécanisme de base (ID → ligne → vecteur) est déjà expliqué dans les deux pages canoniques.
- Les options avancées sont propres à l'API PyTorch et ne sont pas nécessaires pour expliquer le code GPT actuel.
- Aucune page du projet ne semble actuellement faire une affirmation qui exige de citer ces options avancées.
- Extraire ces paramètres créerait un bloc d'API sans usage pédagogique ou d'implémentation identifié.

**Disposition :** référence technique maintenue dans le catalogue ; couverture conceptuelle existante ; pas d'extraction. Réouvrir la décision si une implémentation PyTorch, un exemple de padding, un transfert de poids préentraînés ou un cas de gradients clairsemés est ajouté au projet.

## Limites et travaux non effectués

- Pas de pin de version de la documentation stable vers un commit ou une version précise.
- Pas d'audit de `EmbeddingBag`, des variantes quantifiées/QAT, des API fonctionnelles, des détails CUDA ou des garanties exhaustives d'optimiseurs.
- Pas d'exécution de code ni de tests PyTorch.
- Pas de scan exhaustif du dépôt pour établir l'absence de tout usage PyTorch d'embeddings.
- Le statut de licence et les droits de réutilisation de la documentation restent ceux du catalogue ; aucun contenu ni figure n'est reproduit.

## Sources internes croisées

- `site/en/embedding-space.qmd`
- `site/fr/embedding-space.qmd`
- `src/llm_lab/foundations/gpt.py`
- `data/sources.yml` — entrée `pytorch-embedding-api`
- `docs/source-reviews/source-extraction-triage-2026-11.md`

## Suite opérationnelle

1. Garder cette source comme référence technique sans extraction.
2. Si une API PyTorch devient réellement utilisée, effectuer un scan complet des appels et tests, puis ajouter une extraction limitée aux garanties effectivement mobilisées.
3. Continuer le lot A avec la source technique suivante, en retrouvant son ID catalogue avant toute modification.
