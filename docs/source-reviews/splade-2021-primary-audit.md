# SPLADE — audit de la source primaire

**Source :** Formal, Piwowarski & Clinchant, *SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking*, SIGIR 2021, pp. 2288–2292. [DOI](https://doi.org/10.1145/3404835.3463098) · [arXiv](https://arxiv.org/abs/2107.05720)

## Synthèse

SPLADE produit des représentations creuses pondérées sur le vocabulaire BERT. Les activations contextualisées token-vers-vocabulaire sont agrégées par ReLU et saturation logarithmique. Le modèle optimise conjointement le classement et la parcimonie, ce qui permet une expansion lexicale apprise exploitable par index inversé.

## Preuves examinées

- Architecture et agrégation : §3.2, équation (4).
- Objectif de classement et régularisations L1/FLOPS : §3.2, équations (5)–(6).
- Résultats MS MARCO passage ranking et TREC DL 2019 : §4, Table 1.

## Limites et controverses

L'étude porte sur le premier étage de recherche, avec BERT-base, quatre GPU V100 et un index Python/Numba personnalisé. Les FLOPS estimés et les mesures de cet index ne sont pas des mesures universelles de latence de production. Les résultats de leaderboard ne sont pas directement interchangeables ; les rerankers BERT sont exclus du périmètre.

## Décision documentaire

Extraction dédiée justifiée. Les pages bilingues *cosine similarity* et *document retrieval* utilisent réellement cette source. Les concepts existants suffisent ; aucune relation ou concept nouveau n'est proposé.

## Périmètre de l'audit

Lecture ciblée du papier publié, §§3–4 et Table 1. Code, checkpoints, corpus et index non exécutés indépendamment. Aucun visuel reproduit ; droits de réutilisation non établis.