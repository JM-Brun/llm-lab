# Audit pédagogique du parcours LLM — 2026-11-09

**Statut au 2026-11-09 :** huit passes de revue FR/EN couvrent l'entrée du site, le parcours Understand principal, le parcours Build et l'exercice d'évaluation. Les pages facultatives listées comme « À lire » restent à auditer en profondeur. Le rendu Quarto et l'audit navigateur ont réussi pour le lot principal #754 et pour le commit `4ca9088` du complément #760 ; les modifications de la passe I doivent encore être validées sur le commit courant. L'accessibilité manuelle et la validation avec un apprenant indépendant ne sont pas encore réalisées. Ce document distingue inventaire, lecture de source, validation technique et preuve pédagogique.

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
| Entrée du site | `index` | Orienter vers Understand, Build, Deepen et Practice ; rendre visibles les parcours et les preuves attendues | Page d'orientation, pas une leçon : les quatre portes d'entrée et la carte des notions remplissent la fonction de synthèse | Revue FR/EN effectuée |
| Orientation | `llm-overview` | Définir LLM/GPT/Transformer, situer le modèle pédagogique et annoncer le noyau prédictif ; conduire vers l'aperçu de génération | Ajout d'un rappel d'une minute FR/EN distinguant catégories, distribution conditionnelle, trois usages et architecture/apprentissage/utilisation | Revue FR/EN effectuée + synthèse ajoutée |
| Comparaison d'architectures (optionnel) | `transformer-architectures` | Comparer encodeur seul, encodeur-décodeur et décodeur seul ; distinguer architecture, objectif et tâche | Ajout d'un rappel d'une minute FR/EN ; le paragraphe de complexité est désormais un approfondissement replié, l'activité pratique reste explicitement facultative | Revue FR/EN effectuée + niveaux clarifiés |
| Aperçu d'inférence | `generation` | Donner la boucle complète avec paramètres fixes ; transition vers texte/tokens sans exiger les détails internes | Rappel d'une minute et self-check FR/EN ; aperçu du loop puis retour détaillé sur la même page canonique | Revue FR/EN effectuée |
| Entrée texte | `text-data` | Texte → tokens → IDs → lookup ; distinguer prompt d'inférence et corpus d'entraînement | Rappel bref et self-check présents ; vocabulaire nuancé pour ne pas présenter tout tokenizer comme doté d'un vocabulaire appris | Revue FR/EN effectuée |
| Stratégies de tokenisation | `tokenization-strategies` | Comparer unités, algorithmes et compromis ; préparer le passage des IDs aux vecteurs | Section « À retenir » et self-check présents ; le Deepen sur l'évaluation évite de surcharger Understand | Revue FR/EN effectuée |
| Unicode (optionnel) | `unicode-text` | Approfondissement sur encodage, normalisation et texte ; ne pas bloquer la route principale | Une fiche n'est pas requise si une courte conclusion et des liens suffisent | À lire |
| Embeddings | `embedding-space` | ID → ligne de matrice ; distinguer table statique, vecteur initial et états contextualisés | Rappel « une minute », exemple matriciel calculable et self-check présents ; transition vers position explicite | Revue FR/EN effectuée |
| Position | `positional-encoding` | Expliquer le besoin d'ordre, distinguer position explicite, RoPE et masque causal | Ajout d'un rappel « une minute » distinguant injection absolue/relative/RoPE et visibilité causale ; self-check existant conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Représentations contextualisées | `contextualized-representations` | Distinguer lookup initial et états dépendant du contexte ; conduire vers le calcul du Transformer | Ajout d'un rappel « une minute » distinguant ID, embedding initial, position, contexte et masque d'architecture ; self-check existant conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Tenseurs (optionnel) | `tensors` | Support de formes et opérations ; ne pas en faire un prérequis général | Vérifier que la fiche sert le Build / Deepen sans interrompre Understand | À lire |
| RoPE (optionnel) | `rope` | Approfondir la géométrie et les variantes positionnelles | Fiche de référence facultative ; vérifier les hypothèses et les conventions | À lire |
| Vue d'ensemble Transformer | `transformer` | Replacer les opérations dans le bloc et le forward pass, jusqu'aux logits | Ajout d'un rappel d'une minute FR/EN sur entrée, bloc, répétition et logits ; self-check conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Q/K/V | `queries-keys-values` | Projections depuis les états d'entrée de chaque bloc ; Q/K déterminent les poids, V fournit le contenu | Rappel enrichi FR/EN : projections, apprentissage conjoint, routage/contenu, invariance et périmètre ; self-check conservé | Revue FR/EN effectuée + synthèse renforcée |
| Attention | `scaled-dot-product-attention` | Scores, mise à l'échelle, softmax, agrégation ; réutiliser Q/K/V sans redéfinir leurs rôles | Rappel d'une minute, exemple numérique et self-check présents ; la page prend le relais exact des projections Q/K/V | Revue FR/EN effectuée |
| Masque causal | `causal-masking` | Contraindre l'accès au futur ; distinguer masque causal, padding et convention d'API | Rappel d'une minute, micro-vérification d'invariance et self-check ; distingue visibilité et contribution à la loss | Revue FR/EN effectuée |
| Cross-attention (optionnel) | `cross-attention` | Extension distincte, non requise pour le GPT décodeur seul | Garder l'optionnalité explicite ; pas de fiche imposée | À lire |
| Mise à l'échelle (optionnel) | `attention-score-scaling` | Dérivation et propriétés de la mise à l'échelle ; approfondissement après attention | Fiche courte facultative, surtout si elle aide à réactiver la dérivation | À lire |
| Logits | `logits` | Projection vocabulaire et scores non normalisés ; transition vers softmax | Rappel bref et self-check présents ; distingue classement, score et probabilité | Revue FR/EN effectuée |
| Probabilités | `probabilites` / `probabilities` | Softmax et distribution conditionnelle ; ne pas confondre probabilité et vérité | Rappel bref, exemple numérique, explorateur de température et self-check présents ; température présentée comme transformation de distribution, non comme apprentissage | Revue FR/EN effectuée |
| Entropie | `entropy` | Incertitude de la distribution prédictive ; distinguer entropie et score d'une cible observée | Ajout d'un rappel d'une minute FR/EN distinguant entropie prédictive, surprise observée, bornes et limites d'interprétation ; self-check conservé | Revue FR/EN effectuée + synthèse ajoutée |
| Génération détaillée | `generation` (réutilisée) | Revenir sur prefill, decode, cache, sélection, feedback et arrêt | Rappel bref et self-check présents ; distingue prefill/decode (phases) de decoding (règle de sélection) et du forward pass | Revue FR/EN effectuée |
| Stratégies avancées (optionnel) | `decoding-strategies` | Top-k/top-p, beam, contrastif, compromis et reproductibilité | Pas de rappel bref repéré dans le premier relevé ; à examiner après la route centrale | À lire |
| Vraisemblance | `vraisemblance` / `likelihood` | Scorer une cible observée, factoriser une séquence ; pas de sélection de token | Ajout d'un rappel d'une minute FR/EN distinguant scoring, règle de chaîne, log-vraisemblance, NLL et conventions de comparaison | Revue FR/EN effectuée + synthèse ajoutée |
| Entropie croisée | `cross-entropy` | Mesurer l'écart entre distribution prédite et cible ; relier au NLL | Ajout d'un rappel d'une minute FR/EN sur cible one-hot/générale, alignement, masques et réduction | Revue FR/EN effectuée + synthèse ajoutée |
| Loss | `loss` | Agréger les pertes token par token avec masque et réduction | Rappel d'une minute et self-check présents ; distingue perte locale, objectif de batch, masques, réduction et métriques | Revue FR/EN effectuée |
| Gradients | `gradients` | Dériver l'objectif et expliquer la mise à jour des paramètres | Rappel d'une minute et self-check présents ; distingue sensibilité locale, rétropropagation, SGD et choix d'optimiseur | Revue FR/EN effectuée |
| Parcours de construction | `build-path` | Ordonner les visites du code, jalons G0–G9, branche de données et preuves attendues | Tableau des jalons et statuts déjà synthétique ; distingue référence, implémentation partielle, plan conceptuel et critères non démontrés | Revue FR/EN effectuée |
| Corpus (branche Build) | `corpus-preparation` | Provenance, filtrage, déduplication, splits, tokenizer figé ; branche de données | Fiche de révision et self-check FR/EN ajoutés ; contrat de sortie et séparation corpus/tokenizer/exemples explicites | Revue FR/EN effectuée + fiche ajoutée |
| Exemples d'entraînement (branche Build) | `training-examples` | Fenêtres, cibles décalées, teacher forcing, packing/padding/masks ; rejoint G8 | Fiche de révision et self-check FR/EN ajoutés ; distingue teacher forcing, causal mask et loss mask ; contrat de formes et checklist de débogage | Revue FR/EN effectuée + fiche ajoutée |
| Évaluation / pratique | `evaluation-experimentale` et collections d'exercices | Évaluer une tâche et un protocole ; ne pas présenter l'exercice existant comme benchmark d'un GPT entraîné | Exercice autonome FR/EN relu : questions, grille de correction et auto-évaluation ; collection plus large encore à construire | Revue FR/EN effectuée |
| Catalogue d'exercices | `exercises` | Orienter vers les collections disponibles et distinguer self-checks et exercices multi-étapes | Registre des disponibilités relu ; statut de la collection Évaluation clarifié pour signaler l'exercice autonome déjà publié | Revue FR/EN effectuée |

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


