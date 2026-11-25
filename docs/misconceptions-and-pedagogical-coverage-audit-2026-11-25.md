# Audit des idées reçues sur les LLMs et plan de couverture pédagogique

**Date :** 2026-11-25  
**Statut :** audit initial documenté ; couverture détaillée à vérifier ; registre canonique à construire.  
**Périmètre :** idées reçues techniques, conceptuelles et sociotechniques sur les LLMs et les systèmes qui les utilisent.

## 1. Objectif et décision éditoriale

LLM Lab doit apprendre non seulement à décrire les composants d'un LLM, mais aussi à raisonner correctement sur son fonctionnement, ses capacités, ses limites et son déploiement.

Pour chaque affirmation trompeuse, le projet doit isoler le noyau de vérité, identifier la distinction confondue, expliquer le mécanisme correct et vérifier que l'apprenant sait le reconstruire et le mettre à l'épreuve.

**Une page qui mentionne une correction ne prouve pas que l'idée reçue est pédagogiquement traitée.** La couverture doit être démontrée par des explications, des exercices ou des expériences, et non déduite d'un titre ou d'un mot-clé.

Le résultat attendu n'est pas une nouvelle collection de pages autonomes. C'est une couche éditoriale et de traçabilité reliée aux registres existants. Les pages principales enseignent ; les pages dédiées de « S'exercer et expérimenter » accueillent les exercices qui croissent dans le temps ; un index transversal oriente sans recopier les cours.

## 2. Cadre conceptuel et sources

### 2.1 Colonne vertébrale computationnelle

La [colonne vertébrale computationnelle canonique](canonical-computational-spine.md) décrit un mécanisme prédictif partagé :

$$
z_t = f_\theta(x_{<t}), \qquad
p_\theta(\cdot \mid x_{<t}) = \operatorname{softmax}(z_t).
$$

Cette distribution conditionnelle alimente plusieurs usages distincts :

- **Génération :** décodage, sélection/échantillonnage, ajout du token au contexte ; paramètres fixes.
- **Scoring :** probabilité attribuée à une cible observée.
- **Évaluation :** scoring sur des exemples tenus à l'écart, sans mise à jour.
- **Apprentissage :** agrégation des pénalités, différentiation et mise à jour des paramètres.

Ce cadre prévient les confusions génération/scoring, inférence/apprentissage, distribution/échantillon et contexte observé/token généré. Il impose aussi de distinguer texte/tokenisation, IDs/embeddings initiaux, calculs internes des blocs Transformer, états contextualisés, logits et distribution. Q/K/V sont calculés dans chaque bloc à partir de ses états d'entrée, et non après les représentations contextualisées finales.

### 2.2 Source de recherche structurante

