# Méthode de synthèse des sources

**Statut :** méthode éditoriale pour construire une ressource d'apprentissage cumulative et traçable.  
**Périmètre :** comparaison et synthèse multi-sources ; complète le catalogue des sources et le workflow en deux phases.

## 1. Objectif : compiler des perspectives, pas dupliquer les pages

La plupart des sources utiles traiteront de notions déjà abordées par LLM Lab. C'est normal. Une collection devient précieuse lorsqu'elle permet de combiner plusieurs manières de comprendre un même sujet : dérivations mathématiques et formelles ; vues computationnelles, tensorielles et d'implémentation ; intuitions géométriques et visuelles ; exemples linguistiques et modèles mentaux ; contexte historique ; résultats empiriques et expériences reproductibles ; compromis d'ingénierie, modes d'échec et critiques ; séquences pédagogiques adaptées à différents niveaux.

Le but n'est ni de reproduire toutes les sources, ni de maximiser le nombre de références ou la longueur des pages. Il s'agit de construire une expérience d'apprentissage originale, cohérente et traçable.

## 2. Partir de la question de l'apprenant

Une synthèse commence par une question durable, pas par une liste d'URL. Exemples : que calcule l'attention et pourquoi sépare-t-on Q, K et V ? Pourquoi un même token peut-il avoir des états contextualisés différents ? Qu'est-ce qui change entre un schéma conceptuel du Transformer et une implémentation réelle ? Quelles affirmations sur les poids d'attention sont justifiées, et lesquelles relèvent d'une surinterprétation ?

Identifier les pages canoniques, les prérequis attendus et la position dans le parcours. Scinder les questions réellement différentes plutôt que de les forcer dans un même dossier.

## 3. Comparer les contributions explicatives

| Dimension | Question de comparaison |
|---|---|
| Question d'apprentissage | Quelle difficulté ou question cette contribution traite-t-elle ? |
| Angle explicatif | Mathématique, computationnel, géométrique, linguistique, historique, empirique, ingénierie, etc. ? |
| Forme pédagogique | Définition, dérivation, analogie, exemple, figure, expérience, implémentation, étude de cas, critique ? |
| Modèle mental | Quelles entités et relations l'apprenant imagine-t-il ? Où le modèle cesse-t-il d'être valide ? |
| Niveau | Quels prérequis et quel niveau d'abstraction sont supposés ? |
| Valeur distinctive | Qu'est-ce qui devient plus facile à comprendre grâce à cette contribution ? |
| Preuve | Preuve, résultat empirique, implémentation documentée, illustration, opinion ou hypothèse ? |
| Limites | Quelles hypothèses, réserves, contre-exemples ou défaillances doivent rester visibles ? |
| Destination | Socle, perspective optionnelle, approfondissement, étude de cas, expérience, référence ou lien ? |

Ne pas imposer à chaque source un angle unique. Plusieurs sources peuvent renforcer une même explication ; cette convergence peut être utile, mais des tutoriels dérivés les uns des autres ne constituent pas des confirmations indépendantes. Des sources peuvent aussi être en désaccord : conserver le désaccord et l'examiner plutôt que de le masquer.

## 4. Construire une carte des contributions

Pour un sujet couvert par plusieurs sources pertinentes, créer un dossier dans docs/source-syntheses/ en suivant son README. La carte doit rendre visibles la question d'apprentissage et la couverture canonique ; les sources et identifiants exacts des éléments extraits ; la contribution de chaque source ; les perspectives complémentaires, convergences et désaccords ; la décision d'intégration et sa destination ; les éléments optionnels, liés, différés ou exclus ; les lacunes restantes.

Le dossier est un index de synthèse éditoriale, pas un remplacement des enregistrements de sources, de la bibliographie, du graphe de concepts ou du contenu des leçons. Conserver les affirmations détaillées et leurs localisateurs dans les extractions ; les lier plutôt que les recopier.

## 5. Synthétiser sans aplatir les différences

Une bonne synthèse n'est pas une concaténation de résumés. Rédiger une explication cohérente avec la voix du projet. Utiliser l'explication la plus claire comme socle, puis introduire une perspective complémentaire lorsqu'elle résout une difficulté différente. Placer les dérivations avancées, détails d'implémentation et points de vue spécialisés dans les niveaux adaptés. Conserver des explications alternatives comme perspectives optionnelles ou ressources liées lorsqu'elles offrent un choix utile sans interrompre le parcours central. Garder les exemples qui éclairent des phénomènes différents. Délimiter chaque analogie. Distinguer illustration pédagogique et preuve sur le comportement interne du modèle. Attribuer les exemples et idées issus des sources ; ne pas copier de texte, code ou figure protégé sans droits vérifiés. Ne jamais fusionner des affirmations distinctes en une phrase qui semblerait provenir d'une seule source ou disposer de preuves plus fortes qu'en réalité.

## 6. Preuves et indépendance des sources

La complémentarité pédagogique et la qualité des preuves scientifiques sont deux dimensions distinctes. Une analogie claire peut être utile pédagogiquement mais constituer une preuve faible du mécanisme. Un article primaire peut fournir des preuves solides tout en étant une mauvaise explication pour débutant.

Lorsque plusieurs sources convergent, déterminer si elles sont réellement indépendantes, remonter aux sources primaires lorsque possible, distinguer répétition pédagogique et confirmation empirique indépendante, et conserver les qualifications. Lorsque des sources divergent, formuler précisément le désaccord, comparer définitions, hypothèses, modèle/version, données, tâche, méthode et mesure ; consulter les sources primaires et réplications ; laisser la question ouverte si les éléments ne permettent pas de trancher.

## 7. Décider ce qui entre dans l'expérience d'apprentissage

Pour chaque contribution, choisir et justifier une disposition : intégrer, corriger, clarifier, lier, citer, étude de cas, expérience, différer ou rejeter. Une contribution peut être utile sans appartenir à la page centrale : socle indispensable ; perspective optionnelle ; approfondissement formel ou technique ; étude de cas ; expérience reproductible ; référence ; lien croisé vers un contenu déjà expliqué.

La décision doit équilibrer bénéfice pédagogique, charge cognitive, périmètre de la page et coût de maintenance. Le nombre de sources n'est pas une mesure de qualité.

## 8. Quand créer un dossier ?

Créer un dossier lorsque plusieurs sources apportent des contributions matériellement différentes, lorsque des affirmations divergent, lorsqu'un sujet central est appelé à évoluer, ou lorsqu'une décision éditoriale doit rester compréhensible pour les mainteneurs futurs. Ne pas en créer pour chaque source isolée ou recouvrement trivial. Le garder concis et lier les enregistrements canoniques.

## 9. Critères de fin

La synthèse est terminée lorsque la question d'apprentissage et la couverture canonique sont explicites ; les sources et éléments extraits sont traçables ; perspectives distinctes, recouvrements, convergences et désaccords sont distingués ; la qualité des preuves et l'indépendance ne sont pas exagérées ; les décisions sont justifiées ; les changements publiés conservent réserves, provenance et parité bilingue ; les lacunes et questions non résolues sont consignées.
