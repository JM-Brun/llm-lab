# Référence pédagogique transversale — le fil rouge du scribe

**Statut :** référence éditoriale interne, proposition de fil rouge  
**Langues :** français et anglais  
**Périmètre :** parcours Understand, Build, Deepen et Practice lorsqu'un exemple de bout en bout est utile  
**Dernière revue :** 2026-11-10

> Ce document est la source de vérité pour l'exemple fil rouge. Il décrit le scénario, les formulations réutilisables, les déclinaisons pédagogiques par page et les garde-fous scientifiques. Il ne remplace ni les explications canoniques des pages ni les sources de vérité du curriculum.

## 1. Intention

Utiliser comme fil rouge la scène du scribe Otis dans *Astérix et Obélix : Mission Cléopâtre* (Alain Chabat, 2002), interprété par Édouard Baer. Le **contexte fourni au modèle (prompt / préfixe)** est la question de Panoramix : « C'est une bonne situation, ça, scribe ? ». La **continuation** commence par : « Vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation... ». C'est cette inversion qui porte la démonstration : le prompt est déjà présent dans le contexte ; la boucle autoregressive produit ensuite la suite, token après token.

La scène est une accroche culturelle, pas une source scientifique. L'exemple pédagogique ci-dessous est une **adaptation originale** : ne pas recopier la tirade du film. La référence IMDb identifie le rôle d'Otis : <https://www.imdb.com/fr/title/tt0250223/characters/nm0046347/>. Une présentation de la scène et de son contexte est également disponible dans [Le Parisien](https://www.leparisien.fr/culture-loisirs/cinema/ressortie-d-asterix-et-obelix-mission-cleopatre-le-monologue-dotis-encore-plus-interminable-04-07-2023-NA6P2W7M2JE6RA5WYVXEND4B4Q.php).

### Pourquoi cet exemple fonctionne

- **Un préfixe familier et court :** la question de Panoramix est le contexte initial ; la tirade d'Otis est la continuation.
- **Une suite conditionnée mais non déterministe :** le contexte influence les tokens suivants, sans imposer une continuation unique.
- **Une structure narrative :** question, réponse, associations, digressions et conclusion.
- **Un potentiel de transformation :** la même phrase peut être examinée comme texte brut, tokens, IDs, vecteurs, états contextualisés, scores, probabilités, puis génération.
- **Un contrepoint mémorable :** un modèle ne comprend pas une tirade comme un humain ; il calcule des distributions conditionnelles sur des tokens.

## 2. Scénario canonique à réutiliser

### 2.1 Préfixe fourni au modèle

Le **prompt / contexte initial** est la question de Panoramix :

> **Préfixe :** « C'est une bonne situation, ça, scribe ? »

Ce préfixe est déjà présent dans le contexte au début de la génération. Il ne doit pas être présenté comme le texte produit par le modèle.

### 2.2 Continuation

La continuation de la scène commence par la réplique d'Otis :

> **Début de continuation :** « Vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation... »

Pour les démonstrations reproductibles, utiliser aussi une continuation pédagogique originale, indépendante du dialogue du film :

> **Continuation jouet :** « Être scribe, c'est relier des histoires. Les rencontres apportent de nouveaux récits ; le contexte aide à choisir les mots justes. Chaque phrase prépare la suivante. »

La réplique du film sert d'illustration culturelle du couple préfixe/continuation ; la continuation jouet sert aux calculs et aux tests. Ni l'une ni l'autre ne doit être présentée comme la sortie effective d'un modèle entraîné. Lorsqu'une page étudie la génération, montrer explicitement la boucle : prédire un token, l'ajouter au contexte, puis recalculer le token suivant.

### 2.3 Unités et conventions

- Le préfixe et la continuation sont encodés en UTF-8 pour les fichiers, mais le modèle reçoit des IDs de tokens produits par **un tokenizer déterminé**.
- Les IDs dépendent du tokenizer et de son vocabulaire : ne jamais publier un ID numérique comme universel.
- Les vecteurs d'embedding sont des tableaux numériques dont les dimensions dépendent de la configuration du modèle. Ne pas inventer des valeurs ou dimensions comme s'il s'agissait d'un checkpoint réel.
- Les états cachés après les blocs Transformer dépendent du contexte et des paramètres du modèle ; ils ne sont pas les embeddings initiaux.
- Les logits et probabilités sont propres à un modèle, un contexte et un pas de génération. Sans calcul effectif, employer des valeurs explicitement fictives ou des symboles.
- Le texte jouet ne démontre ni qualité linguistique ni compréhension. Le GPT de référence initialisé aléatoirement illustre les opérations, pas une génération cohérente.

