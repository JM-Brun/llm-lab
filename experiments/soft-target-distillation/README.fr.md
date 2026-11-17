# Cibles souples et supervision one-hot : une expérience contrôlée de distillation

## Question

Que conserve-t-on lorsqu'un étudiant apprend à partir de toute la distribution de probabilités d'un professeur, plutôt qu'à partir de sa seule classe la plus probable ?

## Exécution

Depuis la racine du dépôt :

```bash
python experiments/soft-target-distillation/run.py
uv run pytest tests/unit/test_soft_target_distillation.py
```

Seule la bibliothèque standard de Python est nécessaire.

## Protocole

On fixe une distribution de professeur (q_T=(0,7;0,2;0,1)). L'étudiant est un modèle catégoriel à trois logits entraînables, initialisé avec une distribution uniforme. On l'entraîne deux fois avec la même descente de gradient :

1. **Cible dure (*one-hot*) :** la classe la plus probable du professeur est convertie en vecteur ((1,0,0)).
2. **Cible souple :** l'étudiant reçoit la distribution complète ((0,7;0,2;0,1)).

Pour des logits (z), une prédiction (p=operatorname{softmax}(z)) et une cible (q), le gradient de la cross-entropie par rapport aux logits vaut (p-q).

## Résultat reproductible

Avec un taux d'apprentissage de 0,1 et 400 étapes, l'étudiant entraîné sur la cible souple se rapproche de la distribution du professeur :

- Étudiant avec cible souple : environ ((0,6999;0,1998;0,1003)).
- Étudiant avec cible one-hot : environ ((0,9825;0,0088;0,0088)).

La divergence KL du professeur vers l'étudiant vaut environ (7,4\times10^{-7}) nat avec la cible souple, contre (0,632) nat avec la cible one-hot. La cible souple conserve les préférences relatives du professeur pour les deuxième et troisième classes ; la cible one-hot perd cette information.

## Ce que l'expérience montre — et ne montre pas

- Elle illustre pourquoi la distribution complète du professeur contient davantage d'information que son seul argmax.
- Elle vérifie numériquement (H(q_T,p_S)=H(q_T)+D_{KL}(q_T\|p_S)).
- Elle ne démontre **pas** que la distillation améliore toujours l'exactitude, la généralisation ou la compression.
- Le professeur est imposé et non entraîné ; aucun jeu de données, réseau neuronal ou flux binaire n'est utilisé.
- Une distribution de professeur n'est pas une vérité terrain. La distillation peut transmettre ses erreurs, ses défauts de calibration et ses biais.
- Il s'agit d'une illustration contrôlée de l'optimisation, pas de la reproduction d'un article particulier sur la distillation.

## Lien avec la série sur la compression

La Partie 2 explique la cross-entropie et la distillation à partir de cibles souples. Cette expérience isole l'information portée par la distribution cible. L'[expérience de compression prédictive](../predictive-compression/README.fr.md) montre séparément l'utilisation de probabilités conditionnelles et un aller-retour exact de codage arithmétique. Les deux sujets sont liés par les distributions prédictives, mais ce script ne code pas lui-même un message.

Voir la leçon bilingue sur l'[entropie croisée](../../site/fr/cross-entropy.qmd) et les [mathématiques avancées du langage](../../site/fr/language-modeling-math.qmd).
