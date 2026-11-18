# Revue de source — Su et al., « RoFormer: Enhanced Transformer with Rotary Position Embedding »

**Source canonique :** [arXiv:2104.09864](https://arxiv.org/abs/2104.09864) · [texte intégral HTML, version 5](https://arxiv.org/html/2104.09864v5) · [extraction structurée](../../data/extractions/su-roformer-rope-2021.yml)

**Statut bibliographique :** prépublication déposée le 20 avril 2021, version 5 révisée le 8 novembre 2023. La page HTML arXiv affiche une licence CC BY-NC-ND 4.0 ; cela ne vaut pas autorisation de réutiliser les figures, ni de publier des adaptations de contenu. Le catalogue conserve donc les modalités de réutilisation existantes et les assets restent en lien seulement.

## 1. Question et contribution

Le papier cherche une fonction d'encodage positionnel pour laquelle le produit scalaire entre une requête à la position (m) et une clé à la position (n) dépend du contenu et du décalage relatif, plutôt que des deux positions absolues séparément (§3.1, équation 11).

La solution RoPE applique une rotation dépendant de la position aux vecteurs projetés (Q) et (K), avant le produit (QK^T). Les valeurs (V) ne sont pas directement tournées dans la construction standard décrite ici.

## 2. Mécanisme et résultat mathématique

Dans le cas 2D, les vecteurs projetés sont multipliés par une rotation d'angle proportionnel à leur position (§3.2.1, équations 12–13). Pour une dimension paire plus grande, l'espace est partitionné en paires de coordonnées, avec une fréquence propre à chaque paire (§3.2.2, équations 14–16).

L'identité centrale est :

[
(R_m q)^T(R_n k)=q^T R_m^T R_n k=q^T R_{n-m}k.
]

Elle montre que la contribution du produit scalaire dépend du décalage (n-m), pour les contenus (q,k) fixés. Les matrices de rotation sont orthogonales : elles préservent la norme des vecteurs tournés.

**Précision importante :** cette propriété du score ne signifie pas que les poids appris encodent nécessairement une relation utile, ni que le modèle extrapole sans dégradation à des longueurs arbitraires.

## 3. Fréquences et « long-term decay »

Le papier définit une famille de fréquences géométriquement espacées, puis analyse le produit scalaire en regroupant les coordonnées deux par deux (§§3.2.2 et 3.4.3). À l'aide d'une transformation d'Abel, il borne le terme par une somme de sommes partielles complexes et observe que la magnitude moyenne de ces sommes partielles décroît avec le décalage relatif pour le calendrier de fréquences retenu (équations 35–37 et figure 2).

Il faut éviter de reformuler ce résultat comme « chaque score d'attention diminue avec la distance ». Il s'agit d'une propriété agrégée du calendrier de fréquences et de la borne présentée, pas d'une monotonie universelle de chaque contribution, logit ou poids d'attention.

## 4. Extension à l'attention linéaire

La section 3.3 adapte la rotation à une formulation d'attention linéaire factorisée (équations 17–19). Les auteurs conservent le dénominateur non tourné pour éviter le risque de division par zéro ; le numérateur peut contenir des termes négatifs. Ils précisent que les coefficients obtenus ne sont donc pas strictement des poids probabilistes normalisés.

Cette construction ne doit pas être présentée comme équivalente à l'attention softmax standard, ni comme une recette automatiquement applicable à toutes les variantes d'attention linéaire.

## 5. Expériences : périmètre et résultats à ne pas généraliser

Le papier décrit cinq familles d'évaluation (§4) :
- traduction WMT 2014 anglais–allemand : BLEU 27,5 pour RoFormer contre 27,3 pour le Transformer de référence (table 1) ;
- pré-entraînement de type BERT avec longueur maximale 512 et mesure de la loss MLM ;
- six tâches GLUE : RoFormer est meilleur sur trois tâches du tableau, mais moins bon sur les trois autres (table 2) ;
- Performer sur Enwik8, avec comparaison des courbes de loss ;
- tâches chinoises sur documents longs, dont CAIL2019-SCM : 69,79 % de précision test à une coupure de 1 024 tokens, contre 68,29 % pour la configuration RoFormer à 512 tokens (table 5).

Les résultats sont conditionnés par les jeux de données, les configurations, les longueurs, les baselines et les métriques de chaque expérience. Ils ne prouvent pas une supériorité universelle de RoPE.

## 6. Limites explicitement reconnues par les auteurs

La section 4.5.5 reconnaît deux lacunes :
- le papier n'explique pas complètement pourquoi RoFormer converge plus vite que les modèles de référence ;
- il ne fournit pas d'explication fidèle de ses meilleurs résultats sur les textes longs, malgré l'analyse théorique de décroissance à long terme.

Le papier rappelle également que le pré-entraînement d'un Transformer requiert des ressources matérielles. Aucune reproduction indépendante des résultats, exécution du dépôt lié ou vérification des checkpoints n'a été réalisée dans cet audit.

## 7. Décision d'intégration

- **Extraction créée :** cinq items atomiques couvrant la dérivation Q/K, l'orthogonalité, la portée exacte du résultat de décroissance, l'adaptation à l'attention linéaire et le périmètre expérimental.
- **Pages reliées :** approfondissements RoPE FR/EN et pages générales d'encodage positionnel FR/EN.
- **Concepts :** réutilisation du concept canonique existant `positional-encoding` ; aucun nouvel identifiant de concept n'est créé.
- **Données inconnues et droits :** aucune date, licence ou permission de réutilisation n'est inventée ou élargie.
- **À ne pas conclure :** la présence d'une rotation ne garantit ni l'extrapolation en longueur, ni la décroissance monotone de chaque score, ni une supériorité générale sur les autres méthodes.
