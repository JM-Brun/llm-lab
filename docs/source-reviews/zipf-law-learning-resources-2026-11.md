# Loi de Zipf — sélection et audit initial de ressources pédagogiques

**Date de recherche :** 2026-11-24  
**Périmètre :** loi de Zipf appliquée aux fréquences lexicales, ses variantes, ses interprétations et ses usages pour comprendre les corpus textuels en amont de la tokenisation.  
**Statut :** sélection documentée et inspection initiale ; ce dossier ne prétend pas à une extraction exhaustive des articles, figures, données ou annexes.

## 1. Décision éditoriale proposée

Intégrer la loi de Zipf dans le domaine **Texte et tokenisation** (text-tokenization), en lien avec la préparation des corpus (corpus-preparation) et les statistiques descriptives du langage.

La placer avant ou à proximité de la tokenisation, dans une courte leçon de compréhension consacrée aux propriétés statistiques des corpus. Ne pas la présenter comme une propriété du tokenizer ni comme une loi qui expliquerait à elle seule la structure du langage.

La leçon devrait répondre à quatre questions :
1. Que mesure-t-on lorsqu'on classe les mots par fréquence ?
2. Pourquoi une relation approximativement inverse entre rang et fréquence apparaît-elle ?
3. Comment la vérifier sur un corpus réel, et quelles décisions de comptage influencent le résultat ?
4. Quelles conséquences cette distribution a-t-elle pour les corpus et les modèles de langage ?

**Intégration minimale recommandée :** une leçon bilingue FR/EN de compréhension, une fiche d'exercices séparée dans Practice & experiment, et un petit notebook/workbench reproductible. Une page Deepen distincte ne se justifie que si les explications mathématiques et les modèles génératifs prennent assez d'ampleur.

## 2. Ressources retenues

### A. Piantadosi (2014) — référence critique centrale

Steven T. Piantadosi, *Zipf's word frequency law in natural language: A critical review and future directions*, Psychonomic Bulletin & Review, 21, 1112–1130 (2014). DOI : https://doi.org/10.3758/s13423-014-0585-6. Texte intégral : https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592/.

- **Type / niveau :** article de revue scientifique ; avancé, mais excellent matériau pour une synthèse pédagogique.
- **Apport :** formule classique \(f(r)\propto r^{-\alpha}\), loi de Zipf–Mandelbrot, phénomènes empiriques au-delà de la droite log-log, comparaison de modèles et examen critique des explications proposées.
- **Valeur pour LLM Lab :** empêche de transformer une régularité empirique approximative en loi exacte ou en explication causale acquise. Souligne que le modèle le mieux ajusté dépend du corpus et que plusieurs mécanismes peuvent contribuer.
- **Limite :** ce n'est pas un tutoriel débutant ni un guide d'implémentation ; l'article doit être synthétisé, pas reproduit.
- **Inspection initiale :** page PMC, résumé, introduction, équations et sections visibles sur la complexité de la distribution et les familles d'explications. Annexes et données sous-jacentes non reproduites dans cette passe.
- **Disposition :** référence scientifique principale à citer dans la leçon et dans la partie « limites / explications ».

### B. Wolfram Demonstrations — laboratoire visuel interactif

Giovanna Roda (2024), *Zipf's Law for Natural Languages*, Wolfram Demonstrations Project : https://demonstrations.wolfram.com/ZipfsLawForNaturalLanguages/. Licence indiquée : CC BY-NC-SA.

- **Type / niveau :** démonstration interactive ; introductif.
- **Apport :** sélectionner un texte, compter les occurrences, ordonner les mots, limiter le rang affiché et observer la relation rang–fréquence en échelle log-log. Le survol des points donne accès aux termes et aux valeurs.
- **Valeur pour LLM Lab :** bon modèle d'activité exploratoire : partir des données, observer les rangs, puis interpréter la pente.
- **Limites :** démonstration optimisée pour ordinateur ; dépend de l'environnement Wolfram. La licence NC-SA ne doit pas être interprétée comme une autorisation générale de recopier ou d'adapter le notebook dans le dépôt.
- **Inspection initiale :** page de démonstration et description ; notebook non exécuté et code non audité.
- **Disposition :** lien externe d'inspiration ; reproduire une expérience indépendante avec code et corpus contrôlés plutôt que dépendre de ce widget.

