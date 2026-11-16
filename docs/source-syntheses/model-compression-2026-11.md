# Compression des LLM — synthèse critique

**Source :** Sasirekha Cota, “Understanding Compression of Large Language Models (LLMs)”, 22 novembre 2023.  
**URL :** https://medium.com/@sasirekharameshkumar/understanding-compression-of-large-language-models-2ee3b8a350a2  
**Langue :** anglais. **Type :** article introductif de vulgarisation.  
**Scan :** corps complet récupéré ; ressources liées partiellement vérifiées.  
**Réutilisation :** lien et reformulation seulement ; aucune licence de republication établie.

## 1. Question d'apprentissage

Comment réduire l'empreinte mémoire, le coût de calcul ou la latence d'un modèle de langage sans dégrader excessivement ses capacités ?

**Position pédagogique :** cette source traite de la **compression du modèle** (réduction des paramètres, de leur précision ou transfert vers un modèle étudiant). Elle ne traite pas du même sens de « compression » que la modélisation probabiliste / compression prédictive abordée dans le dossier [LLMs and compression algorithms](llms-and-compression-algorithms-2026-11.md). Les deux sujets doivent rester explicitement distincts.

## 2. Résumé fidèle

L'article présente trois familles :
1. **Pruning (élagage)** : supprimer des poids ou des composants considérés comme peu utiles.
2. **Quantization (quantification)** : représenter les poids et parfois les activations avec une précision numérique plus faible.
3. **Knowledge distillation (distillation de connaissances)** : entraîner un modèle étudiant plus petit à reproduire certains comportements d'un modèle enseignant.

Il distingue l'élagage structuré et non structuré, la quantification post-entraînement (PTQ) et l'entraînement conscient de la quantification (QAT), ainsi que la distillation black-box et white-box. Il évoque aussi la quantification du cache KV.

## 3. Carte des contributions

| Élément | Contribution | Nature / force |
|---|---|---|
| Taxonomie pruning / quantization / distillation | Trois familles faciles à distinguer | Bonne porte d'entrée, non exhaustive |
| Élagage structuré / non structuré | Relie la granularité de suppression à la forme de sparsité | Distinction utile ; performance matérielle non garantie |
| PTQ / QAT | Distingue compression après entraînement et adaptation pendant entraînement | Distinction fondamentale |
| Activations et outliers | Introduit une difficulté pratique de la quantification | Simplifiée ; à approfondir avec des travaux dédiés |
| Teacher / student | Rend intuitive la distillation | Bon modèle mental, mais dépendant des objectifs et données |
| Cache KV | Ouvre vers la mémoire d'inférence | À séparer de la taille persistante du checkpoint |

## 4. Corrections et nuances indispensables

### 4.1 Pruning : sparsité ne signifie pas automatiquement accélération

- L'élagage **structuré** retire des unités organisées (neurones, canaux, têtes ou couches selon la méthode) et peut produire des dimensions plus petites, directement exploitables par des kernels denses.
- L'élagage **non structuré** met à zéro des poids individuels ; il produit une matrice irrégulièrement creuse.
- Une matrice avec 50 % de zéros n'entraîne pas automatiquement 2× moins de latence. Il faut que le format de sparsité, les kernels et le matériel puissent exploiter ces zéros sans surcoût supérieur.
- SparseGPT montre qu'un élagage one-shot peut atteindre au moins 50 % de sparsité sur les modèles GPT étudiés, et jusqu'à 60 % sur OPT-175B et BLOOM-176B avec une hausse négligeable de perplexité dans les expériences rapportées. C'est un résultat expérimental circonscrit, pas une garantie générale de vitesse ou de qualité.

### 4.2 Quantization : préciser ce qui est quantifié

