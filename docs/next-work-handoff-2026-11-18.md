# LLM Lab — cahier de reprise opérationnel

**Date de l'instantané :** 18 novembre 2026 (Europe/Paris)  
**Branche de référence observée :** `main`  
**SHA de `main` vérifié :** `b32663df12166ad0bbffaff7e948a79c551a429c`  
**Objet :** transmettre aux prochaines sessions un ordre de travail exécutable, avec les états GitHub et les limites de preuve.  
**Règle :** ce document est un cahier de reprise daté, pas un second système de suivi. Les issues et PR restent les sources de vérité pour leur état.

## 1. État des PR actives

### PR #1277 — tests d'invariants critiques

- URL : https://github.com/JM-Brun/llm-lab/pull/1277
- Branche : `test/critical-invariants-audit-clean`
- HEAD vérifié : `68f9bc205699a40a21a378bd6902dd4b0b7ca0f4`
- État au dernier fetch : ouverte, non fusionnée, mergeable.
- Validation terminée sur ce HEAD exact :
  - Python quality and domain checks : succès (job `135017010363`, run `44365219499`).
  - Suite complète de tests : succès (job `135017012033`, run `44365219499`).
  - Quarto : succès (run `44365219545`).
  - Secret scanning : succès (run `44365219836`).
  - Inventaire full-corpus et benchmark de capacité : ignorés, car opt-in et non déclenchés par cet événement PR.
- Un commentaire de validation finale a été ajouté à la PR après la vérification des jobs.
- La PR #1275 est fermée sans fusion ; son travail a été repris dans #1277 sur une branche propre.

**À faire :** examiner le diff complet et la pertinence des invariants ajoutés ; si cela apporte une vraie valeur, effectuer une mutation ciblée pour vérifier que les tests échouent lorsque l'invariant est violé. Ne pas merger automatiquement : la validation CI ne remplace pas la revue du contenu.

### PR #1276 — matrice de validation des sources

- URL : https://github.com/JM-Brun/llm-lab/pull/1276
- Branche : `docs/source-contract-matrix-as-built`
- HEAD précédemment vérifié : `6fddd450f903faec1efbf8bedd9de04e0708d7c5`
- État au dernier fetch : ouverte, non fusionnée, mergeable.
- La matrice décrit le comportement réellement implémenté, les tests directs et les garanties non établies. Elle ne présente pas les règles proposées comme déjà appliquées.
- Les checks CI, Quarto et secret scanning avaient réussi sur le HEAD cité dans le commentaire de suivi de cette PR.

**À faire :** refetcher la PR, son HEAD et ses checks avant toute décision. Relire les champs bibliographiques, droits, langue, version et historique de scan à la lumière de cette matrice. Ajouter des tests seulement lorsque le contrat est explicite et compatible avec les données historiques.

## 2. Priorité A — provenance et graphe de connaissances (#1211)

Issue : https://github.com/JM-Brun/llm-lab/issues/1211

### Instantané de couverture connu

Sur le snapshot de `main` vérifié au SHA `b32663df12166ad0bbffaff7e948a79c551a429c` :

- 139 sources canoniques, 84 fichiers d'extraction, 432 items et 102 concepts.
- Aucun `source_id` d'extraction orphelin ; les jointures doivent utiliser le `source_id` déclaré dans le YAML, jamais une heuristique sur le nom du fichier.
- 55 sources sans extraction dédiée. C'est une file de revue, pas un défaut automatique.
- 5 sources sans lien concept et 3 sans destination de page.
- 44 dates de publication inconnues et 128 statuts de licence inconnus à l'échelle du catalogue.
- 134 sources partiellement scannées, 3 scannées et 2 inaccessibles.
- Les 55 sources sans extraction ont des pointeurs vers des dossiers d'audit, mais ces pointeurs ne prouvent pas qu'une décision source par source a été documentée.

### Travail restant

1. **Terminer les 12 papiers prioritaires**, un par un :
   - identifier le claim exact utilisé dans les pages FR/EN ;
   - retrouver la version canonique et un localisateur précis (page, section, tableau, figure ou passage) ;
   - consigner méthode, corpus/données, protocole, métriques, hypothèses et limites ;
   - distinguer source primaire et secondaire ;
   - décider si une extraction atomique améliore réellement la traçabilité.
2. **Classer les 43 autres sources sans extraction** : référence bibliographique/contexte, référence d'implémentation, cours/tutoriel, extraction justifiée, différée, inaccessible, doublon/supersédée ou rejetée. Chaque décision doit avoir une raison vérifiable.
3. **Réconcilier l'historique de scan avec le périmètre réellement inspecté**. Ne pas promouvoir un scan partiel en scan complet sans preuve.
4. **Examiner les 5 divergences nom de fichier / `source_id`** et documenter la convention d'identité. Ne pas renommer les fichiers uniquement pour aligner leur nom.
5. **Revoir les sources inaccessibles et les métadonnées inconnues** sans fabriquer dates, versions ou licences. Distinguer les droits du texte, des figures, du code et des données.
6. **Vérifier les liens canoniques** vers pages, concepts et dossiers d'audit, sans confondre présence d'un lien et qualité de son contenu.