## 3. Fil rouge de bout en bout

| Étape | Question pédagogique | Déclinaison de l'exemple | Ce qu'il faut faire observer |
|---|---|---|---|
| Situation initiale | Que demande-t-on au modèle ? | Panoramix fournit le préfixe initial ; la réponse d'Otis constitue la continuation à générer. | Distinguer le préfixe déjà fourni (question de Panoramix) des tokens de continuation (réponse d'Otis). |
| Texte brut | Quel est le texte fourni ? | Afficher la question de Panoramix comme préfixe, puis la réponse d'Otis comme continuation séparée. | Le modèle ne reçoit pas directement des mots comme unités sémantiques ; il reçoit une représentation tokenisée. |
| Tokenisation | Comment le texte est-il découpé ? | Faire encoder le préfixe et, séparément, la continuation avec le tokenizer réellement utilisé dans la page ou le code. | Les frontières de tokens ne coïncident pas nécessairement avec les mots ; elles varient selon le tokenizer. |
| Vocabulaire et IDs | Comment les morceaux sont-ils identifiés ? | Montrer les tokens et leurs IDs obtenus à l'exécution. | Un ID est une adresse de ligne dans la table de vocabulaire/embedding du tokenizer concerné ; ce n'est pas une coordonnée vectorielle. |
| Embeddings | Comment les IDs deviennent-ils des vecteurs ? | Sélectionner les lignes de la matrice d'embedding correspondant aux IDs. | Même ID = même vecteur initial dans un checkpoint donné ; les lignes ne sont pas des définitions lexicales. |
| Position | Comment l'ordre est-il conservé ? | Comparer les mêmes tokens placés à des positions différentes, ou présenter l'ajout/encodage positionnel réellement choisi. | Le modèle doit disposer d'une information de position ; ne pas supposer une méthode unique. |
| États contextualisés | Pourquoi un token dépend-il des autres ? | Comparer la représentation d'un même token dans le prompt seul et dans un contexte enrichi. | Les états cachés deviennent dépendants du contexte au fil des couches. |
| Transformer | Quelles opérations transforment les représentations ? | Suivre les tokens du prompt dans un bloc, puis dans la pile de blocs. | Attention, MLP, résidus et normalisation ont des rôles distincts. |
| Q/K/V | Comment chaque position interagit-elle avec les autres ? | Prendre le token courant de la question et illustrer ses requêtes, clés et valeurs vis-à-vis des positions accessibles. | Q, K et V sont des projections apprises, pas trois types de tokens. |
| Attention | Comment les informations sont-elles agrégées ? | Calculer les scores puis la pondération des valeurs pour une petite séquence jouet. | Les poids dépendent des scores et du contexte ; ils ne sont pas des explications fiables de l'attention humaine. |
| Masque causal | Quelles positions sont accessibles ? | Montrer que le token en cours ne peut pas consulter les tokens futurs de la continuation. | Le masque interdit l'accès au futur dans l'attention causale. |
| Logits | Que produit la tête de sortie ? | À la position finale du prompt, produire un score par token du vocabulaire. | Un logit est un score non normalisé, pas une probabilité. |
| Probabilités | Quelles suites sont plausibles ? | Appliquer softmax aux logits et examiner quelques candidats pour le token suivant. | La distribution est conditionnelle au préfixe et au modèle ; elle ne donne pas une réponse entière d'un seul coup. |
| Décodage | Comment choisit-on le token suivant ? | Comparer argmax, échantillonnage et température sur la même distribution. | Le choix dépend de la stratégie ; la température transforme la distribution avant l'échantillonnage. |
| Génération | Comment la tirade se construit-elle ? | Ajouter un token, le réinjecter dans le contexte, recalculer et répéter jusqu'au critère d'arrêt. | La génération est autoregressive ; le modèle ne rédige pas nécessairement toute la phrase en une seule opération. |
| Vraisemblance | Comment évaluer une suite déjà écrite ? | Donner la continuation jouet comme cible observée et calculer la probabilité conditionnelle de ses tokens successifs. | Scorer une séquence observée n'est pas la même opération que choisir une continuation. |
| Entropie / cross-entropy | À quel point la prédiction est-elle incertaine ou surprenante ? | Comparer des distributions de prochain token, puis mesurer la pénalité sur la cible jouet. | Entropie d'une distribution et cross-entropie entre prédiction et cible ne sont pas interchangeables. |
| Loss | Quel signal résume l'erreur ? | Agréger les pertes des tokens cibles du mini-exemple. | La loss dépend des cibles, du masque et de la réduction choisie. |
| Gradients | Comment les paramètres sont-ils informés ? | Rétropropager la loss à travers le calcul du prochain token. | Les gradients indiquent comment les paramètres influencent la loss ; ils ne sont pas des explications textuelles. |
| Build / entraînement | Comment les exemples sont-ils préparés et appris ? | Construire des fenêtres de contexte et des cibles décalées à partir du texte jouet, puis entraîner sur un corpus autorisé et documenté. | Le texte du film ne doit pas devenir un corpus d'entraînement par défaut ; un exemple minuscule ne suffit pas à entraîner un modèle utile. |
| Évaluation | Le modèle a-t-il appris à répondre ? | Évaluer sur des exemples séparés et des baselines ; comparer les continuations sans réutiliser le test pour ajuster le modèle. | Une démonstration, un test logiciel et une évaluation de qualité sont trois preuves différentes. |

