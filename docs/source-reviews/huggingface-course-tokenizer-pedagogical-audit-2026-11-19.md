# Hugging Face LLM Course — audit pédagogique ciblé du chapitre 6, section 8

**Date d'accès :** 2026-11-19  
**Source catalogue :** `huggingface-course-tokenizers-chapter6`  
**URL catalogue :** https://huggingface.co/docs/course/chapter6/8  
**Contenu consulté :** version vivante du cours, section « Building a tokenizer, block by block » ; aucune révision immuable n'a été établie.  
**Nature :** audit documentaire et pédagogique ; aucun notebook, code, dataset ou entraînement n'a été exécuté.

## Synthèse et décision

La section apporte davantage qu'un résumé des algorithmes BPE, WordPiece et Unigram : elle construit progressivement des tokenizers concrets avec la bibliothèque Hugging Face Tokenizers, en séparant normalizer, pre-tokenizer, modèle, trainer, post-processor et decoder. Elle fournit un corpus d'entraînement, des exemples BERT/WordPiece, GPT-2/BPE et XLNet/Unigram, puis expose les sorties structurées de l'objet `Encoding`.

Les pages bilingues LLM Lab couvrent déjà les rôles conceptuels du pipeline, les différences entre algorithmes, les effets de normalisation/pré-tokenisation, les offsets et les tokens spéciaux. Elles ne remplacent toutefois pas entièrement un parcours reproductible de construction de trois tokenizers avec les API et trainers concrets.

**Disposition :** conserver comme ressource pédagogique intégrée et référence technique ; ne pas créer d'extraction de claims ni recopier le tutoriel. Un éventuel enrichissement pédagogique de LLM Lab devrait prendre la forme d'un exercice bilingue court et versionné, après exécution réelle et vérification de compatibilité des API. L'audit ne suffit pas à conclure que la leçon est entièrement couverte.

## 1. Périmètre consulté

La section présente :
- le pipeline de tokenisation et les sous-modules de Tokenizers ;
- l'acquisition de WikiText-2 et la génération d'un corpus par lots ;
- la construction d'un tokenizer WordPiece de type BERT ;
- la construction d'un tokenizer BPE de type GPT-2 ;
- la construction d'un tokenizer Unigram de type XLNet ;
- les étapes d'encodage et de post-traitement.

La page est une documentation vivante. Le contenu consulté ne permet pas d'attribuer une date de publication, une date de mise à jour fiable ni un commit précis à la version effectivement servie.

## 2. Apports pédagogiques distinctifs

### Pipeline comme composition de composants

Le cours rend explicite une architecture composable autour de `Tokenizer` : `normalizers`, `pre_tokenizers`, `models`, `trainers`, `post_processors` et `decoders`. Cette présentation donne une procédure de construction concrète plutôt qu'une simple taxonomie des étapes.

### Progression par trois familles de modèles

Le parcours met en regard :
- WordPiece pour un tokenizer de type BERT, avec normalisation, segmentation, vocabulaire et tokens spéciaux ;
- BPE pour un tokenizer de type GPT-2 ;
- Unigram pour un tokenizer de type XLNet, avec normalisation et pré-tokenisation de type Metaspace.

Ces exemples sont des configurations pédagogiques particulières, pas des recettes universelles ni une spécification exhaustive des tokenizers BERT/GPT-2/XLNet.

### Corpus et entraînement

Le cours montre comment produire un itérateur de textes WikiText-2 par lots, écrire les textes dans un fichier, puis entraîner via un itérateur ou des fichiers. Cela relie la configuration du tokenizer à l'entrée réelle de son apprentissage. Le dataset et les paramètres montrés restent des choix d'exemple ; ils ne prouvent pas qu'un tokenizer entraîné sur ce corpus serait adapté à un autre usage.

### Sorties observables

La leçon rappelle que l'encodage expose notamment IDs, tokens, offsets, attention mask, token type IDs, masque de tokens spéciaux et séquences débordantes. Elle rend ainsi visible que la tokenisation produit davantage qu'une simple liste de chaînes.

