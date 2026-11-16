# Entropie prédictive et surprisal : une expérience jouet

## Question

L'entropie d'une distribution est-elle la même chose que la surprise d'un événement observé ?

## Exécuter

Depuis la racine du dépôt :

```bash
python experiments/entropy-surprisal-toy/run.py
```

Aucune dépendance externe n'est nécessaire.

## Résultat attendu

Pour une source binaire avec (P(A)=0{,}99) et (P(B)=0{,}01) :

- entropie moyenne : environ 0,0808 bit par tirage ;
- surprisal de A : environ 0,0145 bit ;
- surprisal de B : environ 6,6439 bits.

La source a une faible entropie moyenne, mais l'événement rare B est très surprenant lorsqu'il se produit.

## Interprétation

- L'entropie est une moyenne sur une distribution.
- Le surprisal concerne un événement effectivement observé.
- Une distribution prédictive peu incertaine ne garantit pas que chaque observation sera prévisible.
- Ni faible entropie ni faible surprisal ne prouvent qu'un token est inutile ou supprimable.

Cette expérience est un contre-exemple mathématique minimal. Elle ne teste aucun LLM, ne mesure aucune utilité sémantique et ne valide aucune méthode de pruning.
