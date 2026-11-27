# Issue #1739 — contributions intellectuelles du panorama et de l'entrée texte

**Date :** 2026-11-27  
**Périmètre :** audit source FR/EN des deux premières pages du parcours Understand, `llm-overview` et `text-data`, avec les exercices dédiés à `text-data`. Le pilote #1739 `embedding-space` est déjà documenté séparément et n'est pas répété ici.  
**Méthode et limites :** inspection des sources Quarto, métadonnées de page, exemples et exercices, puis rapprochement avec le parcours canonique. Pas de validation du rendu navigateur, de l'accessibilité manuelle ni d'efficacité pédagogique.

## Résultat de synthèse

Ces deux pages jouent des rôles distincts et complémentaires :

- Le **panorama** donne le modèle mental global : une distribution conditionnelle du prochain token, trois usages, et trois axes indépendants (architecture, apprentissage, utilisation).
- **Texte et données** construit le contrat d'entrée symbolique : texte → tokens → IDs → vecteurs initiaux, en insistant sur le fait que les IDs ne sont pas des nombres sémantiques et que tokenizer et poids doivent rester associés.

Elles apportent davantage qu'une introduction terminologique : elles empêchent plusieurs erreurs de catégorie qui contamineraient les leçons suivantes.

## Matrice page par page

