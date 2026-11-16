# Structure séquentielle et compression prédictive — expérience jouet

## Question

Un modèle prédictif qui tient compte de l'ordre des symboles exploite-t-il des régularités invisibles à un modèle qui ne voit que les fréquences marginales ?

## Protocole

1. Générer une séquence déterministe à partir d'une règle simple et d'un alphabet fini.
2. Réserver un segment de test contigu, sans le mélanger à l'entraînement.
3. Ajuster deux modèles de référence : unigramme et bigramme avec lissage.
4. Permuter les symboles du corpus en conservant les fréquences marginales, puis réentraîner et réévaluer.
5. Rapporter la cross-entropy en bits/token et plusieurs graines.

## Ce que l'expérience peut montrer

Elle illustre que des dépendances séquentielles peuvent améliorer la prédiction hors échantillon et qu'une permutation peut détruire ces dépendances tout en conservant les fréquences marginales.

## Ce qu'elle ne montre pas

- Elle ne calcule pas l'épiplexité formelle de Finzi et al.
- Elle ne mesure ni la compréhension, ni la conscience, ni la subjectivité.
- Elle ne démontre pas que les LLM « apprennent le bruit » ou qu'une stratégie narrative est supérieure.
- Elle n'établit aucune équivalence entre les monoïdes An/Fn et les réseaux neuronaux.

## Exécution

Depuis la racine du dépôt :

~~~bash
python experiments/compression-strategy-spectrum/run.py
uv run pytest tests/unit/test_compression_strategy_spectrum.py
~~~

Le script utilise uniquement la bibliothèque standard de Python. Les sorties sont des mesures synthétiques reproductibles, pas des benchmarks de modèles de langage.
