# Audit Logits et Gradients — 2026-11-27

## Périmètre

Audit ciblé des pages bilingues :
- `fr/logits` / `en/logits`
- `fr/gradients` / `en/gradients`

Contrôle croisé avec `cross-entropy`, les exercices liés, les métadonnées PAGE-MAP et les références officielles PyTorch.

## 1. Logits : vérification mathématique et pédagogique

Les points vérifiés sont cohérents :

- La projection de sortie transforme l'état final en un vecteur de (V) scores, un par identifiant du vocabulaire.
- La forme ((B,T,V)) distingue correctement batch, positions et vocabulaire.
- L'exemple numérique utilise (h=(1,-1)) et quatre lignes de projection donnant ((ln 6,ln 2,0,0)). La softmax donne bien ((0.6,0.2,0.1,0.1)).
- L'invariance de la softmax à l'ajout d'une constante commune est correctement expliquée ; la relation \(\log(p_i/p_j)=z_i-z_j\) rend maintenant explicite que l'écart entre deux logits est le log-rapport des probabilités correspondantes.
- La multiplication de tous les logits par un facteur positif conserve le classement mais modifie la concentration de la distribution.
- La distinction entre score, probabilité, confiance et vérité est explicite.

Le lien vers l'exercice sur les représentations contextualisées est pertinent : il demande de comparer une ligne de logits commune sous deux continuations et de distinguer la distribution conditionnelle de la cible utilisée pour calculer la perte.

La référence PyTorch CrossEntropyLoss confirme que l'entrée attendue est constituée de logits non normalisés. Il n'est pas nécessaire d'appliquer une softmax explicite avant ce critère. La page explique aussi que la fonction de perte peut intégrer cette opération de manière numériquement stable.

## 2. Gradients : vérification des dérivations

Les dérivations ont été vérifiées pour le cas annoncé — cross-entropie non pondérée et cible one-hot :

[
p=operatorname{softmax}(z), qquad
rac{partial ell}{partial z_i}=p_i-mathbb{1}[i=y].
]

La somme des composantes vaut zéro, conformément à l'invariance par décalage commun des logits.

Pour la moyenne non pondérée sur les positions valides (mathcal M), le facteur (1/|mathcal M|) et la dérivée nulle sur les positions ignorées sont cohérents avec la réduction décrite dans la page Loss.

Le passage sur les masques distingue correctement :
- la dérivée nulle des logits ignorés dans le terme de perte ;
- la possibilité qu'une représentation à cette position contribue encore à des logits valides via une dépendance d'attention, et reçoive donc un gradient par ce chemin.

La règle de chaîne est formulée avec le jacobien des logits par rapport aux paramètres. L'explication de la rétropropagation comme produit jacobien-transposé-vecteur, sans construction explicite du jacobien complet, est correcte.

L'exemple de mise à jour de la tête de sortie est numériquement cohérent :
- (g_z=(-0.4,0.2,0.1,0.1)) ;
- (h=(1,-1)), donc (|h|^2=2) ;
- avec (eta=0.1), (z'=z-eta|h|^2g_z) ;
- la probabilité de la cible passe de (0.600) à environ (0.626), en gardant l'état (h) fixe.

Les limites sont correctement précisées : cet exemple ne représente pas une mise à jour complète du Transformer et les paramètres de la représentation cachée ne sont pas mis à jour dans ce calcul isolé.

## 3. Corrections éditoriales effectuées

- Définition explicite de (p=operatorname{softmax}(z)) avant la formule du gradient.
- Définition de (p_{b,t}) dans le cas batch et positions valides.
- Précision bilingue sur les conditions de validité de `gradcheck` : les valeurs par défaut sont conçues pour la double précision ; les points non différentiables et les entrées à mémoire chevauchante peuvent faire échouer le contrôle même si la dérivée analytique n'est pas simplement erronée.

## 4. Références canoniques ajoutées

Trois notices PyTorch ont été ajoutées à `data/sources.yml`, avec extractions atomiques et relations vers les pages existantes :

| Source | Pages | Contribution |
|---|---|---|
| `pytorch-cross-entropy-loss-api` | Logits, Cross-entropy | Contrat d'entrée logits non normalisés, formes et cibles |
| `pytorch-autograd-mechanics` | Gradients | Graphe dynamique et différentiation automatique en mode inverse |
| `pytorch-gradcheck-api` | Gradients | Comparaison analytique / différences finies et conditions d'utilisation |

Les sources restent `partially-scanned` et `partially-integrated` : le périmètre API utile aux pages a été vérifié, sans revue exhaustive de PyTorch ni exécution des exemples de code. La documentation PyTorch est vivante ; la version et les redirections doivent être revérifiées lors d'une mise à jour future.

## 6. Décision sur Jay Alammar — The Illustrated GPT-2

La section *Model Output* de [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) explique que le vecteur final est multiplié par la matrice d'embedding pour obtenir un score par élément du vocabulaire. C'est une illustration utile du passage représentation finale → scores vocabulaire dans le cas GPT-2.

La source est toutefois spécifique à GPT-2 et son propre auteur signale plusieurs simplifications : vocabulaire décrit comme des « words », différences entre inférence et entraînement, et éléments de normalisation omis ou simplifiés dans les figures. L'usage de la matrice d'embedding comme projection de sortie ne doit pas être généralisé à toutes les architectures.

**Décision : ne pas intégrer de nouveau paragraphe ni de figure.** La page Logits possède déjà un exemple numérique autonome qui expose explicitement la matrice de projection, les dimensions et les scores. Le contenu d'Alammar serait largement redondant et n'apporterait pas une nuance nécessaire au tronc principal. La source reste disponible comme ressource GPT-2 générale ; aucune figure n'est reprise, les droits de réutilisation des images n'étant pas établis.

## 5. Décisions et limites

Aucune erreur mathématique bloquante n'a été identifiée dans les deux leçons auditées. Les corrections portent sur l'explicitation des notations et les conditions d'interprétation de la vérification numérique.

Aucun nouveau concept canonique, tag de page, relation de graphe ou workflow CI n'est requis. Les notions `logits`, `cross-entropy`, `gradient`, `optimizer` et `parameter-update` suffisent.

## Sources officielles

- [PyTorch — CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [PyTorch — Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)
- [PyTorch — torch.autograd.gradcheck](https://docs.pytorch.org/docs/stable/generated/torch.autograd.gradcheck.gradcheck.html)
