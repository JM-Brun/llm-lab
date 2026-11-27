# Réconciliation bibliographique ICL — 2026-11-27

## Objet

Réconcilier les références de `fr/in-context-learning` et `en/in-context-learning` avec le catalogue canonique `data/sources.yml`, sans confondre notice bibliographique, consultation d'une source et intégration pédagogique de ses résultats.

## Résultat de la vérification bibliographique

Six notices canoniques ont été ajoutées au catalogue :

| Identifiant canonique | Publication | Identifiant vérifié | Rôle documentaire |
|---|---|---|---|
| `brown-et-al-gpt3-few-shot-2020` | NeurIPS 2020 | arXiv:2005.14165 | Démonstration de la capacité few-shot de GPT-3 sans mise à jour de gradient |
| `olsson-et-al-induction-heads-2022` | Transformer Circuits Thread, 2022 | arXiv:2209.11895 | Hypothèse mécaniste des induction heads |
| `xie-et-al-implicit-bayesian-icl-2022` | ICLR 2022 | arXiv:2111.02080 | Explication théorique par inférence bayésienne implicite dans un cadre de préentraînement spécifié |
| `min-et-al-demonstrations-icl-2022` | EMNLP 2022 | DOI:10.18653/v1/2022.emnlp-main.759 | Étude du rôle des démonstrations et de leurs composantes |
| `yoo-et-al-ground-truth-labels-icl-2022` | EMNLP 2022 | DOI:10.18653/v1/2022.emnlp-main.155 | Réexamen de l'effet des associations entrée-étiquette correctes |
| `xiang-et-al-order-sensitivity-icl-2024` | Findings of ACL 2024 | DOI:10.18653/v1/2024.findings-acl.386 | Approfondissement sur la sensibilité à l'ordre des démonstrations |

Les métadonnées ont été recoupées avec les pages de publication officielles NeurIPS, Transformer Circuits, OpenReview/arXiv et ACL Anthology.

## Décisions de modélisation

- Une notice unique par publication, partagée entre les versions française et anglaise.
- Identifiants pérennes : arXiv pour les prépublications concernées, DOI pour les actes ACL.
- `related.pages` associe les six sources aux deux pages ICL ; `related.concepts` réutilise les concepts déjà existants.
- Aucun nouveau concept canonique n'est créé pour les induction heads, la correction des labels ou l'ordre des démonstrations.
- Les statuts sont `scan_status: partially-scanned` et `integration_status: deferred`. La vérification de métadonnées et d'abstract ne constitue ni une lecture complète ni une intégration claim-level.
- Les licences restent inconnues et les contenus/figures sont link-only tant que les droits ne sont pas vérifiés.
- Aucun statut `integrated` n'est attribué sur la seule base d'une citation dans une bibliographie.

## Lecture pédagogique à préserver

Les résumés officiels montrent que Min et al. (2022) et Yoo et al. (2022) étudient tous deux l'effet des démonstrations et des associations entrée-étiquette, mais que Yoo et al. réexaminent explicitement les résultats antérieurs avec d'autres métriques et configurations expérimentales. Il serait incorrect de réduire ces résultats à une règle générale du type « les labels corrects ne comptent pas » ou à l'affirmation inverse « ils sont toujours nécessaires ». Une synthèse claim-level exige la lecture des protocoles, des métriques, des résultats par tâche/modèle et des limites des deux articles.

Olsson et al. (2022) propose une hypothèse mécaniste sur les induction heads. Le niveau de preuve doit rester explicite : les auteurs rapportent des éléments causaux plus forts dans les petits modèles attention-only et des éléments plus indirects/corrélationnels pour les grands modèles avec MLP. Cette source ne justifie pas d'enseigner que les induction heads expliquent à elles seules tout ICL dans tous les LLM.

Xie et al. (2022) fournit une explication théorique par inférence bayésienne implicite, dans un cadre formalisé de préentraînement à mélange de HMM. Ne pas la présenter comme une description universelle et démontrée du mécanisme de tout modèle entraîné sur des corpus naturels.

Xiang et al. (2024) reste une ressource d'approfondissement sur l'ordre des démonstrations. Son résumé rapporte une sensibilité différente entre les modèles causaux et prefix-LM évalués ; les limites de cette comparaison devront être reprises à partir du protocole complet avant toute généralisation.

## Limites de cette passe d'ingestion

Cette passe vérifie les métadonnées bibliographiques, les identifiants, les abstracts et les résumés officiels. Elle ne constitue pas une revue complète des six publications. Aucun PDF n'a été relu intégralement ici ; aucun résultat expérimental n'a été reproduit ; aucune extraction atomique claim/evidence n'a été créée.

Les notices restent donc différées. La prochaine étape d'ingestion est une lecture ciblée des articles Min et Yoo en priorité, puis Olsson et Xie pour stabiliser les niveaux de preuve et les limites de portée. Xiang reste une ressource facultative d'approfondissement.

## Sources de vérification

- Brown et al., [NeurIPS 2020 proceedings](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) et [arXiv:2005.14165](https://arxiv.org/abs/2005.14165).
- Olsson et al., [Transformer Circuits Thread](https://www.transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) et [arXiv:2209.11895](https://arxiv.org/abs/2209.11895).
- Xie et al., [OpenReview — ICLR 2022](https://openreview.net/forum?id=RdJVFCHjUMI) et [arXiv:2111.02080](https://arxiv.org/abs/2111.02080).
- Min et al., [ACL Anthology — EMNLP 2022](https://aclanthology.org/2022.emnlp-main.759/).
- Yoo et al., [ACL Anthology — EMNLP 2022](https://aclanthology.org/2022.emnlp-main.155/).
- Xiang et al., [ACL Anthology — Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.386/).
