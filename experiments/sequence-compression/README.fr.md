# Compression de séquences : comparaison reproductible entropie / zlib

Depuis la racine du dépôt :

```bash
python experiments/sequence-compression/run.py
uv run pytest tests/unit/test_sequence_compression.py
```

Le script génère trois séquences déterministes de 20 000 symboles sur l'alphabet A/B/C/D : un motif répété ; une source de Markov d'ordre 1, avec une probabilité de 0,9 de répéter le symbole précédent ; une source IID uniforme générée avec la graine 20261116.

Il compare l'entropie marginale empirique H0, l'entropie conditionnelle d'ordre 1 H1 et la taille réellement obtenue avec zlib en bits par symbole. H1 prend en compte les dépendances à un pas que l'entropie marginale ignore.

Limites : les entropies empiriques par maximum de vraisemblance ont un biais en échantillon fini ; H1 ne capture que les dépendances d'ordre 1 ; zlib utilise un mécanisme plus riche de type LZ77/DEFLATE et ajoute un surcoût de format/codage. C'est une expérience pédagogique reproductible, pas une preuve que zlib atteint le taux d'entropie ni un benchmark de compression de LLM.