## 4. Déclinaison page par page

Les pages ci-dessous sont les destinations canoniques identifiées dans le parcours actuel. Les pages FR et EN sont des paires : toute intégration de l'exemple doit être faite dans les deux langues au même changement. Cette matrice est un contrat éditorial de couverture, pas une nouvelle séquence obligatoire.

### 4.1 Understand — parcours conceptuel

| Page FR | Page EN | Usage précis du fil rouge | Garde-fou / limite |
|---|---|---|---|
| `fr/llm-overview.qmd` | `en/llm-overview.qmd` | Accroche : une question courte et une continuation longue illustrent une tâche de modèle de langage. | Ne pas confondre le personnage, un assistant conversationnel et un LLM. |
| `fr/generation.qmd` | `en/generation.qmd` | Introduire le cycle autoregressif avec le préfixe du scribe et la continuation d'Otis ; utiliser le parallèle Monty Python dans la version anglaise. | Ne pas faire croire qu'un modèle choisit toute la tirade en un seul bloc. |
| `fr/text-data.qmd` | `en/text-data.qmd` | Afficher le préfixe « C'est une bonne situation, ça, scribe ? » avant tokenisation, puis distinguer les tokens de continuation ; dans la page anglaise, prendre la scène des Romains comme parallèle culturel. | Conserver ponctuation, espaces et accents ; distinguer prompt et cible. |
| `fr/tokenization-strategies.qmd` | `en/tokenization-strategies.qmd` | Comparer la segmentation effective du prompt avec deux tokenizers si les outils sont disponibles. | Les tokens ne sont pas forcément des mots ; ne pas figer une segmentation universelle. |
| `fr/embedding-space.qmd` | `en/embedding-space.qmd` | Relier chaque ID obtenu à une ligne de la matrice d'embedding. | Employer « adresse de ligne » pour l'index de la table ; la coordonnée vectorielle est une autre notion. |
| `fr/positional-encoding.qmd` | `en/positional-encoding.qmd` | Montrer que l'ordre des mots du prompt compte, même si les IDs de tokens sont identiques. | Décrire la méthode positionnelle effectivement étudiée, sans généraliser à toutes les architectures. |
| `fr/contextualized-representations.qmd` | `en/contextualized-representations.qmd` | Suivre un token du prompt dans deux contextes légèrement différents. | Ne pas appeler « embedding » tout état caché ; distinguer vecteur initial et représentation contextualisée. |
| `fr/transformer.qmd` | `en/transformer.qmd` | Vue d'ensemble du passage du prompt aux logits dans les blocs Transformer. | Garder le niveau système ; renvoyer les détails à leurs pages canoniques. |
| `fr/queries-keys-values.qmd` | `en/queries-keys-values.qmd` | Isoler une position du prompt et visualiser ses Q/K/V. | Ne pas personnifier Q/K/V comme des questions, réponses ou mots. |
| `fr/scaled-dot-product-attention.qmd` | `en/scaled-dot-product-attention.qmd` | Calculer les scores et l'agrégation sur une séquence très courte dérivée du prompt. | Toute matrice numérique doit être explicitement jouet ou issue d'un calcul reproductible. |
| `fr/causal-masking.qmd` | `en/causal-masking.qmd` | Montrer qu'une position ne peut pas voir les tokens futurs de la réponse. | Distinguer masque causal et masque de padding. |
| `fr/logits.qmd` | `en/logits.qmd` | Lire les scores de candidats au premier token de continuation. | Un logit n'est ni une probabilité ni un degré de vérité. |
| `fr/probabilites.qmd` | `en/probabilities.qmd` | Normaliser les scores et comparer quelques tokens candidats. | Indiquer modèle, contexte, tokenizer et valeurs synthétiques si elles ne sont pas calculées. |
| `fr/vraisemblance.qmd` | `en/likelihood.qmd` | Scorer la continuation jouet comme séquence observée. | Ne pas confondre score de séquence et qualité littéraire. |
| `fr/entropy.qmd` | `en/entropy.qmd` | Comparer une distribution concentrée et une distribution diffuse pour le token suivant. | L'entropie caractérise une distribution, pas la difficulté subjective du scribe. |
| `fr/cross-entropy.qmd` | `en/cross-entropy.qmd` | Calculer la pénalité associée au token cible réellement observé. | Préciser la cible et la convention de réduction. |
| `fr/loss.qmd` | `en/loss.qmd` | Agréger les pertes des tokens de la continuation jouet. | Ne pas présenter la loss comme un jugement humain de la réponse. |
| `fr/gradients.qmd` | `en/gradients.qmd` | Illustrer la rétropropagation depuis la loss du prochain token. | Ne pas inventer de gradients ou de mise à jour sans calcul. |