Zhicheng Lin, *Six misconceptions about large language models: A minimal model and diagnostic taxonomy*, PNAS Nexus, 8 juillet 2026 :
- [Article éditeur](https://academic.oup.com/pnasnexus/article/5/7/pgag236/8728241)
- [Texte intégral PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13378163/)
- [DOI](https://doi.org/10.1093/pnasnexus/pgag236)

L'article propose quatre distinctions : objectif de pré-entraînement / système déployé ; distribution apprise / échantillon généré ; mémoire paramétrique / contextuelle / externe ; compétence / agentivité. Il analyse six idées reçues : « simple prédicteur/perroquet » ; « moyenne d'Internet » ; régurgitation des données ; mémoire totale ou nulle ; fine-tuning/RLHF comme filtre superficiel ; compréhension humaine ou absence totale de compréhension.

Cette taxonomie constitue une source de diagnostic, pas une taxonomie exhaustive ni un consensus universel. Elle est complétée ci-dessous par les erreurs techniques liées aux tokens, représentations, attention, probabilités, optimisation, évaluation et systèmes. Chaque slogan peut contenir un noyau de vérité ; l'erreur vient de sa généralisation abusive.

## 3. Taxonomie initiale des idées reçues

Les IDs ci-dessous sont des identifiants de travail pour l'audit, pas encore les IDs persistants du futur registre. Les formulations sont des affirmations à diagnostiquer, non des citations attribuées à une population mesurée.

### A. Nature du modèle et niveau de description

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| A01 | « Un LLM n'est qu'un autocomplete. » | L'objectif de prédiction ne décrit pas à lui seul représentations, compétences mesurées et système déployé. |
| A02 | « Il prédit le prochain mot. » | Il prédit un token ; un token n'est pas nécessairement un mot. |
| A03 | « La prédiction du prochain token explique tout son comportement. » | Distinguer objectif, paramètres, contexte, décodage, post-entraînement et orchestration. |
| A04 | « Tous les LLM sont des GPT/Transformers causaux. » | Architectures, objectifs, modalités et masques diffèrent. |
| A05 | « Le modèle et l'assistant sont la même chose. » | Le produit peut ajouter instructions, templates, filtres, outils, récupération, mémoire et orchestration. |
| A06 | « Le modèle génère toute sa réponse en une opération. » | La génération autorégressive produit une suite de tokens conditionnels. |

### B. Texte, tokenisation et représentations

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| B01 | « Un token est un mot. » | Les unités dépendent du tokenizer : mots, sous-mots, octets ou autres segments. |
| B02 | « Le tokenizer comprend la morphologie. » | Segmentation et encodage ne garantissent pas une analyse linguistique. |
| B03 | « Les IDs ont une distance sémantique. » | Les IDs sont des indices catégoriels ; leur ordre numérique ne définit pas une proximité. |
| B04 | « Deux IDs proches ont des embeddings proches. » | La proximité dépend des vecteurs appris, pas des indices. |
| B05 | « Un embedding est une définition du mot. » | C'est un vecteur appris, pas une définition lexicale. |
| B06 | « Un token a toujours une seule représentation. » | Le lookup initial est lié à l'ID ; les états ultérieurs dépendent de position, contexte et couches. |
| B07 | « L'embedding initial est déjà contextualisé. » | Distinguer lookup, information positionnelle et états contextualisés. |
| B08 | « Chaque dimension correspond à un concept humain. » | Les coordonnées sont distribuées ; leur interprétation individuelle n'est généralement pas directe. |
| B09 | « Les embeddings sont universels et comparables entre modèles. » | Espaces, dimensions, tokenizer et paramètres diffèrent ; toute comparaison exige un protocole. |

### C. Transformer et attention

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| C01 | « L'attention est une mémoire qui stocke les mots importants. » | Elle calcule des interactions dépendantes du contexte et agrège des valeurs. |
| C02 | « Q, K et V sont trois types de tokens. » | Ce sont des projections apprises des états d'entrée d'un bloc. |
| C03 | « Q cherche, K contient le sens et V mesure l'importance. » | Q/K déterminent les scores de compatibilité ; V porte le contenu agrégé. |
| C04 | « Q/K/V arrivent après les représentations contextualisées finales. » | Ils sont calculés dans chaque bloc et contribuent à produire les états suivants. |
| C05 | « Tous les tokens peuvent toujours se regarder. » | Les masques et l'architecture déterminent les positions accessibles. |
| C06 | « Le masque causal empêche toute fuite future. » | Il contraint l'accès aux positions futures dans l'attention concernée ; il ne remplace pas l'hygiène des données et protocoles. |
| C07 | « Un poids d'attention élevé explique causalement une sortie. » | Les poids sont un élément du calcul, pas une explication causale complète. |
| C08 | « Chaque tête a une fonction sémantique humaine distincte. » | Les têtes sont des sous-calculs appris ; leur interprétation exige des expériences. |
| C09 | « Le MLP est accessoire à l'attention. » | Le sous-réseau feed-forward applique des transformations non linéaires essentielles. |
| C10 | « Tous les Transformers ont le même ordre résiduel/normalisation. » | Pre-LN, Post-LN et autres variantes existent. |

### D. Probabilités, génération et décodage

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| D01 | « La probabilité du token mesure la probabilité que l'affirmation soit vraie. » | Probabilité conditionnelle sur des tokens, pas probabilité de vérité factuelle. |
| D02 | « Le modèle choisit toujours le token le plus probable. » | C'est le décodage glouton ; sampling et autres politiques existent. |
| D03 | « Le token localement le plus probable donne la meilleure séquence. » | Une décision locale ne garantit pas un optimum global. |
| D04 | « La température modifie les paramètres ou connaissances. » | Elle transforme la distribution utilisée pour sélectionner les tokens ; elle ne met pas à jour les poids. |
| D05 | « Une température élevée rend le modèle plus intelligent/créatif. » | Elle modifie concentration et diversité des échantillons, pas les capacités acquises. |
| D06 | « Top-k et top-p sont équivalents. » | Top-k conserve un nombre fixe de candidats ; top-p un ensemble défini par masse cumulée. |
| D07 | « Une génération déterministe n'utilise pas de distribution. » | Une distribution peut être calculée puis exploitée par une règle déterministe. |
| D08 | « Prefill et decode sont deux modèles distincts. » | Ce sont des phases d'exécution d'une même inférence. |
| D09 | « Le KV cache ajoute des connaissances. » | Il réutilise des états K/V déjà calculés pour éviter du travail redondant. |
| D10 | « Le modèle sait toujours quand arrêter. » | L'arrêt dépend de tokens de fin, limites, orchestration et paramètres. |

### E. Entraînement, objectifs et optimisation

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| E01 | « Le modèle apprend de chaque conversation par défaut. » | L'inférence standard ne met pas à jour les paramètres ; le produit peut conserver données ou mémoire externe. |
| E02 | « Générer et apprendre sont la même opération. » | Le forward produit des prédictions dans les deux cas ; l'apprentissage ajoute cible, loss, rétropropagation et mise à jour. |
| E03 | « Teacher forcing consiste à donner la bonne réponse au modèle. » | Les tokens précédents observés conditionnent les prédictions ; les cibles suivantes servent à calculer la loss. |
| E04 | « La loss est la probabilité que le modèle ait raison. » | Objectif numérique calculé depuis prédictions et cibles, avec masque et réduction. |
| E05 | « Une loss faible garantit intelligence ou vérité. » | Elle mesure l'ajustement à un objectif et une distribution, pas toutes les compétences ni la factualité. |
| E06 | « La perplexité est un score universel d'intelligence. » | Elle dépend du corpus, tokenizer et calcul ; elle ne résume pas toutes les tâches. |
| E07 | « Le gradient indique directement la meilleure réponse. » | Il décrit la dérivée locale de l'objectif par rapport aux paramètres. |
| E08 | « Gradient et optimiseur sont la même chose. » | Le gradient fournit une information différentielle ; l'optimiseur définit la mise à jour. |
| E09 | « L'évaluation met à jour le modèle comme l'entraînement. » | L'évaluation mesure sans mise à jour, sur des données et un protocole définis. |
| E10 | « Le fine-tuning ajoute simplement des faits. » | Il modifie les paramètres et peut changer plusieurs comportements et compromis. |
| E11 | « RLHF apprend la vérité. » | Le signal de préférence/récompense est un substitut appris, dépendant des objectifs et données. |
| E12 | « Le post-entraînement est un filtre externe amovible. » | SFT et méthodes de préférence peuvent modifier les poids ; filtres externes et adaptation sont distincts. |

### F. Contexte, mémoire et récupération

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| F01 | « Le modèle se souvient de toutes les conversations. » | Distinguer mémoire paramétrique, contexte actif et stockage externe du produit. |
| F02 | « Le modèle ne possède aucune mémoire. » | Les poids encodent des régularités ; le contexte sert de mémoire de travail ; un système peut ajouter un stockage externe. |
| F03 | « Une grande fenêtre garantit la compréhension de tout son contenu. » | Capacité, récupération et exploitation effective sont distinctes. |
| F04 | « L'in-context learning est du fine-tuning. » | Le comportement peut s'adapter au contexte sans mise à jour des paramètres. |
| F05 | « Le RAG apprend les documents au modèle. » | Il récupère et transmet des informations au contexte ; cela ne modifie pas automatiquement les paramètres. |
| F06 | « Une information dans une base vectorielle est connue du modèle. » | Elle doit être retrouvée, sélectionnée, transmise puis exploitée. |
| F07 | « Un document dans le prompt sera correctement utilisé. » | Sa présence ne garantit ni interprétation ni fidélité. |
| F08 | « Le KV cache est une mémoire persistante de conversation. » | C'est un cache de calcul associé à l'exécution, pas une mémoire applicative durable. |
| F09 | « Toute information hors contexte est définitivement oubliée. » | Elle peut exister dans les paramètres ou un système externe ; elle n'influence pas directement l'appel sans transmission/récupération. |

### G. Hallucinations, factualité et fiabilité

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| G01 | « Le modèle sait toujours quand il ne sait pas. » | L'incertitude exprimée et la confiance peuvent être mal calibrées. |
| G02 | « Une réponse fluide et assurée est probablement vraie. » | La qualité rhétorique n'est pas une preuve factuelle. |
| G03 | « Une hallucination est une erreur aléatoire. » | Les erreurs peuvent être systématiques et liées aux données, contexte, objectif ou système. |
| G04 | « Un bon entraînement élimine les hallucinations. » | L'objectif prédictif ne garantit pas la vérité des affirmations. |
| G05 | « Donner des sources élimine les hallucinations. » | Sources erronées, récupération, transmission, interprétation et contradictions peuvent provoquer des échecs. |
| G06 | « Le RAG garantit la factualité. » | Chaque étape récupération-sélection-transmission-exploitation-vérification peut échouer. |
| G07 | « Une bonne perplexité garantit la factualité. » | Modélisation de tokens et véracité factuelle sont distinctes. |
| G08 | « Un benchmark élevé garantit la fiabilité en production. » | Distribution, population, workflow, outils et conditions peuvent différer. |
| G09 | « Le modèle peut vérifier seul toutes ses affirmations. » | L'auto-critique peut échouer ; les affirmations importantes exigent des preuves et vérifications. |
| G10 | « Une citation produite prouve que la source existe et soutient l'affirmation. » | Existence, identité et soutien effectif doivent être vérifiés. |

### H. Compétence, généralisation et anthropomorphisme

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| H01 | « Le modèle comprend exactement comme un humain. » | Une compétence fonctionnelle n'établit pas une compréhension expérientielle ou humaine. |
| H02 | « Le modèle ne comprend absolument rien puisqu'il prédit des tokens. » | L'objectif ne suffit pas à caractériser les compétences ; celles-ci doivent être testées. |
| H03 | « Le modèle raisonne nécessairement comme nous. » | Distinguer performance et mécanismes cognitifs humains. |
| H04 | « Le modèle possède des croyances et intentions stables parce qu'il parle à la première personne. » | Le style conversationnel ne démontre pas des états mentaux ou une agentivité. |
| H05 | « Toute réussite vient de la mémorisation. » | Évaluer la généralisation sur des cas nouveaux et contrôler la contamination. |
| H06 | « Toute capacité émergente apparaît brutalement à un seuil de taille. » | L'apparence dépend des métriques, seuils, tâches et protocoles. |
| H07 | « Plus le modèle est grand, meilleur il est partout. » | Les gains dépendent des données, objectifs, architecture, budget et domaine. |
| H08 | « Une conversation convaincante démontre conscience ou expérience subjective. » | Ces affirmations ne se déduisent pas de la seule fluidité ou performance. |

### I. Outils, multimodalité et déploiement

| ID | Affirmation trompeuse | Correction / distinction |
|---|---|---|
| I01 | « Le modèle effectue lui-même une recherche web ou une requête API. » | L'action peut être orchestrée par le système ; l'outil exécute puis son résultat est transmis. |
| I02 | « Les outils font partie des paramètres du modèle. » | Les outils sont généralement externes ; le modèle peut apprendre à les invoquer. |
| I03 | « Un LLM calcule exactement ou exécute du code par lui-même. » | Distinguer génération de code, exécution par outil et vérification. |
| I04 | « Tous les modèles multimodaux convertissent simplement les entrées en texte. » | Les modalités peuvent utiliser encodeurs, représentations et chemins spécifiques. |
| I05 | « Open weights signifie open source. » | La disponibilité des poids ne garantit ni code, données, recette, droits ou reproductibilité. |
| I06 | « Le comportement dépend uniquement du modèle. » | Prompt, template, décodage, mémoire, récupération, outils, filtres et orchestration comptent. |
| I07 | « Un agent est un LLM qui répond plus longtemps. » | Un système agentique ajoute boucle de contrôle, actions, observations, état et politiques d'arrêt. |
| I08 | « Un benchmark suffit à comparer tous les systèmes. » | Contrôler versions, prompts, outils, budgets, données, métriques et conditions. |

Cette liste est un inventaire de travail raisonné, non une mesure statistique de fréquence. La granularité sera consolidée lors de l'ingestion des sources et du pilote. Fusionner les doublons uniquement si mécanisme, correction et preuve pédagogique coïncident.

## 4. Audit initial de couverture

### Méthode et limite

Un examen ciblé du dépôt a consulté les pages françaises : panorama, texte et tokens, stratégies de tokenisation, embeddings, représentations contextualisées, QKV, génération, décodage, vraisemblance, entropie croisée, loss, boucle d'entraînement, post-entraînement, limites des LLMs, RAG/mémoire, ingénierie du contexte, apprentissage en contexte, évaluation expérimentale et architectures Transformer.

Cet examen est un **audit structurel ciblé**, pas une revue exhaustive de toutes les pages FR/EN, ancres, exercices ou rendus publiés. Les appréciations sont provisoires.

| Famille | Ressources identifiées | Appréciation provisoire | Vérification / amélioration |
|---|---|---|---|
| A. Nature et fonctionnement | llm-overview, generation, transformer-architectures, llm-limits | Bonne base | Distinguer modèle, système, objectif et compétence. |
| B. Tokens et représentations | text-data, tokenization-strategies, embedding-space, contextualized-representations | Base forte | Vérifier transfert, dimensions et comparaisons inter-modèles. |
| C. Transformer et attention | transformer, queries-keys-values, scaled-dot-product-attention, causal-masking, transformer-architectures | Bonne base | Auditer interprétabilité, causalité, variantes et effets Q/K/V. |
| D. Probabilités et génération | generation, decoding-strategies, probabilites, logits, vraisemblance | Bonne base | Vérifier comparaisons à paramètres et prompt fixes. |
| E. Entraînement | vraisemblance, cross-entropy, loss, gradients, training-loop, post-training | Base forte | Vérifier teacher forcing, masques et séparation scoring/évaluation/training. |
| F. Mémoire et contexte | in-context-learning, context-engineering, rag-memory-boundaries, generation | Bonne base | Vérifier mémoire paramétrique/contextuelle/externe et KV cache. |
| G. Hallucinations et factualité | llm-limits, evaluation-experimentale, rag-memory-boundaries | Partielle à consolider | Diagnostic par étapes et vérification des affirmations/sources. |
| H. Compétence et agentivité | llm-limits, emergence, scaling-laws, evaluation-experimentale | Partielle à consolider | Critères opérationnels et protocoles de généralisation. |
| I. Outils et déploiement | llm-overview, post-training, context-engineering, multimodal-architectures, document-retrieval | Partielle / à auditer | Frontière modèle/application, outils et boucles agentiques. |

Pages examinées au niveau structure/contenu ciblé :
- site/fr/llm-overview.qmd : objectif prédictif, distribution, usages, architecture/apprentissage/utilisation, localisation de l'information et système conversationnel.
- site/fr/text-data.qmd et tokenization-strategies.qmd : texte, tokens/IDs et segmentation.
- site/fr/embedding-space.qmd et contextualized-representations.qmd : lookup initial et états dépendants du contexte.
- site/fr/queries-keys-values.qmd : rôles Q/K/V.
- site/fr/generation.qmd et decoding-strategies.qmd : boucle autorégressive, prefill/decode, cache et sélection.
- site/fr/vraisemblance.qmd, cross-entropy.qmd, loss.qmd et training-loop.qmd : scoring, pénalité, agrégation, gradients et optimisation.
- site/fr/post-training.qmd : SFT, méthodes à préférences, paramètres et contexte.
- site/fr/llm-limits.qmd : garanties de l'objectif, hallucinations, calibration, compréhension et émergence.
- site/fr/rag-memory-boundaries.qmd, context-engineering.qmd et in-context-learning.qmd : stockage, récupération, transmission, exploitation et adaptation contextuelle.
- site/fr/evaluation-experimentale.qmd : protocole, calibration, robustesse et analyse des erreurs.
- site/fr/transformer-architectures.qmd : diversité des architectures.

L'existence de ressources pertinentes n'établit pas la couverture complète de chaque item. Les correspondances item/page/ancres doivent être établies et revues en français et en anglais.

### Échelle de couverture à adopter

| Niveau | Signification | Preuve minimale |
|---|---|---|
| 0 — Absent | Aucun traitement pertinent | Recherche documentée et pages candidates examinées |
| 1 — Mentionné | Affirmation/correction nommée sans reconstruction | Ancre exacte et constat du manque |
| 2 — Expliqué | Distinction et mécanisme expliqués avec limites | Ancres exactes et revue de l'objectif d'apprentissage |
| 3 — Vérifiable | Une activité évalue raisonnement ou transfert | Activité, consigne, critères et corrigé/feedback |
| Non audité | Éléments insuffisants | Motif et périmètre restant |

Un quiz de reconnaissance ne suffit pas pour une idée reçue qui nécessite une reconstruction causale ou mathématique.

## 5. Lacunes transversales identifiées

1. **Corrections dispersées :** le lecteur doit parfois reconstruire seul les liens entre plusieurs pages. Un index doit pointer vers les explications canoniques sans les dupliquer.
2. **Mentions sans objectifs d'apprentissage :** nommer l'hallucination ne suffit pas à apprendre à la diagnostiquer. Chaque entrée doit viser un résultat observable.
3. **Diagnostic des hallucinations :** distinguer information absente des paramètres/contexte ; information paramétrique non rappelée ; information externe absente ; échec de récupération ; mauvais classement ; source non transmise ; source mal interprétée ; extrapolation ; vérification insuffisante. Ces causes ne sont pas exclusives et ne permettent pas d'inférer avec certitude la provenance interne d'une sortie.
4. **Frontière modèle/système :** le comportement dépend aussi des templates, prompts, décodage, outils, mémoire externe, récupération, filtres et orchestration. Un schéma système doit compléter le graphe du modèle sans les confondre.
5. **Affirmations cognitives :** « comprend », « raisonne », « apprend », « se souvient », « crée » et « sait » doivent être reliés à une tâche, une population, un protocole, une métrique et une limite d'interprétation.

## 6. Registre canonique à construire

Créer data/misconceptions.yml comme source structurée, reliée aux registres existants et non comme ontologie parallèle.

Champs à piloter :
- id : identifiant stable, indépendant de la langue ;
- claim : formulation FR/EN ;
- kernel_truth : part de vérité qui rend l'affirmation plausible ;
- correction : formulation nuancée ;
- conflated_distinctions : distinctions confondues ;
- concepts : IDs vérifiés de data/concepts.yml ;
- domains : domaines de data/domains.yml ;
- resources : pages et ancres FR/EN ;
- activities : exercices existants ou à créer, avec rôle ;
- experiments : protocoles associés ;
- severity : priorité pédagogique argumentée, pas une fréquence ;
- coverage : niveau 0–3 ou not_audited, avec preuve ;
- sources : références ;
- status : proposed, audited, integrated, validated ou retired.

Le schéma exact sera défini après un pilote. Les sources de vérité restent :
- data/concepts.yml pour les concepts ;
- data/domains.yml pour les domaines ;
- data/resources.yml pour les ressources non-page ;
- data/computational-graph.yml pour calculs et flux ;
- data/guided-route.yml pour la progression ;
- pages Quarto pour les explications ;
- pages d'exercices dédiées pour l'évaluation formative ;
- data/misconceptions.yml pour les relations et l'état d'audit.

Ne pas convertir automatiquement une relation computationnelle en prérequis pédagogique. Ne pas utiliser un lien related générique comme preuve de couverture.

## 7. Modèle pédagogique

Chaque activité doit aider à :
1. Reconnaître l'affirmation et ses conditions implicites.
2. Nuancer le noyau de vérité et la généralisation abusive.
3. Diagnostiquer la distinction confondue.
4. Reconstruire le calcul, flux d'information ou protocole.
5. Prédire l'effet d'une modification.
6. Tester par calcul, code, visualisation ou observation.
7. Transférer à une autre architecture ou configuration.

Une correction n'est pas seulement une réponse vrai/faux. Elle explique pourquoi l'erreur est séduisante, quelles hypothèses elle cache et dans quelles limites une formulation voisine reste valable.

## 8. Expériences pilotes proposées

Ces expériences ne sont pas considérées comme réalisées. Elles doivent suivre [le protocole expérimental](experiment-protocol.md).

### EXP-01 — Distribution, décodage et échantillon
Question : à paramètres et contexte identiques, comment changent distribution et sorties lorsque température, top-k ou top-p changent ? Baseline : logits fixés et greedy. Variantes : températures, sampling, top-k, top-p. Mesures : distribution transformée, diversité, fréquences empiriques, reproductibilité. Contrôles : mêmes logits/prompts, graines et versions. Cibles : A03, D02–D07.

### EXP-02 — Décomposition Q/K/V
Question : que change une modification indépendante de Q, K ou V lorsque les autres projections et le masque sont fixes ? Baseline : petite séquence et matrices explicites. Mesures : scores, poids, agrégation, sortie. Contrôles : dimensions et entrées fixes. Cibles : C01–C08.

### EXP-03 — IDs, lookup et contextualisation
Question : que conserve ou modifie le passage ID → embedding initial → états contextualisés ? Variantes : IDs voisins/non voisins, même token dans deux contextes, positions différentes. Mesures : IDs, égalité du lookup, états cachés. Cibles : B03–B09.

### EXP-04 — Teacher forcing, scoring et génération
Question : quelles entrées et cibles interviennent dans scoring, teacher forcing et génération ? Baseline : séquence courte avec logits inspectables. Variantes : préfixe observé vs token généré, décalage des cibles et masques. Mesures : contexte, cible, log-probabilité, loss et token réinjecté. Cibles : E01–E04, D02, F04.

### EXP-05 — Chaîne de récupération et exploitation
Question : à quel stade une information externe devient-elle disponible puis exploitable ? Variantes : stockée/non indexée ; indexée/non récupérée ; récupérée/non transmise ; transmise ; transmise avec conflit/bruit. Mesures : rappel/précision, présence dans contexte, fidélité et citations vérifiées. Cibles : F05–F07, G05–G06.

### EXP-06 — Fluidité, confiance et exactitude
Question : confiance exprimée, fluidité et justesse varient-elles ensemble sur des questions vérifiables ? Variantes : sources présentes/absentes, paraphrases, ambiguïtés, contradictions. Mesures : exactitude, abstention, calibration si probabilité interprétable, fidélité aux preuves. Cibles : G01–G10.

Privilégier des modèles jouets ou petits modèles locaux lorsque cela suffit. Ne pas dépendre d'un service distant coûteux pour démontrer un mécanisme déterministe.

## 9. Travail restant et critères de sortie

### P0 — Piloter le modèle et établir une couverture fiable
1. Piloter le schéma sur six idées reçues : A01, D04, E01, F05, G06 et H01.
2. Examiner pour chacune pages FR/EN, ancres précises, exercices et preuves.
3. Vérifier IDs de concepts, domaines et ressources.
4. Définir les relations permises entre idées reçues, concepts, pages, ancres, exercices et expériences.
5. Créer data/misconceptions.yml seulement après validation du pilote.
6. Définir un validateur : IDs uniques, champs bilingues, références existantes, couverture et preuves.
7. Générer une vue de couverture depuis le registre.

**Sortie P0 :** six entrées pilotes bilingues et valides ; chaque niveau est justifié ; références cassées détectées ; aucun cours dupliqué.

### P1 — Auditer les neuf familles et fermer les lacunes
1. Auditer A à I et fusionner les doublons justifiés.
2. Vérifier exactitude, profondeur, niveau et accessibilité.
3. Prioriser modèle/système ; distribution/échantillon ; mémoire paramétrique/contextuelle/externe ; objectif/compétence ; génération/scoring/apprentissage ; récupération/transmission/exploitation.
4. Ajouter les exercices manquants dans les pages dédiées, avec corrigés et critères.
5. Vérifier parité FR/EN et liens.
6. Créer une page de cours seulement si une lacune réelle le justifie.

**Sortie P1 :** chaque idée prioritaire atteint niveau 2 ; les idées critiques choisies atteignent niveau 3 ; aucun simple related ne sert de preuve.

### P2 — Valider par expérimentation et expérience apprenant
1. Prioriser EXP-01, EXP-04 et EXP-05, puis EXP-02/03/06 selon valeur et coût.
2. Implémenter les protocoles et enregistrer versions, résultats, limites et échecs.
3. Faire relire par un novice et un lecteur technique.
4. Vérifier la capacité à expliquer et transférer, pas seulement reconnaître.

**Sortie P2 :** au moins trois expériences reproductibles ; activités testées et révisées avec retours apprenants.

### P3 — Rendre la couverture navigable et maintenable
1. Créer un index common-misconceptions FR/EN, généré depuis le registre.
2. Organiser par confusion et mécanisme, pas comme une liste de slogans.
3. Regrouper par famille, niveau, concept et couverture.
4. Ajouter des renvois discrets depuis les cours lorsque cela aide.
5. Documenter ajout, fusion, retrait et révision.
6. Intégrer les contrôles au validateur/CI existant ; aucun workflow par idée reçue.

**Sortie P3 :** index bilingue accessible et généré ; maintenance documentée ; CI signale références invalides et entrées sans preuve.

## 10. Gouvernance et maintenance

Créer une entrée si l'affirmation est importante, contient une confusion identifiable, se rattache à un mécanisme enseignable et justifie renvoi, exercice ou expérience. Fusionner si mécanisme, correction et preuve coïncident. Archiver les entrées redondantes ou obsolètes en conservant provenance et motif.

Pour chaque source externe, enregistrer titre, auteur, date, URL, type, licence connue et date de consultation. Distinguer affirmations de la source, interprétation éditoriale et décisions de conception. Ne pas présenter une taxonomie d'article comme un consensus universel.

L'article de Lin (2026) est en accès ouvert CC BY 4.0. Son intégration au catalogue doit suivre le workflow d'ingestion du projet ; conserver attribution et licence en cas de réutilisation.

Indicateurs : entrées auditées/non auditées ; niveaux de couverture par famille et langue ; entrées niveau 2/3 avec preuves ; références invalides ; écarts FR/EN ; activités sans critères ; entrées à réexaminer après modification d'une page liée. Les comptes ne mesurent pas la qualité : une revue qualitative périodique reste nécessaire.

## 11. Décisions à préserver

1. Le registre complète les registres existants ; il ne les remplace pas.
2. Le graphe computationnel décrit les calculs ; le graphe de connaissances décrit les relations conceptuelles ; le parcours décrit un ordre pédagogique.
3. Une mention n'est pas une preuve de maîtrise.
4. Les exercices restent dans les pages dédiées à la pratique.
5. Les expériences sont reproductibles, proportionnées et réutilisent les outils existants.
6. Les affirmations sur compréhension, raisonnement, mémoire et agentivité exigent critères et limites explicites.
7. Ne pas créer de pages avant l'audit des ressources canoniques.
8. Ne pas confondre absence dans le contexte actif et absence dans les paramètres ou systèmes externes.
9. Les niveaux de couverture ne sont ni scores globaux de qualité ni mesures de fréquence.

## 12. Prochaine action

Réaliser le **pilote de schéma et d'audit sur six idées reçues** (A01, D04, E01, F05, G06, H01), en examinant pages FR/EN, ancres précises, exercices et preuves pédagogiques. À l'issue du pilote seulement, figer le schéma minimal, créer le registre, puis dérouler l'audit complet. Cette séquence limite le risque d'un registre volumineux mais non maintenable.
