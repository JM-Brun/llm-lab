# Issue #1739 — contributions intellectuelles des branches génération, scoring et apprentissage

**Date :** 2026-11-27  
**Périmètre :** audit source FR/EN des leçons Understand `generation`, `vraisemblance` / `likelihood`, `loss`, `gradients` et `training-loop`. La leçon `cross-entropy` est couverte par le pilote #1739 dédié ; elle est réutilisée ici comme interface entre scoring et gradients, sans répéter son inventaire.  
**Méthode :** inspection des sources Quarto, des objectifs et contrats de page, puis rapprochement avec les audits Practice du 25 novembre et le parcours canonique. Ce dossier ne certifie ni le rendu navigateur, ni l'accessibilité manuelle, ni l'efficacité réelle sur les apprenants.

## Résultat de synthèse

Ces pages exposent trois régimes d'utilisation d'un même modèle causal :

- **Génération :** le modèle prédit, une politique sélectionne un token, puis le token sélectionné est réinjecté.
- **Scoring :** le préfixe de référence est conservé ; le modèle attribue des probabilités aux tokens observés et leur agrège un score.
- **Apprentissage :** les préfixes et cibles de référence servent à calculer une loss ; le gradient est calculé à paramètres fixes, puis l'optimiseur met effectivement les paramètres à jour.

Le fil distinctif de LLM Lab est de comparer ces régimes sur les mêmes objets — préfixe, distribution, token cible, paramètres — au lieu de présenter génération, vraisemblance et entraînement comme des mécanismes sans relation.

## Matrice page par page

