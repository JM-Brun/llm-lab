# Audit ciblé — Hugging Face Transformers tokenizer summary — 19 novembre 2026

## Décision

**Référence / déduplication confirmée ; aucune extraction dédiée.**

La page fournit un panorama pédagogique de BPE, WordPiece, Unigram et SentencePiece. Elle est utile comme orientation vers l'écosystème Transformers, mais son apport conceptuel est déjà couvert de façon plus nuancée dans les pages bilingues du projet et la synthèse transversale. Les exemples de familles de modèles et les descriptions simplifiées sont dépendants de la version et ne doivent pas être transformés en règles universelles.

## Source et périmètre

- ID catalogue : `huggingface-tokenizer-algorithms-summary`.
- URL canonique : https://huggingface.co/docs/transformers/main/en/tokenizer_summary
- Titre courant observé : « Tokenization algorithms ».
- Version : branche documentaire `main`, page vivante ; aucun commit ou release immuable n'a été établi.
- Consultation : 19 novembre 2026.
- Comparaison limitée à la page de synthèse, aux pages FR/EN du projet et au dossier de collection.

## Contenu observé

La page courante présente :
- BPE comme une suite de fusions de paires adjacentes, avec pré-tokenisation et vocabulaire initial ;
- WordPiece comme une sélection de fusions fondée sur un score lié à la vraisemblance ;
- Unigram comme un modèle probabiliste qui part d'un ensemble de candidats et réduit le vocabulaire en fonction de l'impact sur la perte ;
- SentencePiece comme une bibliothèque qui peut appliquer BPE ou Unigram au texte brut, avec une convention visible pour les espaces.

La page décrit également des modèles précis comme exemples d'utilisation. Ces associations ne constituent pas des garanties pour toutes les versions, variantes ou configurations de ces modèles.

## Couverture existante dans LLM Lab

Les pages `site/en/tokenization-strategies.qmd` et `site/fr/tokenization-strategies.qmd` couvrent déjà, dans les deux langues :
- les différences entre BPE, WordPiece et Unigram ;
- la distinction entre entraînement du tokenizer et encodage d'un nouveau texte ;
- le rôle de la pré-tokenisation, de la normalisation, du vocabulaire et des tokens spéciaux ;
- la distinction entre algorithme, bibliothèque et implémentation ;
- les variantes byte-level et leurs garanties limitées ;
- le fait que SentencePiece est une bibliothèque et non un algorithme unique ;
- les limites d'une démonstration BPE pédagogique par rapport à un tokenizer de production.

Le dossier `docs/source-reviews/tokenization-embeddings-source-collection.md` rassemble déjà les apports complémentaires du cours Hugging Face, des implémentations tiktoken/minbpe/SentencePiece et des références historiques. Il précise notamment qu'aucun pipeline universel ni aucune équivalence entre variantes BPE ne doivent être inférés.

## Points de vigilance sur la source

1. Les exemples de modèles sont illustratifs et versionnés ; ne pas attribuer un algorithme à tous les modèles d'une famille à partir d'une liste de la page de synthèse.
2. Les formulations introductives sur les unités de base et les inconnus sont simplifiées. La couverture réelle dépend du modèle, du pré-tokenizer, de la normalisation et des mécanismes byte fallback.
3. La description de SentencePiece est une vue d'ensemble ; elle ne remplace pas la documentation/version de la bibliothèque ni l'inspection de sa configuration.
4. Les pages versionnées de Transformers peuvent présenter des formulations ou exemples différents. Une comparaison de comportements doit épingler la version de la documentation et du tokenizer réellement utilisé.

## Pourquoi aucune extraction

- Les mécanismes généraux sont déjà présents dans les deux pages canoniques et leur dossier de synthèse.
- Les éléments propres à Transformers ne sont pas nouveaux au regard de la couverture actuelle.
- Les associations modèle/algorithme ne sont pas suffisamment stables pour devenir des claims généraux.
- Une extraction répéterait des explications de panorama sans localisateur scientifique ou contrat d'API distinctif.

**Disposition :** conserver comme référence de synthèse, sans extraction. Réouvrir si une version déterminée de Transformers est utilisée dans un exemple du projet et qu'une affirmation précise sur son tokenizer nécessite une preuve versionnée.

## Limites

- Page documentaire vivante, non épinglée à un commit ou une release.
- Pas d'audit de code, de configuration de modèle ou de fichiers tokenizer.
- Aucun tokenizer n'a été exécuté ; aucun comportement ni benchmark n'a été reproduit.
- Les métadonnées de publication, de mise à jour et de licence restent inconnues dans le catalogue ; aucune réutilisation de texte ou figure n'est proposée.

## Sources internes croisées

- `site/en/tokenization-strategies.qmd`
- `site/fr/tokenization-strategies.qmd`
- `docs/source-reviews/tokenization-embeddings-source-collection.md`
- `data/sources.yml` — entrée `huggingface-tokenizer-algorithms-summary`

## Suite opérationnelle

Garder cette référence dans le catalogue et éviter une extraction redondante. Prioriser désormais les sources dont les affirmations ou les implémentations ne sont pas encore corroborées par le dossier transversal, en commençant par les sources primaires ou les ressources pédagogiques qui apportent une activité distincte.
