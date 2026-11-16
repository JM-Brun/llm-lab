# Théorie de l'information et LLM : mini-expérience reproductible

Depuis la racine du dépôt :

```bash
python experiments/information-theory-llm/run.py
uv run pytest tests/unit/test_information_theory_llm.py
```

Le script, qui n'utilise que la bibliothèque standard, calcule entropie, entropie croisée, divergence KL et information mutuelle sur de petites distributions synthétiques. Il vérifie (H(P,Q)=H(P)+D_{KL}(P\|Q)).

Il s'agit d'une illustration numérique, pas d'une expérience sur un LLM ni d'une analyse de l'attention. L'information mutuelle est calculée à partir d'une distribution jointe explicite. Les poids d'attention sont des coefficients d'agrégation dépendant de l'entrée, pas l'information mutuelle elle-même.

Les résultats flottants sont approximatifs. Aucun réseau neuronal, entraînement, corpus réel ou tenseur d'attention n'est utilisé.


Le script comprend aussi un exemple XOR équilibré pour la V-information prédictive. Il compare une famille limitée à des prédicteurs constants à une famille capable de représenter l'interaction XOR. C'est un calcul jouet exact illustrant la définition de Xu et al. (ICLR 2020), pas un benchmark de réseau neuronal ni une reproduction du théorème PAC de l'article.

Papier primaire : https://openreview.net/forum?id=r1eBeyHFDH (également https://arxiv.org/abs/2002.10689).

Pour comparer entropie marginale, entropie conditionnelle d'ordre 1 et taille zlib sur des séquences reproductibles, voir l'[expérience dédiée](../sequence-compression/README.fr.md).
