# Audit pédagogique du parcours LLM — 2026-11-09

**Statut :** audit initial en cours, fondé sur les sources de `main` consultées le 2026-11-09. Ce document distingue explicitement l'inventaire, la lecture effective du contenu et la validation du rendu. Il ne constitue pas encore une validation complète page par page.

## 1. Périmètre et sources canoniques

L'ordre de lecture est celui de `data/guided-route.yml`, interprété avec :

- `docs/learning-path.md` : objectifs, modules et dépendances pédagogiques ;
- `docs/content-section-mapping.md` : destination, responsabilité éditoriale et inventaire des pages ;
- `docs/canonical-computational-spine.md` et `data/computational-graph.yml` : calcul partagé et branches génération / scoring / entraînement / évaluation ;
- `data/concepts.yml` : concepts et relations sémantiques ;
- `docs/information-architecture.md` et `docs/page-template-system.md` : propriété des données et composition des pages.

Le parcours conceptuel n'est pas le parcours d'implémentation. La génération est d'abord présentée comme aperçu global, puis revisitée avec ses mécanismes détaillés. La préparation du corpus et les exemples d'entraînement forment une branche Build qui rejoint le modèle au jalon G8 ; ils ne sont pas des prérequis à l'inférence. Après la distribution conditionnelle, génération, scoring et entraînement sont des usages frères, pas les étapes d'une boucle unique.

## 2. Contrat pédagogique de révision

### Convention à réutiliser

Plusieurs leçons possèdent déjà deux composants complémentaires :