### 4.2 Build — dépendances de construction

Le Build path est une voie distincte du parcours Understand. Le même exemple sert à rendre les données et les opérations concrètes, mais ne doit pas faire croire que l'ordre conceptuel et l'ordre d'implémentation sont identiques.

| Page FR | Page EN | Usage précis du fil rouge | Garde-fou / limite |
|---|---|---|---|
| `fr/build-path.qmd` | `en/build-path.qmd` | Montrer où le prompt, le tokenizer, les tenseurs, le modèle et la génération interviennent dans la construction. | Garder visibles les étapes planifiées et les limites d'implémentation actuelles. |
| `fr/corpus-preparation.qmd` | `en/corpus-preparation.qmd` | Utiliser un petit corpus fictif de phrases originales sur le métier de scribe pour illustrer provenance, nettoyage et séparation. | Ne pas constituer un corpus à partir du dialogue protégé du film sans base de droits adaptée. |
| `fr/training-examples.qmd` | `en/training-examples.qmd` | Transformer une phrase originale en fenêtres de contexte et cibles décalées. | Montrer précisément les frontières de document et les tokens spéciaux utilisés. |
| `fr/gpt-config-walkthrough.qmd` | `en/gpt-config-walkthrough.qmd` | Relier longueur de contexte, taille du vocabulaire et dimensions du modèle au prompt. | Les nombres sont ceux de la configuration de démonstration, pas des propriétés du film ou du texte. |
| `fr/gpt-ops-walkthrough.qmd` | `en/gpt-ops-walkthrough.qmd` | Tracer les opérations tensorielles appliquées à la séquence tokenisée. | Conserver les formes exactes et les conventions de dimensions du code. |
| `fr/transformer-block-walkthrough.qmd` | `en/transformer-block-walkthrough.qmd` | Suivre une passe avant dans un bloc avec le prompt jouet. | Distinguer calcul de référence, poids aléatoires et poids entraînés. |
| `fr/gpt-model-walkthrough.qmd` | `en/gpt-model-walkthrough.qmd` | Relier embedding, blocs, normalisation finale et tête de sortie. | Ne pas prétendre que le modèle aléatoire connaît la scène ou le film. |
| `fr/gpt-generation-walkthrough.qmd` | `en/gpt-generation-walkthrough.qmd` | Exécuter la boucle de génération et inspecter les tokens ajoutés. | Les sorties incohérentes d'un modèle non entraîné sont attendues et doivent être signalées. |

