# Sennrich et al. (2016) — audit de la source primaire

**Source :** Rico Sennrich, Barry Haddow et Alexandra Birch, *Neural Machine Translation of Rare Words with Subword Units*, ACL 2016, pp. 1715–1725. [ACL Anthology](https://aclanthology.org/P16-1162/) · [PDF](https://aclanthology.org/P16-1162.pdf) · DOI: 10.18653/v1/P16-1162.

## Synthèse

Cette étude traite le problème des mots rares et inconnus en traduction neuronale. Elle adapte l'idée de remplacement itératif de paires de Gage (1994) à la segmentation en sous-unités : chaque mot est initialisé comme séquence de caractères avec marqueur de fin, les paires adjacentes les plus fréquentes sont fusionnées successivement, et les règles apprises sont appliquées aux mots nouveaux.

Cette contribution constitue un jalon majeur du BPE sous-lexical en NLP, mais **ne décrit pas le BPE byte-level de GPT**. Le papier utilise des unités de caractères, des frontières de mots et un marqueur de fin ; les tokenizers modernes ajoutent leurs propres pré-découpages, unités de base, règles de vocabulaire et conventions d'encodage.

## Preuves examinées

- Motivation open-vocabulary et sous-unités : résumé et §§1, 3, pp. 1715–1717.
- Adaptation BPE et pseudo-code : §3.2, Algorithm 1 et Figure 1, pp. 1717–1718.
- Expériences : §4.2, Tables 2–3 et §5, pp. 1719–1722.
- Protocole : WMT 2015, anglais-allemand et anglais-russe ; architecture récurrente encoder-decoder Groundhog, avec vocabulaire et baselines décrits dans le papier.
- Résultats : les modèles sous-mots améliorent le traitement des mots rares/inconnus par rapport au modèle lexical avec dictionnaire de secours ; les gains BLEU rapportés vont jusqu'à 1,1 (EN→DE) et 1,3 (EN→RU) dans les comparaisons d'ensemble citées.

## Limites et controverses

- Résultats propres à la traduction automatique neuronale de 2015, pas à l'évaluation de tokenizers GPT ou de modèles pré-entraînés contemporains.
- Les auteurs soulignent que toutes les segmentations ne sont pas transparentes linguistiquement et que le sur-découpage peut être nuisible à l'efficacité.
- Les scores varient selon la segmentation, la direction de traduction et l'ensemble de modèles ; les auteurs signalent une variabilité entre entraînements.
- Le dépôt logiciel et les données n'ont pas été exécutés ou reproduits indépendamment dans cet audit.

## Décision documentaire

La recherche dans le dépôt ne trouve pas de citation explicite de Sennrich dans les pages bilingues de tokenisation. En revanche, les deux pages décrivent précisément l'adaptation NLP du BPE à partir de l'algorithme de compression de Gage. Sennrich est donc une source primaire pertinente pour cette étape historique : ajout d'une référence explicite dans la section de distinction historique, sans lui attribuer la spécification du BPE byte-level moderne.

Aucun nouveau concept ni nouvelle relation de graphe n'est nécessaire ; le concept canonique `token` et les pages bilingues existantes suffisent.

## Périmètre de l'audit

Lecture du PDF ACL publié : résumé, §§1, 3.2, 4.2 et 5, Algorithm 1, Figure 1 et Tables 1–3. Pas d'exécution du code, de reproduction des entraînements ou d'audit des artefacts logiciels.