- **Weight-only** : les poids du checkpoint sont quantifiés ; les activations peuvent rester en précision supérieure.
- **Weight-activation (par ex. W8A8)** : poids et activations sont quantifiés, ce qui peut permettre des calculs entiers efficaces si le matériel et les kernels le prennent en charge.
- **PTQ** : la quantification est appliquée après l'entraînement, souvent avec calibration sur des exemples représentatifs.
- **QAT** : le modèle est entraîné ou adapté en tenant compte des effets de quantification.
- Les outliers d'activations peuvent rendre la quantification difficile. SmoothQuant illustre une méthode PTQ qui déplace une partie de la difficulté des activations vers les poids par une transformation mathématiquement équivalente.
- Les chiffres de réduction « 4× » ou d'accélération « 2×–3× » cités dans l'article ne sont pas des lois générales. Les résultats dépendent des tenseurs quantifiés, de la précision, des échelles/zéros, du format, des kernels, du matériel, du batch, de la longueur de contexte et de la charge de travail.

### 4.3 KV cache : mémoire d'exécution, pas poids du modèle

Le cache clé-valeur conserve des états intermédiaires utiles pendant la génération autoregressive. Sa quantification peut réduire la mémoire de travail et parfois le trafic mémoire, mais elle ne réduit pas directement la taille du fichier de poids du modèle. Elle peut affecter la qualité et dépend aussi des kernels d'inférence. À enseigner comme une optimisation distincte du checkpoint.

### 4.4 Distillation : transfert sélectif, pas copie parfaite

- Le modèle étudiant apprend à partir de sorties, logits, représentations ou signaux intermédiaires du modèle enseignant, selon la méthode.
- La distillation black-box n'expose que les sorties accessibles ; la white-box peut exploiter des informations internes lorsque celles-ci sont disponibles.
- L'étudiant ne récupère pas nécessairement toutes les capacités du professeur. La qualité dépend de la capacité de l'étudiant, des données, des objectifs de distillation et du protocole d'évaluation.
- DistilBERT rapporte une réduction de taille de 40 %, 97 % des capacités de compréhension évaluées et une vitesse supérieure de 60 % dans le cadre de ses expériences. Ces chiffres sont propres à cette méthode, ce modèle et ses benchmarks ; ils ne doivent pas être extrapolés à tous les LLM génératifs.

### 4.5 La taxonomie n'est pas exhaustive

L'article fournit une introduction, pas un panorama complet. Il laisse notamment de côté les factorisations de faible rang, le partage de paramètres, les architectures intrinsèquement plus efficaces, les optimisations de kernels et les compromis de parallélisme/mémoire.

## 5. Ancrage technique recommandé

| Famille | Objet modifié | Bénéfice visé | Risque / coût |
|---|---|---|---|
| Pruning structuré | Dimensions ou blocs entiers | Modèle réellement plus petit et calcul dense potentiellement plus efficace | Perte de capacité ; dépend de la granularité |
| Pruning non structuré | Poids individuels mis à zéro | Réduction du nombre de poids non nuls | Sparsité irrégulière, support matériel nécessaire |
| Quantification poids | Précision des poids | Réduction mémoire du checkpoint et de la bande passante | Erreur de quantification, déquantification éventuelle |
| Quantification poids + activations | Précision des poids et activations | Calcul et transfert plus efficaces | Calibration, outliers, contraintes kernels |
| Distillation | Paramètres et objectifs d'apprentissage d'un étudiant | Modèle étudiant plus compact | Entraînement supplémentaire et capacités non conservées |

**Distinction à retenir :** la compression du checkpoint, la réduction de la mémoire temporaire à l'inférence et l'accélération effective du calcul sont trois objectifs liés mais non équivalents.

## 6. Décision d'intégration dans LLM Lab

**Décision :** conserver l'article comme introduction complémentaire, mais ne pas créer une nouvelle page de leçon ni de nouveaux concepts canoniques sur la seule base de ce billet.