## 12. Passe E — revue de l'apprentissage et de la branche Build (2026-11-09)

### Pages relues en français et en anglais

- `loss` : pénalité locale par token, objectif scalaire de batch, positions valides, décalage des cibles, masques, réductions, perplexité et diagnostic d'une courbe.
- `gradients` : dérivée de la cross-entropy par rapport aux logits, effet de la réduction, règle de chaîne, rétropropagation, mise à jour SGD et vérification par différences finies.
- `corpus-preparation` : provenance, parsing, filtrage, déduplication, splits, ajustement/fixation du tokenizer et contrat de sortie.
- `training-examples` : décalage entrée-cible, teacher forcing, fenêtres/stride, frontières documentaires, packing, padding, masques, formes et débogage.
- `build-path` : ordre des visites du code, jalons G0–G9, branche de données G1b/G2 et niveaux de preuve attendus.

### Décisions et modifications de cette passe

1. **Loss et gradients :** leurs rappels d'une minute et leurs auto-vérifications existent déjà en FR/EN ; pas de nouvelle fiche ni de duplication.
2. **Corpus et exemples :** les fiches opérationnelles et self-checks FR/EN ajoutés dans le lot précédent sont cohérents avec les contrats d'entrée/sortie de ces pages Build.
3. **Teacher forcing :** dans la page de vraisemblance FR/EN, ajout d'un lien explicite vers `training-examples`. Le même préfixe de référence est utilisé pour scorer une séquence et comme conditionnement pendant l'entraînement, mais le scoring ne sélectionne pas de token, ne réinjecte pas de prédiction et ne met pas à jour les paramètres.
4. **Aucune fiche distincte pour build-path :** cette page est un guide de réalisation et de preuve, pas une leçon conceptuelle. Son tableau de jalons et ses critères de vérification remplissent déjà une fonction de synthèse opérationnelle.