| Page canonique FR / EN | Apports distinctifs présents | Valeur pédagogique et placement | Décision |
|---|---|---|---|
| `llm-overview` | 1. Le modèle estime une distribution du prochain token ; cette même computation sert à générer, scorer ou entraîner, qui sont des usages distincts et non trois étapes d'une exécution. 2. LLM, Transformer et GPT sont séparés comme catégorie de modèle, famille d'architectures et famille decoder-only ; le projet choisit un petit GPT pour rendre le calcul reconstructible, sans prétendre que tous les LLM sont des GPT. 3. Architecture, apprentissage et utilisation forment trois axes de description indépendants : comment le réseau transforme l'information, comment ses paramètres sont obtenus/adaptés, et comment le modèle est utilisé. 4. La section « où réside l'information » distingue paramètres appris, contexte transmis et informations externes récupérées ; les poids ne sont pas une base documentaire consultable et une ressource récupérée n'est pas automatiquement dans le contexte. 5. Le transfert depuis le préentraînement est présenté comme réutilisation de régularités, avec limites : il dépend des données, de la tâche et de l'évaluation et n'est ni universel ni automatique. | 1–3 constituent le noyau d'orientation. Le point 4 prépare proprement context engineering/RAG et évite de personnifier les poids comme mémoire documentaire. Le point 5 est une ouverture utile, à conserver avec ses réserves. Les familles d'architecture et l'histoire détaillée restent dans les pages dédiées. | **Conserver.** Le panorama est déjà structurant ; ne pas transformer sa vue d'ensemble en catalogue d'architectures ou de techniques. |
| `text-data` | 1. La chaîne texte → tokens → IDs → lookup est suivie sur une occurrence réelle, pas seulement définie abstraitement. 2. Un ID est un identifiant local à un vocabulaire, pas une grandeur numérique de sens ; deux tokenizers peuvent découper différemment et attribuer des IDs non comparables. 3. Le tokenizer fait partie du **contrat du checkpoint** : vocabulaire, normalisation, pré-tokenisation, tokens spéciaux, reconstruction/décodage et poids indexés par vocabulaire doivent rester cohérents. Changer de tokenizer sans adapter les paramètres indexés par vocabulaire fait lire les mauvaises lignes et associe les logits aux mauvais tokens. 4. Les exemples FR/EN montrent que les frontières peuvent traverser des fragments de mots, inclure des espaces et interagir avec les octets UTF-8 ; les frontières ne sont ni celles des mots ni toujours celles des caractères Unicode. 5. Les différences de longueur ont des conséquences sur budget de contexte et coût potentiel ($T^2$ pour le nombre de paires d'une attention dense), mais un comptage isolé ne classe pas la qualité d'un tokenizer ni la maîtrise d'une langue. 6. La préparation du tokenizer/corpus au Build est distinguée de l'encodage d'un prompt à l'inférence. | Les points 1–3 sont essentiels au parcours principal et doivent rester. Le point 4 est un exemple discriminant à conserver, sans faire de la page une leçon Unicode. Le point 5 est une conséquence pratique avec des réserves importantes ; les détails de benchmarking multilingue restent dans l'approfondissement dédié. Le point 6 évite de confondre préparation des données et exécution du modèle. | **Conserver.** Aucun ajout requis ; garder le contrat tokenizer–poids et l'avertissement sur l'interprétation des IDs. |

## Points particulièrement distinctifs

### 1. Une computation, trois usages

Le panorama pose une distribution conditionnelle unique et distingue :
- la génération, qui sélectionne puis réinjecte un token ;
- le scoring, qui attribue un score à une cible ou séquence observée ;
- l'apprentissage, qui utilise les cibles pour construire une loss et mettre à jour les paramètres.

Cela fournit le cadre commun des branches détaillées ensuite. Il ne faut pas transformer ces trois usages en une séquence linéaire dans laquelle le scoring serait un passage obligatoire avant la génération.

### 2. Trois dimensions qui ne sont pas interchangeables

La séparation architecture / apprentissage / utilisation empêche de confondre une architecture (decoder-only), un régime d'apprentissage (préentraînement, fine-tuning) et un mode d'utilisation (inférence, scoring, adaptation par contexte). Elle donne un repère stable pour classer les variantes de modèles sans confondre leurs propriétés.

### 3. L'identité du tokenizer est une partie du contrat des poids

Le tokenizer ne fait pas que « couper les mots ». Il définit l'espace d'indices auquel se rapportent les lignes de la matrice d'embeddings et les classes de la projection de sortie. Les mêmes nombres entiers n'ont pas de signification transférable entre vocabulaires. Le checkpoint doit donc conserver les artefacts et conventions exacts associés aux poids.

### 4. Le coût en tokens n'est ni la qualité ni la compréhension

Le nombre de tokens est utile pour estimer l'occupation d'une fenêtre et, avec prudence, une partie du coût de calcul. Mais une séquence plus courte ne démontre pas une meilleure couverture linguistique, une meilleure qualité ou une meilleure compréhension. Les exemples du projet le disent explicitement ; ne pas retirer ces garde-fous lors d'une refonte visuelle.

## Alignement Practice et limites

- La page `text-data` dispose d'une page Practice dédiée qui vérifie l'identité des vecteurs pour un ID répété, la non-comparabilité des IDs de deux vocabulaires, l'effet des longueurs sur le budget, la séparation préfixe/continuation et le passage jusqu'aux lignes d'embeddings.
- La collection plus large d'exercices contient une trace reproductible avec `tiktoken==0.14.0`, des vérifications de séquences/IDs et un transfert vers le lookup. Cette preuve concerne la version et les exemples déclarés, pas tous les tokenizers ou toutes les langues.
- Le panorama renvoie ses questions et exercices vers une page dédiée ; la leçon conserve le modèle mental et le parcours principal.
- Le pilote #1739 `embedding-space` complète cette chaîne sur l'égalité des lookups et les invariances de table ; il reste une unité d'audit séparée.

## Cohérence avec les modèles canoniques

- `data/guided-route.yml` ordonne `llm-overview` → `text-data` → `embedding-space` → représentations. Les pages conservent cette progression.
- Les distinctions token / ID / embedding / représentation contextualisée sont déjà couvertes par les concepts canoniques. Aucun nouveau concept n'est justifié par ce lot.
- Les métadonnées `LLM-LAB-PAGE-MAP v1` décrivent déjà objectifs, périmètres et destinations. Aucun champ supplémentaire ou registre des contributions n'est requis.

## Décisions

1. **Aucune modification des deux leçons n'est justifiée par ce passage source.** Les contributions sont présentes, structurantes et déjà reliées à des pages dédiées.
2. Préserver dans le panorama : distribution prédictive commune, trois usages distincts, axes architecture/apprentissage/utilisation, et limites du transfert.
3. Préserver dans `text-data` : ID local au vocabulaire, contrat tokenizer–poids, exemple concret de segmentation, coût sans surinterprétation, et frontière prompt-inference / préparation-corpus-Build.
4. Garder les détails Unicode, familles d'algorithmes et benchmarks multilingues dans les destinations spécialisées.
5. **Validation restante :** rendu FR/EN, figure de génération, blocs d'exemple, tableaux, navigation, mobile, clavier et accessibilité manuelle.

## Sources internes inspectées

- `site/fr/llm-overview.qmd` / `site/en/llm-overview.qmd`
- `site/fr/text-data.qmd` / `site/en/text-data.qmd`
- `site/fr/exercises/text-data.qmd` / `site/en/exercises/text-data.qmd`
- `data/guided-route.yml`
- Dossier pilote #1739 `embedding-space` (réutilisé, non dupliqué)