### C. Linders & Louwerse (2023) — élargissement au dialogue oral

Guido M. Linders & Max M. Louwerse, *Zipf's law revisited: Spoken dialog, linguistic units, parameters, and the principle of least effort*, Psychonomic Bulletin & Review, 30, 77–101 (2023). Publication en ligne : 15 juillet 2022. Texte : https://pmc.ncbi.nlm.nih.gov/articles/PMC9971120/.

- **Type / niveau :** revue théorique / étude de synthèse ; intermédiaire à avancé.
- **Apport :** réexamine les unités linguistiques, les paramètres, le dialogue parlé et le principe du moindre effort ; rappelle les variantes Zipf–Mandelbrot et les écarts à l'exposant proche de 1.
- **Valeur pour LLM Lab :** éviter de généraliser les résultats d'un corpus écrit monologique de mots unigrammes à toute forme de langage. Ouvre la question du choix de l'unité : mot, lemme, token, n-gramme, tour de parole.
- **Limite :** la thèse du moindre effort doit être présentée comme une famille d'explications théoriques, pas comme une cause démontrée par la seule observation de la loi.
- **Inspection initiale :** page PMC, résumé et introduction/formalisation ; analyses empiriques détaillées et suppléments à lire lors d'une passe dédiée.
- **Disposition :** source complémentaire pour une section « portée et limites » ou un approfondissement.

### D. *Unzipping Zipf's law* (2017) — modèle syntaxe / sémantique

*Unzipping Zipf's law* (2017), article en accès libre : https://pmc.ncbi.nlm.nih.gov/articles/PMC5549924/.

- **Type / niveau :** article de recherche avec modèle computationnel ; avancé.
- **Apport :** propose que l'interaction entre classes syntaxiques de tailles différentes et contraintes sémantiques de spécificité/réutilisabilité puisse produire une distribution proche de Zipf. Le modèle soutient que ces ingrédients combinés sont nécessaires dans le cadre étudié.
- **Valeur pour LLM Lab :** donne un exemple concret de passage d'une régularité descriptive à une hypothèse mécaniste testable, avec simulation.
- **Limite :** ne pas présenter ce modèle comme l'explication consensuelle ou définitive ; le statut est celui d'une proposition parmi plusieurs.
- **Inspection initiale :** résumé, introduction, formulation de la proposition et description générale du modèle ; code, données et analyses complètes non reproduits.
- **Disposition :** approfondissement optionnel, après l'observation empirique et la critique des explications.

### E. Source historique — Zipf, *The Psycho-Biology of Language*

George Kingsley Zipf, *The Psycho-Biology of Language* (1935 ; édition réimprimée accessible via PDF) : https://iqla.org/wp-content/uploads/2025/05/Zipf_1935_1965_Psycho-Biology_Language.pdf.

- **Type / niveau :** ouvrage historique ; avancé et daté.
- **Apport :** contexte original de la courbe de Zipf, distinction entre fréquence et rang, ambition explicative autour de la régularité linguistique.
- **Valeur :** contextualisation historique et lecture des formulations originelles du principe du moindre effort.
- **Limite :** ouvrage ancien, dont les hypothèses ne doivent pas être confondues avec l'état actuel des connaissances.
- **Inspection initiale :** préface/présentation et passages indexés ; livre entier non lu.
- **Disposition :** référence historique facultative, pas source principale de la leçon.

## 3. Synthèse comparative