### Cohérence des transitions et du parcours Build

- La préparation du corpus et le tokenizer figé sont une branche de données ; ils ne sont pas des prérequis pour comprendre l'inférence depuis un prompt.
- La construction des exemples transforme le flux d'IDs en entrées/cibles alignées. Teacher forcing décrit le préfixe observé fourni au modèle ; le masque causal empêche l'accès au futur.
- Le masque d'attention contrôle la visibilité dans le forward pass ; le masque de perte contrôle les cibles qui contribuent à l'objectif. Une cible ignorée peut néanmoins influencer une représentation utilisée par une cible valide si le masque d'attention l'autorise : la distinction est explicitée dans loss/gradients.
- La cross-entropy donne les pénalités par cible ; loss les agrège selon une convention documentée ; gradients transportent la dérivée vers les paramètres ; l'optimiseur définit ensuite la mise à jour effective.
- Le guide Build rend explicite que G2 est une branche parallèle requise avant l'entraînement, mais non avant la génération.
- L'état du projet est présenté sans surpromesse : fenêtres et cibles décalées sont partiellement implémentées/testées ; packing, padding, batching et masques restent à construire ; le calcul de loss existe mais pas une boucle d'entraînement complète, un optimiseur ou un pipeline de validation automatisé.
- G9 (parité avec une référence indépendante compatible) et E1 (évaluation complète d'un GPT entraîné) sont des critères définis, pas des capacités déjà démontrées.

### Points de vigilance

- Ne pas présenter teacher forcing comme une règle de sélection du token, une fonction de perte ou une mise à jour de paramètres.
- Ne pas laisser entendre que le masque de perte empêche une fuite d'information dans le forward pass.
- Maintenir les conventions de réduction (somme, moyenne par token valide, moyenne par séquence) explicites dans tout résultat quantitatif.
- Le guide Build indique que le modèle de référence est initialisé aléatoirement : il démontre des mécanismes et des formes, pas une qualité de langage apprise.
- Les pages `build-path`, `loss` et `gradients` ne doivent pas être interprétées comme preuve d'un entraînement de bout en bout déjà disponible.

### Validation

Revue source FR/EN des pages conceptuelles et Build, vérification des contrats et des statuts de jalons effectuées. Les tests automatisés du dépôt ne remplacent pas une validation formative par apprenant ; le rendu navigateur et l'accessibilité restent à vérifier sur le dernier commit.


## 13. Passe F — revue de la page d'orientation et du noyau partagé (2026-11-09)

### Pages relues en français et en anglais

- `llm-overview` : définition de LLM, distinction LLM/GPT/Transformer, prédiction autorégressive, distribution conditionnelle, tronc computationnel partagé, usages génération/scoring/apprentissage, architecture/apprentissage/utilisation, adaptation et choix RAG/fine-tuning.

### Décisions et modifications de cette passe

1. **Synthèse initiale :** ajout d'un rappel d'une minute FR/EN, qui fixe les distinctions de catégorie, la distribution prédictive, les trois usages du même calcul et les trois dimensions descriptives d'un modèle.
2. **Teacher forcing :** reformulation FR/EN pour éviter d'en faire une phase d'inférence ou une étiquette indifférenciée du scoring. Le scoring d'une séquence connue et l'entraînement utilisent tous deux des préfixes de référence ; pendant l'entraînement, ce conditionnement est appelé teacher forcing.
3. **Pas de duplication du graphe :** la page réutilise les fragments générés du graphe computationnel partagé et de l'évaluation. La fiche résume le sens de ce graphe sans reproduire ses détails.
4. **Auto-vérification :** les deux questions existantes sont conservées ; elles testent déjà le choix RAG/fine-tuning et la distinction entre architecture et adaptation.

### Cohérence de l'entrée du parcours

`llm-overview → generation (aperçu) → text-data → … → generation (retour détaillé)`

- L'aperçu de génération sert de motivation initiale, pas de prérequis aux détails internes.
- La page d'orientation distingue désormais explicitement le forward pass partagé des trois usages et leurs effets sur les paramètres.
- Le retour détaillé à `generation` est une réutilisation de la même page canonique, pas une seconde leçon.
- La branche Build et les approfondissements restent des destinations parallèles ; ils ne sont pas présentés comme des étapes obligatoires avant de comprendre l'inférence.

### Points de vigilance

- La définition de LLM ne doit pas être réduite à un nombre de paramètres ou à une architecture unique.
- Les modèles de fondation, les GPT et les Transformers sont des catégories qui se recoupent, mais ne sont pas synonymes.
- L'aperçu du noyau partagé doit rester cohérent avec `docs/canonical-computational-spine.md` et les fragments générés ; ne pas recréer une chaîne linéaire qui fusionnerait génération, scoring et apprentissage.
- La page d'orientation est une vue d'ensemble : les équations, formes et détails de chaque mécanisme restent dans leurs pages propriétaires.

### Validation

Revue source FR/EN et cohérence avec le noyau computationnel effectuées. Rendu final et navigation générée à vérifier dans le workflow Quarto/browser en cours ; aucune validation apprenant n'est revendiquée.


## 14. Passe G — ressource de comparaison des architectures et exercice d'évaluation (2026-11-09)

### Pages relues en français et en anglais

- `transformer-architectures` : tableau comparatif, schéma de flux d'information, encodeur seul, encodeur-décodeur, décodeur seul, distinction architecture/objectif/tâche, architectures hybrides et compromis de complexité.
- `evaluation-experimentale` / `experimental-evaluation` : exercice de transfert sur le protocole d'évaluation d'un classement de passages scientifiques, avec estimande, dépendances, fuite, sélection de modèle, AP, calibration, incertitude et reproductibilité.

### Décisions et modifications de cette passe

1. **Architectures Transformer :** ajout d'une synthèse FR/EN des trois configurations et de la distinction architecture/objectif/tâche.
2. **Séparation des niveaux :** le paragraphe sur la complexité asymptotique, le parallélisme et les dépendances séquentielles est conservé intégralement mais placé dans un callout replié « approfondissement ». La comparaison principale reste lisible sans imposer le niveau Deepen.
3. **Pratique :** la comparaison pratique BERT/GPT-2/T5 reste un renvoi facultatif séparé, explicitement hors du parcours conceptuel et du Build.
4. **Évaluation expérimentale :** pas de fiche « une minute » ajoutée. La page est un exercice de transfert : l'énoncé, les questions, la grille de correction et l'auto-évaluation forment déjà un dispositif complet de révision active.

### Cohérence

- La page architectures est une ressource facultative liée depuis le panorama ; elle ne devient pas un prérequis avant la génération.
- Le résumé fixe les distinctions nécessaires avant que le lecteur explore les détails ou l'activité pratique.
- Le contenu de complexité conserve son lien vers le guide spécialisé, sans interrompre la comparaison des flux d'information.
- L'exercice d'évaluation intervient après les fondations et les exercices ; il teste le transfert vers un protocole scientifique, pas la construction du GPT pédagogique.
- L'AP, la calibration et l'incertitude sont traitées comme des dimensions d'évaluation distinctes de la loss d'entraînement.

### Validation

Revue source FR/EN effectuée. La page d'architecture a été réorganisée sans suppression de contenu ; les liens et le rendu responsive du tableau restent à vérifier dans le navigateur. L'exercice d'évaluation est vérifié comme ressource pédagogique, pas comme résultat expérimental.


## 15. Passe H — point d'entrée, catalogue d'exercices et ressources de transfert (2026-11-09)

### Pages relues en français et en anglais

- `index` : portes d'entrée Understand/Build/Deepen/Practice, carte des notions, repères épistémiques, schéma interactif des processus et liens vers les ressources.
- `exercises` : registre des collections, prérequis, disponibilité, exercices corrigés et séparation entre self-checks courts et exercices approfondis.
- `evaluation-experimentale` / `experimental-evaluation` : exercice autonome de transfert évaluant la conception d'un protocole, sans implémenter ni rapporter un benchmark.

### Décisions et modifications de cette passe

1. **Point d'entrée :** aucune fiche de révision ajoutée à la page d'accueil. Sa fonction est de choisir un parcours et de rendre visibles les relations et les niveaux de preuve ; un résumé conceptuel y serait redondant avec `llm-overview`.
2. **Catalogue d'exercices :** clarification de la ligne « Évaluation » FR/EN. Un exercice autonome est déjà publié, tandis que la collection complète (baselines, métriques, contamination, incertitude et analyse d'erreurs) reste à construire.
3. **Exercice d'évaluation :** pas de fiche additionnelle ; les questions, la grille de correction et l'auto-évaluation constituent déjà un cycle de rappel actif et de transfert.
4. **Parcours Build :** le tableau G0–G9 est conservé comme synthèse opérationnelle. Il distingue clairement ce qui est testé, partiellement implémenté, planifié ou non démontré.

