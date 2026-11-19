# Audit ciblé — documentation Hugging Face et implémentations BPE

**Date d'inspection :** 2026-11-18  
**Périmètre :** documentation officielle Hugging Face Tokenizers, code public de `openai/tiktoken` et `karpathy/minbpe`.  
**Nature :** inspection statique de documentation et de chemins de code ; aucune exécution, aucun benchmark ni test de compatibilité n'a été réalisé.

## Synthèse

Les trois ressources répondent à des questions différentes et ne doivent pas être traitées comme trois spécifications équivalentes :

- **Hugging Face Tokenizers** documente une architecture de pipeline configurable : normalisation, pré-tokenisation, modèle, post-traitement ; le décodage est traité comme le chemin inverse/une opération associée. La documentation décrit les responsabilités et les points d'extension, pas un comportement universel identique à tous les tokenizers.
- **tiktoken** est une bibliothèque BPE orientée production. L'API Python délègue le cœur d'encodage à l'extension native `_tiktoken.CoreBPE`; les encodages concrets combinent une expression de pré-découpage, des rangs de tokens fusionnables et un ensemble de tokens spéciaux. L'API rend explicite la politique d'autorisation/interdiction des chaînes de tokens spéciaux.
- **minbpe** est une implémentation pédagogique Python. `BasicTokenizer` expose le BPE byte-level sans pré-découpage regex ni tokens spéciaux ; `RegexTokenizer` ajoute ces conventions ; `GPT4Tokenizer` reconstruit les fusions d'un encodage tiktoken pré-entraîné et traite une permutation historique des 256 octets de base.

La différence importante n'est donc pas « BPE contre autre BPE », mais le niveau d'abstraction et les conventions autour du cœur de fusion : unités initiales, pré-tokenisation, rangs, vocabulaire, tokens spéciaux, décodage et optimisation.

## 1. Hugging Face Tokenizers — pipeline