Les 12 papiers prioritaires recensés dans l'issue comprennent notamment RoFormer/RoPE, Goldman et Schmidt sur l'évaluation des tokenizers, Sentence-BERT, ColBERT/ColBERTv2, SPLADE, BEIR et ColPali. Reprendre la table détaillée de l'issue #1211 avant de choisir le prochain papier ; ne pas reconstruire la liste de mémoire.

## 3. Priorité B — contrat et validateur (#1226)

Issue : https://github.com/JM-Brun/llm-lab/issues/1226

### État connu

- L'inventaire complet porte sur 84 fichiers et 432 items.
- Les contrôles actuels trouvent zéro locator absent, scalaire ou de forme non prise en charge dans `items[].locator`, et zéro erreur YAML/enregistrement dans le snapshot audité.
- Le contrat observé de `items[].locator` est une correspondance avec `type` et `value` non vides ; `label` est facultatif (361 présents, 71 absents).
- Ces résultats ne couvrent pas les chaînes descriptives de locateur dans les graphes pédagogiques, qui relèvent d'un autre contrat.
- PR #1276 documente l'état « as-built » du validateur ; elle ne change pas le validateur ni les données canoniques.

### Travail restant

1. Auditer les métadonnées source : URL canonique, titre, créateurs/éditeur, langue, date, version/révision, licence et droits de réutilisation.
2. Auditer les événements d'historique de scan et leur cohérence avec le contenu réellement consulté.
3. Clarifier les sémantiques des types de locateur, en particulier `section` (très fréquent) et `external-source` / `external-code`. Ne pas imposer une grammaire uniforme si les usages historiques sont hétérogènes.
4. Définir quels cas restent des avertissements ou rapports (types inconnus, clés additionnelles, métadonnées manquantes) et lesquels sont des erreurs structurelles.
5. Séparer explicitement :
   - erreur structurelle ;
   - avertissement de qualité ;
   - décision éditoriale/scientifique nécessitant une revue humaine.
6. Ajouter des fixtures temporaires ciblées pour les seules règles contractuelles établies. Garder les dates/licences inconnues comme inconnues ; ne pas convertir une lacune historique en échec CI sans politique décidée.
7. Maintenir la distinction entre attribution d'une preuve, relation d'un claim à une source, niveau de confiance et indépendance des sources.

## 4. Prochaine tranche scientifique — compression et codage

Le pilote existant distingue déjà l'attention exacte IO-aware (FlashAttention), l'information mutuelle et les contrôles négatifs. Le codeur lossless rationnel exact sert d'oracle pédagogique, mais n'est pas un codeur de production.

Prochaine étape technique recommandée :

1. implémenter un codeur arithmetic/range à état entier borné avec renormalisation ;
2. spécifier et tester underflow, terminaison, framing, troncature et corruption ;
3. conserver l'oracle rationnel comme référence ;
4. ajouter golden vectors et tests exhaustifs sur petits alphabets/états, puis cas de longues séquences et désaccord modèle/table ;
5. rendre explicite le coût de transmission des tables, du modèle, de l'en-tête et du padding ;
6. seulement ensuite définir le protocole causal-LM BPC/BPT : versions modèle/tokenizer, corpus et split, licence, conventions BOS/EOS, contexte/stride et séparation des coûts.

Ne pas confondre codage de la source, compression du modèle (quantization/pruning/distillation) et coûts d'exécution (KV cache, activations, HBM).

## 5. Règles de méthode à préserver

- Un locateur structurellement présent n'est pas nécessairement résoluble.
- Un locateur résoluble ne prouve pas que la source a été consultée.
- Une source consultée ne prouve pas qu'elle soutient le claim associé.
- Plusieurs références ne prouvent pas une corroboration indépendante.
- Un lien vers un dossier d'audit n'est pas une décision documentée.
- Un statut de scan n'est pas une preuve autonome du périmètre inspecté.
- Les résultats de validation doivent toujours être rapportés avec le SHA exact et les identifiants de run/job.
- Ne pas dupliquer les registres ou schémas ; faire évoluer les sources canoniques et les contrats existants.
- Ne pas fusionner de PR ni fermer d'issue sans autorisation explicite.

## 6. Protocole de reprise pour la prochaine session

