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
