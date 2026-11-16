# Compression prédictive : une petite expérience reproductible

## Question

Un modèle qui attribue de fortes probabilités aux symboles observés peut-il aider à encoder une séquence avec moins de bits ?

## Ce que l'expérience montre

Un petit **modèle bigramme** apprend des probabilités conditionnelles à partir d'une chaîne synthétique fixe. Il attribue ensuite une probabilité à chaque symbole en fonction du symbole précédent. Ces probabilités définissent des intervalles imbriqués de codage arithmétique. Le programme choisit une fraction binaire finie dans l'intervalle final, puis la décode.

- Un symbole plus prévisible coûte moins de bits dans le code idéal.
- La somme des surprises est le coût informationnel idéal : `-sum(log2(p(token | contexte)))`.
- Le codeur produit un code fini et le décodeur reconstruit exactement la séquence d'origine.
- Un modèle uniforme sur quatre symboles sert de référence simple : 2 bits par symbole.

C'est un modèle jouet, **pas un réseau neuronal ni un benchmark de LLM**. Il ne démontre pas qu'un LLM de production peut compresser efficacement n'importe quel fichier.

## Exécuter

Depuis la racine du dépôt :

~~~bash
python experiments/predictive-compression/run.py
uv run pytest tests/unit/test_predictive_compression.py
~~~

Seule la bibliothèque standard de Python est nécessaire pour l'expérience. Le corpus d'entraînement, le message test, l'alphabet et le lissage sont fixés dans le script. Le test vérifie le décodage exact.

## Résultat vérifié

Avec les constantes du dépôt :

~~~text
Predictive compression — exact toy experiment
Training symbols: 40
Message:          ABABACABADABABACABAD
Ideal model cost: 19.642 bits
Uniform baseline: 40.000 bits
Actual code:      21 bits
Decoded exactly:  True
Decoded message:  ABABACABADABABACABAD
~~~

Le code fini de 21 bits est légèrement plus long que le coût idéal de 19,642 bits. Le décodage restitue exactement le message.

## Comparer un domaine familier et un domaine décalé

Le script `domain_shift.py` entraîne deux modèles sur des séquences AB ou CD, puis évalue chaque modèle sur les deux motifs :

~~~bash
python experiments/predictive-compression/domain_shift.py
~~~

Cette expérience contrôlée montre qu'un modèle peut attribuer un coût faible aux motifs proches de son entraînement et un coût plus élevé à un motif décalé. Elle illustre la dépendance à la distribution ; elle ne mesure pas les performances d'un LLM ni un effet universel de fréquence.

## Expériences à essayer

1. Modifier MESSAGE pour obtenir une séquence moins prévisible.
2. Modifier TRAINING et observer l'effet sur les probabilités conditionnelles.
3. Modifier SMOOTHING ; une valeur positive évite les probabilités nulles pour les transitions jamais observées.
4. Lire interval_for : chaque symbole observé réduit l'intervalle selon sa probabilité conditionnelle.
5. Lire decode : le même modèle et les mêmes conventions sont nécessaires pour retrouver les symboles.

## Interprétation et limites

- La longueur idéale est mesurée en **bits**, avec des logarithmes en base 2.
- Le code binaire fini peut être un peu plus long que la longueur idéale.
- Le décodeur est supposé connaître le modèle et la longueur du message ; leur coût de transmission n'est pas inclus. Le modèle d'entraînement de 40 symboles et les métadonnées ne sont pas comptés : les 21 bits ne représentent que le message codé.
- Le modèle est entraîné et évalué sur une source synthétique ; cela ne mesure pas sa généralisation au langage naturel.
- Le décodage exact démontre le codage sans perte pour ce protocole, pas la reconstruction sans perte à partir d'un simple prompt LLM.
- Un LLM peut fournir des probabilités à un codeur entropique, mais la génération seule n'est pas une décompression.

## Liens avec LLM Lab

Consulter la leçon sur l'[entropie](../../site/fr/entropy.qmd), celle sur l'[entropie croisée](../../site/fr/cross-entropy.qmd) et la [synthèse comparative sur la compression](../../docs/source-syntheses/compression-two-meanings-2026-11.md).
