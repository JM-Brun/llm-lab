# Auditer et améliorer le parcours Comprendre, page par page

Le cas de départ est [l’audit des plongements d’entrée (#1493)](https://github.com/JM-Brun/llm-lab/issues/1493). Une unité de travail est une leçon centrale FR/EN, lue avec ses deux voisines immédiates, sa fiche et les exercices qui vérifient ses acquis. La leçon centrale donne le périmètre de l’audit. Une modification d’une voisine se justifie par un raccord identifié.

Cette procédure applique la [méthode éditoriale](../reader-experience-and-editorial-method.md#7-review-workflow-for-a-page-concept-or-learning-stage) et l’[audit du parcours Comprendre](../../.agents/skills/understand-path-audit/SKILL.md) aux itérations de contribution. Le [registre du parcours](../../data/guided-route.yml) possède l’ordre et les appartenances, l’[inventaire d’audit](../page-audit-inventory.md) les preuves au niveau des pages et le [suivi #971](https://github.com/JM-Brun/llm-lab/issues/971) la continuité de lecture. Les [règles de suivi des issues](../issue-governance.md) s’appliquent aux constats qui demandent une correction.

## 1. Choisir la leçon et retrouver l’état du travail

Depuis la racine du dépôt, produire la liste des paires à partir de l’inventaire existant. Le filtre prend toutes les appartenances centrales dans l’ordre des étapes. Une leçon revisitée apparaît une fois avec tous ses emplacements. Comparer la liste à l’inventaire d’audit, aux issues et aux PR pour choisir la première paire dont la revue reste à faire, ou reprendre la paire demandée.

```bash
audit_dir=$(mktemp -d)
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 \
  python site/tools/audit_revision_coverage.py --json "$audit_dir/revision.json"
python3 - "$audit_dir/revision.json" <<'PY'
import json
import sys
from pathlib import Path

inventory = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
pairs = {}
for page in inventory["pages"]:
    if page["route_status"] == "core" and page["language"] in {"fr", "en"}:
        pairs.setdefault(page["topic"], {})[page["language"]] = page


def positions(page):
    return sorted(
        (item["stage_index"], item["page_index"])
        for item in page["route_memberships"]
        if item["role"] == "core"
    )


for topic, pair in pairs.items():
    if set(pair) != {"fr", "en"} or positions(pair["fr"]) != positions(pair["en"]):
        raise SystemExit(f"Appartenances centrales FR/EN divergentes pour {topic}")

print("Étape.leçon\tThème\tPage FR\tPage EN")
for topic, pair in sorted(pairs.items(), key=lambda item: positions(item[1]["fr"])):
    locations = ",".join(f"{stage}.{page}" for stage, page in positions(pair["fr"]))
    print(locations, topic, pair["fr"]["id"], pair["en"]["id"], sep="\t")
PY
```

Relever le SHA de départ et les versions publiées réellement consultées. Pour chaque constat, vérifier s’il est déjà traité sur `main`, couvert par une PR ouverte ou encore visible dans la version publiée. Indiquer les versions examinées et reprendre les propositions restant à appliquer. Réutiliser l’issue locale lorsqu’elle existe et revenir à #971 pour un problème de continuité commun. Une page sans changement justifié se consigne avec sa preuve dans l’inventaire. Un défaut partagé, par exemple un bandeau généré, se suit une fois chez le propriétaire du composant.

## 2. Auditer l’expérience de lecture

Dans chaque langue, parcourir **page précédente → leçon → page suivante**, puis **plan → fiche → exercice → retour**. Pour une leçon réutilisée à plusieurs étapes, vérifier le rôle qu’elle joue à chaque passage. En début ou fin de parcours, vérifier explicitement l’entrée ou la destination de sortie. Relever les références FR/EN à partir du registre et des métadonnées de page, y compris quand les slugs diffèrent.

| Surface | Question à trancher | Preuve à relever |
| --- | --- | --- |
| Progression | Que sait déjà le lecteur, que peut-il faire après la leçon et quel objet ou quelle question passe à la suivante ? | Prérequis déclaré, phrase de transition, passage utile et lien vers l’ancre. Vérifier aussi le retour vers la preuve depuis la fiche et le saut vers un exercice qui mobilise une notion enseignée plus loin. |
| Modélisation | Le `purpose`, le `scope`, le squelette, le concept canonique et le graphe de calcul désignent-ils le bon objet ou la bonne opération ? | Métadonnées de page, registre, fragment généré ou vue de la carte. Distinguer prérequis, lecture conseillée, hiérarchie et association. |
| Contenu et forme | La première lecture donne-t-elle un exemple que l’on peut suivre jusqu’au résultat attendu ? Les symboles, axes, conditions et portées sont-ils cohérents ? | Texte, formule, figure, légende et texte alternatif. Décrire les frictions de rendu à partir du HTML ou du navigateur en précisant le niveau de preuve. |
| Révision | La fiche permet-elle de retrouver l’acquis de mémoire et d’accéder directement à son application ? | Question, corrigé, lien vers la bonne ancre et chemin de retour, dans les deux langues. |
| Pratique | L’exercice vérifie-t-il une prédiction, un calcul ou un raisonnement à partir de l’énoncé et des prérequis déjà étudiés ? | Énoncé, hypothèses, réponse raisonnée et critère observable. Vérifier la différence entre rappel immédiat et transfert à un cas nouveau. |

Pour chaque frontière, nommer l’objet transmis et l’action que la page suivante effectue dessus. Si une comparaison porte sur deux cas, préciser ce qui reste fixe, ce qui varie et ce que le lecteur doit expliquer. Quand le fil rouge, une illustration et un exercice jouet coexistent, signaler au point de raccord le changement de données, de modèle ou d’hypothèse. Réutiliser la question de rappel ou l’exercice par son ancre quand il mesure déjà l’acquis visé.

Pour un exemple reproductible, repartir de l’entrée que le lecteur peut copier depuis le rendu et la comparer à celle du code. Vérifier les espaces, la ponctuation et, si pertinent, les caractères Unicode. Relever la configuration et la version utilisées. Choisir une assertion qui détecte l’écart étudié, par exemple la séquence d’IDs complète lorsque sa segmentation est l’objet de la leçon. Lorsque les entrées FR/EN diffèrent, vérifier le même acquis dans chaque langue avec le contrôle existant.

Si un point résiste à la seule comparaison interne, partir des [comparaisons existantes](../comparable-projects-landscape.md). Inspecter la section précise d’une ressource comparable ou d’une référence primaire qui permet de trancher. Noter sa version ou sa date, ce qu’elle apporte, et la décision pour LLM Lab. Une comparaison de formats pédagogiques fournit des hypothèses de conception. L’effet sur l’apprentissage se mesure avec un lecteur.

## 3. Transformer les constats en un lot applicable

Pour chaque écart, relever la preuve et son emplacement, la difficulté probable pour l’apprenant, la priorité selon les conventions du projet, le changement minimal, les éléments à préserver et le critère d’acceptation. Préciser si la preuve est une observation directe, une inférence ou un point à vérifier.

Choisir d’abord parmi clarifier, déplacer, fusionner ou relier un contenu existant. Garder l’explication canonique au bon niveau, raccourcir le rappel et relier la pratique à son ancre précise. Pour tout déplacement, noter l’origine et la destination FR/EN, les ancres entrantes, les hypothèses, la figure et son texte alternatif, le corrigé, les références ou le code concernés. Justifier une suppression par l’emplacement de la connaissance préservée ou par une correction explicitement documentée.

Un lot devient applicable lorsque chaque changement proposé a une preuve, une destination et un critère d’acceptation. Une incertitude sur une affirmation scientifique ou un prérequis concerne le changement qui repose sur cette affirmation. Les corrections indépendantes peuvent avancer. Dans l’issue existante, préciser le premier lot, les dépendances entre lots et les contrôles à exécuter sur la version modifiée. Un contrôle navigateur ou un pilote planifié conserve son statut jusqu’à l’obtention de la preuve correspondante.

### Fiche à coller dans le suivi existant

```markdown
## Leçon et base examinée
FR / EN · SHA des sources · rendu observé et date · issue/PR et état

## Raccords et acquis
Précédente → leçon → suivante · plan · fiche · exercice et retour
Acquis observable et exemple ou manipulation qui peut le vérifier
Objet transmis · ce qui reste fixe et ce qui varie · ancre de la preuve

## Constats et décisions
| Priorité et emplacement | Preuve et effet pour le lecteur | Décision, destination FR/EN et préservation | Critère de vérification |
| --- | --- | --- | --- |

## Résultat et reprise
PR, état et SHA vérifié · vérifications exécutées et limites · dépendances, suites et propriétaires · prochaine paire
```

## 4. Appliquer, vérifier et passer à la suite

1. Modifier ensemble la paire et les ressources nécessaires au même raccord lorsque le changement est autorisé. L’[architecture](../information-architecture.md) indique quelle source porte chaque information. Éditer les sources canoniques et régénérer leurs projections avec les commandes de [contribution](../../CONTRIBUTING.md#maintenance-and-validation-workflow). Garder une PR ciblée. Lors d’un conflit sur une carte ou un fragment généré, résoudre d’abord les sources, relancer le générateur sur l’arbre combiné et vérifier le diff par rapport à la base de la PR.
2. Comparer les sources avant/après pour le sens, les exemples et les hypothèses. Vérifier les ancres et destinations déplacées. Quand la leçon ou la navigation change, rendre les pages concernées en FR/EN. Rejouer les raccords et le trajet de révision, y compris les volets repliables, au clavier et en largeur étroite et de bureau. Quand le changement porte sur une sortie vérifiable, exécuter le calcul ou le code extrait de la documentation. Vérifier sur le SHA courant l’état de fusion et les résultats des contrôles CI pertinents lorsque la PR est publiée.
3. Consigner séparément le résultat de la revue source, des contrôles, du rendu, du navigateur et de l’observation éventuelle d’un apprenant. Pour un test de transfert, réutiliser le [protocole existant](../audits/learning-path-learner-evaluation.md). Relever les chemins empruntés et les réponses afin de distinguer un problème d’accès d’un problème de compréhension.
4. Lier l’issue et la PR depuis le suivi pertinent, préciser l’état réel du lot (audité, prêt, intégré ou validé, avec les preuves disponibles) et relever la prochaine paire dans la liste courante. Dans la fenêtre suivante, réutiliser les preuves de la frontière commune si les sources et le rendu n’ont pas changé. À chaque fin d’étape, vérifier qu’un lecteur peut parcourir la chaîne complète depuis le plan jusqu’au retour de l’exercice. La revue couvre la liste lorsque chaque paire a une décision et une preuve ou une suite explicite.

## Cas de référence · les plongements d’entrée

- **Fenêtre** · [Du texte aux tokens](../../site/fr/text-data.qmd) → [Plongements](../../site/fr/embedding-space.qmd) → [Position](../../site/fr/positional-encoding.qmd), avec la contextualisation comme frontière suivante. Les correspondants EN, la [fiche](../../site/fr/revision-embedding-space.qmd) et le [plan](../../site/fr/review-path.qmd#representations) complètent la lecture.
- **Preuve et décision** · Le plan prévoit déjà l’ordre, la répétition et la renumérotation. La leçon explique surtout un ID et la fiche omet le lien direct vers l’[exercice de lookup](../../site/fr/exercises/text-data.qmd#ex-text-to-embedding-lookup). Utiliser le cas jouet déjà disponible dans le texte, la figure et la formule, puis relier la fiche à l’exercice. Préserver le fil rouge du projet, la trace GPT-2 et les exercices plus avancés à leur emplacement.
- **Critère** · Le lecteur restitue `[17, 42, 8, 17]` comme ordre des lignes lues, justifie l’égalité des vecteurs aux positions 0 et 3 à table fixe, puis prévoit la compensation de la permutation. Le calcul additif se poursuit dans [l’exercice positionnel](../../site/fr/exercises/text-data.qmd#ex-token-to-block-input).
- **Suivi** · [#1493](https://github.com/JM-Brun/llm-lab/issues/1493) porte les améliorations de la leçon, [#1492](https://github.com/JM-Brun/llm-lab/issues/1492) porte la transition depuis la tokenisation et la [PR #1491](https://github.com/JM-Brun/llm-lab/pull/1491) documente le raccord déjà intégré. Reprendre la fenêtre suivante sur la position et la contextualisation avec ces références.

### Raccord depuis le panorama et la tokenisation

- **Entrée et preuve** · Dans l’audit [#1492](https://github.com/JM-Brun/llm-lab/issues/1492#issuecomment-7070825224), l’apostrophe droite du préfixe français de la trace donne 15 tokens avec `gpt2` (`tiktoken==0.14.0`). L’apostrophe typographique du texte affiché en donne 16. Les deux séquences finissent par `5633`. Un contrôle du dernier ID répond à la question sur la ponctuation finale. Vérifier l’entrée copiable et toute la séquence pour établir la fidélité du préfixe montré.
- **Passage à la pratique** · La boucle du panorama illustre la prédiction en représentant « Vous » par une unité. Avec GPT-2, `␠Vous` donne deux tokens. Le préfixe GPT-2 fournit ensuite un ID réel. La séquence `[17, 42, 8, 17]` et sa table jouet permettent de calculer le lookup et de reprendre le même vecteur dans l’exercice de position. Expliciter ces changements de convention au fil de la lecture et faire pointer la fiche vers l’exercice existant.
- **Contrôle et intégration** · Sur la [PR #1489](https://github.com/JM-Brun/llm-lab/pull/1489), la régénération des cartes a résolu les conflits. Le même extrait Python vérifie les deux préfixes, ce qui préserve le contrat du [contrôle bilingue](../../site/tools/check_embedding_trace.py). Les valeurs de chaque préfixe, le rendu et l’état de la PR sont des vérifications distinctes.