### 4.3 Practice, Deepen et évaluation

- **Exercises par page :** reprendre le même prompt ou une variante contrôlée pour demander au lecteur de prédire une étape, lire une forme tensorielle, interpréter une distribution ou repérer une confusion conceptuelle. Une variante doit annoncer ce qui change.
- **Tokenization / Unicode Deepen :** conserver le texte avec accents et ponctuation ; comparer normalisation et segmentation sans laisser entendre que UTF-8 et tokenisation sont la même opération.
- **Attention / math Deepen :** utiliser des matrices minuscules, valeurs calculées ou explicitement synthétiques, et préciser les dimensions.
- **Decoding Deepen :** repartir des mêmes logits pour isoler température, top-k, top-p et arrêt ; une seule variable change à la fois.
- **Experimental evaluation :** traiter le prompt comme une tâche d'évaluation seulement si l'on définit un jeu d'exemples, une baseline, des critères et un protocole reproductible. Une anecdote n'est pas un benchmark.
- **History / glossary :** ne pas ajouter le film aux pages d'histoire technique du Transformer ; la référence relève de l'accroche pédagogique, pas de la généalogie scientifique.

## 5. Règles d'usage éditorial

1. **Une source canonique :** modifier ce document lorsque le scénario, le prompt, la continuation jouet ou la couverture des pages change.
2. **Pas de copier-coller de la tirade :** garder la citation d'ouverture courte et référencée ; employer le texte original de LLM Lab pour les démonstrations.
3. **Bilinguisme :** chaque ajout dans une page FR doit avoir son équivalent EN dans la même PR. Dans les pages françaises, conserver le préfixe Astérix et la continuation d'Otis. Dans les pages anglaises, privilégier le parallèle Monty Python de *Life of Brian* (question sur les Romains puis réponses successives) plutôt qu'une traduction artificielle des répliques françaises ; utiliser *Holy Grail* en complément pour le contexte conversationnel et les contraintes successives.
4. **Répétition utile, pas duplication :** chaque page réutilise le même scénario pour enseigner son concept propre. Elle ne répète pas l'explication des pages précédentes.
5. **Véracité numérique :** aucun ID, vecteur, score, logit, poids ou gradient inventé présenté comme résultat réel. Les chiffres illustratifs sont marqués « jouet », « fictifs » ou calculés.
6. **Respect des frontières de parcours :** Understand expose la chaîne conceptuelle ; Build suit les dépendances d'implémentation. Deepen ajoute des détails facultatifs ; Practice vérifie le transfert.
7. **Accessibilité et sobriété :** l'humour doit rester dans l'accroche ou le texte d'exemple ; les termes techniques, les limites et les légendes restent explicites.
8. **Éviter la personnification trompeuse :** Otis est un personnage de fiction ; le modèle n'a ni souvenirs, ni rencontres, ni goût du travail bien fait. Ces notions appartiennent au récit humain, pas au mécanisme computationnel.
9. **Provenance :** conserver le lien IMDb comme identification de la scène et ajouter des sources primaires pour toute affirmation sur tokenizers, architectures, entraînement ou évaluation.

## 5 bis. Équivalent anglophone — Monty Python

Pour les pages anglaises, utiliser comme parallèle culturel la scène « What have the Romans ever done for us? » de *Monty Python's Life of Brian* (1979).

- **Prefix / prompt :** “What have the Romans ever done for us?”
- **Continuation illustrée dans la scène :** les autres membres du groupe répondent successivement par des exemples tels que “Aqueducts”, “sanitation”, “roads” et “irrigation”.
- **Pourquoi c'est un bon parallèle :** une question initiale contraint le champ des réponses ; les éléments suivants enrichissent progressivement la liste et modifient le contexte disponible pour la suite.