**Source publiée :** [The tokenization pipeline](https://huggingface.co/docs/tokenizers/python/latest/pipeline.html)  
**Source de code de la documentation consultée :** `huggingface/tokenizers`, commit `1a9ec50b1cdf1cf97da689aad32003aa73d49755` (2026-11-18), fichier `docs/source-doc-builder/pipeline.mdx`.

La page décrit quatre étapes d'encodage :
1. **Normalization** : transforme éventuellement la chaîne (casse, Unicode, accents, espaces). Modifier cette étape peut nécessiter de réentraîner le tokenizer.
2. **Pre-tokenization** : découpe le texte en segments qui bornent les unités auxquelles le modèle pourra appliquer ses règles ; les offsets relient les segments à la chaîne d'origine.
3. **Model** : applique les règles et le vocabulaire appris ; les modèles cités incluent BPE, Unigram, WordLevel et WordPiece.
4. **Post-processing** : transforme l'encodage final, par exemple en ajoutant des tokens spéciaux de séquence.

Le décodage est documenté séparément. Il ne faut donc pas présenter la liste des quatre étapes d'encodage comme une liste exhaustive incluant le decoder. Les composants sont configurables et leurs effets sont dépendants de leur configuration.

**Apport utile pour le projet :** la séparation entre pipeline, algorithme de segmentation et conventions de décodage est déjà présente dans les pages bilingues. La documentation confirme la structure et ses responsabilités ; elle ne justifie pas une extraction atomique supplémentaire à ce stade, car les éléments sont déjà couverts et aucune garantie nouvelle n'a été identifiée.

**Limites :** documentation vivante, sans révision immuable garantie par l'URL `latest` ; l'inspection ne couvre ni toutes les API d'alignement/offsets, ni les bindings, ni les comportements de chaque composant.

### Vérification des bindings, offsets et limites de version

Le commit documentaire inspecté (`1a9ec50b1cdf1cf97da689aad32003aa73d49755`) contient un avertissement important qui doit accompagner toute lecture générale du pipeline :

- `pipeline.mdx`, `components.mdx` et `quicktour.mdx` avertissent que les bindings `rc0` ne permettent alors que de charger un `tokenizer.json`, puis d'encoder et décoder. Construire un tokenizer depuis ses composants, le modifier, le sauvegarder et l'entraîner ne sont pas exposés dans ces bindings.
- `api/encoding.mdx` annonce explicitement que `offsets`, `tokens`, `sequence_ids`, `word_ids`, `overflowing` et plusieurs autres attributs ne sont pas encore disponibles dans les bindings `rc0`.
- `api/tokenizer.mdx` indique de même que les propriétés `decoder`, `model`, `normalizer`, `post_processor` et `pre_tokenizer` ne sont pas encore exposées en lecture dans ces bindings ; les pages d'API des normalizers, pre-tokenizers et decoders portent elles aussi un avertissement de documentation de référence non encore générée.
- `REQUIRED_FOR_V1.md` décrit des éléments retirés ou en attente de réintroduction avant 1.0 : setters, écriture de `tokenizer.json`, constructeurs, truncation/padding et tests. Le document signale notamment que la pipeline peut actuellement ignorer silencieusement une configuration de truncation/padding lue depuis `tokenizer.json`. Ce point est une limite documentée de cette révision, pas une affirmation sur toutes les versions de Tokenizers.

Une incohérence documentaire ciblée mérite d'être conservée comme réserve : le quicktour donne un exemple d'accès à `output.offsets`, alors que la page de référence `api/encoding.mdx` dit que cet attribut n'est pas disponible dans les bindings `rc0`. L'exemple d'offset illustre en outre deux référentiels d'indexation : Python montre `(26, 27)` pour l'emoji dans la chaîne Unicode, tandis que Rust montre `(26, 30)` pour les octets UTF-8. Les valeurs ne doivent pas être comparées sans préciser le référentiel et le langage.

**Conséquence pour le projet :** citer la documentation du pipeline pour expliquer l'architecture conceptuelle, mais ne pas en déduire que toutes les opérations décrites sont exposées dans chaque binding/version. Pour un usage pratique, consigner la version de Tokenizers, le langage, le type d'offset (caractères/octets) et la disponibilité effective des API. Les offsets sont un point de vérification prioritaire dans un futur audit exécuté.


### Comparaison de versions documentaires — 2026-11-19

Une vérification supplémentaire distingue maintenant explicitement les documentations stables et non versionnées :

- La page versionnée [Tokenizers v0.23.3 — pipeline](https://huggingface.co/docs/tokenizers/v0.23.3/en/pipeline) décrit les quatre étapes d'encodage (normalization, pre-tokenization, model, post-processing), puis le décodage dans une section distincte. Son sélecteur de version indique qu'une version plus récente, v1.0.0-rc.4, est disponible.
- La page non versionnée [Tokenizers — pipeline](https://huggingface.co/docs/tokenizers/pipeline) affiche un avertissement relatif aux bindings « rc0 » : ils chargent un `tokenizer.json` et exposent l'encodage/décodage, mais pas la construction d'un tokenizer à partir de composants, sa modification, sa sauvegarde ni son entraînement. Ne pas transformer cette réserve de version en propriété générale de la bibliothèque.
- Les pages de composants précisent que le normaliseur est optionnel et que le modèle est le seul composant obligatoire. Le pré-tokenizer peut également modifier la chaîne, pas seulement la découper ; ByteLevel remappe notamment les octets vers des caractères visibles.
- La documentation indique que changer normalisation ou pré-tokenisation peut imposer un réentraînement, tandis que modifier le post-processor n'en impose pas. Cette distinction est un conseil lié au modèle et à sa configuration, pas une garantie universelle pour toute bibliothèque.
- Le pipeline conceptuel reste cohérent entre les pages versionnée et non versionnée. En revanche, les garanties de disponibilité des API, les offsets et les bindings doivent être attribués à une version et à un langage précis.

**Conséquence documentaire :** conserver la page versionnée v0.23.3 comme référence stable pour les explications d'API historiques ; utiliser l'URL non versionnée uniquement avec la date et l'avertissement de bindings. Aucun test d'exécution n'a été effectué dans cette vérification, et aucune compatibilité entre versions n'est revendiquée.

## 2. tiktoken — production et module éducatif

**Dépôt :** [openai/tiktoken](https://github.com/openai/tiktoken)  
**Révision inspectée :** `79dc2c0533685b893616c78160b5d9e40876e724` (2026-11-08).

Chemins inspectés : `tiktoken/core.py`, `tiktoken/_educational.py`, `tiktoken_ext/openai_public.py`.

### Chemin de production

- `Encoding` reçoit un `pat_str`, un dictionnaire `mergeable_ranks` (séquences d'octets vers rangs/IDs) et un dictionnaire distinct de `special_tokens`.
- Le cœur Python instancie `_tiktoken.CoreBPE` : l'algorithme central est exécuté dans l'extension native, et non par la boucle Python pédagogique.
- `encode()` contrôle explicitement les chaînes correspondant aux tokens spéciaux : par défaut, les tokens spéciaux non autorisés déclenchent une erreur ; `allowed_special` et `disallowed_special` modifient ce comportement.
- Les configurations publiques définissent des expressions de pré-découpage, des fichiers de rangs et les tokens spéciaux propres à chaque encodage. Un nom d'encodage désigne donc une configuration précise, pas un vocabulaire BPE générique.

### Module éducatif

`_educational.py` rend l'algorithme visible en Python : expression regex, conversion UTF-8 en octets, initialisation des 256 octets, recherche répétée de la paire fusionnable de rang minimal, reconstruction des octets et décodage. Il peut afficher les fusions intermédiaires et charger les rangs d'un encodage existant.

Ce module est explicitement pédagogique : il ne faut pas le confondre avec le chemin natif optimisé utilisé par la bibliothèque. Il travaille sur les rangs fusionnables et ne reproduit pas à lui seul la politique de tokens spéciaux de l'API de production.

## 3. minbpe — décomposition pédagogique des variantes

**Dépôt :** [karpathy/minbpe](https://github.com/karpathy/minbpe)  
**Révision inspectée :** `1acefe89412b20245db5a22d2a02001e547dc602` (2024-04-22).

Chemins inspectés : `minbpe/base.py`, `minbpe/basic.py`, `minbpe/regex.py`, `minbpe/gpt4.py`.

- **BasicTokenizer** : part des octets UTF-8 et apprend les fusions sur les paires adjacentes ; le code précise qu'il ne gère ni le pré-découpage regex ni les tokens spéciaux.
- **RegexTokenizer** : ajoute un découpage préalable par expression régulière et la gestion explicite de tokens spéciaux ; les segments sont encodés séparément, empêchant les fusions de franchir les frontières créées par le pattern.
- **GPT4Tokenizer** : n'est pas un tokenizer à entraîner. Il récupère `cl100k_base` depuis tiktoken, reconstruit l'arbre/ordre des fusions à partir des rangs existants, puis gère une permutation des octets de base pour reproduire le mapping attendu.

Cette architecture est particulièrement utile pour enseigner les différences entre algorithme de fusion, pré-tokenisation et conventions propres à un vocabulaire pré-entraîné. Elle ne constitue pas une preuve de compatibilité générale avec tous les modèles GPT ni une implémentation de production optimisée.

## 4. Comparaison synthétique

| Dimension | tiktoken | minbpe |
|---|---|---|
| Finalité | Bibliothèque rapide, encodages OpenAI nommés | Démonstration minimale et lisible |
| Unités de base | Octets, avec rangs fournis par encodage | 256 octets UTF-8 dans les variantes byte-level |
| Pré-tokenisation | Pattern propre à chaque encodage | Absente dans Basic ; regex configurable dans Regex/GPT4 |
| Fusions | Rang de séquence d'octets ; cœur natif `CoreBPE` | Boucle Python explicite, priorité de rang |
| Tokens spéciaux | API dédiée avec allow/deny explicite | Registre et choix `allowed_special` dans RegexTokenizer |
| Vocabulaire | Rangs et fichiers de vocabulaire propres à chaque encoding | Vocabulaire appris ou reconstruit ; GPT4 importe `cl100k_base` |
| Décodage | Décodage des tokens via les octets et gestion des cas Unicode | Reconstruction d'octets puis décodage UTF-8 avec remplacement |
| Compatibilité | Référence opérationnelle pour les encodages qu'il expose | GPT4Tokenizer vise explicitement `cl100k_base`, avec adaptations particulières |
| Performance | Cœur natif optimisé | Code Python volontairement simple ; aucune comparaison mesurée ici |

## 5. Décisions documentaires et graphe

- Conserver Hugging Face comme documentation de référence pour les responsabilités des composants du pipeline.
- Conserver tiktoken comme implémentation de production et `_educational.py` comme démonstration du mécanisme BPE ; ne pas fusionner ces deux rôles.
- Conserver minbpe comme implémentation pédagogique complémentaire, particulièrement utile pour comparer Basic, Regex et la reconstruction d'un tokenizer pré-entraîné.
- Ne pas créer d'extraction dédiée : les pages et synthèses existantes couvrent déjà les distinctions générales. Cette inspection ajoute surtout une comparaison d'implémentations et des localisateurs vérifiables, pas un ensemble de claims scientifiques indépendants.
- Graphe canonique : aucun nouveau concept ni aucune relation scientifique nouvelle ne sont justifiés. Les liens existants suffisent : `token` → pages de tokenisation ; `token-embedding` → pages d'embeddings ; le graphe computationnel relie `token-ids` → `token-context` → l'opération `embedding-lookup` → `token-embeddings`. Les ressources techniques restent des preuves documentaires attachées aux pages et concepts existants, pas des nœuds conceptuels.

## 6. Limites de l'audit

Aucun code n'a été exécuté ; aucun token ID n'a été comparé sur un corpus partagé ; aucune mesure de vitesse, mémoire ou qualité n'a été produite ; aucun benchmark du README de tiktoken n'est repris. Les révisions des dépôts sont enregistrées, mais la documentation Hugging Face `latest` reste une ressource vivante. Toute future affirmation de compatibilité devra être testée sur une version précise et un jeu d'entrées explicite.