1. un rappel bref (« L'idée à retenir en une minute » ou équivalent) ;
2. « Vérifier sa compréhension », avec questions et réponses repliées.

La collection `site/fr/exercises.qmd` / `site/en/exercises.qmd` accueille les exercices plus longs, calculs, diagnostics et transferts. Cette séparation est utile et doit être conservée.

**Décision : ne pas créer un nouveau système de fiches, de shortcode ou de registre.** Une fiche de révision peut être une section courte de la page, un rappel existant amélioré, ou une fiche transversale pour un groupe de notions. Elle n'est pas un résumé redondant de chaque section.

### Contenu minimal attendu selon le besoin

- **Rappel de page (3–6 points)** : objet, mécanisme, distinction critique, équation ou notation utile, limite ou piège.
- **Récupération active (3–5 questions)** : au moins une question de restitution, une question d'explication ou de calcul, et une question de transfert/diagnostic quand le sujet s'y prête. Réponses masquées.
- **Fiche de groupe** : reconstruire les liens entre plusieurs pages (par exemple texte → IDs → embeddings → position → états contextualisés, ou logits → distribution → génération/scoring/training). Elle ne répète pas les rappels locaux.
- **Build** : synthèse opérationnelle sous forme de contrat d'entrée/sortie, invariants, formes, limites et tests à consulter ; ne pas transformer les pages Build en cours conceptuels dupliqués.

Ne pas imposer le même nombre de questions ni une section artificielle à une page de référence, d'historique ou de Deepen. Les hypothèses et limites qui conditionnent une affirmation restent visibles, jamais enfouies dans la fiche.

## 3. Audit du parcours, page par page

Légende :
- **Inventoriée** : la page figure dans la route ou dans le mapping canonique.
- **Lecture source partielle** : le corps a été lu sur les sections disponibles lors de cette première passe ; les équations, exemples, liens et contre-exemples restent à vérifier.
- **À lire** : aucune conclusion sur la qualité du contenu n'est encore tirée.
- **Rendu / apprenant** : non validé par ce relevé source.

| Étape | Page FR / EN | Rôle et transition à contrôler | Synthèse / révision : premier constat | État |
|---|---|---|---|---|
| Orientation | `llm-overview` | Définir LLM/GPT/Transformer, situer le modèle pédagogique et annoncer le noyau prédictif ; conduire vers l'aperçu de génération | Le corps FR a été parcouru partiellement ; vérifier la présence d'une synthèse qui distingue architecture, objectif, paramètres et usages frères | Lecture source partielle |
| Aperçu d'inférence | `generation` | Donner la boucle complète avec paramètres fixes ; transition vers texte/tokens sans exiger les détails internes | Le corps FR contient objectifs, rappel « une minute », boucle, prefill/decode et frontière teacher forcing ; éviter de recopier la même fiche au retour détaillé | Lecture source partielle |
| Entrée texte | `text-data` | Texte → tokens → IDs → lookup ; distinguer prompt d'inférence et corpus d'entraînement | Rappel bref et self-check présents ; vocabulaire nuancé pour ne pas présenter tout tokenizer comme doté d'un vocabulaire appris | Revue FR/EN effectuée |
| Stratégies de tokenisation | `tokenization-strategies` | Comparer unités, algorithmes et compromis ; préparer le passage des IDs aux vecteurs | Section « À retenir » et self-check présents ; le Deepen sur l'évaluation évite de surcharger Understand | Revue FR/EN effectuée |
| Unicode (optionnel) | `unicode-text` | Approfondissement sur encodage, normalisation et texte ; ne pas bloquer la route principale | Une fiche n'est pas requise si une courte conclusion et des liens suffisent | À lire |
| Embeddings | `embedding-space` | ID → ligne de matrice ; distinguer table statique, vecteur initial et états contextualisés | Rappel « une minute », exemple matriciel calculable et self-check présents ; transition vers position explicite | Revue FR/EN effectuée |
| Position | `positional-encoding` | Expliquer le besoin d'ordre, distinguer position explicite, RoPE et masque causal | Ajout d'un rappel « une minute » distinguant injection absolue/relative/RoPE et visibilité causale ; self-check existant conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Représentations contextualisées | `contextualized-representations` | Distinguer lookup initial et états dépendant du contexte ; conduire vers le calcul du Transformer | Ajout d'un rappel « une minute » distinguant ID, embedding initial, position, contexte et masque d'architecture ; self-check existant conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Tenseurs (optionnel) | `tensors` | Support de formes et opérations ; ne pas en faire un prérequis général | Vérifier que la fiche sert le Build / Deepen sans interrompre Understand | À lire |
| RoPE (optionnel) | `rope` | Approfondir la géométrie et les variantes positionnelles | Fiche de référence facultative ; vérifier les hypothèses et les conventions | À lire |
| Vue d'ensemble Transformer | `transformer` | Replacer les opérations dans le bloc et le forward pass, jusqu'aux logits | Self-check repéré ; vérifier une synthèse du flux et la séparation Understand / Build / Deepen | Lecture source partielle |
| Q/K/V | `queries-keys-values` | Projections depuis les états d'entrée de chaque bloc ; Q/K déterminent les poids, V fournit le contenu | Rappel bref et self-check repérés ; vérifier que les exercices couvrent les rôles, projections, apprentissage des paramètres et transfert | Lecture source partielle |
| Attention | `scaled-dot-product-attention` | Scores, mise à l'échelle, softmax, agrégation ; réutiliser Q/K/V sans redéfinir leurs rôles | Rappel bref et self-check repérés ; vérifier que le calcul canonique et les limites sont synthétisés | Lecture source partielle |
| Masque causal | `causal-masking` | Contraindre l'accès au futur ; distinguer masque causal, padding et convention d'API | Rappel bref et self-check repérés ; exemples numériques et invariance de préfixe à vérifier | Lecture source partielle |
| Cross-attention (optionnel) | `cross-attention` | Extension distincte, non requise pour le GPT décodeur seul | Garder l'optionnalité explicite ; pas de fiche imposée | À lire |
| Mise à l'échelle (optionnel) | `attention-score-scaling` | Dérivation et propriétés de la mise à l'échelle ; approfondissement après attention | Fiche courte facultative, surtout si elle aide à réactiver la dérivation | À lire |
| Logits | `logits` | Projection vocabulaire et scores non normalisés ; transition vers softmax | Rappel bref et self-check présents ; distingue classement, score et probabilité | Revue FR/EN effectuée |
| Probabilités | `probabilites` / `probabilities` | Softmax et distribution conditionnelle ; ne pas confondre probabilité et vérité | Rappel bref, exemple numérique, explorateur de température et self-check présents ; température présentée comme transformation de distribution, non comme apprentissage | Revue FR/EN effectuée |
| Entropie | `entropy` | Incertitude de la distribution prédictive ; distinguer entropie et score d'une cible observée | Ajout d'un rappel d'une minute FR/EN distinguant entropie prédictive, surprise observée, bornes et limites d'interprétation ; self-check conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Génération détaillée | `generation` (réutilisée) | Revenir sur prefill, decode, cache, sélection, feedback et arrêt | Rappel bref et self-check présents ; distingue prefill/decode (phases) de decoding (règle de sélection) et du forward pass | Revue FR/EN effectuée |
| Stratégies avancées (optionnel) | `decoding-strategies` | Top-k/top-p, beam, contrastif, compromis et reproductibilité | Pas de rappel bref repéré dans le premier relevé ; à examiner après la route centrale | À lire |
| Vraisemblance | `vraisemblance` / `likelihood` | Scorer une cible observée, factoriser une séquence ; pas de sélection de token | Ajout d'un rappel d'une minute FR/EN distinguant scoring, règle de chaîne, log-vraisemblance, NLL et conventions de comparaison | Revue FR/EN effectuée + synthèse ajoutée |
| Entropie croisée | `cross-entropy` | Mesurer l'écart entre distribution prédite et cible ; relier au NLL | Ajout d'un rappel d'une minute FR/EN sur cible one-hot/générale, alignement, masques et réduction | Revue FR/EN effectuée + synthèse ajoutée |
| Loss | `loss` | Agréger les pertes token par token avec masque et réduction | Rappel bref et self-check repérés ; vérifier la séparation entre score, objectif et mise à jour | Lecture source partielle |
| Gradients | `gradients` | Dériver l'objectif et expliquer la mise à jour des paramètres | Rappel bref et self-check repérés ; vérifier la frontière avec l'optimiseur et le training loop | Lecture source partielle |
| Corpus (branche Build) | `corpus-preparation` | Provenance, filtrage, déduplication, splits, tokenizer figé ; branche de données | Aucun rappel/self-check repéré ; candidate à une fiche opérationnelle de sortie et de contrôle | Lecture source partielle |
| Exemples d'entraînement (branche Build) | `training-examples` | Fenêtres, cibles décalées, teacher forcing, packing/padding/masks ; rejoint G8 | Aucun rappel/self-check repéré ; candidate prioritaire à une synthèse opérationnelle et à un auto-diagnostic | Lecture source partielle |
| Évaluation / pratique | `evaluation-experimentale` et collections d'exercices | Évaluer une tâche et un protocole ; ne pas présenter l'exercice existant comme benchmark d'un GPT entraîné | Réutiliser le hub d'exercices et expliciter les limites ; vérifier le renvoi depuis les pages scoring/training | À lire |

Les pages listées comme optionnelles ne deviennent pas des étapes obligatoires. Les pages Build ne doivent pas être évaluées avec exactement le même gabarit que les leçons conceptuelles.

## 4. Premiers constats étayés

### Points déjà solides

- Le parcours narratif distingue explicitement l'aperçu de génération de son étude détaillée ultérieure.
- La route computationnelle ne place pas Q/K/V après les états contextualisés finaux : Q/K/V sont des opérations internes aux blocs Transformer.
- Le modèle distingue désormais génération, scoring de cibles observées, évaluation sans mise à jour et entraînement avec gradients / mises à jour.
- La branche G1b → G2 (corpus puis exemples d'entraînement) rejoint G8 ; elle ne précède pas artificiellement l'inférence.
- Le hub d'exercices distingue les self-checks courts intégrés aux leçons des exercices approfondis et activités de transfert.
- Plusieurs pages centrales disposent déjà d'un rappel bref et d'un self-check ; le besoin principal est la cohérence de couverture et la qualité des transitions, pas la création d'un nouveau composant.

### Lacunes ou vérifications prioritaires

1. **Pages Build sans synthèse explicite repérée :** `corpus-preparation` et `training-examples`. Leur ajouter un récapitulatif d'entrée/sortie, invariants, erreurs fréquentes et contrôles, puis 3–5 questions courtes si elles servent réellement l'apprentissage.
2. **Entropie :** ajouter un rappel bref seulement après vérification que la page ne possède pas déjà une conclusion équivalente.
3. **Vue Transformer :** vérifier que la synthèse finale n'est pas seulement un self-check ; elle doit restituer le rôle du bloc et la frontière avec le calcul de sortie.
4. **Scoring :** rendre mémorisable la différence entre probabilité d'une cible, log-vraisemblance de séquence, NLL par token et loss agrégée.
5. **Transitions :** chaque fin de page doit répondre à « qu'est-ce qui vient d'être établi ? » et « quelle question la page suivante résout-elle ? », sans transformer les liens en une longue liste de navigation.
6. **Bilinguisme :** chaque correction de synthèse/self-check doit être faite et comparée en FR/EN dans le même lot.

## 5. Ordre des prochaines passes

- **Passe A — entrée et représentations :** terminer la lecture complète des pages orientation, génération aperçu, texte, tokenisation, embeddings, position et états contextualisés ; vérifier les transitions et la parité FR/EN. Réutiliser la séquence formative TR-A/TR-B/TR-C existante.
- **Passe B — Transformer et attention :** relire Transformer, Q/K/V, attention et masque causal ; vérifier les prérequis locaux, les notations, la progression des exercices AT/TF et les renvois Deepen.
- **Passe C — prédiction et branches :** relire logits, probabilités, entropie, génération détaillée, vraisemblance, cross-entropy, loss et gradients ; tester la cohérence avec le graphe computationnel et les fiches de révision.
- **Passe D — Build et apprentissage :** corpus, exemples d'entraînement, teacher forcing, boucle d'entraînement G8 et validation ; maintenir les gates de prérequis et les statuts de code.
- **Passe E — adaptation et évaluation :** vérifier les destinations existantes et les gaps, sans faire croire que les étapes non implémentées sont disponibles.
- **Passe F — contrôle final :** FR/EN, ancres/liens, métadonnées invisibles au lecteur, Quarto, rendu navigateur desktop/mobile, clavier et lecteur d'écran. Les preuves de rendu et l'étude apprenant restent séparées des tests source/CI.

## 6. Règles de décision

Pour chaque page, consigner une décision parmi :

- **Conserver** : le contenu et la place sont adaptés.
- **Clarifier** : corriger une définition, une transition ou une distinction.
- **Compléter** : ajouter un exemple, un rappel ou un self-check manquant.
- **Déplacer** : transférer une profondeur ou un contenu vers sa page propriétaire, en conservant une destination explicite.
- **Relier** : ajouter ou corriger un lien utile sans dupliquer l'explication.
- **Déférer** : besoin réel mais dépendant d'une revue, d'un rendu ou d'une preuve non disponible.

Aucune information existante ne doit être supprimée sans cartographie de sa destination. Les statuts « source lue », « CI passée », « rendu navigateur vérifié » et « testé avec des apprenants » ne sont jamais interchangeables.

## 7. Historique des validations

| Date | Validation | Résultat |
|---|---|---|
| 2026-11-09 | Lecture des sources canoniques curriculum, route, mapping, architecture, épine computationnelle et templates | Cohérence d'architecture confirmée au niveau documentaire ; revue exhaustive des pages non terminée |
| 2026-11-09 | Relevé de structure de plusieurs pages FR de la route | Rappels et self-checks déjà présents sur plusieurs pages ; deux pages Build candidates à compléter ; détails et EN à vérifier |
| À venir | Relecture complète FR/EN et validation des transitions | Non réalisée |
| À venir | Rendu navigateur et accessibilité | Non réalisé dans cet audit |
| À venir | Validation formative avec apprenant indépendant | Non réalisée |


## 8. Passe A — revue du groupe « texte → représentations » (2026-11-09)

### Pages relues en français et en anglais

- `text-data` : rôle d'orientation, chaîne texte → tokens → IDs → lookup, distinction prompt/corpus, et frontières vers les pages spécialisées.
- `tokenization-strategies` : granularités, composants du pipeline, familles BPE/WordPiece/unigramme, exemple pas à pas, limites et séparation apprentissage du tokenizer / encodage.
- `embedding-space` : lookup matriciel, dimensions \(V\) et \(d\), distinction Word2Vec statique / embedding initial / état contextualisé, exemple calculable et prudence géométrique.
- `positional-encoding` : équivariance par permutation, encodages absolus, mécanismes relatifs, RoPE et distinction avec le masque causal.
- `contextualized-representations` : même ID et même lookup initial, effets de position et du contexte, causalité du décodeur, comparaison avec les encodeurs bidirectionnels.

### Décisions et modifications de cette passe

1. **Pas de réécriture globale :** les pages text-data, tokenization-strategies et embedding-space ont déjà une synthèse adaptée à leur niveau et un contrôle formatif. Leur ajouter une seconde fiche aurait créé de la redondance.
2. **Position :** ajout d'un rappel d'une minute en FR/EN. Il résume le besoin d'ordre, l'emplacement des mécanismes absolus/relatifs et le rôle distinct du masque causal.
3. **Représentations contextualisées :** ajout d'un rappel d'une minute en FR/EN. Il fixe la distinction entre ID, embedding initial et état caché contextualisé, sans attribuer au lookup une compréhension du contexte.
4. **Précision de vocabulaire :** dans text-data FR/EN, remplacer l'affirmation trop générale d'un « vocabulaire appris » par un vocabulaire défini, souvent appris pour les tokenizers modernes à sous-mots.
5. **Parité linguistique :** les ajouts et la nuance terminologique ont été appliqués en parallèle en FR et EN.

### Cohérence des transitions observée

`text-data → tokenization-strategies → embedding-space → positional-encoding → contextualized-representations → transformer`

- La première page établit les objets et renvoie aux spécialisations ; elle ne fait pas de l'apprentissage du tokenizer un prérequis à l'encodage d'un prompt.
- La page tokenisation s'arrête avant le lookup ; l'embedding-space prend explicitement le relais avec une matrice \(E\in\mathbb{R}^{V\times d}\).
- L'embedding-space introduit le vecteur initial et laisse à positional-encoding le traitement de l'ordre.
- Positional-encoding distingue les mécanismes d'injection positionnelle du masque causal ; contextualized-representations explique ensuite comment les blocs transforment les états.
- Contextualized-representations prépare le passage vers Transformer et Q/K/V sans prétendre détailler les opérations internes du bloc.

### Points à conserver en surveillance

- Le stepper de text-data présente les étapes en vue d'ensemble, tandis que tokenization-strategies est une page spécialisée : ne pas interpréter cette juxtaposition comme deux tokenisations successives.
- Le pipeline général ne doit pas laisser croire que RoPE est un vecteur ajouté au lookup ; les pages text-data, positional-encoding et contextualized-representations portent maintenant explicitement cette réserve.
- La figure externe de contextualized-representations reste soumise à la vérification de provenance et de droits déjà suivie dans l'issue #156 ; cette passe ne tranche pas cette question.
- Unicode, les détails du tokenizer et les métriques de comparaison restent des approfondissements ; ils ne sont pas requis pour comprendre le lookup et la contextualisation.

### Validation

Cette passe est une revue de source FR/EN et des transitions déclarées. Elle ne constitue pas une preuve de rendu navigateur, de conformité d'accessibilité ou d'efficacité d'apprentissage auprès d'un lecteur indépendant. Les vérifications Quarto/CI sont à relever sur le commit final de la branche.


## 9. Passe B — revue du groupe « Transformer → attention » (2026-11-09)

### Pages relues en français et en anglais

- `transformer` : place le calcul interne du GPT entre représentations d'entrée et logits ; distingue auto-attention, MLP, résidus, normalisation, profondeur/largeur et génération.
- `queries-keys-values` : définit les projections issues du même flux en auto-attention, leurs paramètres et dimensions, les rôles Q/K vs V, ainsi que les conséquences d'une modification de projection.
- `scaled-dot-product-attention` : scores \(QK^\top\), mise à l'échelle, masque éventuel, softmax ligne par ligne et agrégation \(AV\), avec exemple numérique.
- `causal-masking` : contrainte \(j\leq i\), masque additif, convention entrée/cible décalée, distinction des masques causal, padding, frontière documentaire et loss, et test d'invariance.

### Décisions et modifications de cette passe

1. **Transformer :** ajout d'un rappel d'une minute FR/EN pour restituer le forward pass, le rôle des sous-couches, la répétition des blocs et la sortie logits. Il précise que Q/K/V sont internes à l'auto-attention et que softmax/décodage ne sont pas la sortie du réseau.
2. **Q/K/V :** enrichissement du rappel existant en FR/EN. Il couvre les trois projections, l'apprentissage conjoint, la séparation routage/contenu, l'invariance des poids lorsque V seul change, et la portée de la formulation self-attention standard.
3. **Attention :** rappel d'une minute et auto-vérification déjà présents dans les deux langues ; pas de duplication ajoutée.
4. **Masque causal :** rappel d'une minute et auto-vérification déjà présents ; la distinction avec le masque de perte est explicite, ce qui raccorde cette page à `training-examples`.
5. **Aucune suppression ni déplacement :** les compléments optionnels (géométrie, gradients QKV, variantes MQA/GQA, code et tests) sont conservés dans leurs blocs repliés. Leur emplacement devra être réévalué lors de l'audit Understand/Deepen/Build complet, sans perdre les références ni les exemples.

### Cohérence des transitions observée

`contextualized-representations → transformer → queries-keys-values → scaled-dot-product-attention → causal-masking → logits`

- La page Transformer donne le flux global et s'arrête aux logits ; elle ne réenseigne pas le tokenizer ni la boucle de génération.
- Q/K/V repartent du flux d'entrée de la sous-couche d'attention : ce n'est pas une étape qui suit les états contextualisés finaux du modèle.
- La page Q/K/V définit les projections mais délègue les scores et l'agrégation ; la page suivante prend exactement ce relais.
- La page attention définit le masque additif comme entrée de l'étape softmax, puis délègue à causal-masking le choix des positions interdites et les lignes entièrement masquées.
- Causal-masking relie la visibilité au décalage entrée/cible : la position \(i\) voit jusqu'à \(i\), puis prédit la cible \(i+1\). Elle distingue ce masque du masque de perte.
- Le passage vers logits correspond à la sortie du réseau ; la distribution et la génération restent des étapes distinctes.

### Points de vigilance

- **Notion de contextualisation :** éviter toute représentation linéaire qui placerait Q/K/V après la contextualisation finale. Chaque bloc reçoit un état déjà transformé par les blocs précédents et calcule ses propres projections.
- **Softmax :** les poids sont relatifs aux clés accessibles d'une ligne ; ils ne constituent pas une mesure universelle de pertinence ou de causalité.
- **Masques :** conserver les distinctions entre visibilité attentionnelle, padding, frontière documentaire et contribution à la loss. Ne pas présenter le masque de perte comme une protection contre la fuite d'information dans le forward pass.
- **Code et niveau :** les pages Understand contiennent des références à l'implémentation et des micro-ateliers optionnels. Leur présence n'est pas en soi un défaut, mais les contenus de construction détaillés doivent rester dans Build/Practice et les dérivations avancées dans Deepen.
- **Terminologie :** garder une correspondance stable entre « états cachés / hidden states », « représentations contextualisées », « poids d'attention » et « valeurs » ; ne pas appeler les valeurs des « poids ».

### Validation

Cette passe établit la cohérence de contenu et des transitions à partir des sources FR/EN. Elle ne vérifie pas encore le rendu des diagrammes, la navigation au clavier, les liens générés par les includes, ni la compréhension par un lecteur indépendant.


## 10. Passe C — revue du groupe « logits → distribution → génération » (2026-11-09)

### Pages relues en français et en anglais

- `logits` : vecteur \(z\in\mathbb R^V\), scores non normalisés, classement local, projection de sortie et interface avec la cross-entropie.
- `probabilites` / `probabilities` : softmax, distribution conditionnelle, exemple numérique, température, calibration et vérité factuelle.
- `entropy` : entropie prédictive conditionnelle, surprise d'un token observé, factorisation de séquence, dépendance au tokenizer et à la température.
- `generation` : boucle autorégressive, prefill, decode incrémental, KV cache, sélection du token, feedback et critères d'arrêt.

### Décisions et modifications de cette passe

1. **Logits :** rappel d'une minute et self-check déjà présents en FR/EN ; aucune duplication.
2. **Probabilités :** rappel d'une minute, exemple, exploration interactive de la température et self-check déjà présents ; aucune duplication.
3. **Entropie :** ajout d'un rappel d'une minute en FR/EN, car la page disposait d'un self-check mais pas d'une synthèse rapide. La fiche sépare l'entropie de la distribution de la surprise du token cible et rappelle les bornes en nats.
4. **Précision de traduction :** la formulation anglaise du rappel précise qu'une faible entropie ne garantit ni correction factuelle ni calibration.
5. **Génération :** rappel et self-check déjà présents ; la page distingue bien les phases prefill/decode, la règle de decoding et la boucle complète.

### Cohérence des transitions observée

`causal-masking → logits → probabilities → entropy → likelihood / cross-entropy`

La page `generation` est volontairement réutilisée à deux endroits : d'abord comme aperçu du comportement global, puis comme retour détaillé après la distribution. Elle ne doit pas être dupliquée.

- Les logits restent des scores non normalisés ; la page probabilités prend explicitement en charge leur transformation par softmax.
- La distribution est conditionnée par le préfixe ; elle porte sur les IDs du tokenizer et non directement sur des propositions sémantiques.
- La température transforme la distribution de décodage sans modifier les paramètres appris ; elle ne doit pas être présentée comme un mécanisme d'entraînement.
- L'entropie mesure la dispersion de toute la distribution avant observation ; la surprise \(-\log p(x_t\mid x_{<t})\) concerne une cible réalisée.
- La vraisemblance de séquence est obtenue par factorisation des probabilités conditionnelles ; elle ne doit pas être confondue avec l'entropie prédictive.
- La génération sélectionne un token puis le réinjecte dans le contexte ; scoring et entraînement utilisent la même distribution prédictive mais n'effectuent pas cette sélection de la même manière.

### Points de vigilance

- La température apparaît dans probabilités, entropie et génération avec trois fonctions pédagogiques : transformation mathématique de la distribution, effet sur l'entropie, puis effet sur la sélection en boucle. Garder ces niveaux distincts plutôt que supprimer les répétitions utiles.
- La page probabilités présente déjà des exemples et une exploration interactive ; vérifier leur rendu réel et leur accessibilité au clavier lors de la passe navigateur.
- Les pages scoring et training restent à auditer dans le groupe suivant : vraisemblance, cross-entropy, loss et gradients.
- La génération depuis un checkpoint local est explicitement décrite comme non encore disponible dans l'état du dépôt ; ne pas laisser entendre que le parcours Build a déjà livré cette capacité.

### Validation

Revue source FR/EN et contrôle des frontières éditoriales effectués. Rendu navigateur, fonctionnement de l'explorateur interactif, accessibilité et validation par apprenant non réalisés dans cette passe.


## 11. Passe D — revue du groupe « vraisemblance → objectif de prédiction » (2026-11-09)

### Pages relues en français et en anglais

- `vraisemblance` / `likelihood` : factorisation par règle de chaîne, scoring d'une séquence observée avec préfixes de référence, log-vraisemblance, NLL, moyenne par token et dépendance au tokenizer.
- `cross-entropy` : cible one-hot et distribution cible générale, alignement logits/labels, masquage des positions invalides, réduction, perplexité et lien avec le gradient.

### Décisions et modifications de cette passe

1. **Vraisemblance :** ajout d'un rappel d'une minute FR/EN. Il distingue explicitement scoring à paramètres fixes, génération avec feedback, et entraînement avec gradients.
2. **Cross-entropy :** ajout d'un rappel d'une minute FR/EN. Il distingue le cas one-hot du cas cible générale et fixe les contrôles d'alignement et de réduction.
3. **Pas de nouveau self-check :** les deux pages disposaient déjà de questions avec réponses ; les nouveaux rappels préparent ces questions sans les remplacer.
4. **Aucune réécriture des exemples ou des dérivations :** les formules existantes et les limites d'implémentation sont conservées.

### Cohérence des transitions observée

`probabilities → entropy / likelihood → cross-entropy → loss → gradients`

- L'entropie prédictive décrit la distribution avant observation ; la vraisemblance attribue une probabilité à une séquence effectivement observée.
- La règle de chaîne justifie le produit des probabilités conditionnelles sans supposer l'indépendance des tokens.
- La NLL d'une séquence est une somme de surprises token par token ; la moyenne par token est une réduction distincte.
- La cross-entropy one-hot est la NLL locale d'une cible ; avec une cible générale, elle compare une distribution cible à la distribution prédite.
- L'alignement des logits et des labels doit être cohérent avec le décalage autorégressif. Le masque causal protège le forward pass ; le masque de perte exclut des cibles de l'objectif. Aucun ne remplace l'autre.
- La perplexité est une exponentielle de la cross-entropy moyenne selon une base de logarithme et un protocole donnés ; elle ne résume pas la qualité globale d'un assistant.

### Points de vigilance

- Les pages vraisemblance et cross-entropy contiennent déjà beaucoup de détails ; les synthèses ajoutées restent courtes et ne dupliquent ni les exemples ni les dérivations.
- La relation entre somme NLL, moyenne par token et réduction de batch doit rester visible dans les pages suivantes (loss) et dans les comparaisons de modèles.
- La relation exacte entre teacher forcing, scoring à préfixes de référence et entraînement devra être maintenue : même conditionnement observé, mais opérations et effets sur les paramètres distincts.
- Les variantes à cibles souples et divergence KL restent un approfondissement, pas un prérequis au cas one-hot.

### Validation

Revue source FR/EN et cohérence conceptuelle effectuées. Les vérifications de rendu, d'accessibilité et d'apprentissage restent ouvertes.



## 12. Passe E — revue du groupe « exemples → objectif → gradients → apprentissage » (2026-11-09)

### Pages relues en français et en anglais

- \`training-examples\` : construction de fenêtres entrée-cible décalées, teacher forcing comme conditionnement sur le préfixe observé, stride, packing, frontières documentaires, padding, masques et formes \`[B,L]\` / \`[B,L,V]\`.
- \`loss\` : agrégation des pénalités par token valide, conventions de réduction, masquage des cibles, perplexité et limites d'interprétation des courbes.
- \`gradients\` : dérivée de la cross-entropie par rapport aux logits, règle de chaîne jusqu'aux paramètres, rétropropagation, mise à jour SGD élémentaire et vérification par différences finies.
- G8 dans \`docs/learning-path.md\` et sa spécification [#656](https://github.com/JM-Brun/llm-lab/issues/656) : contrat d'implémentation attendu et limites de la référence publique actuelle.

### Décisions et frontières confirmées

1. **Construction des exemples (Build/G2) :** \`training-examples\` est la page propriétaire du décalage entrée-cible et du teacher forcing. Ce dernier est correctement défini comme une stratégie de conditionnement sur le préfixe de référence ; ce n'est ni la loss, ni l'optimiseur, ni une mise à jour des paramètres.
2. **Objectif (Understand) :** \`loss\` prend le relais pour définir le scalaire obtenu après agrégation des pertes par token. Elle distingue correctement masque de visibilité et masque de contribution à l'objectif, ainsi que moyenne par token valide et autres réductions.
3. **Dérivation (Understand) :** \`gradients\` relie la loss aux logits puis aux paramètres par la règle de chaîne. La formule $p_i-\mathbb{1}[i=y]$ est locale aux logits ; elle ne constitue pas le backward du GPT complet.
4. **Implémentation (Build/G8) :** le code public fournit actuellement les fenêtres décalées, la cross-entropie moyenne et son gradient par rapport aux logits, ainsi qu'un forward GPT NumPy/float64. Il ne fournit pas encore le backward à travers les opérations et les paramètres du GPT, un optimiseur, une boucle d'entraînement, un runner de validation ou un checkpoint.
5. **Gate G8 :** la spécification #656 maintient une revue préalable des acquis comme condition d'entrée. Les audits de sources Wolfe et Raschka enrichissent les choix de conception, mais ne lèvent pas cette condition et ne justifient pas de commencer l'implémentation.
6. **Pas de duplication :** les pages existantes couvrent déjà les explications conceptuelles et les contrôles formatifs nécessaires. Aucun nouveau chapitre teacher forcing, aucune nouvelle fiche loss/gradient et aucun nouveau jalon ne sont justifiés par cette passe.

### Cohérence des relations et de la séquence

La relation pédagogique peut se lire :

\[
\text{Corpus tokenisé}
\rightarrow \text{Exemples entrée-cible}
\rightarrow \text{Forward GPT}
\rightarrow \text{Logits}
\rightarrow \text{Cross-entropy par cible}
\rightarrow \text{Loss agrégée}
\rightarrow \text{Gradient des logits}
\rightarrow \text{Backward à travers les paramètres}
\rightarrow \text{Mise à jour}
\]

Cette représentation décrit les dépendances de calcul, pas une séquence de lecture imposant de maîtriser tout G8 avant de comprendre l'inférence.

- \`training-examples\` fournit les entrées et cibles ; le forward produit des logits par position ; la loss compare ces logits aux cibles alignées.
- Le masque causal contrôle les informations visibles pendant le forward ; le masque de perte contrôle les cibles supervisées. Une cible ignorée peut malgré tout fournir une représentation utile à un autre calcul autorisé : une dérivée nulle sur ses propres logits ne coupe pas nécessairement tous les chemins du graphe.
- Le gradient de la loss par rapport aux logits est disponible dans \`losses.py\`. La règle de chaîne doit encore le propager à travers les opérations du GPT pour obtenir les gradients des paramètres.
- L'optimiseur transforme ces gradients en mises à jour ; il n'est ni la rétropropagation ni la loss.
- La validation mesure le comportement sur des données tenues à l'écart de l'optimisation ; elle ne remplace ni les tests de gradients ni la vérification de la bonne construction des exemples.
- Le checkpoint doit permettre de transférer les paramètres effectivement entraînés vers la boucle de génération. Il ne peut être revendiqué avant un test de sauvegarde, rechargement et génération.

### Décisions éditoriales

- **Conserver** les trois pages à leur niveau actuel : le contraste Understand/Build est utile et cohérent.
- **Ne pas déplacer** teacher forcing vers \`loss\` ou \`gradients\` : son propriétaire est la construction des exemples et son articulation avec l'inférence.
- **Ne pas transformer** la chaîne ci-dessus en nouveau parcours linéaire ou en nouvelle ontologie ; elle complète le graphe computationnel existant.
- **Maintenir** les détails d'optimiseur et de vérification numérique dans les approfondissements conceptuels tant que G8 n'a pas franchi sa gate.
- **Déférer** toute nouvelle leçon ou modification de code à la levée explicite du prérequis G8 et à une lacune démontrée.

### Validation et limites

La revue source FR/EN et le contrôle des frontières avec G8 sont effectués. La table des jalons et l'audit d'implémentation confirment les limites du code public ; ils ne constituent pas une revue scientifique indépendante ni une validation apprenant. La revue préalable privée de G8 n'est pas considérée comme satisfaite dans cette passe. Aucun code d'entraînement, backward, optimiseur ou checkpoint n'a été ajouté.
