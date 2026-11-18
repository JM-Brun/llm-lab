# BEIR — audit de la source primaire

**Source :** Thakur et al., *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models*, NeurIPS Datasets and Benchmarks 2021. [Proceedings](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html) · [PDF](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf)

## Synthèse

BEIR compare plusieurs familles de systèmes de recherche en transfert zero-shot sur des tâches et domaines hétérogènes. Son résultat central n'est pas un classement universel : BM25 reste une baseline robuste, les rerankers et méthodes à interaction tardive obtiennent de bons résultats moyens à coût supérieur, et les performances varient selon les jeux de données.

## Preuves examinées

- Familles de tâches et composition : §1, Figure 1 et Table 1.
- Comparaisons lexical, sparse, dense, late-interaction et reranking : §4 et tableau de résultats.
- Biais lexical potentiel des jugements et analyse TREC-COVID : §§1–2 et discussion des jugements manquants.

## Limites et controverses

Les 18 jeux de données correspondent au périmètre d'évaluation zero-shot ; MS MARCO apparaît aussi comme jeu d'entraînement/référence dans le tableau élargi. Les systèmes diffèrent par leurs données d'entraînement et stratégies de négatifs : le benchmark n'isole donc pas causalement l'effet de l'architecture. Les annotations peuvent favoriser les systèmes lexicaux. La composition de BEIR n'est pas exhaustive.

## Décision documentaire

Extraction dédiée justifiée : composition, résultats comparatifs et biais d'annotation. Les pages bilingues *cosine similarity* et *document retrieval* utilisent directement cette source. Aucun concept ou lien nouveau n'est requis.

## Périmètre de l'audit

Lecture ciblée du papier publié : résumé, §§1–2, Figure 1, Table 1, configuration des systèmes et tableau de résultats. Aucun benchmark ou code exécuté ; aucun visuel reproduit.