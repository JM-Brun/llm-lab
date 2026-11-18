# ColPali — audit de la source primaire

**Source :** Faysse et al., *ColPali: Efficient Document Retrieval with Vision Language Models*, ICLR 2025. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/99e9e141aafc314f76b0ca3dd66898b3-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/99e9e141aafc314f76b0ca3dd66898b3-Paper-Conference.pdf)

## Synthèse

ColPali adapte PaliGemma pour encoder les pages comme ensembles de vecteurs de patchs, puis les compare aux vecteurs des tokens de la requête par interaction tardive de type ColBERT. L'unité de recherche est la page, pas un passage textuel précis. Le papier introduit ViDoRe, un benchmark visuel multi-domaines.

## Preuves examinées

- Architecture multi-vecteurs et interaction tardive : §4.1, équation (1).
- Construction de ViDoRe : §3.1 et Table 1.
- Résultats nDCG@5 : §5.1, Table 2 (81,3 pour ColPali ; 67,0 pour Unstructured + captioning avec BGE-M3).
- Données d'entraînement et coûts : §§2, 4.2 et 5.2 ; appendice B.4 à approfondir pour les valeurs matérielles.

## Limites et controverses

Les scores agrégés sont propres aux tâches ViDoRe et aux systèmes comparés ; les résultats varient par tâche. La recherche au niveau page ne fournit pas automatiquement des extraits exacts ou des valeurs structurées. Il faut distinguer indexation hors ligne et latence de requête en ligne. Les chiffres détaillés de stockage et latence ne doivent pas être repris avant vérification de l'appendice et du matériel exact.

## Décision documentaire

Extraction dédiée justifiée. Les pages bilingues *document retrieval* utilisent directement cette source ; *cosine similarity* l'emploie comme exemple de recherche visuelle. Les concepts existants suffisent ; aucune nouvelle relation n'est proposée.

## Périmètre de l'audit

Lecture ciblée du papier publié : résumé, §§1–5.1, Figures 1–2 et Tables 1–2. Code, checkpoints, jeux de données et benchmark non exécutés indépendamment. Aucun visuel reproduit ; droits de réutilisation non établis.