1. Lire ce document puis refetcher `main`, #1276, #1277, #1211 et #1226 : les états et SHA peuvent avoir changé.
2. Vérifier les workflows associés aux HEAD actuels ; ne pas réutiliser un résultat d'un ancien commit.
3. Si #1277 est toujours ouverte, effectuer la revue du diff et une mutation ciblée pertinente ; consigner le résultat dans la PR.
4. Choisir **un seul** lot source à examiner dans #1211 : reprendre la table des 12 papiers prioritaires ou sélectionner un sous-lot identifié des 43 autres sources.
5. Pour chaque source, documenter le claim, le localisateur consulté, la version, la méthode, les limites, le rôle dans le projet et la décision d'extraction.
6. Reporter les résultats dans l'issue propriétaire et dans les fichiers canoniques concernés ; éviter les commentaires génériques qui ne font que répéter les compteurs.
7. Ne créer une PR qu'avec un diff cohérent, des tests adaptés et une synthèse des validations sur le HEAD exact.

## 7. État de ce document

Ce cahier de reprise décrit les informations vérifiées lors de la session du 18 novembre 2026. Il ne certifie pas que les PR sont fusionnables aujourd'hui, que les sources ont été relues ou que les conclusions scientifiques ont été validées. Refaire les vérifications live avant toute action.

---

## 8. Mise à jour de reprise — fin de session du 18 novembre 2026

**Snapshot main contrôlé :** 67feb1fc528f73d253be0b4092dd64949291bd33.  
**Branche documentaire :** docs/next-session-handoff-2026-11-18, créée depuis ce snapshot.  
Les états GitHub ci-dessous ont été refetchés pendant cette session ; refaire les vérifications avant toute action.

### 8.1 PR #1315 — workflows verts, revue humaine toujours bloquante

- PR : https://github.com/JM-Brun/llm-lab/pull/1315
- HEAD exact : 76aca6d5a4eb0c1ddb5e6a55a37d772a0d0f49e5
- Base : main ; PR ouverte, non fusionnée, techniquement mergeable.
- Checks sur ce HEAD exact :
  - CI : success, run 44413627053.
  - Secret scanning : success, run 44413627057.
  - Quarto site : success, run 44413627164.
- Reviews soumises : aucune. Inline review threads : aucun.
- Un commentaire final a été ajouté à la PR pour consigner les trois succès et rappeler l'exigence de revue indépendante.

**À faire :** obtenir une revue indépendante du diff et des deux tests de régression. Revoir le patch complet, pas seulement les descriptions. Ne pas fusionner tant que cette revue n'est pas présente et satisfaisante. Ne pas prétendre que les tests ont été exécutés localement dans cette session.

### 8.2 #1306 — contrat livré, backfill toujours non réalisé

- PR #1312 est fusionnée : contrat initial du registre et de l'appartenance explicite.
- PR #1313 est fermée comme superseded, non fusionnée ; ne pas la réouvrir ni réutiliser ses affectations non approuvées.
- PR #1315 complète le validateur : aucun champ collections dans une extraction ; validation du type de status avant test d'appartenance.
- data/source-collections.yml est volontairement vide ; aucune appartenance source n'a été ajoutée.
- Les deux dossiers de collection nommés explicitement sont :
  - docs/source-reviews/qkv-source-collection.md
  - docs/source-reviews/tokenization-embeddings-source-collection.md
- Le dossier visuel docs/source-reviews/visual-learning-resources-2026-11.md ne suffit pas à décider qu'il constitue une collection autonome.
- Les tags, thèmes, concepts, titres, chemins, citations et proximités documentaires ne sont jamais une preuve d'appartenance.

**À faire après revue/fusion de #1315 :**
1. Faire approuver les identités des collections (ID stable, titre, chemin canonique, périmètre, statut).
2. Pour chaque source candidate, obtenir une décision explicite : collection(s) assignée(s), ou liste vide explicite. Conserver les cas ambigus non assignés.
3. Réconcilier séparément les nombres de sources distinctes, fichiers d'extraction et items atomiques.
4. N'ajouter les appartenances qu'après approbation, puis vérifier les comptes calculés par le validateur.
5. Garder #1306 ouverte jusque-là.

### 8.3 #1211 — couverture et prochaine source à traiter

Instantané déclaré dans le corps courant de l'issue :
- 139 sources canoniques ; 84 fichiers d'extraction ; 84 source_id déclarés uniques ; zéro ID d'extraction orphelin.
- 55 sources sans extraction dédiée : file de revue, pas défaut automatique.
- Parmi ces 55 : 27 dates de publication inconnues, 48 statuts de licence inconnus, 53 scans partiels et 2 sources inaccessibles.
- Les noms de fichiers ne sont pas l'identité canonique : toutes les jointures utilisent le source_id YAML.

