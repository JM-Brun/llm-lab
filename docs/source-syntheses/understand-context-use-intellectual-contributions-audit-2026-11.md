# Issue #1739 — contributions intellectuelles autour du contexte

**Date :** 2026-11-27  
**Périmètre :** audit source FR/EN des deux leçons Understand `in-context-learning` et `context-engineering`, avec leurs exercices Practice dédiés. Le lot suit les deux branches déjà auditées (génération/scoring/apprentissage) et vérifie la frontière entre adaptation par le prompt et conception système du contexte.  
**Méthode et limites :** inspection des sources Quarto, métadonnées de page, exercices et liens de destination. Pas de validation du rendu navigateur, de l'accessibilité manuelle, des performances d'un système RAG réel ni de l'efficacité pédagogique auprès d'apprenants.

## Résultat de synthèse

Les deux leçons répondent à des questions voisines mais différentes :

- **In-context learning (ICL)** : comment le modèle utilise-t-il des instructions et démonstrations effectivement présentes dans le prompt, à paramètres fixes ?
- **Context engineering** : comment l'application sélectionne-t-elle, organise-t-elle, actualise-t-elle et sécurise-t-elle les informations qu'elle transmet au modèle ?

La distinction évite deux erreurs fréquentes : traiter RAG ou la mémoire comme des capacités internes équivalentes à l'ICL ; supposer que tout ce que l'application stocke ou récupère est automatiquement visible par le modèle.

## Matrice page par page

| Page canonique FR / EN | Apports distinctifs présents | Valeur pédagogique et placement | Décision |
|---|---|---|---|
| `in-context-learning` | 1. Définition opérationnelle de l'ICL à paramètres fixes, avec distinction zero-shot / one-shot / few-shot. 2. La page signale honnêtement que le périmètre du terme varie dans la littérature ; elle annonce sa définition large au lieu de faire passer un choix terminologique pour un consensus universel. 3. La comparaison avec préentraînement, fine-tuning et RAG sépare adaptation du contexte et mise à jour des paramètres. 4. La limite centrale est explicitée : imiter le format ou les motifs superficiels ne prouve pas l'apprentissage de la règle ni la généralisation. 5. Les induction heads sont présentées comme une hypothèse mécaniste étudiée pour certains comportements, et non comme une explication universelle de l'ICL. | Les points 1–4 sont essentiels dans Understand. La réserve terminologique doit rester concise mais visible. Le point 5 appartient à Deepen ; son statut de mécanisme partiel et non universel est important pour ne pas surinterpréter le comportement. Les protocoles expérimentaux détaillés restent dans Practice/Deepen. | **Conserver.** La page contient déjà une valeur distinctive suffisante ; ne pas ajouter une longue revue des mécanismes internes au noyau. |
| `context-engineering` | 1. Modèle à trois niveaux : contexte disponible dans le système, séquence effectivement transmise dans la fenêtre, puis positions accessibles à une requête selon architecture/masque. 2. L'information stockée, l'information récupérée et l'information effectivement transmise sont trois états différents ; une mémoire persistante n'est pas automatiquement visible. 3. Une fenêtre plus grande n'assure pas une meilleure réponse : pertinence, position, lisibilité, bruit, contradictions, fraîcheur et coût comptent. 4. La séparation instructions fiables / données externes non fiables rend le risque d'injection indirecte concret. 5. La conception du contexte est présentée comme une boucle de sélection, récupération, structuration, priorisation, compression, mise à jour, sécurisation et évaluation, pas comme une fonctionnalité ou architecture de modèle. 6. L'évaluation proposée mesure qualité, fidélité aux sources, erreurs non étayées, latence et coût sous conditions comparables. | Le modèle à trois niveaux et la frontière stocké → sélectionné → transmis → accessible sont centraux et doivent rester dans Understand. Les familles de retrievers, les architectures RAG et les détails de mémoire sont renvoyés vers les pages spécialisées. La sécurité et l'évaluation restent au niveau conceptuel dans le noyau, avec les protocoles détaillés en Practice. | **Conserver.** La distinction en trois niveaux est la contribution structurante principale. Ne pas fusionner cette page avec ICL, RAG ou contextualized representations. |

## Contributions à préserver

### 1. ICL est un comportement conditionné, pas une mise à jour

Les démonstrations font partie de l'entrée active et orientent le calcul des représentations ; elles ne modifient pas les poids. Une réponse différente à un prompt différent ne constitue donc pas, à elle seule, une adaptation persistante du modèle.

La comparaison avec RAG est soigneusement bornée : la récupération ajoute des documents au contexte, mais ne met pas les paramètres à jour par elle-même. RAG peut alimenter une situation d'ICL, mais les deux termes ne désignent pas le même mécanisme.

### 2. Succès sur les exemples vus ≠ généralisation

La leçon et les exercices distinguent reproduction d'un format, imitation de motifs et application d'une règle à des cas nouveaux. L'exercice Practice recommande de séparer la conformité de format de l'exactitude de contenu, de tester des exemples non vus et de perturber l'ordre ou la pertinence des démonstrations. Ce sont des mesures comportementales ; elles ne révèlent pas à elles seules l'algorithme interne appris.

