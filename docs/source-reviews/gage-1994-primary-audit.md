# Philip Gage (1994) — audit de la source primaire

**Source :** Philip Gage, *A New Algorithm for Data Compression*, **The C Users Journal**, 12(2), 23–38, février 1994. [PDF](https://www.derczynski.com/papers/archive/BPE_Gage.pdf) · DOI : 10.5555/177910.177914.

## Synthèse

Gage présente Byte Pair Encoding (BPE) comme un algorithme généraliste de **compression de données binaires**. Dans un bloc d'octets, il compte les paires adjacentes, remplace les occurrences d'une paire fréquente par une valeur d'octet inutilisée, répète l'opération et écrit une table permettant de reconstruire les données.

Le décodeur parcourt les octets encodés et développe les codes de paires à l'aide d'une pile. La compression est multi-passe, tandis que l'expansion est conçue comme un parcours en un seul passage. Le traitement par blocs répond aux contraintes de mémoire et au nombre limité de valeurs disponibles.

**Gage est la source primaire de l'algorithme de compression par paires d'octets, pas une spécification des tokenizers NLP ou GPT.** Les variantes NLP changent notamment les unités initiales, le pré-découpage, les frontières, la construction du vocabulaire et la procédure d'encodage.

## Preuves examinées

- **Principe de substitution :** §1, p. 1. Comptage des paires d'octets adjacentes, choix de la paire la plus fréquente, remplacement par un octet inutilisé et enregistrement de la substitution.
- **Traitement par blocs :** §1, p. 1. L'algorithme multi-passe exige un bloc en mémoire ; les blocs séparés apportent une adaptation locale et répondent aux contraintes de flux et d'alphabet.
- **Implémentation :** §2, p. 2 et Listings 1–4, pp. 7–13. Table de hachage des fréquences, seuil minimal, remplacement en place et programmes C de compression/décompression.
- **Table de paires :** §3, pp. 2–3 et Figure 1. Le code de remplacement est l'index de l'entrée correspondante ; la table est elle-même encodée.
- **Expansion :** §4, p. 4, Listing 2 et Figure 2. Une pile développe les paires imbriquées avant de reprendre la lecture du flux encodé.
- **Résultats :** §6, Table 1, pp. 5–6. Sur WIN386.EXE (544 789 octets), environnement compatible 486DX à 33 MHz, MS-DOS 5.0 et Borland C++ 3.0 : BPE par défaut, 276 955 octets, 55 s de compression et 20 s d'expansion ; LZW 12 bits, 299 118 octets, 28 s et 27 s.
- **Réserves :** §§6–8. Les performances varient selon les données et les tailles de blocs ; la compression est plus lente que LZW dans le test présenté, mais l'expansion est plus rapide.

## Limites et interprétation

1. **Unité de base :** octets, dans un alphabet de 256 valeurs. Il ne s'agit pas de caractères Unicode, de graphèmes ou de sous-mots linguistiques.
2. **Objectif :** réduire la taille d'un flux et permettre sa reconstruction exacte ; pas construire un vocabulaire destiné à un modèle de langue.
3. **Contrainte d'alphabet :** les substitutions consomment des valeurs d'octet inutilisées. Le programme s'arrête lorsqu'il n'existe plus de code disponible ou que le seuil de fréquence n'est plus atteint.
4. **Traitement :** multi-passe à l'intérieur de blocs, avec table de substitution par bloc. Ce n'est pas un ordre de fusions persistant pour encoder de nouveaux textes.
5. **Résultats :** un seul exécutable binaire et un environnement matériel/logiciel historique. Aucune conclusion générale sur la supériorité de BPE sur LZW n'est justifiée.
6. **Reproductibilité :** le code C a été lu mais pas compilé ni exécuté ; les mesures ne sont pas reproduites.
7. **Provenance :** le PDF accessible précise qu'il s'agit d'une reconstruction de 2020 à partir de la page HTML de l'article original. Les droits de réutilisation des figures et du code restent inconnus.

## Décision documentaire

La page bilingue de stratégies de tokenisation explique déjà correctement la distinction historique : Gage fournit l'idée de remplacement de paires d'octets ; les variantes NLP adaptent cette idée à des unités textuelles et à un vocabulaire de sous-mots ; GPT byte-level BPE est une conception particulière.

L'extraction dédiée est justifiée, car le texte primaire apporte des détails absents d'une simple référence contextuelle : contraintes d'alphabet et de blocs, table de substitutions, décodage par pile et limites des résultats expérimentaux. L'intégration doit rester ciblée : enrichir la provenance historique et les limites, sans recopier l'implémentation C ni transformer l'article en référence normative des tokenizers modernes.

Aucun nouveau concept ni aucune relation de graphe ne sont nécessaires. Le concept canonique `token` et les deux pages existantes suffisent. Le statut de licence et les droits de réutilisation des figures et du code restent inconnus.

## Périmètre de l'audit

Lecture du PDF : résumé, §§1–8, Figures 1–2, Table 1, Listings 1–4 et références bibliographiques. Inspection des pseudocodes et du code source C sans exécution. Aucune reproduction des mesures, aucun audit des références citées et aucune réutilisation des figures ou du code.