## 3. Points techniques à conserver avec prudence

- Les tokens spéciaux doivent être transmis au trainer lorsqu'ils ne figurent pas dans le corpus ; la leçon l'illustre avec les tokens BERT. Cette configuration doit être vérifiée pour chaque trainer et version.
- Le pré-tokenizer `Whitespace` ne signifie pas « espaces uniquement » : l'exemple sépare aussi ponctuation ; `WhitespaceSplit` a une sémantique différente.
- Les normalizers composés ne sont pas nécessairement équivalents à un normalizer préconstruit : la leçon signale notamment des différences de nettoyage de caractères de contrôle.
- Les préfixes de sous-mots, les tokens inconnus, les tailles de vocabulaire, les seuils de fréquence et les processeurs de séquence dépendent du modèle et de sa configuration.
- Les exemples d'API du cours vivant peuvent évoluer. Aucune compatibilité avec une version donnée de Tokenizers n'est affirmée par cet audit.

## 4. Comparaison avec LLM Lab

Les pages `en/tokenization-strategies.qmd` et `fr/tokenization-strategies.qmd` décrivent déjà les composants du pipeline, les effets de normalisation/pré-tokenisation, les familles d'algorithmes, les tokens spéciaux et plusieurs exemples Hugging Face. Le dossier transversal et l'audit de l'API Tokenizers couvrent les responsabilités des composants et certaines limites de version.

L'apport distinctif restant est principalement **la progression d'atelier** : corpus → configuration des composants → entraînement → encodage → post-traitement, déclinée sur trois familles. Il s'agit d'une valeur pédagogique, non d'une nouvelle contribution théorique ou d'une preuve empirique.

Aucune extraction atomique supplémentaire n'est justifiée à ce stade : les faits techniques sont documentés ailleurs et les recettes API sont version-sensibles. Une activité pédagogique dédiée ne sera pertinente que si elle peut être exécutée, testée et maintenue dans le dépôt.

## 5. Limites de l'audit

- Consultation documentaire de la section et de ses exemples ; aucune exécution de code.
- Aucun notebook ni dataset téléchargé.
- Aucun tokenizer n'a été entraîné ; aucune sortie n'a été reproduite.
- La version exacte de Tokenizers utilisée par les exemples n'a pas été établie.
- La licence de la page, les droits de réutilisation de ses figures et ceux des notebooks/datasets ne sont pas établis par cette revue.
- Les métadonnées de publication et de mise à jour restent inconnues.

## 6. Suite opérationnelle

1. Conserver le lien vers la source ; ne pas copier les figures ni le code dans LLM Lab sans vérification des droits.
2. Si l'atelier devient un objectif pédagogique, choisir une version de Tokenizers, figer les dépendances et exécuter un parcours minimal sur un corpus contrôlé.
3. Ajouter des assertions sur normalisation, pré-tokenisation, tokens spéciaux, offsets, post-traitement et décodage ; distinguer résultats réellement observés et exemples du cours.
4. Concevoir une activité bilingue courte seulement si elle apporte une manipulation que les pages actuelles ne permettent pas.
5. Ne pas modifier le statut de licence ou les dates tant qu'une source primaire fiable ne les établit pas.

## Sources consultées

- [Section du cours — Building a tokenizer, block by block](https://huggingface.co/learn/llm-course/chapter6/8)
- [Section du cours — Normalization and pre-tokenization](https://huggingface.co/learn/llm-course/chapter6/4)
- [Source du chapitre dans le dépôt Hugging Face Course](https://github.com/huggingface/course/blob/main/chapters/en/chapter6/8.mdx)
- [Page EN LLM Lab — Tokenization strategies](https://github.com/JM-Brun/llm-lab/blob/main/site/en/tokenization-strategies.qmd)
- [Page FR LLM Lab — Stratégies de tokenisation](https://github.com/JM-Brun/llm-lab/blob/main/site/fr/tokenization-strategies.qmd)
