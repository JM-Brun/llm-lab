# minbpe — audit complémentaire des exercices, tests et limites

**Date d'inspection :** 2026-11-19  
**Dépôt :** https://github.com/karpathy/minbpe  
**Révision épinglée :** `1acefe89412b20245db5a22d2a02001e547dc602` (2024-04-22)  
**Fichiers inspectés :** `README.md`, `exercise.md`, `lecture.md`, `minbpe/base.py`, `minbpe/basic.py`, `minbpe/regex.py`, `minbpe/gpt4.py`, `tests/test_tokenizer.py`, `LICENSE`.  
**Nature :** inspection statique uniquement. Aucun test, entraînement, notebook ou benchmark n'a été exécuté.

## Synthèse et décision

Cette revue complète l'audit transversal du 18 novembre. La valeur pédagogique distinctive de minbpe n'est pas seulement son code court : c'est la progression explicite de l'exercice en cinq étapes, du BPE byte-level minimal à la pré-tokenisation regex, puis à la reconstruction d'un tokenizer pré-entraîné et à la gestion des tokens spéciaux. Le dépôt associe cette progression à des tests de round-trip, à un cas canonique de fusion et à des tests de parité avec tiktoken pour `cl100k_base`.

**Décision :** garder minbpe comme implémentation de référence pour l'étape « comprendre et construire BPE », sans copier une seconde implémentation dans LLM Lab. Son intérêt est complémentaire à tiktoken (production/native), à Hugging Face Tokenizers (pipeline configurable) et aux pages théoriques bilingues. L'issue #766 ne peut pas être fermée : la partie vidéo n'a pas fait l'objet d'une inspection audiovisuelle avec timestamps.

## 1. Progression pédagogique vérifiée

L'exercice `exercise.md` propose :

1. construire `BasicTokenizer` avec `train`, `encode` et `decode` ;
2. ajouter un pré-découpage regex, traiter les segments séparément et observer l'absence de fusions transfrontalières ;
3. reconstruire les fusions d'un tokenizer pré-entraîné depuis les rangs de `cl100k_base`, en comprenant la récupération des merges et la permutation des octets ;
4. ajouter les tokens spéciaux avec un choix explicite d'autorisation ;
5. comparer les unités byte-level à d'autres familles de tokenizers, avec une piste d'exploration SentencePiece.

Cette séquence enseigne des couches distinctes : unité initiale, règles de fusion, segmentation préalable, vocabulaire pré-entraîné et protocole d'interprétation des tokens spéciaux. Le passage de l'étape 2 à 3 est le plus discriminant : entraîner un BPE de même famille ne suffit pas à reproduire les IDs d'un tokenizer pré-entraîné.

La vidéo associée est mentionnée dans le README et la transcription `lecture.md` est disponible. Cette inspection textuelle ne remplace pas une inspection audiovisuelle ; aucun timestamp, geste, animation ou apport visuel spécifique n'est revendiqué ici.

## 2. Invariants et détails d'implémentation observés

### BPE minimal

- Le vocabulaire commence avec les 256 valeurs d'octets.
- L'entraînement compte les paires adjacentes, choisit une paire de fréquence maximale, lui attribue le prochain ID et remplace ses occurrences non chevauchantes.
- L'encodage applique ensuite les merges disponibles dans l'ordre de priorité de leurs IDs/rangs, jusqu'à ce qu'aucune paire ne soit fusionnable.
- Les égalités de fréquence ne sont pas départagées par une règle linguistique : `max(stats, key=stats.get)` dépend de l'ordre d'itération/insertion du dictionnaire. Il ne faut pas présenter un tie-break stable et universel comme une propriété de BPE.
- Le vocabulaire est reconstruit de manière déterministe à partir des merges ; les octets initiaux permettent de représenter tout texte UTF-8 sans unité « inconnue » au niveau des octets.

### Pré-tokenisation

`RegexTokenizer` encode chaque segment séparément. Les merges ne traversent donc pas les frontières produites par le pattern. Le pattern GPT-2 et le pattern GPT-4 sont différents ; ils ne sont pas des variantes interchangeables. Le pattern GPT-4 inclut notamment des règles distinctes pour nombres, ponctuation, espaces et contractions.

### Tokens spéciaux

L'API `RegexTokenizer.encode` distingue `all`, `none`, `none_raise` et un ensemble explicite de tokens autorisés. Les tokens spéciaux sont découpés et insérés comme IDs réservés, plutôt que fusionnés comme du texte ordinaire. La politique est pédagogique et explicite, mais elle ne doit pas être assimilée sans vérification à toutes les versions de tiktoken ou à toutes les bibliothèques.

### Reconstruction GPT-4 / cl100k_base

`GPT4Tokenizer` importe les rangs privés `enc._mergeable_ranks` depuis tiktoken, reconstruit les fusions et applique une permutation des octets de base. Il s'agit d'une adaptation à `cl100k_base`, dépendante d'une structure interne de tiktoken. La classe refuse l'entraînement et la sérialisation standard ; elle n'est pas un constructeur générique de tokenizers GPT-4/GPT-2 ni une voie autonome sans dépendance à tiktoken.

## 3. Tests présents — inventaire statique

Le fichier `tests/test_tokenizer.py` contient :