Les induction heads sont correctement confinées à un approfondissement mécaniste : elles éclairent certains phénomènes de copie/continuation dans certains Transformers, mais ne rendent pas compte de toutes les formes d'ICL.

### 3. Trois niveaux de contexte, trois questions différentes

1. **Contexte du système :** quelles informations l'application a-t-elle sélectionnées pour cet appel ?
2. **Séquence d'entrée / fenêtre :** quels tokens et contenus structurés ont effectivement été transmis, dans quel budget ?
3. **Contexte accessible à une position :** quelles positions une requête peut-elle consulter compte tenu du masque et de l'architecture ?

Une application peut conserver 200 messages et une mémoire persistante tout en n'envoyant que deux passages et la question. Et, dans un décodeur causal, les positions futures restent inaccessibles à une requête antérieure même si elles appartiennent à la séquence d'entrée. Cette séparation relie proprement l'ingénierie système au masque causal sans confondre sélection applicative et calcul du Transformer.

### 4. Le contexte est une frontière de sécurité et de provenance

Un document récupéré ou un résultat d'outil est une donnée, pas une instruction de confiance. La page donne un exemple explicite d'injection indirecte et recommande hiérarchie d'instructions, délimitation des sources externes, limitation des permissions d'outils et tests adversariaux. Elle précise qu'un rappel textuel seul ne garantit pas la sécurité.

La provenance, la fraîcheur et la pertinence des éléments récupérés sont également des propriétés à examiner. Cette dimension est une contribution distinctive du passage du modèle isolé au système LLM.

### 5. Une fenêtre de contexte est un budget, pas une métrique de qualité

Une entrée plus longue peut améliorer la réponse si elle apporte des éléments utiles, mais peut aussi ajouter bruit, répétitions, contradictions et coût. Le critère n'est pas de remplir la fenêtre : il est de fournir les éléments pertinents et accessibles, avec une qualité et une provenance contrôlables.

## Alignement Practice et frontières de contenu

- La page ICL indique deux questions de transfert avec réponses. L'exercice EN distingue explicitement amélioration de format et amélioration d'exactitude, puis propose un test de généralisation sur des cas inédits. Le contenu FR suit la même structure.
- La page context engineering annonce sept questions Practice. Les exercices couvrent sélection/transmission, distinction des trois niveaux, RAG et mémoire, injection indirecte, évaluation comparative, provenance et évolution du contexte entre deux appels.
- Les exercices restent séparés des leçons, conformément à l'architecture Practice. Aucun nouvel exercice générique n'est justifié par ce passage.
- La relation avec `contextualized-representations` est explicite et correcte : les états cachés sont les résultats du calcul sur les tokens accessibles, pas des informations stockées ou sélectionnées par l'application.
- Les destinations spécialisées existent déjà : `document-retrieval` et `rag-memory-boundaries`. Les approfondissements mécanistes ICL sont conservés dans la section Deepen de la page elle-même ; aucune nouvelle page n'est justifiée.

## Cohérence avec les modèles canoniques

- `data/guided-route.yml` place `in-context-learning` après la génération, puis `context-engineering`. Cela exprime une progression de la boucle d'inférence vers l'utilisation applicative du contexte ; cela ne signifie pas que context engineering est une étape interne du forward pass.
- `data/concepts.yml` et `data/computational-graph.yml` doivent continuer à distinguer les concepts de contexte et les opérations du modèle. Les trois niveaux de contexte sont une distinction pédagogique et système ; ils ne justifient pas de transformer chaque niveau en nœud computationnel.
- Les métadonnées `LLM-LAB-PAGE-MAP v1` couvrent déjà le scope, purpose, les liens et le niveau. Aucun nouveau champ, registre d'apports ou nœud conceptuel n'est nécessaire.

## Décisions

1. **Aucune modification des deux leçons n'est justifiée par ce passage source.** Les apports distinctifs identifiés sont déjà présents, structurés et reliés aux exercices.
2. Préserver la différence entre ICL (usage des exemples présents dans le prompt) et context engineering (conception de ce qui est transmis).
3. Préserver les trois niveaux de contexte et la frontière stocké / récupéré / transmis / accessible.
4. Ne pas présenter les induction heads comme explication générale de l'ICL, ni RAG/mémoire comme synonymes de contexte.
5. Conserver dans Practice les tests de généralisation, d'injection indirecte, de provenance et de contexte entre appels.
6. **Validation restante :** rendu FR/EN, diagramme SVG sur desktop/mobile, navigation, liens, équations, clavier et revue manuelle d'accessibilité. L'inspection source ne valide pas le rendu ni l'efficacité pédagogique.

## Sources internes inspectées

- `site/fr/in-context-learning.qmd` / `site/en/in-context-learning.qmd`
- `site/fr/context-engineering.qmd` / `site/en/context-engineering.qmd`
- `site/fr/exercises/in-context-learning.qmd` / `site/en/exercises/in-context-learning.qmd`
- `site/fr/exercises/context-engineering.qmd` / `site/en/exercises/context-engineering.qmd`
- `data/guided-route.yml`