| Destination existante | Usage proposé | Limite |
|---|---|---|
| fr/llm-computational-complexity / en/llm-computational-complexity | Relier mémoire, poids, cache KV et coût d'inférence | Ne pas transformer la page en catalogue de méthodes |
| fr/llm-evolution / en/llm-evolution | Mentionner la compression comme axe d'efficacité des modèles | Rester synthétique et pointer vers les références |
| Dossier de synthèse des sources | Comparer les approches et garder les nuances | Ne pas confondre compression du modèle et compression prédictive |

Aucun identifiant de concept existant ne couvre exactement pruning, quantization ou distillation dans le registre inspecté. Aucun nouveau concept n'est proposé dans cette ingestion : un ajout devra être justifié par une couverture pédagogique stable et des sources techniques complémentaires.

## 7. Expérience pédagogique reproductible proposée

Comparer, sur un même modèle et un jeu de validation fixe, plusieurs variantes :

1. Baseline FP16/BF16.
2. Quantification poids-only (par exemple 8 bits puis 4 bits).
3. Quantification poids + activations lorsque le backend la prend en charge.
4. Pruning structuré ou semi-structuré avec kernels compatibles.
5. Étudiant distillé, entraîné sur le même périmètre de tâches.

Mesurer séparément :
- taille du checkpoint sur disque ;
- mémoire GPU/CPU au chargement et au pic d'inférence ;
- latence de préremplissage et de génération ;
- tokens/seconde et débit sous concurrence ;
- qualité sur un jeu de tâches représentatif, avec plusieurs graines si pertinent.

Contrôler le modèle, le tokenizer, le matériel, le backend, le batch, la longueur du contexte et les paramètres de génération. Ne pas comparer des chiffres issus de matériels ou protocoles différents. Une variante plus petite sur disque n'est pas nécessairement plus rapide.

## 8. Limites de la source

- Article introductif publié en 2023, non évalué par les pairs.
- Aucune expérience, table de résultats ou protocole reproductible propre à l'article.
- Plusieurs chiffres de réduction et d'accélération sont présentés sans conditions matérielles suffisamment détaillées ; ne pas les généraliser.
- Les travaux primaires cités dans cette synthèse ont été vérifiés au niveau de leurs pages de publication/résumés, pas reproduits ni audités intégralement.
- Les illustrations et commentaires de l'article n'ont pas été examinés.
- Les licences et droits de réutilisation ne sont pas établis.

## 9. Synthèse opérationnelle

**À retenir :** pruning, quantization et distillation réduisent l'empreinte d'un modèle par des mécanismes différents. Leurs effets sur la taille, la mémoire d'exécution, la latence, le débit et la qualité doivent être mesurés séparément.

**À ne pas conclure :** que 50 % de poids nuls donnent automatiquement 2× d'accélération, que passer de FP32 à INT8 donne toujours 4× de réduction et 3× de vitesse, ou qu'un étudiant conserve toutes les capacités du professeur.

**Valeur pour LLM Lab :** bonne comme orientation initiale ; insuffisante comme référence technique autonome. Les pages de complexité et d'évolution restent les destinations canoniques ; une fiche visuelle comparative ne sera pertinente qu'après validation du périmètre et des exemples quantitatifs.

## Références techniques de contrôle

- Frantar & Alistarh (2023), [SparseGPT: Massive Language Models Can be Accurately Pruned in One-Shot](https://proceedings.mlr.press/v202/frantar23a.html), ICML / PMLR. Résultat spécifique d'élagage non structuré one-shot.
- Xiao et al. (2023), [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://proceedings.mlr.press/v202/xiao23c.html), ICML / PMLR. PTQ W8A8 et traitement des outliers d'activations.
- Sanh et al. (2019), [DistilBERT, a distilled version of BERT](https://arxiv.org/abs/1910.01108). Exemple de distillation avec résultats bornés à ses évaluations.
- Sasirekha Cota (2023), [Understanding Compression of Large Language Models (LLMs)](https://medium.com/@sasirekharameshkumar/understanding-compression-of-large-language-models-2ee3b8a350a2), Medium. Consulté le 16 novembre 2026.
