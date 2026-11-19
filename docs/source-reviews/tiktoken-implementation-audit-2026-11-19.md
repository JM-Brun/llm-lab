# OpenAI tiktoken — audit ciblé de l'implémentation et des tests

**Date :** 2026-11-19  
**Révision upstream :** `79dc2c0533685b893616c78160b5d9e40876e724`  
**Nature :** inspection statique de code et de tests ; aucune commande de test, aucun benchmark et aucun exemple n'ont été exécutés.

## Synthèse et décision

La ressource doit être conservée comme référence technique et pédagogique complémentaire. Elle ne justifie pas une nouvelle explication générique de BPE : les pages bilingues et les audits minbpe/SentencePiece couvrent déjà le principe de fusion. Sa valeur distinctive est la comparaison concrète entre :

- un chemin de production Python qui délègue le BPE à l'extension native `_tiktoken.CoreBPE` ;
- un module éducatif Python qui rend visibles le pré-découpage regex, la conversion UTF-8 en octets, le choix itératif des fusions et le décodage ;
- les tests qui spécifient plusieurs comportements observables (tokens spéciaux, aller-retour, octets, offsets, batch et entrées Unicode).

**Disposition :** conserver les deux entrées du catalogue, sans extraction conceptuelle supplémentaire à ce stade. Compléter l'audit d'implémentation par une validation exécutée et des fixtures communes avant toute conclusion comparative. Le code n'est pas copié dans LLM Lab.

## 1. Révision et périmètre effectivement inspectés

