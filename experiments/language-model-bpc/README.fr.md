# Surprisal des modèles de langage et bits par caractère (BPC)

**Statut : spécification du protocole uniquement. Aucun modèle n'a été évalué et aucun résultat empirique n'est revendiqué.**

## Question

Comment le coût de codage prédictif d'un modèle causal varie-t-il selon les domaines de texte tenus à l'écart, et dans quelle mesure l'estimation dépend-elle de la longueur du contexte et des conventions d'évaluation ?

Cette expérience rend opérationnelle la distinction entre surprisal au niveau du token et bits par caractère à l'échelle d'un corpus. Elle ne constitue pas une reproduction de Huang et al. (2024), un benchmark d'intelligence ni une preuve que la compression cause les capacités.

## Grandeurs principales

Pour une séquence de tokens \(x_1,\ldots,x_T\), le surprisal est

\[
s_t=-\log_2 P(x_t\mid x_{<t}),
\]

et la somme des log-vraisemblances négatives vaut \(L=\sum_t s_t\), en bits.

Pour un segment de texte défini précisément et contenant \(C\) points de code Unicode :

\[
\mathrm{BPC}=L/C.
\]

La convention du dénominateur doit être explicite. Ce protocole utilise les points de code Unicode du texte évalué décodé, et non les octets, graphèmes, tokens ou caractères après une normalisation non documentée. Le nombre d'octets UTF-8 est rapporté comme dénominateur secondaire afin de ne pas confondre BPC et bits par octet (BPB).

La perplexité est dérivée de la NLL moyenne par token et dépend du tokenizer. Elle n'est pas interchangeable avec le BPC.

## Plan expérimental

### Phase 1 — évaluation contrôlée d'un checkpoint

- Choisir un checkpoint causal et figer sa révision immuable, son architecture, les fichiers du tokenizer et sa révision.
- Charger uniquement un snapshot local explicite ou une source à révision figée. Indiquer si les poids ont été téléchargés ; ne jamais résoudre silencieusement une étiquette de modèle mutable.
- Utiliser un petit corpus d'évaluation dont la redistribution est autorisée ou des textes locaux fournis par l'utilisateur. Documenter provenance, licence, empreintes exactes des fichiers, encodage et prétraitement.
- Définir les partitions au niveau du document avant toute inspection ou sélection. Exclure les documents d'évaluation de la construction des prompts, de l'entraînement, de la calibration et du choix du modèle.
- Séparer les domaines (par exemple prose générale, prose technique et code) uniquement si provenance et licences le permettent ; ne pas agréger les scores en un chiffre global sans qualification.
- Évaluer chaque document indépendamment. Ne pas concaténer les documents de façon à permettre au précédent de conditionner le suivant.

### Conventions de calcul

- Utiliser le masque d'attention causal et le mode inférence ; désactiver le dropout.
- Évaluer chaque token de contenu exactement une fois. Les fenêtres chevauchantes peuvent fournir du contexte gauche, mais les tokens déjà évalués ne doivent pas être recomptés.
- Figer la longueur maximale de contexte et le stride. Documenter le contexte effectivement disponible pour chaque token cible, y compris la convention de préfixe initial.
- Expliquer comment le premier token de contenu est évalué. Préférer un token BOS explicite et documenté lorsqu'il est pris en charge. À défaut, déclarer la convention de préfixe compatible avec le modèle et ses conséquences.
- Ne pas compter les tokens spéciaux de préfixe dans le dénominateur de caractères. Préciser si les tokens spéciaux ajoutés par le tokenizer sont évalués ou exclus.
- Additionner les log-probabilités de manière stable (log-softmax, sans arrondir les probabilités). Rapporter le nombre total de tokens évalués, la NLL totale en bits, les points de code Unicode, les octets UTF-8 et les BPC/BPB correspondants.
- Vérifier que chaque position cible est évaluée une fois, que le nombre de tokens de contenu évalués correspond à la séquence attendue et qu'un petit exemple calculable à la main correspond à l'implémentation.

### Comparaisons pré-enregistrées