| Besoin pédagogique | Ressource principale | Rôle |
|---|---|---|
| Définir et formaliser la loi | Piantadosi (2014) | Référence critique et mathématique |
| Voir la distribution sur des données | Wolfram Demonstration | Inspiration d'activité interactive |
| Comprendre les limites de généralisation | Linders & Louwerse (2023) | Diversité des unités et corpus |
| Étudier une explication mécaniste | *Unzipping Zipf's law* (2017) | Modèle computationnel alternatif |
| Situer historiquement la loi | Zipf (1935) | Source historique |

Ces sources ne sont pas cinq tutoriels équivalents : elles couvrent cinq fonctions différentes. La combinaison recommandée est Piantadosi + une expérience reproductible inspirée de Wolfram + Linders/Louwerse pour la portée + un modèle explicatif en approfondissement.

## 4. Squelette pédagogique recommandé

### Leçon principale — Comprendre la distribution des fréquences lexicales

1. **Partir d'un corpus concret.** Compter les occurrences de mots dans un texte court. Distinguer occurrence (token au sens linguistique) et forme lexicale distincte (type).
2. **Classer les fréquences.** Trier les formes par fréquence décroissante et attribuer un rang. Traiter explicitement les ex æquo et la normalisation.
3. **Observer l'asymétrie.** Montrer les quelques mots très fréquents et la longue traîne de mots rares. Introduire la courbe rang–fréquence.
4. **Formaliser.** Présenter \(f(r)=C/r^\alpha\), le cas usuel \(\alpha\approx1\), puis la représentation log-log : \(\log f=\log C-\alpha\log r\).
5. **Vérifier plutôt que supposer.** Estimer la pente sur un domaine annoncé, comparer plusieurs corpus et montrer que les extrémités peuvent dévier.
6. **Introduire les variantes.** Présenter Zipf–Mandelbrot \(f(r)=C/(r+\beta)^\alpha\), sans multiplier les modèles dans la première explication.
7. **Questionner les explications.** Distinguer observation, ajustement statistique et mécanisme causal ; présenter brièvement moindre effort, réutilisation/préférence, modèles de génération et approche syntaxe–sémantique.
8. **Relier à LLM.** Examiner ce que la distribution implique pour la couverture lexicale d'un corpus, les fréquences des tokens, les tokens rares et la segmentation. Ne pas conclure que la loi détermine directement BPE ou la qualité d'un tokenizer.

### Activité expérimentale dédiée

À partir de deux petits corpus de genres différents et d'un corpus multilingue :
- compter les formes avec une politique de normalisation explicitée (casse, ponctuation, contractions, Unicode) ;
- comparer mots, lemmes si disponibles, caractères et tokens d'un tokenizer donné ;
- tracer fréquence en fonction du rang en axes linéaires et log-log ;
- ajuster une pente sur une plage de rangs déclarée, puis vérifier sa stabilité ;
- comparer Zipf et Zipf–Mandelbrot sans conclure sur la seule apparence d'une droite ;
- mesurer la part du corpus couverte par les 10, 100, 1 000 formes les plus fréquentes ;
- analyser les différences entre langues, genres et tailles de corpus.

Le protocole doit fixer les règles de comptage, le corpus et sa licence, les versions des outils, les paramètres et les limites. Les résultats doivent être décrits comme propres aux corpus choisis.

### Exercices séparés

La page d'exercices devrait progressivement couvrir :
- calculer rangs et fréquences à partir d'un tableau ;
- retrouver \(\alpha\) à partir d'une pente log-log ;
- distinguer fréquence absolue, fréquence relative, rang, type et occurrence ;
- repérer une conclusion abusive tirée d'un graphique log-log ;
- expliquer l'effet du changement de segmentation ou de normalisation ;
- comparer deux corpus et formuler une conclusion bornée ;
- distinguer une loi empirique d'une explication mécaniste.

## 5. Placement et relations dans le modèle de connaissances

