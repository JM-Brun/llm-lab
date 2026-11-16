# Théorie de l'information et LLM : mini-expérience reproductible

Depuis la racine du dépôt :

```bash
python experiments/information-theory-llm/run.py
uv run pytest tests/unit/test_information_theory_llm.py
```

Le script, qui n'utilise que la bibliothèque standard, calcule entropie, entropie croisée, divergence KL et information mutuelle sur de petites distributions synthétiques. Il vérifie (H(P,Q)=H(P)+D_{KL}(P\|Q)).

Il s'agit d'une illustration numérique, pas d'une expérience sur un LLM ni d'une analyse de l'attention. L'information mutuelle est calculée à partir d'une distribution jointe explicite. Les poids d'attention sont des coefficients d'agrégation dépendant de l'entrée, pas l'information mutuelle elle-même.

Les résultats flottants sont approximatifs. Aucun réseau neuronal, entraînement, corpus réel ou tenseur d'attention n'est utilisé.