**RoFormer / Su et al. (2021) : traité dans les artefacts existants**, pas à refaire :
- data/extractions/su-roformer-rope-2021.yml : cinq items atomiques.
- docs/source-reviews/roformer-rope-2021.md : revue primaire.
- Pages RoPE et encodage positionnel FR/EN reliées.
- La revue conserve l'absence de reproduction indépendante et les limites de généralisation.

**Prochaine tranche recommandée : Goldman (2024) et Schmidt (2024)**, dans les pages tokenizer-design-evaluation FR/EN. Pour chacun : identifier précisément le claim, retrouver la version primaire, consigner protocole, échantillon, métriques, hypothèses et limites ; distinguer corrélation et preuve causale. Ensuite traiter Sentence-BERT, ColBERT/ColBERTv2, SPLADE/BEIR et ColPali selon la table de l'issue. Classer les 43 autres sources sans extraction sans en créer une par défaut.

### 8.4 #156 et #163 — assets : ne pas confondre inventaire, provenance et licence

- #156 reste ouverte.
- Dernière mise à jour documentaire mentionnée dans l'issue : PR #1304 fusionnée, inventaire de 81 SVG locaux ; le diff de cette PR ne modifiait que le registre, pas les images ni les pages.
- Les quatre SVG historiquement signalés pour confirmation de provenance sont : contextualization-pipeline-en.svg, contextualization-pipeline-fr.svg, transformer-stack-en.svg, transformer-stack-fr.svg. Vérifier le registre courant et les confirmations avant de les considérer résolus.
- Les sources statiques identifient des images distantes et des mécanismes responsives, mais ne prouvent pas le currentSrc effectivement sélectionné, ni le succès réseau du rendu.
- L'illustration Rushang Chauhan est documentée comme lien externe et non comme embed courant sur les pages contextualized-representations après #1308 ; ne pas la requalifier sans nouvelle preuve.
- #163 porte la décision de licence asset-level ; aucune licence ne doit être inférée de la provenance. Les SVG restent exclus des licences MIT/CC BY-SA tant qu'aucune décision explicite n'est prise.

**À faire :**
1. Obtenir les confirmations propriétaires restantes ou les détails d'origine/adaptation.
2. Réaliser l'inventaire DOM rendu FR/EN sur desktop et mobile : page, viewport, élément, currentSrc, src, srcset, sizes, alt, dimensions naturelles et résultat réseau.
3. Dédupliquer sans supprimer les paramètres d'URL nécessaires à l'accès ; distinguer images intégrées et simples liens.
4. Rattacher chaque observation au registre ; séparer disponibilité technique, provenance, droits et attribution.
5. Préserver absolument les illustrations existantes : ne pas retirer, remplacer, masquer, désactiver ou convertir en lien dans le cadre de cet audit.

### 8.5 ENG-02 — mutations non exécutées, KPI non mesuré

- Inventaire candidat ATTENTION/LOSSES : docs/audits/eng-02-critical-invariants-inventory-2026-11-18.md.
- Le décompte historique de 48 regroupements est retiré comme dénominateur ; granularité à poursuivre et approbation du dénominateur encore nécessaires.
- ENG-02 reste **not measured**.
- MUT-01 à MUT-05 n'ont pas été exécutées. Les tests présents et les inspections statiques ne prouvent pas leur sensibilité.
- Protocole attendu : clone propre, SHA noté, une mutation à la fois, sentinelle ciblée, capture du résultat, restauration, git diff --exit-code, arbre propre et SHA inchangé. Pas de commit/push des mutations.

**À faire :** reprendre les décompositions atomiques ATTENTION/LOSSES et concevoir le test discriminant GEN-03, puis exécuter les cinq mutations uniquement dans un véritable environnement local disponible. Ne publier aucun pourcentage avant approbation du dénominateur et exécution réelle.

### 8.6 Ordre de reprise recommandé

1. Refetcher #1315 et ses checks sur le HEAD actuel ; obtenir la revue indépendante ; fusion uniquement après approbation.
2. Après fusion, reprendre #1306 avec les décisions explicites d'identité et d'appartenance ; ne pas remplir le registre par inférence.
3. Sur #1211, traiter Goldman et Schmidt avec extraction seulement si elle ajoute une traçabilité claim-source réelle.
4. Sur #156, obtenir les confirmations de provenance et préparer le protocole DOM rendu ; préserver tous les visuels.
5. Reprendre ATTENTION/LOSSES et GEN-03 ; préparer l'environnement réel pour les mutations sans simuler de résultat.
6. Après chaque lot, mettre à jour l'issue propriétaire et ce cahier de reprise avec SHA, fichiers, preuves, décisions et blocages.

**Règle de session :** commencer par les états live et les SHA, ne jamais traiter un statut ancien comme actuel, et maintenir séparément les preuves statiques, les résultats CI, la revue humaine, le rendu navigateur et la sensibilité aux mutations.