### Cohérence globale observée

- Le site commence par des portes d'entrée non linéaires, puis le parcours Understand fournit la progression conceptuelle ; Build et Deepen restent des voies complémentaires.
- Les self-checks intégrés aux pages servent la récupération immédiate ; le catalogue regroupe les exercices multi-étapes et les transferts. Il ne faut pas les fusionner en une seule collection de quiz.
- La page d'évaluation pratique est accessible depuis l'accueil et l'exercice hub, mais n'est pas présentée comme un benchmark du petit GPT.
- Les statuts d'implémentation du Build et de disponibilité des exercices restent explicites : la présence d'une page ou d'un exercice ne prouve pas qu'un pipeline complet existe.

### État de couverture à ce stade

- **Revu FR/EN et transitions vérifiées :** entrée, panorama, architectures principales, représentation, Transformer/attention, prédiction, scoring, objectif de perte, gradients, corpus, exemples d'entraînement, Build path et exercice de protocole expérimental.
- **À poursuivre comme ressources facultatives :** Unicode, tenseurs, RoPE, cross-attention, mise à l'échelle détaillée, variantes de décodage, histoire, limites des LLM, fondements mathématiques, complexité et activité pratique des trois architectures.
- **À valider techniquement :** rendu final et navigation des pages modifiées, liens générés, interaction des schémas et tableaux responsive, clavier et lecteur d'écran.
- **À valider pédagogiquement :** test de parcours par un lecteur indépendant, notamment capacité à reconstruire le tronc computationnel et à distinguer génération, scoring et apprentissage sans consulter les fiches.

