# Issue #1739 — matrice consolidée des contributions du parcours Understand

**Date de consolidation :** 2026-11-27  
**Périmètre :** leçons canoniques du parcours principal définies par `data/guided-route.yml`, une ligne par sujet bilingue. Les dossiers de lots et pilotes restent les preuves détaillées ; ce document est leur index de couverture, pas un registre de connaissances supplémentaire.

## 1. Matrice de couverture page par page

| Étape canonique | Leçon FR / EN | Apports distinctifs à préserver | Preuve détaillée / état de l'audit source |
|---|---|---|---|
| Orientation | `llm-overview` | Une distribution prédictive commune à trois usages ; distinction LLM / Transformer / GPT ; axes indépendants architecture, apprentissage, utilisation ; poids ≠ base documentaire ; transfert non automatique. | [Audit panorama et entrée texte](understand-overview-text-input-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Entrée texte | `text-data` | Token ≠ mot ; ID local au vocabulaire et non quantitatif ; contrat tokenizer–poids couvrant vocabulaire et conventions ; exemples de segmentation/Unicode ; longueur de tokens ≠ qualité linguistique ; prompt encoding ≠ préparation du corpus. | [Audit panorama et entrée texte](understand-overview-text-input-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Représentations | `embedding-space` | Lookup d'une ligne par ID ; égalité des occurrences répétées à table fixée ; invariance sous renumérotation cohérente des IDs et des lignes ; limites d'interprétation géométrique. | [Pilote embeddings et matrice des destinations](embedding-space-intellectual-contributions-pilot-2026-11.md) (PR #1794). L'invariance de renumérotation est développée dans le contrat tokenizer–modèle, Practice et la fiche de révision, pas dans la leçon core. |
| Représentations | `positional-encoding` | Taxonomie par point d'insertion (entrée, score/valeurs, biais, rotations Q/K) ; information positionnelle ≠ visibilité causale ; computabilité d'un encodage ≠ généralisation en longueur. | [Audit représentations](understand-representations-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Représentations | `contextualized-representations` | Même ID et même embedding initial, mais états cachés dépendants du préfixe ; frontière causale sur le futur ; contextualisation ≠ géométrie sémantique propre ou interprétation garantie d'une tête. | [Audit représentations](understand-representations-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Calcul | `transformer` | Distinguer passe avant du réseau et boucle de génération ; situer attention, MLP position-wise, résidus, normalisations et projection de sortie ; préciser la variante pré-LN illustrée sans universaliser l'architecture. | [Journal d'audit — Transformer/QKV/attention](../page-audit-inventory.md#2026-11-26-main-understand-route--transformer-block-qkv-and-causal-attention), 2026-11-26. |
| Calcul | `queries-keys-values` | Q/K déterminent les compatibilités ; V transporte le contenu agrégé ; projections calculées à l'intérieur de chaque bloc à partir de ses états d'entrée ; distinction self-attention/cross-attention ; RoPE après projection Q/K. | [Matrice de contributions et destinations Q/K/V](qkv-four-source-comparison-2026-11.md) (PR #1794), [pilote Q/K/V #1739](https://github.com/JM-Brun/llm-lab/pull/1740) et [journal d'audit](../page-audit-inventory.md#2026-11-26-main-understand-route--transformer-block-qkv-and-causal-attention). |
| Calcul | `scaled-dot-product-attention` | Séparer scores, scaling, masque, softmax sur les positions de clés et agrégation de V ; distinguer softmax d'attention et softmax vocabulaire ; poids ≠ pertinence sémantique ni attribution causale. | [Pilote pédagogique attention et matrice des destinations](scaled-dot-product-attention-learning-page-pilot-2026-11.md) (PR #1794) et [journal d'audit](../page-audit-inventory.md#2026-11-26-main-understand-route--transformer-block-qkv-and-causal-attention). |
| Calcul | `causal-masking` | Autoriser j ≤ i et bloquer j > i ; diagonale autorisée avec cibles décalées ; distinguer causal, padding, frontière documentaire et loss masks ; conventions boolean API dépendantes de la fonction. | [Journal d'audit — Transformer/QKV/attention](../page-audit-inventory.md#2026-11-26-main-understand-route--transformer-block-qkv-and-causal-attention), et audit Practice 2026-11-25. |
| Prédiction | `logits` | Projection de l'état final vers une classe par token du vocabulaire ; logits ≠ probabilités ni vérité ; invariance par décalage commun ; axes batch/temps/vocabulaire. | [Journal d'audit — logits, probabilités et entropie](../page-audit-inventory.md#2026-11-26-main-understand-route--logits-probabilities-and-predictive-entropy), 2026-11-26. |
| Prédiction | `probabilites` / `probabilities` | Softmax sur l'axe vocabulaire ; normalisation ≠ calibration ni vérité ; distinguer softmax sur positions et sur tokens ; température/top-k/top-p relèvent de la politique de décodage, pas de la distribution brute. | [Journal d'audit — logits, probabilités et entropie](../page-audit-inventory.md#2026-11-26-main-understand-route--logits-probabilities-and-predictive-entropy), 2026-11-26. |
| Prédiction | `entropy` | Entropie prédictive sur toute la distribution ≠ surprisal d'une cible observée ≠ cross-entropy ; faible entropie ≠ vérité ou calibration. | [Journal d'audit — logits, probabilités et entropie](../page-audit-inventory.md#2026-11-26-main-understand-route--logits-probabilities-and-predictive-entropy), 2026-11-26. |
| Inférence | `generation` | Forward pass → distribution ; décodage → sélection ; génération → boucle et arrêt ; choix local modifie le préfixe futur sans maximiser la vraisemblance globale ; paramètres fixes ; prefill/decode/KV cache situés comme phases/optimisations. | [Audit génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md), 2026-11-27 ; audit Practice 2026-11-25. |
| Usage du contexte | `in-context-learning` | Adaptation conditionnée par les démonstrations à paramètres fixes ; portée du terme ICL variable selon les travaux ; ICL ≠ fine-tuning ni RAG ; imitation de format ≠ généralisation ; induction heads = mécanisme partiel, non universel. | [Audit contexte](understand-context-use-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Usage du contexte | `context-engineering` | Trois niveaux : informations disponibles au système, séquence transmise/fenêtre, positions accessibles ; stocké/récupéré ≠ transmis ; fenêtre plus grande ≠ meilleure réponse ; provenance et injection indirecte ; sélection/organisation/sécurité/évaluation. | [Audit contexte](understand-context-use-intellectual-contributions-audit-2026-11.md), 2026-11-27. |
| Scoring | `vraisemblance` / `likelihood` | Factorisation autorégressive sur préfixes de référence sans hypothèse d'indépendance ; scoring ≠ sélection ; greedy local ≠ maximum de vraisemblance de séquence ; perplexité dépend du tokenizer, corpus et agrégation. | [Audit génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md), 2026-11-27 ; audit Practice 2026-11-25. |
| Scoring | `cross-entropy` | NLL d'une cible one-hot ; coût d'une prédiction confiante mais erronée ; gradient local p−y ; cibles souples et lien KL dans Deepen ; stabilité numérique et contrats d'API bornés. | [Pilote cross-entropy et matrice des destinations](cross-entropy-intellectual-contributions-pilot-2026-11.md) (PR #1794). |
| Apprentissage | `loss` | Indexation par position cible et décalage ; erreur d'alignement pouvant produire une loss plausible pour la mauvaise tâche ; teacher forcing comme conditionnement ; masque de loss ≠ masque d'attention ; réduction et dénominateur explicités. | [Audit génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md), 2026-11-27 ; audit Practice 2026-11-25. |
| Apprentissage | `gradients` | Gradient logits p−y ; règle de chaîne ; gradient ≠ update ; après update, nouvelle passe avant ; position exclue comme cible peut encore transmettre un gradient indirect via clés/valeurs d'une position supervisée. | [Audit génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md), 2026-11-27 ; audit gradient 2026-11-25. |
| Apprentissage | `training-loop` | Seule l'étape de l'optimiseur modifie les paramètres ; distinguer gradient, optimiseur et taux d'apprentissage ; validation à paramètres fixes sans update ; une étape stochastique ne garantit pas une baisse de loss. | [Audit génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md), 2026-11-27 ; audit gradient 2026-11-25. |

## 2. Ce que cette matrice signifie — et ne signifie pas

- **Couverture source :** chaque sujet canonique du parcours Understand est associé à une contribution identifiée et à une preuve d'audit ou un pilote. Pour les lots 2026-11-27, les sources FR/EN ont été relues individuellement ; pour les lots antérieurs, les dossiers datés cités sont la preuve de référence.
- **Pas de certification de rendu :** plusieurs audits sont source-only. Aucun statut « validé » ne doit être déduit de la seule présence d'un dossier ou d'un workflow CI.
- **Pas de quota :** deux ou trois apports sont une cible indicative. La matrice consigne les contributions réellement présentes ; elle n'invente pas une idée supplémentaire pour chaque page.
- **Pas de duplication :** les dossiers détaillés conservent preuves, localisations, limites et décisions. Cette matrice sert à l'orientation et à vérifier la couverture, pas à remplacer les extractions ou le graphe.
- **Traçabilité des destinations :** les dossiers des quatre familles `embedding-space`, `queries-keys-values`, `scaled-dot-product-attention` et `cross-entropy` disposent maintenant d'une matrice de présence FR/EN, de pages et d'ancres courantes dans PR #1794. Les **16 autres leçons Understand** n'ont pas encore été vérifiées à ce niveau. Le contrôle 20/20 ci-dessous porte uniquement sur l'identité des pages, pas sur la complétude de leur traçabilité source → claim → destination.

## 3. Contrat de modélisation retenu

Les représentations existantes répondent à des questions distinctes et doivent rester séparées :

| Représentation | Ce qu'elle décrit | Rôle dans l'audit |
|---|---|---|
| `data/sources.yml` et `data/extractions/<source-id>.yml` | Identité des sources et contributions atomiques avec preuves/localisateurs, concepts, appréciations et décisions d'usage. | Traçabilité des idées dérivées de sources ; une extraction ne doit pas être confondue avec l'apport éditorial final d'une page. |
| Dossiers `docs/source-syntheses/` et journal `docs/page-audit-inventory.md` | Comparaison, synthèse éditoriale, choix de placement et conservation des apports par page ou groupe. | Localisation de l'inventaire de contributions et justification des décisions. |
| `data/concepts.yml` | Entités scientifiques canoniques, indépendantes de la langue, et leurs ressources/relations. | Relier les idées aux concepts sans créer un concept par contribution éditoriale. |
| `data/computational-graph.yml` | Opérations, données, contraintes, modes et boucles de calcul. | Vérifier la justesse computationnelle ; ne pas y stocker des qualités éditoriales. |
| `data/guided-route.yml` | Ordre et objectifs pédagogiques, branches et contrats de leçons. | Vérifier la progression et les usages de la distribution ; ne pas en faire le graphe de calcul. |
| `LLM-LAB-PAGE-MAP v1` | Scope, purpose, navigation, hiérarchie et associations d'une page publiée. | Définir la responsabilité pédagogique de la page ; ne pas ajouter un champ de contributions redondant. |

Le document architectural transmis avec cette tâche formule le même invariant : le graphe de connaissances décrit les relations, le graphe computationnel ce qui se calcule, et le parcours l'ordre d'apprentissage. Ils communiquent sans devenir interchangeables.

### Décision sur le schéma

**Ne pas ajouter de champ `intellectual_contributions` à `LLM-LAB-PAGE-MAP v1` à ce stade.** Les pilotes et les lots n'ont pas montré de besoin transversal justifiant une migration de toutes les pages. Un tel champ mélangerait contenu éditorial, provenance source et relations conceptuelles ; il risquerait de devenir une liste redondante avec `purpose`, les ressources de concepts et les extractions.

La limite actuelle est plutôt documentaire : l'identité des apports propres à une page doit être retrouvable dans les dossiers d'audit et, lorsque l'apport est dérivé d'une source, reliée aux extractions atomiques. Le présent index ferme la lacune de découverte sans créer un registre exécutable parallèle.

**Règle de conservation :** lors d'une refonte, ne supprimer ni déplacer un apport inventorié sans décision explicite, destination précise et vérification FR/EN. Une modification de `purpose` n'est pas une preuve que les apports distinctifs ont été préservés.

## 4. Vérifications restantes

1. **Rendu et accessibilité :** compléter les vérifications Quarto/browser, mobile, figures, formules, navigation, clavier et lecteur d'écran. Les audits source du 27 novembre ne les remplacent pas.
2. **Revue de chaque page dans le navigateur :** vérifier que les apports recensés sont réellement visibles, compréhensibles et non masqués par des accordéons ou une surcharge de premier écran.
3. **Traçabilité des contributions dérivées du projet :** si un apport résulte d'une démonstration, d'une conséquence mathématique ou d'une synthèse interne, le dossier doit le marquer `project-derived`, documenter ses prémisses et son raisonnement, puis vérifier sa destination ; ne pas inventer un item source.
4. **Maintenance :** toute création, scission, fusion ou refonte d'une leçon du parcours doit ajouter/mettre à jour sa ligne dans cette matrice et vérifier les destinations des apports déplacés.
5. **Périmètre :** les pages facultatives/deepen, les pages Build et les collections Practice ne sont pas toutes incluses dans la matrice Understand ; elles peuvent avoir leurs propres audits de contributions sans être artificiellement ajoutées au parcours canonique.

## 5. Références de méthode et de modèle

- [Issue #1739 — valeur ajoutée intellectuelle distinctive](https://github.com/JM-Brun/llm-lab/issues/1739)
- [Contrat des métadonnées de page](../page-metadata-schema.md)
- [Méthode de synthèse des sources](../source-synthesis-method.md)
- [Audit des contributions du panorama et de l'entrée texte](understand-overview-text-input-intellectual-contributions-audit-2026-11.md)
- [Audit des contributions des représentations](understand-representations-intellectual-contributions-audit-2026-11.md)
- [Audit des contributions génération/scoring/apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md)
- [Audit des contributions autour du contexte](understand-context-use-intellectual-contributions-audit-2026-11.md)


## 6. Contrôle de couverture par rapport au parcours canonique

Un contrôle de cohérence a comparé les pages requises de chaque étape de `data/guided-route.yml` (champ `pages.fr`, en excluant volontairement `optional_pages`) aux identifiants de page de cette matrice.

- **20 pages Understand requises** dans le parcours.
- **20/20 identifiants retrouvés** dans la matrice.
- **Aucune page requise manquante.**
- Les pages optionnelles, pages Deepen, Build et Practice ne sont pas comptées dans ce contrôle : elles relèvent d'audits complémentaires et ne doivent pas être assimilées aux leçons canoniques du parcours.

Ce contrôle vérifie la couverture des identifiants, pas la qualité du contenu, la visibilité effective des apports ou leur rendu. Il devra être rejoué à chaque modification de `data/guided-route.yml`.


### Portée de cette décision par rapport aux autres extensions PAGE-MAP

La conclusion ci-dessus est **spécifique à la modélisation des contributions intellectuelles** : les sources, extractions, dossiers de synthèse et relations conceptuelles suffisent ; un champ `intellectual_contributions` serait redondant.

Elle ne constitue pas une interdiction générale d'étendre PAGE-MAP v1. L'audit distinct du contrat PAGE-MAP daté du 27 novembre autorise en principe des extensions additives facultatives, si chaque champ est documenté, validé et testé dans ses consommateurs. Son cas d'usage `estimated_reading_minutes` répond à une autre question éditoriale et doit suivre son propre contrat et sa propre calibration.

Il faut donc appliquer une règle de décision par usage : **ne pas ajouter un champ parce qu'une dimension éditoriale est intéressante ; l'ajouter uniquement si aucune représentation existante ne répond au besoin et si tous ses consommateurs sont explicitement pris en charge.** Les décisions « pas de champ pour les contributions » et « extension facultative possible pour une durée de lecture » sont compatibles.