1. **Ablation du contexte :** évaluer le même checkpoint et les mêmes textes avec plusieurs longueurs de contexte prises en charge. Garder les autres paramètres constants.
2. **Décalage de domaine :** rapporter le BPC par domaine pour le même checkpoint, avec les effectifs par document et l'incertitude.
3. **Contrôle du stride :** répéter le calcul avec plusieurs strides valides et vérifier que la NLL totale est invariante à la tolérance numérique près lorsque le contexte effectif de chaque cible ne change pas. Si le contexte change, traiter cela comme une condition distincte.
4. **Comparaison facultative de checkpoints :** ne comparer des checkpoints qu'avec un corpus commun, des révisions explicites des modèles et tokenizers, des règles de calcul compatibles et une mention claire des différences de tokenizers.

## Comparabilité entre tokenizers

Le BPC normalise par le nombre de caractères, mais cela ne rend **pas automatiquement équivalents** des tokenizers différents. Ils induisent des segmentations et des modèles de probabilité différents sur les séquences de tokens. Une comparaison n'a de sens que si chaque modèle attribue des probabilités au même texte sous une convention d'encodage/décodage clairement spécifiée. Rapporter l'identité du tokenizer, son vocabulaire, la normalisation, le recours au byte fallback et la politique de tokens spéciaux. Considérer les classements entre tokenizers comme dépendants du protocole, et non universels.

Dans la mesure du possible, inclure une comparaison de checkpoints au sein d'un même tokenizer, qui constitue un contrôle plus propre. Ne jamais comparer la NLL moyenne par token ou la perplexité entre tokenizers comme si les unités étaient identiques.

## Informations à enregistrer

Au minimum :

- dépôt du checkpoint, révision immuable, architecture et format des poids ;
- dépôt/révision du tokenizer, vocabulaire et configuration des tokens spéciaux ;
- source, version, licence, empreintes des fichiers, identifiants des documents et partition du jeu de données ;
- décodage du texte, normalisation Unicode (de préférence aucune si elle n'est pas nécessaire), gestion des retours à la ligne et convention de comptage des caractères ;
- longueur du contexte, stride, convention de préfixe/BOS, troncature et comptage des tokens cibles ;
- versions logicielles, matériel, dtype, implémentation d'attention, paramètres déterministes et commande ;
- pour chaque document : nombre de tokens, NLL en bits, nombre de caractères, nombre d'octets, BPC et BPB ;
- méthode d'agrégation, procédure d'incertitude, exclusions et analyse des erreurs.

Rapporter séparément la moyenne macro des BPC par document et le rapport global \(\sum L/\sum C\) : ces deux quantités répondent à des questions différentes. Estimer l'incertitude par rééchantillonnage des documents (ou de groupes de sources supérieurs si les documents sont dépendants), et non des tokens individuels. Avec peu de documents indépendants, préciser que l'incertitude est mal déterminée.

## Limites d'interprétation

- Un BPC plus faible signifie que le modèle attribue une probabilité plus élevée au texte évalué selon ce protocole ; cela n'établit pas une intelligence générale, le raisonnement, la véracité ou une capacité causale.
- L'alignement de domaine, la contamination, la composition du corpus, la taille du modèle, les données d'entraînement, le tokenizer et le contexte influencent le score.
- Le BPC mesure la compression prédictive, pas la compression de la taille du modèle (quantification, pruning ou distillation).
- Une corrélation entre BPC et scores de benchmark n'est pas une causalité et ne définit pas l'intelligence.
- Un résultat sur un checkpoint ou quelques corpus ne peut établir une relation universelle.

## État de reproductibilité

Ce répertoire ne contient actuellement que la spécification du protocole. Avant de publier des résultats, implémenter et tester un calculateur garantissant le comptage exact une seule fois des cibles, une fixture minuscule vérifiable à la main, l'agrégation par document et un chargement explicite de modèle local. Exécuter ensuite toute la CI, le rendu Quarto et les contrôles navigateur. Aucun résultat ne doit être ajouté à la synthèse des sources avant examen indépendant de l'exécution, des droits sur les données et des limites.

## Ressources LLM Lab associées

- [Expérience jouet de compression prédictive](../predictive-compression/README.fr.md)
- [Expérience jouet sur entropie et surprisal](../entropy-surprisal-toy/README.fr.md)
- [Expériences de théorie de l'information](../information-theory/README.md)
- [Protocole expérimental](../../docs/experiment-protocol.md)
- [Synthèse sur compression et efficacité d'inférence](../../docs/source-syntheses/compression-intelligence-and-inference-efficiency-2026-11.md)
