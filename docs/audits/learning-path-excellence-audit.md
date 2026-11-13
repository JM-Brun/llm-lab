# Audit éditorial du parcours principal — valeur pédagogique et profondeur intellectuelle

> **Statut : diagnostic préliminaire, à confirmer.** Ce document conserve les constats et décisions de cadrage issus de l'audit initial du parcours principal. Il ne constitue pas une validation exhaustive du contenu publié : la lecture intégrale des 18 pages dans les deux langues et la vérification du rendu navigateur restent à effectuer.

- Projet : [LLM Lab](https://jm-brun.github.io/llm-lab/)
- Parcours : [LLM overview (FR)](https://jm-brun.github.io/llm-lab/fr/llm-overview.html)
- Skill éditoriale associée : `.agents/skills/learning-path-excellence/SKILL.md` (PR [#1076](https://github.com/JM-Brun/llm-lab/pull/1076))
- Date du diagnostic initial : 13 novembre 2026

## 1. Objectif éditorial

Le parcours doit satisfaire deux publics sans se scinder artificiellement en un cours débutant et une annexe experte :

1. **Lecteur débutant ou en révision** : comprendre le concept, son utilité, son mécanisme et ses prérequis sans être bloqué par des détails prématurés.
2. **Lecteur expérimenté** : trouver sur chaque page au moins un apport intellectuel concret — distinction subtile, hypothèse, compromis, limite, résultat empirique, perspective historique ou lien systémique — qui dépasse la reformulation d'un cours standard.

L'ambition est de compiler et synthétiser les meilleures idées pédagogiques et techniques disponibles, en construisant une progression propre à LLM Lab. Il ne s'agit ni de copier une ressource de référence, ni d'ajouter mécaniquement un encart « pour experts » à chaque page.

## 2. Périmètre et niveau de confiance

Le diagnostic préliminaire a porté sur les 18 pages principales inventoriées ci-dessous, avec une lecture de structures et de contenus, une comparaison structurelle de dix couples français/anglais et un premier benchmark de ressources externes.

**Ce qui est établi à ce stade :**
- le périmètre de 18 pages est identifié ;
- la progression générale et plusieurs distinctions conceptuelles structurantes sont repérées ;
- des zones prioritaires d'enrichissement éditorial ont été identifiées ;
- dix couples FR/EN ont fait l'objet d'une comparaison structurelle.

**Ce qui n'est pas encore établi :**
- la lecture approfondie et exhaustive des 18 pages dans les deux langues ;
- la vérification systématique de l'équivalence pédagogique et scientifique FR/EN ;
- le contrôle visuel de chaque page dans le navigateur ;
- la validation de chaque proposition sur le contenu et les exemples effectivement affichés.

Les classements ci-dessous sont donc des **priorités provisoires**, et non des verdicts définitifs sur l'exactitude ou la qualité de chaque page.

## 3. Inventaire du parcours

Les 18 pages recensées :

1. `llm-overview`
2. `generation`
3. `text-data`
4. `embedding-space`
5. `positional-encoding`
6. `contextualized-representations`
7. `transformer`
8. `queries-keys-values`
9. `scaled-dot-product-attention`
10. `causal-masking`
11. `logits`
12. `probabilites`
13. `entropy`
14. `vraisemblance`
15. `cross-entropy`
16. `loss`
17. `gradients`
18. `training-loop`

## 4. Diagnostic transversal

### 4.1 Fondations déjà prometteuses

Le parcours possède plusieurs choix pédagogiques solides à préserver :

- il distingue l'architecture, l'apprentissage et l'inférence ;
- il suit une progression conceptuelle globalement cohérente ;
- il distingue les représentations initiales des représentations contextualisées ;
- il sépare génération, scoring probabiliste et apprentissage ;
- il utilise des pages d'approfondissement pour accueillir certaines dérivations et certains détails ;
- il cherche à limiter les répétitions entre pages.

Le principal enjeu n'est donc pas d'augmenter uniformément la longueur du parcours. Il est de faire en sorte que chaque page apporte une idée qui mérite d'être retenue, y compris par un lecteur qui connaît déjà les grandes lignes des Transformers.

### 4.2 Relations à rendre plus explicites

Le parcours gagnerait à mieux montrer les liens entre les notions, plutôt que de les laisser comme une succession de chapitres :

- entropie prédictive ↔ incertitude de la distribution du modèle ;
- vraisemblance ↔ évaluation probabiliste ;
- cross-entropy ↔ objectif d'apprentissage ;
- gradients ↔ dynamique d'optimisation ;
- attention ↔ communication et mélange d'information entre positions ;
- tokenisation ↔ coût, couverture linguistique et longueur du contexte ;
- prefill/decode ↔ architecture des systèmes d'inférence ;
- représentations contextualisées ↔ limites de l'interprétabilité.

Ces liens doivent renforcer la progression cumulative : une notion introduite sur une page doit être réutilisée ensuite avec un sens précis.

## 5. Priorisation éditoriale provisoire

### 5.1 Priorité élevée — première vague

| Page | Apport distinctif à rechercher | Pourquoi cela compte |
|---|---|---|
| `text-data` | Conséquences concrètes de la tokenisation : fragmentation, artefacts, différences entre langues, coût en tokens et longueur de contexte. | La tokenisation n'est pas un simple prétraitement neutre ; elle affecte couverture, coût et comportement observable. |
| `logits` | Montrer que les logits sont des scores relatifs ; expliquer l'invariance de softmax à l'ajout d'une constante et, si pertinent, le rapprochement prudent avec les modèles d'énergie. | Éviter de traiter les logits comme des probabilités ou des mesures absolues de confiance. |
| `positional-encoding` | Discuter les symétries, l'invariance au déplacement selon les mécanismes, et les limites de généralisation lorsque la longueur de contexte augmente. | Relier le choix d'encodage aux capacités et limites réelles du modèle. |
| `scaled-dot-product-attention` | Présenter l'attention comme un mécanisme de sélection/routage et de mélange d'information ; expliquer pourquoi les poids d'attention ne constituent pas automatiquement une explication du raisonnement. | Faire comprendre à la fois le mécanisme utile et les limites d'interprétation de ses visualisations. |
| `vraisemblance` | Relier vraisemblance, log-vraisemblance et perplexité ; expliquer la dépendance à la tokenisation et les précautions nécessaires pour comparer des modèles. | Éviter les comparaisons naïves de scores et donner un sens opérationnel à l'évaluation probabiliste. |
| `training-loop` | Donner une intuition de la dynamique d'optimisation et de la généralisation ; relier données, paramètres, calcul et compromis d'entraînement. | Faire passer le lecteur de la boucle algorithmique à la compréhension de l'entraînement comme système. |

Pour chaque page de cette vague : établir d'abord ce qui est déjà expliqué, identifier le manque réel, sélectionner des sources fiables, proposer un apport qui soit propre à LLM Lab, puis modifier les versions FR et EN et valider les deux.

### 5.2 Priorité intermédiaire — deuxième vague

| Page | Apport distinctif à rechercher |
|---|---|
| `llm-overview` | Replacer le LLM comme système probabiliste et distinguer prédiction linguistique, compétence comportementale et compréhension du monde, sans réduire abusivement l'une à l'autre. |
| `generation` | Expliquer KV cache, latence, débit, coût marginal d'un token et compromis entre stratégies de décodage. |
| `contextualized-representations` | Montrer comment les représentations évoluent selon les couches et pourquoi leur interprétation est difficile. |
| `transformer` | Expliquer le flux résiduel comme espace de communication ; préciser la complémentarité entre attention et MLP. |
| `queries-keys-values` | Déconstruire les analogies anthropomorphiques et expliquer que les têtes apprennent des sous-espaces et transformations spécialisés. |
| `causal-masking` | Distinguer causalité computationnelle (contrainte d'accès à l'information future) et compréhension de la causalité dans le monde. |

### 5.3 Pages dont les fondations semblent déjà intéressantes

Ces pages paraissent contenir des distinctions utiles à préserver et à vérifier, plutôt que de les enrichir par principe :

- `embedding-space` : distinction entre adresse d'une ligne, vecteur et représentation contextualisée ;
- `probabilites` : température, calibration et distinction entre probabilité et vérité ;
- `entropy` : dispersion prédictive et surprise d'un événement observé ;
- `cross-entropy` : distribution cible, probabilité attribuée à l'observation et pénalité ;
- `loss` : conventions de masquage et de réduction ;
- `gradients` : sensibilité locale, rétropropagation et mise à jour des paramètres.

Cette appréciation est provisoire : une page « déjà intéressante » peut encore avoir des imprécisions, des lacunes de progression ou une version linguistique moins aboutie.

## 6. Références de benchmark et rôle de chaque ressource

Ces ressources sont complémentaires. Elles servent de références pour comparer des approches pédagogiques et des niveaux de profondeur, pas de modèles à reproduire.

1. **3Blue1Brown — Attention in Transformers, step by step**  
   https://www.3blue1brown.com/lessons/attention/  
   Apport à étudier : visualisation du mécanisme et de l'enchaînement des opérations. Utile pour vérifier qu'une explication donne une intuition dynamique, pas seulement une formule.

2. **Jay Alammar — The Illustrated Transformer**  
   https://jalammar.github.io/illustrated-transformer/  
   Apport à étudier : suivi visuel des représentations et des tenseurs à travers le réseau. Utile pour rendre concret le devenir des données à chaque étape.

3. **Stanford CS336 — Language Modeling from Scratch**  
   https://cs336.stanford.edu/  
   Apport à étudier : vision systémique couvrant données, tokenisation, architecture, entraînement, systèmes, efficacité, évaluation et alignement. C'est un cours avancé : il constitue une référence de profondeur et de couverture, pas le niveau de prérequis à imposer au parcours principal.

4. **DeepLearning.AI — How Transformer LLMs Work**  
   https://www.deeplearning.ai/courses/how-transformer-llms-work  
   Apport à étudier : progression accessible et articulation entre tokenisation et composants Transformer.

**Synthèse recherchée pour LLM Lab :** combiner la force visuelle de 3Blue1Brown, le suivi des représentations de Jay Alammar, la perspective système de Stanford CS336 et la progression accessible de DeepLearning.AI. La valeur propre de LLM Lab doit venir de leur articulation, de la précision des distinctions et d'expériences contrôlées qui permettent au lecteur de vérifier ses intuitions.

## 7. Grille d'examen applicable à chaque page

Quatre dimensions éditoriales à intégrer naturellement — sans en faire obligatoirement quatre sections fixes :

- **A — Mécanisme :** le lecteur peut-il expliquer ce qui se passe, dans quel ordre et sur quelles données ?
- **B — Motivation :** comprend-il pourquoi ce mécanisme ou ce choix de conception existe, et quel problème il résout ?
- **C — Recul critique :** connaît-il les hypothèses, limites, compromis et idées reçues importantes ?
- **D — Système :** sait-il relier cette notion à l'entraînement, à l'inférence, aux capacités du modèle ou aux autres composants ?

Deux tests doivent être appliqués :
- **Test débutant :** après lecture, une personne motivée mais novice peut-elle reformuler l'idée et suivre un exemple sans dépendre d'un savoir non introduit ?
- **Test expérimenté :** une personne connaissant déjà les bases repart-elle avec au moins une distinction, un résultat, une limite ou un lien qu'elle n'aurait pas obtenu d'une explication conventionnelle ?

La profondeur doit être progressive : intuition, mécanisme, formalisation, implications et limites. Les détails avancés ne doivent pas casser le fil principal.

## 8. Plan de travail

### Vague 1 — six pages prioritaires

Ordre de travail initial : `text-data`, `logits`, `positional-encoding`, `scaled-dot-product-attention`, `vraisemblance`, `training-loop`.

Pour chaque page :
1. lire la page française et sa version anglaise en entier ;
2. examiner les pages liées et les prérequis pour éviter les doublons et les ruptures ;
3. comparer avec les références pertinentes et, si nécessaire, consulter des sources primaires ;
4. consigner le diagnostic : points forts, lacunes, risques de confusion ;
5. formuler l'apport distinctif et son emplacement dans la progression ;
6. modifier les deux langues en conservant une équivalence de fond ;
7. vérifier liens, formules, exemples, navigation et rendu ;
8. mettre à jour la fiche de valeur de la page et le présent document.

### Vague 2 — enrichir sans dégrader

Reprendre les pages de priorité intermédiaire et les pages déjà solides. Le critère n'est pas « ajouter du contenu », mais « ajouter une valeur démontrable sans répéter une autre page ni alourdir inutilement l'explication ».

### Vague 3 — audit cumulatif du parcours

Relire les 18 pages comme une expérience unique :
- vérifier les prérequis et les transitions ;
- vérifier que les notions sont réutilisées correctement ;
- supprimer les répétitions et combler les trous ;
- vérifier que les frontières conceptuelles restent nettes ;
- vérifier la cohérence FR/EN ;
- tester la progression depuis les intuitions initiales jusqu'à la compréhension systémique.

## 9. Conditions de validation

Un enrichissement ne doit être considéré comme terminé que si :

- il résout une lacune identifiée, et non un besoin abstrait de longueur ;
- il est scientifiquement exact et correctement nuancé ;
- il aide le débutant sans infantiliser le lecteur expérimenté ;
- il apporte une valeur identifiable à un lecteur déjà familier du sujet ;
- il est placé sur la bonne page et ne crée pas de doublon ;
- il renforce les liens avec le reste du parcours ;
- les versions française et anglaise sont cohérentes ;
- les exemples, équations, liens et renvois sont vérifiés ;
- le rendu est contrôlé lorsque les moyens le permettent ;
- les limites de vérification restantes sont déclarées explicitement.

## 10. Décision éditoriale

Le chantier doit commencer par les six pages de la vague 1. Le diagnostic actuel fournit une carte de priorisation, pas une autorisation à réécrire sans examen. Chaque modification doit être justifiée par une lacune vérifiée, documentée par des sources, et évaluée selon le double public du parcours.

Le principe directeur est simple : **chaque page doit être une porte d'entrée pour le novice et une occasion de réflexion pour le lecteur expérimenté.**
