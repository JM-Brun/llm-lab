# Suite du chantier « Modélisation du langage » — passation inter-sessions

**Date :** 2026-11-26  
**Branche de travail :** `ia/language-modeling-deepen-section`  
**PR associée :** [#1707 — organize Deepen around language modeling](https://github.com/JM-Brun/llm-lab/pull/1707)  
**État :** travail de structuration engagé ; PR non fusionnée ; validation CI incomplète.

Ce document est une feuille de route de reprise. Il distingue les blocages immédiats de la PR, les audits éditoriaux encore nécessaires et les évolutions à envisager ensuite. Il ne constitue pas une validation scientifique de toutes les pages Deepen.

## 1. État acquis à la fin de la session

La PR #1707 introduit une rubrique de navigation **Modélisation du langage / Language modeling**, qui rassemble cinq ensembles éditoriaux :

1. attention, position et architectures ;
2. texte, corpus et tokenisation ;
3. formalisation probabiliste et chaîne de l'entraînement ;
4. inférence et efficacité ;
5. échelle et questions de recherche.

**Outils mathématiques et géométrie** reste une rubrique sœur. La nouvelle rubrique est une collection de découverte : elle n'est ni un domaine de métadonnées, ni un parcours obligatoire, ni une relation de prérequis.

L'audit de redistribution des jours 1 à 3 est documenté dans [calendar-redistribution-destination-audit-2026-11-26.md](calendar-redistribution-destination-audit-2026-11-26.md). Il confirme, pour ce périmètre seulement, où les contenus déplacés ont été conservés dans Approfondir ou Practice. Il a également corrigé la découverte des approfondissements Zipf et tokenizer, le classement éditorial de Zipf et quelques placements de navigation.

Les relations de métadonnées ne doivent pas être déduites de la seule proximité dans le menu : hiérarchie conceptuelle, route de lecture suggérée, liens transversaux et graphe computationnel conservent des sémantiques différentes.

## 2. Priorité 0 — terminer et valider la PR #1707

### 2.1 Contrat de navigation et test — corrigé

**Résolu dans la branche.** Le test `tests/knowledge/test_flat_curriculum_sidebar.py` a été réaligné sur le contrat éditorial effectivement porté par les pages :

- `transformer-architectures`, `llm-limits` et `post-training` ont `destination:understand` et un niveau de leçon fondamentale ;
- elles restent hors de la navigation latérale Approfondir ;
- elles sont reliées depuis la carte éditoriale Deepen comme leçons associées ou point d'entrée, sans être reclassées comme approfondissements.

Le test vérifie désormais ces trois propriétés en français et en anglais, au lieu de conserver l'ancienne attente contradictoire qui exigeait leur présence dans la navigation Approfondir. La nouvelle exécution CI a confirmé la disparition des deux échecs FR/EN. Les quatre seuls échecs restants sur ce commit concernaient les artefacts générés, traités à la section suivante.

Cette correction conserve le contrat des pages et renforce le test : elle ne masque pas une page manquante et ne modifie pas les métadonnées pour satisfaire une assertion historique.

### 2.2 Régénérer les artefacts dérivés de la carte

Quatre tests échouent parce que les artefacts suivis dans Git ne correspondent plus aux sources de navigation et de métadonnées :

- `site/includes/generated-map-list-fr.qmd` ;
- `site/includes/generated-map-list-en.qmd` ;
- `site/includes/generated-map-data-fr.qmd` ;
- `site/includes/generated-map-data-en.qmd`.

Les différences observées comprenaient notamment l'ancien domaine Zipf (`probabilistic-foundations-training` au lieu de `text-tokenization`), les descriptions mises à jour et la nouvelle structure de navigation.

**Régénération effectuée dans la branche.** Les quatre fichiers ont été produits par `site/tools/build_learning_map.py` dans l'environnement CI, puis reportés tels quels dans Git :

- `site/includes/generated-map-list-fr.qmd` ;
- `site/includes/generated-map-list-en.qmd` ;
- `site/includes/generated-map-data-fr.qmd` ;
- `site/includes/generated-map-data-en.qmd`.

Aucune édition manuelle du contenu généré n'a été faite. La génération provient des sources canoniques ; le diff doit être relu avec les autres changements de navigation avant fusion.

### 2.3 Rejouer les contrôles

État au 2026-11-26, après les corrections et avant une nouvelle validation du dernier commit :

| Contrôle / correction | Résultat |
|---|---|
| Contrat de navigation FR/EN | Corrigé : les trois leçons Understand restent hors du menu Approfondir et sont liées depuis la carte éditoriale |
| Test de navigation | Corrigé ; les deux échecs FR/EN ont disparu dans l'exécution CI suivante |
| Quatre artefacts de carte bilingues | Régénérés par le générateur CI puis reportés dans la branche |
| Python quality and domain checks | Réussi sur le commit temporaire de maintenance |
| Secret scanning | Réussi sur le commit temporaire de maintenance |
| Quarto — rendu complet, contrôles de carte/graphe, liens locaux et audit navigateur | Réussi sur le commit temporaire de maintenance |
| Test suite sur ce commit temporaire | 4 échecs restants, tous liés aux artefacts générés qui ont été ensuite remplacés |

Le commit final de branche contient les quatre artefacts générés. L'instrumentation temporaire qui a servi à exporter les fichiers a été retirée ; le workflow Quarto ne conserve qu'un commentaire explicatif sur le contrat de fraîcheur des artefacts. **Aucun workflow CI n'a encore été observé sur ce dernier commit.** Il reste donc à obtenir une exécution fraîche de la suite complète et à vérifier ses résultats avant fusion.

Étapes restantes :

1. obtenir une exécution CI sur le dernier commit de la branche ;
2. vérifier que les tests de fraîcheur des quatre artefacts passent et que la suite complète est verte ;
3. vérifier les contrôles de qualité et de domaine, le scan des secrets, le rendu Quarto complet et l'audit navigateur ;
4. confirmer que la PR est toujours mergeable et que les workflows portent sur le dernier commit.

**Ne pas fusionner avant cette validation finale.** Les artefacts ont été générés depuis les sources canoniques, mais leur fraîcheur doit encore être confirmée par le test sur le dernier commit.

## 3. Priorité 1 — audit éditorial global de la rubrique Approfondir

L'audit de redistribution actuel porte sur les jours 1 à 3 et ne certifie pas la qualité de toutes les pages de destination. Une revue séparée doit couvrir l'ensemble de la rubrique.

Pour chaque page, établir une fiche courte avec :

- question durable à laquelle la page répond ;
- objectif d'apprentissage et périmètre exact ;
- notions et concepts canoniques mobilisés ;
- niveau réel : approfondissement, leçon fondamentale, référence ou pratique ;
- domaine éditorial principal et justification ;
- relation aux pages Understand, Build, Practice et aux autres approfondissements ;
- état FR/EN, ancres, figures, sources et rendu ;
- décision : conserver, déplacer, fusionner, scinder, réécrire ou mettre en attente.

### 3.1 Vérifier les frontières entre les cinq sous-domaines

Vérifier que les cinq sous-domaines de Modélisation du langage sont mutuellement compréhensibles et que chaque page a une place justifiable. Chercher en particulier :

- les pages dont le sujet principal est mal représenté par leur domaine ;
- les pages qui pourraient être classées dans plusieurs sous-domaines sans frontière explicite ;
- les rubriques trop larges ou les pages isolées ;
- les doublons de contenu entre pages voisines ;
- les pages qui relèvent plutôt d'outils mathématiques, de Build, de Practice ou de Reference.

La rubrique est une couche de navigation au-dessus des domaines existants. Ne pas créer un domaine `language-modeling` simplement pour refléter le nouveau titre de menu.

### 3.2 Revoir les frontières avec le parcours principal

Vérifier page par page que :

- Understand conserve le minimum conceptuel indispensable pour comprendre le fonctionnement d'un LLM ;
- Build conserve les explications nécessaires à l'implémentation ;
- Approfondir accueille les dérivations, variantes, analyses empiriques et questions spécialisées ;
- Practice accueille les exercices, manipulations et expériences qui doivent pouvoir croître sans alourdir les leçons ;
- Reference accueille les ressources dont le rôle est documentaire plutôt que pédagogique.

Une page ne devient pas un approfondissement simplement parce qu'elle est longue ou difficile. Le critère est son objectif pédagogique et sa relation au parcours principal.

## 4. Priorité 1 — vérifier la qualité des pages complémentaires des jours 1 à 3

L'audit de traçabilité a vérifié la destination des contenus déplacés, mais ne remplace pas une revue scientifique et éditoriale complète.

À reprendre :

- **Zipf :** vérifier que l'histoire centrale et le deep dive ont chacun un périmètre distinct ; contrôler les unités de comptage, la définition du rang, les conventions de corpus, l'interprétation des paramètres et les limites des comparaisons multilingues.
- **Surprisal :** vérifier la distinction entre information propre, surprisal conditionnel, entropie prédictive et entropie croisée ; confirmer que l'expérience Practice est reproductible et que ses unités sont explicites.
- **Tokenisation :** vérifier la séparation entre mécanismes (BPE, WordPiece, Unigram), décisions de conception, évaluation empirique multilingue et expérience Python ; contrôler les dénominateurs et les protocoles des métriques.

Vérifier aussi que les liens réciproques ne créent pas de dépendance obligatoire et que la lecture des pages complémentaires reste optionnelle.

## 5. Priorité 2 — poursuivre l'audit du calendrier sans extrapoler

L'audit actuel ne couvre que les jours 1 à 3 de la redistribution associée à la PR #1695. Il ne faut pas en déduire que les jours 4 à 24 ont été vérifiés.

À mesure que les jours suivants sont stabilisés :

1. comparer la version avant/après de chaque histoire ;
2. relever chaque contenu retiré, condensé ou ajouté ;
3. attribuer une destination précise : Approfondir, Practice, une page canonique existante, ou backlog pour une édition future ;
4. vérifier que la destination conserve les références, figures, démonstrations, ancres utiles et précautions ;
5. vérifier qu'aucun contenu n'est dupliqué inutilement ;
6. mettre à jour une matrice de traçabilité et les liens de découverte.

Les éléments intéressants mais trop volumineux pour l'histoire doivent être conservés dans un backlog réutilisable, et non supprimés ni ajoutés artificiellement au calendrier.

## 6. Priorité 2 — cohérence bilingue, métadonnées et graphe

Pour chaque page touchée par la structuration :

- vérifier l'équivalence de périmètre et de niveau entre FR et EN, pas seulement la présence des deux fichiers ;
- contrôler les ancres et liens internes dans les deux langues ;
- vérifier les champs `type`, `destination`, `topic`, `level`, `language`, `status` et `domain` selon le schéma existant ;
- maintenir les métadonnées internes invisibles pour le lecteur ;
- vérifier que `scope`, `purpose`, `summary`, `suggested_route`, `hierarchy` et `related` ont des rôles distincts ;
- ne pas utiliser un lien parent/enfant pour encoder une simple succession de calcul ou un ordre de lecture ;
- vérifier les relations vers les concepts canoniques dans `data/concepts.yml` et, si nécessaire, les ressources de `data/resources.yml` ;
- régénérer les artefacts dérivés après modification des sources.

L'objectif n'est pas de multiplier les relations. Chaque lien doit avoir une sémantique justifiable et utile à la découverte.

## 7. Invariants à préserver pendant les prochaines sessions

1. **Une porte du calendrier mène à une seule histoire centrale.** Un approfondissement compagnon est facultatif, n'est pas une seconde porte et ne s'ajoute pas à la durée annoncée de l'histoire.
2. **Approfondir est une collection permanente.** Les pages avancées restent accessibles hors saison et ne doivent pas être transformées artificiellement en histoires courtes.
3. **La navigation ne crée pas les relations conceptuelles.** Le menu, le graphe de connaissances, le graphe computationnel et le parcours pédagogique sont des objets différents.
4. **La chaîne de calcul d'un LLM doit rester exacte.** Ne pas déplacer Q/K/V après les représentations contextualisées finales : Q/K/V sont des projections internes à chaque bloc Transformer, appliquées aux représentations qui entrent dans ce bloc.
5. **Les branches génération, évaluation/scoring et entraînement doivent rester distinguées.** Elles partagent la distribution prédite par le modèle, mais n'ont pas le même objectif ni la même boucle.
6. **Ne pas dupliquer les explications canoniques.** Un approfondissement relie, dérive, compare ou critique ; il ne devient pas une deuxième version d'une leçon Understand.
7. **Ne pas transformer le chantier en infrastructure supplémentaire.** Réutiliser les générateurs, validateurs, registres et contrats existants ; ne pas créer un workflow GitHub Actions par page ou par notion.

## 8. Ordre de reprise recommandé

Pour une prochaine session, suivre cet ordre :

- [ ] Ouvrir la PR #1707 et confirmer son dernier commit, ses commentaires et ses checks.
- [x] Résoudre le contrat de placement de `transformer-architectures`, `llm-limits` et `post-training` : ce sont des leçons Understand, hors menu Approfondir.
- [x] Aligner le test bilingue sur ce contrat et vérifier les liens depuis la carte éditoriale.
- [x] Régénérer les quatre artefacts bilingues depuis `site/tools/build_learning_map.py` et les reporter dans la branche.
- [ ] Examiner le diff final des artefacts et exécuter la suite de tests complète sur le dernier commit.
- [ ] Revalider Quarto, l'audit navigateur, les liens et le scan des secrets sur ce même commit.
- [ ] Faire une revue qualitative de la carte Approfondir FR/EN et de ses frontières avec Understand, Build, Practice et Reference.
- [ ] Continuer ensuite les audits de contenu page par page, puis la traçabilité des jours 4 à 24 au fil de leur stabilisation.

## 9. Sources de reprise

- [PR #1707 — structuration de Modélisation du langage](https://github.com/JM-Brun/llm-lab/pull/1707)
- [Audit de redistribution des jours 1 à 3](calendar-redistribution-destination-audit-2026-11-26.md)
- [Contrat éditorial du calendrier](../advent-calendar-editorial-redesign.md)
- [Schéma des métadonnées de page](../page-metadata-schema.md)
- [Carte Approfondir FR](../../site/fr/deepen.qmd) et [EN](../../site/en/deepen.qmd)
- [Navigation Quarto](../../site/_quarto.yml)
- [Test du contrat de navigation](../../tests/knowledge/test_flat_curriculum_sidebar.py)
- [Générateur des cartes](../../site/tools/build_learning_map.py)


## 10. État de reprise vérifié — fin de session du 2026-11-26

Cette section complète le suivi précédent avec un instantané GitHub obtenu après les dernières réparations. Elle prévaut sur tout état de PR plus ancien mentionné dans les notes de session.

### État exact de la PR

- PR : [#1707](https://github.com/JM-Brun/llm-lab/pull/1707)
- État GitHub : **ouverte**, non fusionnée, non brouillon.
- Branche : `ia/language-modeling-deepen-section`, cible `main`.
- Dernier commit observé sur la tête de PR : `85cdeafaeb2a2d978f4cca3a297f17abd1b05166`.
- Nombre de commits annoncé par GitHub : 46 ; 17 fichiers modifiés.
- État `mergeable` retourné par GitHub lors de cette vérification : `false`.
- Exécution de workflow associée à ce SHA : aucune n'a été retournée par l'API de consultation utilisée pendant cette session.

Le statut `mergeable: false` doit être réévalué à la reprise : il peut être transitoire pendant le calcul GitHub ou refléter un conflit réel. Ne pas supposer lequel sans examiner l'état actualisé et, si nécessaire, le diff avec `main`.

### Travail restant — ordre strict de reprise

1. **Rafraîchir l'état GitHub avant toute écriture.** Relire la PR, la tête de branche, les checks, les commentaires et le diff. Ne pas partir du SHA mémorisé si la branche a avancé.
2. **Diagnostiquer `mergeable: false`.** Vérifier si GitHub signale un conflit avec `main`. Si oui, analyser les fichiers concernés et résoudre uniquement les conflits réels, sans écraser les changements de la branche. Si le statut est indéterminé/transitoire, attendre une nouvelle lecture plutôt que modifier le contenu.
3. **Obtenir une validation CI attachée au SHA courant.** Les succès observés sur le commit temporaire ne valident pas le commit final. Une relance d'un ancien run ne suffit pas si elle teste un ancien SHA. Utiliser une action GitHub prise en charge pour déclencher ou relancer les contrôles sur la tête courante ; si aucune action disponible ne le permet, consigner précisément cette limite.
4. **Lire les résultats, pas seulement le statut global.** Vérifier les quatre tests de fraîcheur des artefacts générés, la suite Python, les contrôles de domaine, le rendu Quarto, les contrôles carte/graphe, les liens locaux, l'audit navigateur et le scan des secrets. Pour chaque échec, relever le job, le test, le fichier et la cause avant de corriger.
5. **Ne corriger que les écarts confirmés.** Si les quatre artefacts échouent encore, relancer le générateur canonique `site/tools/build_learning_map.py` depuis les sources de la branche et comparer son résultat au diff suivi. Ne pas éditer les fragments générés à la main. Ne pas ajouter d'instrumentation temporaire durable au workflow.
6. **Relire le diff final et la documentation.** Confirmer que le commentaire explicatif dans `.github/workflows/quarto.yml` est toujours le seul changement de workflow et qu'aucun artefact temporaire, fichier de diagnostic ou changement hors périmètre ne subsiste.
7. **Fusionner uniquement si les contrôles requis sont verts sur le SHA courant**, que la PR est sans conflit et que son diff final reste conforme au périmètre décrit. Sinon, laisser la PR ouverte et documenter le blocage exact.

### Ce qui n'est pas un blocage immédiat de la PR

Les audits éditoriaux globaux décrits aux sections 3 à 6 restent importants, mais ils ne doivent pas être mélangés à la réparation CI de #1707. Ils constituent des chantiers distincts à planifier après la validation ou la fusion de cette PR :

- revue qualitative de toutes les pages de la rubrique Approfondir ;
- contrôle des frontières entre les cinq sous-domaines et avec Understand, Build, Practice et Reference ;
- vérification scientifique approfondie des destinations Zipf, surprisal et tokenisation ;
- poursuite de la traçabilité des jours 4 à 24, uniquement au rythme de leur stabilisation ;
- audit bilingue des métadonnées, ancres, relations et liens vers les concepts canoniques.

**Règle de reprise :** commencer par établir l'état réel de la PR et valider son dernier commit. Ne pas élargir la PR à un audit éditorial global tant que ce point n'est pas clos.


## 11. Diagnostic du dernier contrôle CI — commit `ef9dc472c2e588f3c8109aeb741df9a3aa510fa4`

Cette section prévaut sur les états antérieurs des sections 2, 8 et 10 pour le diagnostic du dernier contrôle observé.

### 11.1 État vérifié

La PR #1707 est toujours ouverte et non fusionnée. Sa tête est `ef9dc472c2e588f3c8109aeb741df9a3aa510fa4`, basée sur `4152d7bd31a5a1836c169e64f92f44a32437377a`. GitHub indique `mergeable: true`, mais `mergeable_state: unstable` pendant les contrôles.

Exécutions déclenchées pour cette tête :

- [CI — run 45894687167](https://github.com/JM-Brun/llm-lab/actions/runs/45894687167)
- [Quarto — run 45894687145](https://github.com/JM-Brun/llm-lab/actions/runs/45894687145)
- [Secret scanning — run 45894687212](https://github.com/JM-Brun/llm-lab/actions/runs/45894687212)

Résultats observés :
- Python quality and domain checks : **réussi**.
- Secret scanning : **réussi**.
- Test suite : **échoué**, avec **2 échecs, 832 réussites et 1 test ignoré**.
- Quarto site & browser audit : **encore en cours** au dernier relevé ; ne pas le considérer comme réussi.

### 11.2 Cause précise des deux échecs

Les deux échecs sont les variantes FR et EN de :

`tests/knowledge/test_map_artifacts_freshness.py::test_tracked_interactive_map_matches_renderer`

Le générateur de référence attend `domain: "text-tokenization"` pour les enregistrements :
- `fr/zipf-law-deep-dive` dans `site/includes/generated-map-data-fr.qmd` ;
- `en/zipf-law-deep-dive` dans `site/includes/generated-map-data-en.qmd`.

Or les artefacts suivis dans la branche contiennent encore `probabilistic-foundations-training` pour ces deux enregistrements. Les pages sources FR/EN déclarent bien `text-tokenization`. Le problème est donc un écart entre la source canonique et les données interactives générées, pas une erreur du schéma de domaine des pages sources.

**Correction antérieure insuffisante :** les enregistrements générés avaient été modifiés ponctuellement et les rubriques de la carte réconciliées par fusion de champs. Cela n'a pas produit une sortie identique à celle du générateur. La mention précédente d'une régénération complète ne doit donc pas être interprétée comme une validation de fraîcheur sur la tête actuelle. Le test de fraîcheur reste l'arbitre.

### 11.3 Actions immédiates restantes

1. Depuis la racine du dépôt, exécuter le générateur canonique avec l'environnement attendu par les tests :

   ```bash
   uv run --no-project --with-requirements docs/requirements-history-validation.txt \
     --python 3.12 python site/tools/build_learning_map.py
   ```

2. Examiner le diff des quatre artefacts suivis :
   - `site/includes/generated-map-list-fr.qmd`
   - `site/includes/generated-map-list-en.qmd`
   - `site/includes/generated-map-data-fr.qmd`
   - `site/includes/generated-map-data-en.qmd`

   Ne pas reconstruire les JSON à la main et ne pas recopier uniquement le champ `domain`. Conserver toutes les sorties produites par le générateur ; vérifier que les modifications restent cohérentes avec les pages sources FR/EN et la structure éditoriale de cette PR.

3. Exécuter localement, si l'environnement le permet, les tests ciblés de fraîcheur :

   ```bash
   uv run pytest tests/knowledge/test_map_artifacts_freshness.py
   ```

   Puis exécuter la suite complète.

4. Committer les artefacts réellement générés et mettre à jour la PR. Une nouvelle exécution CI doit porter sur la nouvelle tête, pas sur `ef9dc47`.

5. Relever le résultat final de Quarto/browser audit sur le dernier commit. Si le run actuel échoue, diagnostiquer son log avant d'ajouter une correction. S'il réussit sur `ef9dc47`, il ne valide pas automatiquement le commit ultérieur contenant les artefacts régénérés : vérifier si un nouveau run est nécessaire selon le SHA contrôlé.

6. Confirmer sur le même SHA :
   - tests complets verts ;
   - Python quality/domain checks verts ;
   - Quarto full render et browser audit verts ;
   - secret scanning vert ;
   - PR sans conflit et diff final limité au périmètre prévu.

**Ne pas fusionner avant ces contrôles.**

### 11.4 Hors blocage immédiat

L'avertissement de `test_lesson_duration.py` liste des leçons sous la cible éditoriale de 10–15 minutes et quelques leçons au-dessus. Il n'est pas à l'origine de l'échec de la suite (le test a émis un avertissement, pas un échec). Le traiter dans un audit éditorial séparé ; ne pas élargir la réparation CI de #1707 à une réécriture des durées.

Les audits éditoriaux globaux des sections 3 à 6 restent également hors du périmètre de réparation immédiate.


## 12. Réparation canonique des artefacts de carte — 2026-11-26

### Diagnostic exact

La suite de tests sur le commit `e75146270145d59f90584feebbdc45938f758ed2` échouait uniquement sur :

- `test_tracked_interactive_map_matches_renderer[fr]`
- `test_tracked_interactive_map_matches_renderer[en]`

Le diff du test indiquait une divergence dès le premier caractère : les fichiers suivis commençaient directement par `<script type="application/json"...>`, alors que le générateur attend le commentaire de provenance puis le bloc Quarto brut ```{=html}`. Les modifications manuelles du JSON avaient donc supprimé l'enveloppe de rendu générée. Le contenu JSON seul ne suffisait pas à satisfaire le contrat de fraîcheur byte-for-byte.

### Réparation effectuée

- Le générateur canonique `site/tools/build_learning_map.py` a été exécuté dans l'environnement Python 3.12 de la CI Quarto, avec les dépendances `docs/requirements-history-validation.txt`.
- Les sorties complètes ont été commitées depuis ce worktree CI par le commit `2d62cc17d9e707e239cb765662ea4f90218d0d78`.
- Les deux fichiers réécrits sont :
  - `site/includes/generated-map-data-fr.qmd`
  - `site/includes/generated-map-data-en.qmd`
- Les listes FR/EN n'ont pas nécessité de modification supplémentaire.
- Vérification après génération : les deux fichiers commencent à nouveau par le commentaire `Generated by site/tools/build_learning_map.py; do not edit by hand.`, suivi du bloc ```{=html}`; le JSON est parseable.
- La hiérarchie de navigation générée correspond au sidebar : parent `Modélisation du langage / Language modeling`, cinq sous-domaines, puis `Outils mathématiques et géométrie / Mathematical tools and geometry` comme section sœur.
- Les pages Zipf (story et deep dive) portent toutes deux le domaine `text-tokenization` dans les deux langues.

### Nettoyage de l'instrumentation

Une étape temporaire de workflow a été utilisée pour lancer le générateur dans un worktree basé sur la tête de PR et commiter ses sorties exactes. Cette étape a échoué une première fois sur le contrôle Git `safe.directory`, puis a réussi après ajout explicite des chemins du worktree. L'étape temporaire et l'élévation de permission `contents: write` ont ensuite été retirées ; le workflow retrouve `contents: read`. Le commentaire permanent qui explique le contrôle de fraîcheur des artefacts reste en place.

### Validation encore requise

Le commit de génération a déclenché des runs avec le résultat `action_required` (les workflows déclenchés par le bot n'ont pas été exécutés). Le commit de nettoyage du workflow doit être suivi d'une exécution normale sur la tête finale. Vérifier explicitement :

1. `test_tracked_interactive_map_matches_renderer[fr/en]` passe sur le SHA final ;
2. suite complète de tests ;
3. rendu Quarto, contrôles de carte/graphe, liens locaux et audit navigateur ;
4. contrôles Python/domain et secret scanning ;
5. statut de fusion et absence de conflit avec `main`.

Ne pas prendre les succès d'une ancienne tête ni le succès de la seule étape de génération pour une validation de PR. Ne pas fusionner avant que tous les contrôles requis soient verts sur le même SHA.


## 13. Réconciliation avec main et régénération finale — 2026-11-26

Après la réparation du wrapper, `main` a avancé avec le commit `1216d5fca5ad02acff6b95f53b3a3ed9c7b3154e` (PR #1717), qui approfondit le lookup d'embeddings dans les deux langues et met à jour le parcours guidé.

### Intégration préservée

- La branche #1707 a été réconciliée avec ce commit via un commit de fusion à deux parents : `326b1e1ca4de185f250e202714509923e84eda5e`.
- Les changements de #1717 conservés comprennent `data/guided-route.yml`, les leçons FR/EN `embedding-space.qmd` et leurs fiches `revision-embedding-space.qmd`.
- Les données de carte ont ensuite été régénérées sur l'arbre fusionné, afin d'intégrer les métadonnées de l'exercice de lookup tout en préservant l'arborescence Language modeling de #1707.
- Commit de génération canonique : `0c3811881d687c55851c7e42657e2a026e980151`.
- La vérification du JSON généré confirme que les résumés FR/EN de `embedding-space` reflètent la séquence ordonnée d'IDs, et que les sections de navigation restent bilingues et imbriquées comme prévu.
- Les domaines des pages Zipf story/deep dive restent `text-tokenization` en FR et EN.

### Nettoyage et état Git

- L'étape temporaire de régénération/commit du workflow a été retirée.
- Les permissions du workflow sont revenues à `contents: read`.
- Le commentaire permanent sur le test de fraîcheur des artefacts est conservé.
- Dernière tête après nettoyage : `9de7c9e6a7867df558020add0a9e2f70fffdb17c`.
- Comparaison avec `main` : branche en avance de 68 commits, en retard de 0 ; GitHub indique `mergeable: true`.

### Validation finale

Des exécutions CI, Quarto et secret scanning ont été déclenchées sur `9de7c9e6a7867df558020add0a9e2f70fffdb17c`. Leurs résultats doivent être relus sur ce SHA précis. Les runs sur les commits intermédiaires `2d62cc1` et `0c38118` sont `action_required` car ils ont été créés par le bot pendant la régénération ; les runs sur les parents antérieurs échouent encore sur les anciens artefacts et ne sont pas représentatifs de l'état final.

Ne pas fusionner avant que la suite complète, le rendu Quarto/audit navigateur, les contrôles Python/domain et le secret scanning soient tous réussis sur le SHA final.