- **Domaine principal :** text-tokenization.
- **Domaines secondaires possibles :** probabilistic-foundations-training seulement si la page développe réellement les distributions de probabilité ; ne pas l'ajouter pour simple proximité.
- **Pages candidates :** fr/text-data / en/text-data, fr/corpus-preparation / en/corpus-preparation, puis fr/tokenization-strategies / en/tokenization-strategies.
- **Placement recommandé :** leçon Understand liée à la préparation et à la description des corpus, avec un renvoi vers la tokenisation. La loi concerne d'abord les fréquences des unités observées dans un corpus ; elle n'est pas une étape algorithmique du tokenizer.
- **Concepts existants à réutiliser :** token, dataset-curation. Ne pas créer un concept pour chaque terme statistique.
- **Concepts à envisager après audit du registre :** word-frequency, frequency-rank, power-law-distribution, zipf-law. Créer uniquement les concepts réutilisés par plusieurs ressources/pages ou nécessaires à des relations typées. Le nom « Zipf's law » peut rester une notion explicitée dans une page sans imposer automatiquement un nœud dédié.
- **Tags de source candidats :** topic:zipf-law, topic:word-frequency, topic:corpus-statistics, method:power-law, method:log-log-analysis. Ce sont des facettes de recherche, pas des concepts.
- **Importance éditoriale proposée :** supporting plutôt que core : importante pour comprendre les propriétés des corpus, mais pas un mécanisme central du forward pass ou de l'architecture Transformer.

## 6. Garde-fous scientifiques et éditoriaux

- Une droite apparente sur un graphique log-log ne suffit pas à démontrer une loi de puissance.
- L'exposant n'est pas universel : il dépend notamment des unités, du corpus, de la plage de rangs et des méthodes d'estimation.
- Les distributions observées présentent une structure au-delà de la loi simple ; des modèles concurrents peuvent mieux décrire certains corpus.
- Une bonne adéquation descriptive n'identifie pas le mécanisme causal.
- Le principe du moindre effort est une hypothèse explicative historique/théorique, pas une conséquence logique de la formule.
- Ne pas confondre mots, types lexicaux, occurrences, sous-mots et tokens de tokenizer.
- Ne pas extrapoler automatiquement les statistiques d'un corpus écrit monologique à l'oral ou à toutes les langues.
- Ne pas réutiliser les figures ou notebooks des sources sans vérifier leurs licences et conditions ; privilégier une figure originale et un code écrit dans le dépôt.

## 7. Lacunes avant intégration complète

1. Lire intégralement les sections empiriques et méthodes de Piantadosi et Linders/Louwerse.
2. Vérifier précisément les méthodes d'estimation et les domaines d'ajustement présentés par les articles.
3. Inspecter le notebook Wolfram si l'environnement permet d'en vérifier le code et les dépendances ; garder le statut de licence NC-SA explicite.
4. Vérifier les métadonnées bibliographiques et les droits de l'ouvrage historique.
5. Auditer les pages FR/EN existantes et les concepts du registre avant toute modification de contenu.
6. Construire les sources et extractions canoniques selon le schéma actuellement en vigueur ; ce dossier est une comparaison initiale et ne remplace pas ces enregistrements.
7. Valider l'activité avec des corpus petits, documentés et redistribuables, puis effectuer une revue bilingue et une validation apprenant.

## 8. Références

- Piantadosi, S. T. (2014). https://doi.org/10.3758/s13423-014-0585-6 · https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592/
- Roda, G. (2024). https://demonstrations.wolfram.com/ZipfsLawForNaturalLanguages/
- Linders, G. M., & Louwerse, M. M. (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC9971120/
- *Unzipping Zipf's law* (2017). https://pmc.ncbi.nlm.nih.gov/articles/PMC5549924/
- Zipf, G. K. (1935). https://iqla.org/wp-content/uploads/2025/05/Zipf_1935_1965_Psycho-Biology_Language.pdf