| Page canonique FR / EN | Apports distinctifs effectivement présents | Valeur pédagogique et placement | Décision |
|---|---|---|---|
| `generation` | 1. Séparation explicite entre **forward pass** (contexte → distribution), **décodage** (sélection) et **génération** (boucle complète, arrêt inclus). 2. Une sélection locale engage le préfixe futur : un autre token au premier tour change les distributions suivantes ; le greedy ne maximise pas nécessairement la vraisemblance globale d'une séquence. 3. Paramètres fixes et contexte qui s'allonge ; le KV cache réutilise des calculs sans constituer un apprentissage. 4. Prefill du prompt et decode incrémental sont situés dans l'exécution, avec le cache comme optimisation facultative. | Les distinctions 1–3 sont centrales et doivent rester dans Understand. Le détail d'ordonnancement, latence, continuous batching et gestion avancée du cache reste dans Practice/Deepen. Les critères d'arrêt évitent de confondre EOS, longueur maximale et « fin de réflexion ». | **Conserver.** Aucun ajout conceptuel requis dans le noyau sur la base de cette inspection. Maintenir la distinction stricte entre sélection et boucle complète. |
| `vraisemblance` / `likelihood` | 1. La séquence observée est évaluée par factorisation autorégressive, chaque facteur étant conditionné par le préfixe de référence précédent ; aucune hypothèse d'indépendance entre tokens n'est nécessaire. 2. Scoring et génération partagent le modèle mais pas la politique de continuation : le scoring suit les tokens observés, il ne les sélectionne pas. 3. Le greedy maximise le choix conditionnel local, pas nécessairement la probabilité de la séquence entière ; l'exemple comparatif rend ce contrepoint calculable. 4. La perplexité est une transformation de la NLL moyenne et dépend de la convention d'agrégation, du tokenizer et du corpus évalué. | Les points 1–3 sont des contributions de premier plan pour comprendre l'évaluation d'un modèle génératif ; garder dans Understand. Les subtilités de comparabilité inter-tokenizers et protocoles doivent rester un avertissement bref, avec renvoi vers évaluation/Deepen si besoin. | **Conserver.** Vérifier que les deux langues explicitent le préfixe de référence et ne décrivent jamais le scoring comme un décodage. |
| `loss` | 1. L'indexation par **position cible** est explicitée : les logits issus du préfixe (x_{<t}) sont comparés à la cible (x_t), même si certains frameworks indexent les logits par position d'entrée et prédisent (x_{t+1}). 2. Une erreur de décalage d'un token peut produire une loss finie et décroissante tout en entraînant la mauvaise tâche. 3. Teacher forcing est défini comme régime de conditionnement sur les tokens de référence, distinct de la loss, de l'objectif et de l'optimiseur. 4. Le masque de loss choisit les cibles qui contribuent à l'objectif ; il ne rend pas automatiquement ces tokens invisibles à l'attention. 5. La réduction (moyenne/somme/pondération) définit le dénominateur et donc l'échelle de la métrique. | Les distinctions 1–4 sont indispensables à la correction d'un pipeline et doivent rester visibles dans le noyau. Les variantes de réduction et diagnostics détaillés sont des approfondissements, mais le contrat de réduction réellement utilisé doit rester explicite. | **Conserver.** L'alerte sur le décalage silencieux est une contribution distinctive majeure ; ne pas la raccourcir au point de perdre son exemple causal. |
| `gradients` | 1. Le gradient softmax-cross-entropy par rapport aux logits pour une cible one-hot est (p-y). 2. La règle de chaîne transporte ce signal des logits vers les poids et les couches antérieures ; le gradient n'est pas lui-même une mise à jour. 3. L'exemple SGD ferme la boucle : une mise à jour change les poids, puis une nouvelle passe avant recalcule la distribution. 4. **Nuance importante :** une position ignorée par le masque de loss a une dérivée nulle pour ses propres logits dans ce terme, mais sa représentation peut encore recevoir un gradient si elle contribue comme clé ou valeur à une position cible valide via l'attention. | 1–3 constituent le fil principal. Le point 4 évite de confondre absence de supervision directe et absence de tout chemin de gradient. Garder dans Understand sous forme d'une remarque courte clairement conditionnée par le graphe de calcul. Les dérivations de gradients d'attention et vérifications numériques avancées restent dans Deepen/Practice. | **Conserver impérativement.** Ne pas simplifier le point 4 en « les positions masquées ne reçoivent pas de gradient » : ce serait faux en général. |
| `training-loop` | 1. Distingue les opérations qui lisent les paramètres (forward, loss, gradient) de la seule étape qui les modifie (update). 2. Distingue gradient, optimiseur et taux d'apprentissage. 3. La validation est calculée à paramètres fixes sur des données réservées et ne produit aucune mise à jour ; validation et test ont des rôles différents. 4. Le fil numérique relie loss locale, gradient, mise à jour, puis nouvelle passe avant ; il ne promet pas une baisse à chaque pas. | Les points 1–3 sont le cœur d'Understand. Les détails d'optimiseurs adaptatifs, calendriers de learning rate, early stopping et protocole expérimental relèvent d'un approfondissement. | **Conserver.** Le schéma de boucle doit maintenir la validation comme branche de mesure, pas comme étape d'optimisation. |

## Frontières conceptuelles à préserver

### 1. Trois préfixes qui ne doivent pas être confondus

- En **génération libre**, le préfixe s'allonge avec le token sélectionné par la politique de décodage.
- En **scoring**, le préfixe s'allonge avec le token de référence observé, que le modèle l'aurait choisi ou non.
- En **teacher forcing**, les tokens de référence restent les entrées successives pendant l'entraînement ; les logits sont comparés aux cibles décalées. Le modèle ne réinjecte pas ses propres prédictions à la place des tokens de référence.

Le prefill est une phase d'exécution d'inférence sur un prompt connu ; teacher forcing est un régime de conditionnement sur des tokens de référence, généralement associé à des cibles et une loss en entraînement. Le fait que les deux traitent une séquence connue avec un masque causal ne les rend pas équivalents.

### 2. Trois états des paramètres

- Génération : paramètres fixes.
- Scoring/évaluation : paramètres fixes.
- Calcul du gradient : paramètres lus, mais pas encore modifiés.
- Mise à jour de l'optimiseur : paramètres effectivement modifiés.
- Validation : paramètres fixes, aucune mise à jour.

Cette distinction donne au lecteur un invariant transversal pour lire les pages, les figures et les implémentations.

### 3. Masque d'attention et masque de loss

