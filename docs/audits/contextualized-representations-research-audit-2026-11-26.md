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
- Mise à jour du nœud bilingue `contextualized-representation` dans `data/concepts.yml` : définition recentrée sur l'occurrence et le contexte accessible ; ajout des deux pages Advanced comme ressources de ce concept.
- Régénération des fragments `generated-map-data-fr/en.qmd` pour refléter la définition bilingue et les ressources Advanced du nœud conceptuel.
- Réconciliation des fragments générés avec le dernier `main` : les mises à jour indépendantes du calendrier et de la carte `Deepen` sont conservées, tandis que les relations et ressources du concept contextualisé sont ajoutées.
- Ajout d'un avertissement bilingue sur la leçon principale : Q/K/V sont des projections internes au sous-bloc d'auto-attention, pas une étape après les représentations contextualisées.

## 6. État de l'ingestion canonique dans Wiki Knowledge

Les trois publications ont été examinées à partir de leurs pages bibliographiques primaires (ACL Anthology). La vérification de l'index et du registre de Wiki Knowledge n'avait pas révélé de fiches source correspondantes. Les nouveaux artefacts sont maintenant proposés dans [Wiki Knowledge PR #199](https://github.com/JM-Brun/wiki-knowledge/pull/199), qui suit [l'issue #198](https://github.com/JM-Brun/wiki-knowledge/issues/198).

La PR contient trois fiches source, un concept canonique, une synthèse comparative, des entrées d'index et de taxonomie, une mise à jour du registre et un journal d'ingestion. Les fiches sont metadata-only : aucun PDF local n'est déclaré. La PR est actuellement ouverte et non fusionnée. Son état GitHub n'est plus « draft », mais cela ne vaut pas validation scientifique ou technique.

Les critères de l'issue #198 ne sont pas encore réputés satisfaits tant que les éléments suivants n'ont pas été vérifiés sur le head courant :
- existence et qualité des artefacts d'extraction source par source et d'un ChangePlan explicite ;
- vérification des claims atomiques, localisateurs exacts, types/niveaux de preuve et limites ;
- exécution réussie des mécanismes canoniques `wk-sync --registry-only`, `wk-validate`, `wk-lint` et du rapport de provenance ;
- résolution des échecs de CI antérieurs (rendu Quarto, qualité Wiki, audit des identifiants documentaires). Les journaux correspondants n'étaient pas récupérables via le connecteur au moment du contrôle.

Ne pas déclarer de capture locale ni de droits de réutilisation des PDF si ces éléments n'ont pas été archivés et vérifiés.

## 7. Validation LLM Lab — état au 2026-11-26

La PR [LLM Lab #1728](https://github.com/JM-Brun/llm-lab/pull/1728), branche `docs/contextualized-representations-evidence-v4`, est ouverte. Le head contrôlé est `7ebfb17ff01e1c7ac704b022fd611570fe73a248).

Contrôles terminés avec succès :
- qualité Python et contrôles métier ;
- suite de tests : **834 réussis, 1 ignoré** ;
- secret scanning ;
- génération des fragments bilingues de carte et de graphe computationnel ;
- rendu Quarto complet ;
- contrôles des commandes de la carte d'apprentissage et de l'export du graphe de connaissances ;
- parité de la chronologie bilingue ;
- vérification des liens locaux ;
- revue navigateur des pages pédagogiques bilingues et de leur navigation ;
- téléversement des captures et du rapport d'audit navigateur.

Les contrôles du rendu et du navigateur ont terminé avec succès dans le run `45904294331`; les contrôles Python et tests ont terminé avec succès dans le run `45904255898`. Les étapes conditionnelles de rendu incrémental isolé et d'installation Playwright ont été ignorées parce que le parcours complet n'en avait pas besoin ; ce n'est pas un échec.

Cette validation CI ne remplace pas une revue éditoriale humaine des captures, ni un test d'apprentissage auprès de lecteurs. Aucune preuve d'efficacité pédagogique ou de transfert n'est revendiquée.

## 8. Travail restant — LLM Lab

### P0 — Revue finale avant fusion de la PR #1728

- [ ] Examiner visuellement les captures et le rapport d'audit navigateur produits par le run CI, notamment les pages FR/EN Understand, Deepen et Practice.
- [ ] Contrôler à l'écran les formules, les ancres, les blocs repliables des cartes, les retours à la ligne et le comportement mobile ; le succès du rendu ne garantit pas à lui seul la qualité typographique.
- [ ] Faire une dernière lecture comparative FR/EN : précision terminologique, équivalence du contenu, liens et titres.
- [ ] Vérifier le diff final de la PR pour confirmer qu'aucune modification concurrente de la carte ou des métadonnées n'a été perdue.
- [ ] Mettre à jour le corps de la PR si nécessaire et demander/retenir la revue avant fusion. Ne pas fusionner automatiquement.

### P1 — Audit de continuité du parcours

- [ ] Relire les pages rendues dans l'ordre embedding-space → positional-encoding → contextualized-representations → transformer → queries-keys-values.
- [ ] Vérifier que chaque transition annonce correctement la relation : prérequis, étape suivante ou mécanisme interne connexe.
- [ ] Vérifier les liens retour et les relations `related` FR/EN, sans transformer le graphe de connaissances en parcours linéaire.
- [ ] Vérifier que Q/K/V sont présentés comme des projections internes à chaque bloc Transformer, et non comme une étape après l'état contextualisé final.

### P1 — Proportion de la page Advanced

- [ ] Évaluer si l'enquête SAE est à sa juste place et proportionnée par rapport à la formalisation et aux résultats empiriques.
- [ ] Si elle surcharge l'approfondissement, inventorier d'abord les pages existantes sur l'interprétabilité avant de proposer un déplacement ; ne pas créer une page redondante.
- [ ] Vérifier que les résultats de probing restent explicitement distincts d'une preuve d'usage causal ou d'une attribution fonctionnelle exclusive.

### P2 — Évaluation pédagogique

- [ ] Faire relire les cartes et les exercices par un lecteur qui n'a pas suivi la rédaction.
- [ ] Vérifier que les quatre cartes testent des rappels distincts et ne dupliquent pas les exercices de transfert.
- [ ] Observer si le lecteur peut expliquer avec ses propres mots la différence entre lookup, information positionnelle, contexte accessible et état caché.
- [ ] N'étendre le nombre de cartes qu'après avoir identifié un besoin réel.

## 9. Travail restant — Wiki Knowledge

- [ ] Comparer le contenu exact de la PR #199 à l'issue #198 et confirmer que chaque candidat a un ChangePlan traçable.
- [ ] Vérifier les trois fiches source, leurs claims et leurs localisateurs dans les documents complets ; distinguer explicitement ce qui est tiré de l'article de ce qui relève de la synthèse éditoriale.
- [ ] Vérifier les éventuels artefacts d'extraction attendus par les modèles et outils canoniques ; ne pas considérer la présence de fiches source comme preuve que l'ingestion est entièrement achevée.
- [ ] Exécuter ou faire exécuter les validations canoniques sur le head courant : synchronisation du registre, validation, lint, rendu Quarto et audit des identifiants.
- [ ] Examiner les journaux des anciens échecs et les corriger à la source ; si les logs restent inaccessibles, relancer une validation contrôlée plutôt que conclure à partir d'un statut ancien.
- [ ] Vérifier le diff du registre : les changements doivent être limités aux enregistrements attendus et ne pas écraser des mises à jour indépendantes.
- [ ] Faire relire la synthèse comparative, puis seulement passer les statuts de brouillon aux statuts validés appropriés.
- [ ] Mettre à jour l'issue #198 et la PR #199 avec les preuves de validation ; fusionner uniquement après satisfaction des critères d'acceptation.

## 10. Ordre d'exécution recommandé

1. Terminer la revue visuelle et éditoriale de LLM Lab #1728 ; cette branche est techniquement validée.
2. Finaliser séparément l'ingestion Wiki Knowledge #199 ; ne pas bloquer la PR LLM Lab sur une validation documentaire externe si ses propres critères sont satisfaits.
3. Effectuer l'audit de continuité du parcours et le contrôle de proportion de la page Advanced.
4. Organiser un test de lecture court avant toute extension des cartes ou de la page.

**Critère de clôture :** le travail LLM Lab est terminé lorsque la PR #1728 a été relue puis fusionnée, que les pages publiées restent cohérentes dans les deux langues et que l'audit de parcours est clos. Le travail Wiki Knowledge est terminé séparément lorsque les validations canoniques et la provenance sont démontrées et que l'issue #198 peut être fermée sans réserve.