| Test | Ce qu'il vérifie dans le code | Ce qu'il ne démontre pas |
|---|---|---|
| `test_encode_decode_identity` | Round-trip sur chaîne vide, ponctuation, coréen, emoji et corpus fichier, pour les trois classes | Couverture exhaustive Unicode, toutes les frontières regex, robustesse à toute entrée |
| `test_gpt4_tiktoken_equality` | Égalité des IDs avec tiktoken pour les chaînes et le corpus testés | Compatibilité universelle avec toutes versions/encodages tiktoken |
| `test_gpt4_tiktoken_equality_special_tokens` | Parité sur un texte avec tokens spéciaux autorisés | Exhaustivité de toutes les politiques d'erreur ou de tous les tokens réservés |
| `test_wikipedia_example` | Résultat connu après trois merges pour Basic et Regex | Correctitude générale de l'entraînement sur tout corpus |
| `test_save_load` | Round-trip et stabilité encode/decode après sauvegarde/rechargement de RegexTokenizer, avec et sans tokens spéciaux | Sérialisation de GPT4Tokenizer, corruption, versions futures ou fichiers hostiles |

Le test de round-trip inclut des cas Unicode, mais le décodage utilise `errors="replace"` : un round-trip réussi sur ces cas ne constitue pas une preuve que tout flux arbitraire de token IDs correspond à une chaîne UTF-8 valide. Les tests couvrent un ensemble ciblé, non un fuzzing.

## 4. Limites et risques à ne pas masquer

- `BasicTokenizer.train` et `RegexTokenizer.train` supposent qu'il existe au moins une paire à fusionner pour chaque itération demandée ; un corpus vide ou un vocabulaire demandé au-delà des paires apprenables peut provoquer une erreur au choix de paire. Aucun comportement de terminaison anticipée n'est documenté ici.
- La règle de départage des paires de fréquence égale n'est pas explicitement spécifiée.
- Les classes sont des implémentations Python lisibles, pas des alternatives de performance à un cœur natif ; aucune mesure de performance n'a été faite.
- `GPT4Tokenizer` dépend de tiktoken et de son attribut privé `_mergeable_ranks`, et ne peut ni être entraîné ni sauvegardé via les méthodes standard.
- Les affirmations README selon lesquelles tous les LLM modernes utilisent BPE, ou qu'un entraînement RegexTokenizer sur un grand corpus de vocabulaire 100k reproduirait « GPT-4 », sont trop générales pour servir de conclusions. Les choix de tokenizers sont propres aux modèles ; la reproduction d'un tokenizer pré-entraîné exige les données, rangs, pré-tokenisation et conventions exacts.
- Le texte de l'étape 5 de l'exercice simplifie la distinction SentencePiece/byte-level ; ne pas le reprendre comme définition générale des tokenizers SentencePiece ou des modèles Llama sans audit de la configuration et de la version.
- Le fichier `.vocab` est explicitement destiné à l'inspection humaine et peut être lossy pour les fragments d'octets invalides en UTF-8 ; le fichier `.model` est celui utilisé par `load`.
- Le dépôt est sous MIT à la révision épinglée. LLM Lab conserve un lien et ne copie ni code ni figures ; les obligations de licence s'appliqueraient à toute copie substantielle ultérieure.

## 5. Comparaison et bénéfice apprenant

| Ressource | Ce qu'elle enseigne le mieux |
|---|---|
| minbpe | Boucle BPE visible, entraînement, encode/decode, frontières regex, spécial tokens, reconstruction d'un vocabulaire pré-entraîné |
| tiktoken | API et encodages OpenAI, politique de tokens spéciaux, cœur natif optimisé |
| Hugging Face Tokenizers | Pipeline composable et API de normalisation, pré-tokenisation, modèle et post-traitement |
| Pages LLM Lab FR/EN | Concepts, compromis, dépendance aux configurations, limites d'évaluation |

Le bénéfice apprenant est distinctif et concret : le lecteur peut implémenter les étapes plutôt que seulement lire la description d'un algorithme. Le projet peut pointer vers `exercise.md` comme activité externe, mais ne devrait pas recopier le code ni dupliquer les tests.

## 6. Suite et critères de clôture de #766

- [x] Révision du dépôt épinglée et fichiers README, code, tests, exercice, lecture et licence inspectés statiquement.
- [x] Différence entre Basic, Regex et GPT4Tokenizer explicitée.
- [x] Tests inventoriés sans prétendre qu'ils ont été exécutés.
- [x] Licence MIT vérifiée sur le fichier LICENSE de la révision.
- [ ] Inspection audiovisuelle de la vidéo avec timestamps et comparaison de son apport visuel à `lecture.md`.
- [ ] Si une activité LLM Lab est envisagée : exécuter l'exercice sur une version figée, ajouter des tests pour corpus vide, vocabulaire trop grand, égalités, tokens spéciaux et cas Unicode ciblés.
- [ ] Réviser les formulations trop générales de README/exercice uniquement si une correction upstream ou une note pédagogique locale est réellement justifiée.

**Décision issue :** progrès substantiel, mais garder #766 ouverte tant que la partie vidéo et la décision finale sur l'activité pédagogique ne sont pas traitées. Aucun test upstream n'a été exécuté pendant cet audit.

## Sources

- [minbpe — commit épinglé](https://github.com/karpathy/minbpe/tree/1acefe89412b20245db5a22d2a02001e547dc602)
- [README](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/README.md)
- [Exercise](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/exercise.md)
- [BasicTokenizer](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/minbpe/basic.py)
- [RegexTokenizer](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/minbpe/regex.py)
- [GPT4Tokenizer](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/minbpe/gpt4.py)
- [Tests](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/tests/test_tokenizer.py)
- [MIT License](https://github.com/karpathy/minbpe/blob/1acefe89412b20245db5a22d2a02001e547dc602/LICENSE)