Dépôt : [openai/tiktoken](https://github.com/openai/tiktoken)  
Commit : `79dc2c0533685b893616c78160b5d9e40876e724`.

Fichiers consultés à cette révision :

- `tiktoken/_educational.py`
- `tiktoken/core.py`
- `tiktoken_ext/openai_public.py`
- `tests/test_encoding.py`
- `tests/test_offsets.py`
- `LICENSE`

Ce périmètre n'est pas un audit exhaustif du dépôt : il ne couvre pas l'implémentation Rust de `CoreBPE`, toutes les fonctions publiques, toutes les tables d'encodage, toutes les dépendances ni l'historique des versions.

## 2. Module éducatif : ce que le code expose

### Encodage

`SimpleBytePairEncoding.encode` :

1. découpe le texte Unicode avec le motif regex fourni ;
2. encode chaque segment en UTF-8 ;
3. transforme chaque octet en élément initial ;
4. appelle `bpe_encode` sur chaque segment ;
5. concatène les IDs obtenus.

Dans `bpe_encode`, toutes les paires adjacentes sont examinées à chaque itération. La paire concaténée ayant le rang disponible le plus faible est fusionnée ; l'opération est répétée jusqu'à ce qu'aucune paire ne figure dans `mergeable_ranks`. Le code parcourt les paires de gauche à droite et ne remplace le meilleur candidat que pour un rang strictement inférieur : à rang égal, le premier candidat rencontré reste sélectionné dans cette implémentation pédagogique.

### Apprentissage

`bpe_train` initialise les 256 octets possibles avec les rangs 0 à 255. À chaque itération, il compte les paires adjacentes dans les segments pré-découpés, sélectionne la paire la plus fréquente, concatène ses octets et attribue le prochain rang. Il applique ensuite cette fusion aux segments d'entraînement.

**Réserve :** le code utilise `Counter` et `max`; le comportement en cas d'égalité dépend de l'ordre d'insertion des clés observées. Ne pas présenter le départage des égalités comme une règle universelle du BPE.

### Décodage et visualisation

- `decode_bytes` reconstitue les octets à partir des IDs.
- `decode` utilise UTF-8 avec `errors="replace"` : si une frontière de token coupe un caractère multi-octet, le résultat texte peut contenir le caractère de remplacement.
- `decode_tokens_bytes` conserve la représentation en octets token par token.
- La visualisation colore les fragments et décode chaque fragment avec remplacement ; elle est illustrative et ne garantit pas que chaque frontière corresponde à une frontière de caractère Unicode.
- `from_tiktoken` récupère `_pat_str` et `_mergeable_ranks` d'une instance de production : c'est un pont pédagogique qui dépend d'attributs internes.

Le module éducatif n'est donc ni le chemin optimisé de production, ni une API de compatibilité indépendante de la version.

## 3. Chemin de production : contrats visibles dans le code Python

Dans `tiktoken/core.py`, `Encoding` rassemble trois paramètres structurants :

- `pat_str` : pré-découpage regex du texte Unicode ;
- `mergeable_ranks` : séquences d'octets vers rangs/IDs ;
- `special_tokens` : chaînes spéciales vers IDs, séparées des tokens fusionnables.

L'instance délègue l'encodage à `_tiktoken.CoreBPE`. La boucle pédagogique Python ne décrit donc pas le chemin de calcul de production.

La méthode `encode` rend explicite une politique de sécurité/ambiguïté des tokens spéciaux : par défaut, les chaînes reconnues comme tokens spéciaux mais non autorisées déclenchent une erreur ; `allowed_special` et `disallowed_special` permettent une politique explicite. `encode_ordinary` ignore ces tokens spéciaux et équivaut, selon la docstring, à `encode(..., disallowed_special=())`.

Le code expose également des méthodes batch, des sorties NumPy et des chemins de décodage. Les détails du cœur natif et ses garanties ne peuvent pas être inférés du seul wrapper Python.

Dans `tiktoken_ext/openai_public.py`, les encodages nommés ne sont pas interchangeables : ils définissent des regex, vocabulaires/rangs et ensembles de tokens spéciaux différents. Les fichiers d'artefacts sont chargés avec des empreintes attendues. Les noms `gpt2`, `r50k_base`, `p50k_base`, `cl100k_base`, `o200k_base` et `o200k_harmony` désignent des configurations concrètes, pas des propriétés universelles de BPE.

## 4. Tests upstream repérés — inspection statique seulement

### `tests/test_encoding.py`

Les tests consultés couvrent notamment :

- exemples de référence `hello world` sur `gpt2` et `cl100k_base` ;
- séquences numériques répétées et cas regex/espaces ;
- chaîne vide ;
- encodage/décodage d'octets et propriétés sur octets arbitraires ;
- round-trip sur texte, y compris chinois et texte généré par Hypothesis ;
- traitement des paires de substituts et substituts isolés ;
- politique `allowed_special` / `disallowed_special` ;
- cohérence entre encodage ordinaire et politique sans tokens spéciaux ;
- encodage batch et aller-retour batch.

### `tests/test_offsets.py`

Les tests comparent `decode_with_offsets` à une référence calculée sur les préfixes décodés. Ils incluent anglais, token spécial, chinois, tamoul et cas où une séquence d'octets tokenisée traverse une frontière UTF-8.

**Interprétation :** les offsets renvoyés par cette API Python sont ici vérifiés comme positions dans la chaîne décodée (préfixes Python), pas comme offsets bruts en octets UTF-8. Ne pas comparer directement ces valeurs aux offsets d'autres bibliothèques sans harmoniser leur unité.

Aucun de ces tests n'a été exécuté pendant cet audit. Les assertions et propriétés décrivent des tests présents dans la révision inspectée ; elles ne constituent pas des résultats d'exécution.

## 5. Licence et réutilisation

Le fichier `LICENSE` à la révision épinglée contient la licence MIT et les mentions de copyright OpenAI et Shantanu Jain. Cette licence s'applique au dépôt et au module éducatif dans le cadre de cette révision ; elle n'autorise pas à omettre l'avis de copyright et le texte de licence lors d'une redistribution de portions substantielles.

Le projet conserve le code en lien externe et ne le copie pas. L'entrée catalogue `openai-tiktoken-educational-bpe` peut donc être qualifiée MIT vérifiée, avec URL vers le fichier LICENSE de la révision épinglée. Les métadonnées de date de publication/mise à jour restent inconnues et ne sont pas déduites du commit.

## 6. Comparaison et implications pédagogiques

| Dimension | tiktoken éducatif | tiktoken production | À comparer avec minbpe / HF / SentencePiece |
|---|---|---|---|
| Unités initiales | octets UTF-8 | cœur natif BPE byte-level | normalisation et alphabet initial |
| Pré-découpage | regex explicite | regex propre à l'encodage | frontière de segmentation |
| Fusion | boucle Python, rang minimal | extension native, rangs fournis | ordre et comportement observé |
| Apprentissage | fréquence des paires sur corpus | vocabulaires pré-entraînés chargés | données et déterminisme d'apprentissage |
| Tokens spéciaux | absents du modèle pédagogique simple | dictionnaire et politique d'autorisation | reconnaissance/traitement spécial |
| Décodage | bytes, puis UTF-8 avec remplacement | méthodes dédiées et offsets | round-trip, erreurs, offsets |
| Performance | démonstration lisible | implémentation optimisée | benchmark contrôlé nécessaire |

Ne pas comparer les IDs de vocabulaires indépendants. Ne pas interpréter un nombre de tokens inférieur comme une meilleure qualité intrinsèque. Pour chaque expérience, fixer le texte exact, la révision logicielle, le tokenizer et ses artefacts, la politique des tokens spéciaux, le prétraitement et l'unité des offsets.

## 7. Expériences discriminantes à exécuter ensuite

1. **Éducatif vs production sur même encodage :** construire `SimpleBytePairEncoding.from_tiktoken` et comparer les séquences d'octets de tokens/IDs sur des entrées sans tokens spéciaux. Vérifier séparément les hypothèses de départage des égalités.
2. **Frontières UTF-8 :** comparer `decode_tokens_bytes`, `decode_bytes` et `decode` sur emoji, scripts multi-octets et tokens qui ne correspondent pas à des caractères complets.
3. **Tokens spéciaux :** tester chaîne littérale, autorisation explicite, interdiction par défaut et encodage ordinaire.
4. **Offsets :** vérifier unité et comportement sur caractères composés, chinois, tamoul et tokens spéciaux.
5. **Pré-découpage :** confronter ponctuation, contractions, chiffres et espaces entre encodages nommés.
6. **Apprentissage éducatif :** fixer corpus, motif regex, taille de vocabulaire et stratégie de visualisation ; répéter sur des égalités de fréquence pour observer la dépendance à l'ordre.

Ces expériences restent à exécuter. Aucun résultat n'est revendiqué dans ce dossier.

## 8. Suite

- Exécuter les tests upstream ciblés à cette révision, en enregistrant environnement, commandes et résultats.
- Ajouter des tests directs du module éducatif (il n'a pas été trouvé de fichier de test dédié dans le répertoire `tests/` inspecté).
- Inspecter `decode_with_offsets`, `decode_bytes`, le chargement des artefacts et les fonctions d'entraînement du chemin de production plus en profondeur.
- Comparer avec minbpe à sa révision épinglée, SentencePiece v0.2.3 et une configuration Hugging Face précise.
- Ne pas fermer l'issue #768 avant validation exécutée et arbitrage final de réutilisation.

## Sources et traçabilité

- [Dépôt à la révision épinglée](https://github.com/openai/tiktoken/tree/79dc2c0533685b893616c78160b5d9e40876e724)
- [Module éducatif](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/tiktoken/_educational.py)
- [Wrapper Python de production](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/tiktoken/core.py)
- [Déclarations des encodages publics](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/tiktoken_ext/openai_public.py)
- [Tests d'encodage](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/tests/test_encoding.py)
- [Tests d'offsets](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/tests/test_offsets.py)
- [Licence MIT](https://github.com/openai/tiktoken/blob/79dc2c0533685b893616c78160b5d9e40876e724/LICENSE)