### Validation

Revue des pages d'entrée et du catalogue FR/EN effectuée. Le workflow Quarto/browser du lot précédent est encore en cours au moment de cette mise à jour ; le nouveau lot doit être validé sur son propre commit. Aucun test utilisateur n'est revendiqué.


## 16. Passe I — architecture conceptuelle et approfondissements facultatifs (2026-11-09)

### Pages et ressources relues

- `index` FR/EN : représentation d'ensemble des processus et frontière entre scoring et évaluation.
- `tensors` FR/EN : rôle de référence technique, place dans le parcours et parité linguistique.
- `decoding-strategies` FR/EN : transformations de distribution, recherche de séquences et compromis.
- `llm-limits` FR/EN : limites de l'objectif prédictif, définition de la compréhension et interprétation des capacités émergentes.

### Décisions éditoriales et conceptuelles

1. **Scoring rendu explicite sur la page d'accueil :** le texte d'introduction et un rappel placé après le schéma identifient trois usages frères du calcul prédictif : génération, scoring et apprentissage. Le rappel précise les paramètres fixes pour génération/scoring, la mise à jour pour l'apprentissage et le statut transversal de l'évaluation.
2. **Pas de quatrième branche « évaluation » :** l'évaluation agrège des mesures sous un protocole ; elle peut réutiliser le scoring sur des données tenues à l'écart et peut aussi porter sur des sorties générées. Elle n'est pas une opération homologue à génération, scoring et apprentissage.
3. **Schéma d'accueil conservé :** le diagramme interactif existant détaille les boucles de génération, d'apprentissage et le processus d'évaluation. Plutôt que d'étendre le SVG et d'en augmenter fortement la hauteur, le scoring est distingué dans un rappel adjacent. Cette solution évite de surcharger le point d'entrée ; une représentation visuelle intégrée pourra être réévaluée si elle apporte un bénéfice pédagogique démontré.
4. **Parité `tensors` :** le rappel « Place dans le parcours » est ajouté en français, aligné sur le contenu anglais. La page reste une référence Deepen facultative et n'est pas promue au rang de prérequis général du Build.
5. **`decoding-strategies` :** ajout d'un rappel FR/EN qui distingue transformation locale de distribution et recherche de séquence, et résume température, top-k/top-p, greedy/beam et limites. Les détails, exemples, implémentation et références sont conservés.
6. **`llm-limits` :** ajout d'un rappel FR/EN qui sépare vérité, calibration, compétence opérationnelle et émergence mesurée. Les sources et les auto-vérifications existantes sont conservées.

### Cohérence des relations

- La génération sélectionne et réinjecte une prédiction ; le scoring attribue une probabilité à une cible observée à partir de préfixes connus ; l'apprentissage utilise des cibles pour calculer une loss et mettre à jour les paramètres.
- Le teacher forcing est un mode de conditionnement sur les préfixes de référence pendant l'entraînement ; le fait que le scoring utilise également des préfixes observés ne transforme pas le scoring en entraînement.
- Le prefill et le decode restent des phases d'inférence ; les stratégies de décodage transforment la distribution ou recherchent des séquences, sans constituer une mise à jour des paramètres.
- L'évaluation reste une démarche expérimentale transversale, avec choix des données, baselines, métriques, contrôles, incertitude et analyse d'erreurs.

### Validation et limites

- Revue de source FR/EN effectuée pour les pages listées.
- Le workflow Quarto/browser sur le commit précédent du PR #760 a réussi, y compris la revue Playwright ciblée. Cette réussite ne valide pas automatiquement les modifications de cette passe, qui doivent être testées sur leur propre commit.
- Rendu Quarto, liens locaux, navigation au clavier et captures de cette nouvelle passe restent à vérifier.
- Aucun test avec apprenant indépendant n'est revendiqué.
