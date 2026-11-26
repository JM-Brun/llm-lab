# Audit de recherche et de modélisation — représentations contextualisées

Date : 2026-11-26  
Périmètre : leçon Understand FR/EN, page Deepen FR/EN et compagnons Practice FR/EN.

## 1. Question de recherche et périmètre

Question centrale : comment une occurrence de token passe-t-elle d'un vecteur initial sélectionné par son ID à un état caché dépendant de sa position et du contexte accessible ?

La page principale ne doit pas devenir une introduction générale à la géométrie des embeddings, à l'interprétabilité mécaniste ou à toutes les variantes du Transformer. Elle doit établir le modèle mental minimal, puis orienter vers les pages dédiées.

## 2. Sources examinées et métadonnées de recherche

| Source | Type / statut | Apport directement exploitable | Limites et précautions |
|---|---|---|---|
| Peters et al. (2018), [Deep Contextualized Word Representations](https://aclanthology.org/N18-1202/) | Article de recherche primaire, NAACL-HLT 2018 | ELMo construit des représentations de mots comme fonctions apprises des états internes d'un modèle de langue bidirectionnel ; antécédent important des représentations contextualisées. | ELMo repose sur un biLSTM, pas sur l'auto-attention Transformer ; ne pas le présenter comme un mécanisme GPT. |
| Ethayarajh (2019), [How Contextual are Contextualized Word Representations?](https://aclanthology.org/D19-1006/) | Article de recherche primaire, EMNLP-IJCNLP 2019 | Compare la géométrie des représentations d'ELMo, BERT et GPT-2 ; auto-similarité plus faible dans les couches hautes ; moins de 5 % de variance expliquée en moyenne par une représentation statique dans les configurations étudiées ; anisotropie. | Résultats empiriques dépendants des modèles, couches, données et mesures de 2019 ; pas une constante universelle, ni une preuve de séparation nette des sens humains. |
| Tenney, Das & Pavlick (2019), [BERT Rediscovers the Classical NLP Pipeline](https://aclanthology.org/P19-1452/) | Article de recherche primaire, ACL 2019 | Les sondes localisent en moyenne certaines informations linguistiques dans une progression de couches ; les analyses qualitatives montrent aussi des révisions dynamiques de décisions précédentes. | Porte sur BERT et des protocoles de probing ; information décodable ≠ utilisation causale démontrée ; ne pas attribuer une fonction exclusive à chaque couche ou tête. |

### Évaluation de couverture

- **Mécanisme de contextualisation dans un GPT causal :** les sources empiriques ci-dessus motivent et mesurent des propriétés des représentations, mais la définition du mécanisme doit rester fondée sur l'architecture Transformer, les masques et le calcul de la passe avant.
- **Historique :** Peters et al. situe correctement les représentations contextualisées avant les Transformers.
- **Mesure empirique :** Ethayarajh est la source la plus directement liée au degré de contextualité et à la géométrie.
- **Répartition entre couches :** Tenney et al. apporte un résultat de probing utile, à présenter avec ses limites.
- **Interprétabilité :** aucune de ces trois sources ne justifie à elle seule une interprétation mécaniste d'une tête ou d'une feature SAE.

## 3. Compilation : connaissances retenues

1. Le lookup sélectionne une ligne de la matrice d'embeddings à partir de l'ID ; à matrice et ID fixes, le vecteur initial est identique.
2. Le traitement positionnel dépend de l'architecture : ajout d'embeddings absolus dans certains modèles, rotations RoPE de Q/K dans d'autres mécanismes.
3. Un bloc Transformer transforme chaque état en fonction des positions autorisées par le masque. L'auto-attention permet les échanges entre positions ; le MLP agit position par position ; les résidus et la normalisation organisent le flux.
4. Dans un GPT causal, l'état à la position i ne dépend pas des tokens strictement futurs. Une modification du préfixe accessible peut changer cet état ; une modification future ne le peut pas, à paramètres et position fixés.
5. Les études empiriques confirment une dépendance au contexte et montrent des variations entre couches, mais ne justifient ni une géométrie sémantique simple ni une interprétation fonctionnelle exclusive des couches.

### Contradictions apparentes à ne pas aplanir

- ELMo/BERT sont bidirectionnels dans les travaux cités ; GPT-2 est causal. Le mot « contexte » ne désigne donc pas le même ensemble de positions accessibles.
- Une similarité cosinus élevée ne signifie pas que deux états sont identiques ou sémantiquement équivalents ; l'anisotropie est un facteur important.
- Une information décodable par probing n'est pas nécessairement utilisée causalement par le modèle pour produire sa sortie.

## 4. Modélisation pédagogique de l'ensemble

| Élément | Responsabilité | À ne pas lui faire porter |
|---|---|---|
| Understand — contextualized representations | Même ID → même lookup ; position et contexte accessible → états cachés potentiellement différents ; frontière causale passé/futur. | Dérivation détaillée des sous-couches, probing, SAE, géométrie complète. |
| Deepen — contextualized representations advanced | Formalisation de A(i), distinction causal/bidirectionnel, attention/MLP, résidus, normalisation, résultats empiriques et limites. | Reprendre toute l'introduction ou devenir un tutoriel complet d'interprétabilité. |
| Practice — contextualized representations exercises | Rappel actif, cartes de révision, expérience contrôlée passé/futur, application et enquête SAE facultative. | Répéter les paragraphes de la leçon ; mélanger explication et corrigé dans Understand. |
| Résumé | Quatre distinctions : ID/lookup, position, contexte accessible, état caché. | Remplacer les explications ou les exercices. |

### Relations conceptuelles à conserver

- token ID —sélectionne→ ligne initiale d'embedding ;
- position —est traitée par→ mécanisme positionnel ;
- état caché de couche i —est transformé en→ état caché de couche i+1 ;
- auto-attention —mélange l'information entre→ positions accessibles ;
- masque d'attention —contraint→ positions accessibles ;
- MLP —transforme indépendamment→ chaque position ;
- connexion résiduelle —ajoute la sortie de sous-couche au→ flux résiduel ;
- méthode de probing —teste la décodabilité d'une→ représentation de couche.

Ces relations décrivent des dépendances distinctes ; elles ne doivent pas être converties en une chaîne unique indifférenciée.

## 5. Changements appliqués dans cette passe

- Ajout de quatre cartes de révision sur les pages Practice FR/EN : identité du lookup, dépendance des états cachés, frontière causale et différence entre distribution et perte locale.
- Ajout d'une synthèse empirique sourcée dans les pages Deepen FR/EN, avec portée et limites propres à chaque étude.
- Ingestion canonique engagée dans Wiki Knowledge : trois fiches source, un concept, une synthèse, index, registre, taxonomie et journal dans la PR #199.
- Mise à jour de revision_support sur les leçons FR/EN pour signaler explicitement les cartes et le compagnon Practice.
- Conservation de la page principale, de ses exemples localisés, des illustrations et des exercices existants.
- Mise en cohérence des relations `related` FR/EN entre la leçon principale et son approfondissement ; le parcours garde le Transformer comme étape suivante et ne place pas Q/K/V après l'état contextualisé final.

## 6. État de l'ingestion canonique dans Wiki Knowledge

Les trois publications ont été examinées à partir de leurs pages bibliographiques primaires (ACL Anthology). La vérification de l'index et du registre de Wiki Knowledge n'a pas révélé de fiches source correspondantes. Cette passe constitue donc une **revue documentaire externe et une compilation éditoriale pour LLM Lab**, pas encore une ingestion canonique complète dans JM-Brun/wiki-knowledge.

Le suivi est ouvert dans [Wiki Knowledge #198](https://github.com/JM-Brun/wiki-knowledge/issues/198). Les trois fiches source, le concept canonique et la synthèse comparative ont maintenant été créés dans la branche `ingest/contextualized-representations-papers`, proposée dans la [PR #199](https://github.com/JM-Brun/wiki-knowledge/pull/199). Il s'agit de fiches metadata-only : aucun PDF n'est déclaré archivé. La PR reste en brouillon jusqu'à l'exécution de `wk-sync --registry-only`, `wk-validate`, `wk-lint` et du rapport de provenance. Ne pas déclarer de capture locale ni de droits de réutilisation des PDF si ces éléments n'ont pas été archivés et vérifiés.

## 7. Validation et limites

- Revue des sources Quarto FR/EN et des compagnons Practice existants.
- Contrôle de cohérence scientifique des résumés à partir des abstracts et métadonnées des publications primaires.
- Les modifications sont des ajouts bilingues ciblés ; aucun contenu existant n'est supprimé.
- Rendu Quarto, vérification des liens, inspection responsive et contrôles d'accessibilité restent à exécuter sur le head de la PR.
- La qualité d'apprentissage et le transfert chez des lecteurs n'ont pas été évalués.

## 8. Travail restant

1. Réaliser l'ingestion canonique des trois sources dans Wiki Knowledge ; enregistrer les claims, localisateurs, limites et relations.
2. Vérifier le rendu FR/EN des nouvelles cartes et de la section empirique (formules, liens, longueurs et mobile).
3. Auditer la transition embedding-space → positional-encoding → contextualized-representations → transformer → Q/K/V sur les pages rendues, sans modifier les responsabilités déjà établies.
4. Vérifier que la page Advanced reste proportionnée : si l'enquête SAE prend trop de place par rapport à la formalisation et aux résultats empiriques, envisager un déplacement vers une page dédiée à l'interprétabilité, après inventaire des pages existantes.
5. Ne pas ajouter de nouvelles cartes si elles répètent les exercices ; mesurer leur utilité lors d'un test apprenant avant d'étendre le lot.
