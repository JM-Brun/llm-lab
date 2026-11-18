# Sentence-BERT — audit de la source primaire

**Date de revue :** 2026-11-18  
**Issue de suivi :** [#1211](https://github.com/JM-Brun/llm-lab/issues/1211)  
**Source :** Reimers & Gurevych (2019), *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*, EMNLP-IJCNLP 2019, pp. 3982–3992. [ACL Anthology](https://aclanthology.org/D19-1410/) · [PDF](https://aclanthology.org/D19-1410.pdf) · DOI: 10.18653/v1/D19-1410.

**Périmètre :** lecture du PDF publié, de l'architecture, des tables 1–7, des ablations et des limites. Pas de reproduction indépendante, d'exécution de code, d'audit du dépôt Sentence-Transformers ni de téléchargement/inspection des checkpoints.

## Synthèse

Sentence-BERT (SBERT) adapte BERT/RoBERTa pour produire des vecteurs de phrases calculés indépendamment, réutilisables pour comparer des phrases, regrouper des textes ou générer des candidats de recherche. Le papier montre que les sorties BERT brutes moyennées ou le vecteur CLS ne donnent pas nécessairement un espace adapté à la similarité cosinus ; un fine-tuning en architecture siamoise/triplet sur des données NLI améliore fortement les résultats STS évalués.

Trois distinctions doivent rester explicites :

1. **Bi-encodeur et cross-encodeur répondent à des contraintes différentes.** Le bi-encodeur encode chaque phrase séparément ; le cross-encodeur compare les deux phrases dans le même passage Transformer et peut exploiter des interactions fines, mais son score n'est pas pré-calculable indépendamment pour chaque phrase.
2. **L'espace vectoriel est appris pour un objectif et un domaine.** Un score cosinus n'est ni une vérité sémantique universelle ni une probabilité calibrée.
3. **La performance dépend du protocole.** Les résultats STS, l'évaluation cross-topic et le benchmark de débit mesurent des choses différentes ; les chiffres de débit sont liés à du matériel de 2019.

## 1. Architecture et objectifs (§3, pp. 3984–3985)

SBERT ajoute un pooling aux sorties de BERT/RoBERTa afin d'obtenir un vecteur de dimension fixe. Le papier compare :
- **CLS** : sortie du token spécial CLS ;
- **MEAN** : moyenne des représentations contextualisées de tokens (configuration par défaut) ;
- **MAX** : maximum temporel/dimensionnel des sorties de tokens.

Les deux branches de l'architecture siamoise partagent les poids dans le modèle présenté. Cette contrainte décrit le SBERT original ; elle ne définit pas tous les bi-encodeurs modernes.

Le papier compare trois objectifs :
- **Classification NLI** : concaténer (u), (v) et (|u-v|), puis entraîner un classifieur softmax avec cross-entropy.
- **Régression STS** : utiliser la similarité cosinus des deux vecteurs et minimiser une erreur quadratique moyenne.
- **Triplet loss** : rapprocher l'ancre du positif et l'éloigner du négatif d'une marge donnée.

La représentation utilisée à l'inférence est le vecteur de phrase ; le vecteur combiné ((u,v,|u-v|)) est la tête de classification d'entraînement, pas une obligation pour comparer les vecteurs ensuite.

## 2. Résultats STS (§4.1, Table 1)

Sur sept jeux STS, les auteurs rapportent une corrélation moyenne de Spearman de **76,55** pour SBERT-NLI-large, contre **71,22** pour Universal Sentence Encoder et **61,32** pour les embeddings GloVe moyennés. Les sorties BERT moyennées atteignent **54,81** et CLS **29,19** dans ce protocole cosinus.

Ce résultat n'est pas uniforme sur tous les jeux : Universal Sentence Encoder est meilleur sur SICK-R, que les auteurs relient à une adéquation plus forte de ses données d'entraînement à ce jeu. Il faut donc présenter le résultat comme une amélioration agrégée sur le protocole évalué, pas comme une domination sur toute tâche.

Sur STS Benchmark supervisé (Table 2), les résultats changent selon l'architecture et les données : après NLI + STSb, les modèles BERT cross-encoder dépassent les SBERT correspondants dans les configurations reportées. Le papier n'établit donc pas que le bi-encodeur est plus précis pour toute comparaison de paires ; son intérêt majeur est de rendre les vecteurs réutilisables et les comparaisons à grande échelle plus efficaces.

## 3. Généralisation thématique : Argument Facet Similarity (§4.3, Table 3)

Le corpus AFS contient 6 000 paires d'arguments issues de dialogues sur trois sujets. En validation croisée aléatoire à dix plis, SBERT est proche de BERT. En entraînant sur deux sujets et en testant sur le troisième, SBERT perd environ sept points de corrélation de Spearman ; l'écart avec BERT devient plus marqué.

L'interprétation des auteurs est importante : un cross-encoder peut comparer directement les deux arguments et leurs interactions lexicales ; un bi-encodeur doit placer individuellement des arguments d'un sujet inédit dans un espace vectoriel. Ce résultat illustre une limite de généralisation dans ce protocole à trois sujets ; il ne prouve pas que tous les bi-encodeurs échouent hors domaine.

## 4. SentEval et ce que mesure la similarité (§5, Table 5)

Sur sept tâches de classification SentEval, SBERT-NLI-large obtient la meilleure moyenne rapportée et arrive en tête sur cinq tâches sur sept. Mais les auteurs soulignent que les embeddings BERT moyens/CLS peuvent avoir des performances correctes avec une régression logistique alors qu'ils sont mauvais pour la similarité cosinus sur STS.

Pourquoi ? Le classifieur logistique apprend des poids par dimension ; le cosinus traite les dimensions de façon uniforme. **Une représentation utile comme caractéristique d'un classifieur n'est donc pas automatiquement un bon espace de similarité cosinus.**

Les auteurs précisent également que le transfert de tâche n'est pas l'objectif principal de SBERT : pour adapter BERT à une tâche supervisée, le fine-tuning de l'ensemble du modèle reste préférable.

## 5. Ablations et débit (§6–7, Tables 6–7)

L'ablation sur STSb montre que MEAN est le meilleur des trois poolings dans les configurations évaluées ; MAX est nettement moins bon pour la régression STS. Pour la classification NLI, le pooling a un effet plus faible que le choix des caractéristiques de paire, où (|u-v|) joue un rôle important. Ce n'est pas une loi générale en faveur de MEAN pour tous les modèles.

Sur le serveur de l'étude (Intel i7-5820K, Nvidia Tesla V100, CUDA 9.2), SBERT avec smart batching encode 2 042 phrases/s sur GPU, contre 1 876 pour InferSent et 1 318 pour Universal Sentence Encoder. Sur CPU, SBERT est plus lent qu'InferSent. Le smart batching apporte, selon les auteurs, +89 % sur CPU et +48 % sur GPU.

Ces mesures portent sur l'encodage de phrases dans un environnement historique. Elles ne mesurent pas le coût total d'une recherche : indexation, mémoire, approximate nearest neighbours, filtrage, reranking, réseau et latence de service sont hors de ce débit.

## 6. Décisions d'intégration dans LLM Lab

- Garder le contenu dans les pages bilingues existantes sur les embeddings et la similarité cosinus ; ne pas ajouter une étape obligatoire à la route.
- Utiliser SBERT comme exemple primaire du bi-encodeur à vecteur unique, en distinguant son Siamese à poids partagés des bi-encodeurs au sens large.
- Relier le papier au contraste cross-encoder et à ColBERT/late interaction déjà documentés.
- Garder les résultats cross-topic comme avertissement sur la généralisation et la dépendance au protocole.
- Ne pas promouvoir les scores STS ni le débit de 2019 en KPI du projet.
- Aucun nouveau concept ni relation du graphe n'est nécessaire ; le concept existant `contextualized-representation` suffit.

## 7. Travail restant

- Auditer le dépôt Sentence-Transformers et les configurations/checkpoints historiques si une reproduction est réellement nécessaire.
- Vérifier les versions de jeux STS, les scripts de scoring et les seeds avant toute comparaison numérique reproductible.
- Auditer séparément ColBERT et ColBERTv2 sur leurs tables de benchmark, ablations, mémoire d'index et latence, puis BEIR pour le rôle des benchmarks hétérogènes.
- Ne pas présenter la présente revue comme une reproduction ni comme une validation actuelle des performances.