Le masque causal détermine quelles positions d'entrée peuvent contribuer à une représentation. Le masque de loss détermine quelles cibles contribuent à l'objectif agrégé. Une position peut donc être visible comme entrée tout en étant exclue comme cible ; et une représentation non supervisée directement peut participer au calcul d'une autre position supervisée.

## Vérification de cohérence avec les représentations canoniques

- `data/guided-route.yml` conserve les branches distinctes `prediction → inference`, `prediction → scoring` et `scoring → training`. Le passage de scoring à training est une relation pédagogique de réutilisation de la cible observée, pas une étape obligatoire de l'inférence.
- `data/computational-graph.yml` reste le modèle des dépendances/opérations computationnelles ; il ne doit pas devenir une copie du parcours pédagogique.
- `data/concepts.yml` porte les concepts canoniques (autoregressive generation, prefill, decode step, teacher forcing, sequence likelihood, loss mask, gradient, parameter update). Aucun nouveau concept n'est justifié par ce lot.
- Les métadonnées `LLM-LAB-PAGE-MAP v1` expriment scope, purpose, navigation et relations. Elles n'ont pas besoin d'un champ « intellectual contributions » supplémentaire : les preuves atomiques restent dans `data/extractions/`, les décisions comparatives dans les dossiers de synthèse, et la présente matrice dans le journal d'audit.

## Réutilisation des audits antérieurs

- L'audit Practice du 2026-11-25 a déjà vérifié la séparation prefill / teacher forcing / free-running, corrigé une réponse trop compressée de GE-D et ajouté un exercice ciblé. Ne pas créer un autre exercice générique de prefill.
- Le même audit a confirmé que le Build G2 traite les paires décalées et précise que teacher forcing est un régime de conditionnement, pas l'objectif ou l'optimiseur.
- L'audit scoring du 2026-11-25 a déjà vérifié la factorisation, les calculs de vraisemblance et le contre-exemple greedy / vraisemblance de séquence.
- L'audit gradient du 2026-11-25 a déjà vérifié des dérivées représentatives, la chaîne jusqu'aux poids, l'exemple de mise à jour et les exercices. La continuation attention-gradient a ajouté AT-E ; elle ne prouve pas la correction d'un backward multi-tête/batch complet.
- Le pilote #1739 cross-entropy couvre déjà l'apport propre de cette leçon. Le présent dossier ne le duplique pas.

## Décisions et actions

1. **Aucune modification de leçon n'est justifiée par ce passage source.** Les apports distinctifs sont déjà présents et les corrections importantes ont été apportées lors des audits antérieurs.
2. Préserver explicitement dans les futures refontes : choix local vs vraisemblance de séquence ; préfixe de référence vs préfixe généré ; prefill vs teacher forcing ; masque causal vs masque de loss ; gradient direct nul vs chemin indirect par attention ; calcul du gradient vs update ; validation sans update.
3. Maintenir la séparation des trois branches dans les cartes de transition, le parcours et le graphe. Ne pas linéariser artificiellement le chemin de prédiction.
4. **Validation restante :** rendu FR/EN, navigation, équations, figures, mobile, clavier et revue manuelle d'accessibilité. Les audits de source et les checks CI ne constituent pas ces preuves.
5. **Suite #1739 :** poursuivre l'inventaire page par page des leçons Understand non encore couvertes, en partant des registres canoniques ; tenir une matrice exhaustive et éviter de réauditer les pages déjà couvertes par les pilotes et audits datés.

## Sources internes inspectées

- `site/fr/generation.qmd` / `site/en/generation.qmd`
- `site/fr/vraisemblance.qmd` / `site/en/likelihood.qmd`
- `site/fr/cross-entropy.qmd` / `site/en/cross-entropy.qmd` (interface seulement ; pilote #1739 distinct)
- `site/fr/loss.qmd` / `site/en/loss.qmd`
- `site/fr/gradients.qmd` / `site/en/gradients.qmd`
- `site/fr/training-loop.qmd` / `site/en/training-loop.qmd`
- `data/guided-route.yml`
- `docs/page-audit-inventory.md` (audits du 2026-11-25 et du 2026-11-26)