**Précaution pédagogique importante :** dans le film, les éléments sont prononcés par plusieurs personnages dans un dialogue monté. Ce n'est donc pas littéralement une génération autoregressive par un seul locuteur ou un modèle. La scène fournit une analogie mémorable du couple contexte/continuation ; pour les démonstrations de génération token par token, utiliser une séquence textuelle unique et contrôlée, ou la continuation jouet ci-dessus. La phrase anglaise est une adaptation de travail du rôle du prompt, pas une traduction du dialogue d'Astérix.

Source de référence : [Monty Python — *Life of Brian* (1979), citation et contexte](https://fr.wikiquote.org/wiki/Monty_Python_:_La_Vie_de_Brian).

### Compléments anglophones — *Monty Python and the Holy Grail*

Deux scènes de *Monty Python and the Holy Grail* (1975) complètent *Life of Brian*, sans remplacer le parallèle principal de génération.

**1. The Bridge of Death — contexte conversationnel et tours successifs**

Le gardien pose une série de questions aux voyageurs ; les réponses déterminent la suite de l'échange et la possibilité de traverser. Cette scène convient pour illustrer :
- la dépendance d'une réponse aux tours précédents ;
- la distinction entre contexte accumulé et nouveau message ;
- le rôle d'une question suivante dans le déroulement d'un dialogue.

Elle ne constitue pas une génération autoregressive par un seul locuteur : les personnages alternent et la scène est un dialogue. À utiliser dans les pages sur le contexte, les conversations et l'instruction, pas comme exemple de génération monologique.

**2. The Knights Who Say “Ni” — contraintes qui évoluent**

La demande d'un arbuste (*a shrubbery*) devient progressivement plus précise : un second arbuste, une disposition particulière, un chemin, puis une contrainte supplémentaire. Cette scène illustre la manière dont de nouvelles exigences enrichissent le contexte et modifient la tâche à accomplir.

Elle est particulièrement adaptée aux pages sur les instructions, le suivi des contraintes, les conversations multi-tours et l'évaluation de la cohérence avec l'historique. Ne pas l'utiliser comme preuve que le modèle comprend ou satisfait nécessairement les contraintes.

Sources de travail : [transcription du pont de la Mort et des chevaliers de Ni](https://transcripts.foreverdreaming.org/viewtopic.php?t=218005) ; [scène des chevaliers de Ni, transcription alternative](https://python.mzonline.com/holygrail/scene26/). Les transcriptions servent à vérifier le contenu des scènes, pas à reproduire de longs extraits dans les leçons.


## 6. Procédure de remplacement ou de réorganisation

Pour changer de fil rouge sans perdre la cohérence du parcours :

1. Remplacer la référence culturelle et le scénario canonique en sections 1 et 2.
2. Vérifier que le nouveau matériau offre un texte assez court pour la tokenisation, une continuation pour la génération et une séquence cible pour le scoring/loss.
3. Réviser la matrice page par page ; retirer les pages où l'exemple n'apporte rien et ajouter celles où il clarifie une transition.
4. Vérifier que les exemples numériques sont recalculés avec le tokenizer/modèle concernés ou restent explicitement fictifs.
5. Mettre à jour en parallèle les pages FR/EN et leurs exercices ; ne pas faire du document interne une excuse pour dupliquer les explications.
6. Rejouer les contrôles de parité bilingue, métadonnées, liens, rendu Quarto et audit navigateur des pages modifiées.
7. Mettre à jour la date de revue et consigner les changements importants dans l'historique de PR.

## 7. Critères d'acceptation pour les intégrations futures

- Le préfixe canonique est identique partout où l'on compare des résultats.
- La continuation jouet est identifiée comme texte pédagogique original, jamais comme sortie de modèle.
- Les pages FR/EN sont alignées sur le même objectif et le même niveau de détail.
- Les identifiants de tokens proviennent du tokenizer montré ; les « adresses de ligne » restent distinctes des coordonnées des vecteurs.
- Les valeurs numériques sont reproductibles ou explicitement synthétiques.
- Les pages renvoient à leurs explications canoniques au lieu de dupliquer les détails.
- Les deux parcours Understand et Build restent distincts et leurs liens sont contextualisés.
