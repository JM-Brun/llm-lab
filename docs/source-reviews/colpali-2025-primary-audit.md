# ColPali — audit de la source primaire

**Source :** Faysse et al., *ColPali: Efficient Document Retrieval with Vision Language Models*, ICLR 2025. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/99e9e141aafc314f76b0ca3dd66898b3-Abstract-Conference.html) · [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/99e9e141aafc314f76b0ca3dd66898b3-Paper-Conference.pdf)

## Synthèse

ColPali adapte PaliGemma pour encoder les pages comme ensembles de vecteurs de patchs, puis les compare aux vecteurs des tokens de la requête par interaction tardive de type ColBERT. L'unité de recherche est la page, pas un passage textuel précis. Le papier introduit ViDoRe, un benchmark visuel multi-domaines.

## Preuves examinées

- Architecture multi-vecteurs et interaction tardive : §4.1, équation (1).
- Construction de ViDoRe : §3.1 et Table 1 ; tâches académiques et pratiques, modalités et domaines variés, anglais et français.
- Résultats nDCG@5 : §5.1, Table 2 (81,3 pour ColPali ; 67,0 pour Unstructured + captioning avec BGE-M3), avec variation importante selon les tâches.
- Indexation hors ligne : §5.2, Figure 2 et appendice B.4, Table 5. Sur une VM GCP g2-standard-8 avec NVIDIA L4, le tableau rapporte 7,22 s/page pour Unstructured (0,81 layout detection + 2,67 OCR + 3,71 captioning + 0,03 encodage), 0,12 s/page pour SigLIP et 0,39 s/page pour ColPali. Le tableau décrit 1 000 documents ViDoRe échantillonnés ; batchs 8 pour BGE-M3/Unstructured et 4 pour SigLIP/ColPali.
- Empreinte des embeddings : §5.2, appendice B.3, Table 4 : 257,5 KB/page pour ColPali float16 sur DocVQA, contre 8,60 KB pour BGE-M3. Ce n'est pas la taille totale d'un index en production.
- Requête en ligne : §5.2 et note 12 : environ 30 ms pour encoder une requête ColPali contre 22 ms pour BGE-M3 (15 tokens) ; environ 1 ms supplémentaire par 1 000 pages pour l'interaction tardive dans les petits corpus, mesuré batch 1 et moyenné sur 1 000 requêtes.

## Limites et controverses

Les scores agrégés sont propres aux tâches ViDoRe et aux systèmes comparés ; les résultats varient par tâche. La recherche au niveau page ne fournit pas automatiquement des extraits exacts ou des valeurs structurées. Il faut distinguer indexation hors ligne, encodage de requête et score de recherche en ligne. Les gains d'indexation viennent notamment de la suppression des étapes de détection de mise en page, OCR et captioning ; ils ne signifient pas que ColPali accélère ces opérations.

**Incohérence interne à préserver :** la note 13 de la section 5.2 indique une mesure sur 100 pages pour l'indexation, alors que l'appendice B.4 décrit 1 000 documents aléatoires pour le Tableau 5. Ne pas fusionner les deux dénominateurs ni attribuer automatiquement le protocole du Tableau 5 à chaque chiffre de la Figure 2. Les chiffres de latence restent des mesures de laboratoire sur matériel et batchs spécifiés, pas une garantie de performance universelle. Le chiffre de stockage est une taille d'embedding par page, non le coût complet d'un index. La montée à des millions de documents est attribuée à des moteurs d'interaction tardive optimisés, mais n'est pas démontrée par la mesure de latence de petit corpus.

## Décision documentaire

Extraction dédiée justifiée. Les pages bilingues *document retrieval* utilisent directement cette source ; *cosine similarity* l'emploie comme exemple de recherche visuelle. Les concepts existants suffisent ; aucune nouvelle relation n'est proposée.

## Périmètre de l'audit

Lecture ciblée du papier publié : résumé, §§1–5.2, Figures 1–3, Tables 1–2 et appendices B.3–B.4 / Tables 4–5. Code, checkpoints, jeux de données et benchmark non exécutés indépendamment. Aucun visuel reproduit ; droits de réutilisation des figures non établis.
