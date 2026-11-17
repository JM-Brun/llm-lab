# Entraîner un petit GPT sur un GPU distant avec Hugging Face Jobs

**Statut :** recette opérationnelle documentée à partir du dépôt source ; non exécutée indépendamment par LLM Lab.  
**Dépôt de référence :** [scienceetonnante/nanogpt-jobs](https://github.com/scienceetonnante/nanogpt-jobs)  
**Révision examinée :** branche `master`, arbre `781d0e4fe0513de8ec74654e75a39e4aa1809853`  
**Complément :** [revue de la vidéo et des limites de preuve](../../docs/source-reviews/huggingface-jobs-nanogpt-video-2026-11.md)

## Pourquoi cette méthode ?

Elle répond à une contrainte fréquente : le code d'entraînement est disponible, mais la machine locale ne possède pas de GPU suffisamment rapide ou assez de mémoire. Le principe est de conserver le programme Python et de déplacer uniquement son exécution vers un GPU managé.

Cette approche constitue une **voie alternative facultative** dans le parcours Build :
- **local** : développer, comprendre, tester sur CPU/MPS/GPU disponible ;
- **GPU distant managé** : lancer ponctuellement une expérience plus coûteuse sans administrer un serveur ;
- **retour local** : récupérer les checkpoints et analyser les résultats.

Elle ne remplace ni la compréhension de la boucle d'entraînement, ni l'évaluation scientifique, ni les tests locaux.

## Architecture de l'exécution

```text
Machine locale
  ├── code Python + requirements.txt
  ├── hf sync ───────────────┐
  └── run_on_hf.sh           │
                             ▼
                    Hub Storage Bucket privé
                      ├── code/
                      └── out/
                             ▲
                             │ volume monté
                             ▼
                    Hugging Face Job
                      ├── image uv / Python
                      ├── GPU choisi explicitement
                      ├── installation des dépendances
                      ├── téléchargement TinyStories depuis le Hub
                      └── entraînement → out/model.pt
                             │
                             ▼
                    hf sync : récupération locale
```

Le bucket joue deux rôles distincts : transporter le code vers le job et conserver les artefacts au-delà de la durée de vie de la machine. Le jeu TinyStories, lui, est téléchargé par le code avec la bibliothèque `datasets` ; il n'est pas copié depuis le disque local par le launcher.

## Ce que fait le dépôt examiné

| Fichier | Responsabilité |
|---|---|
| `train.py` | Télécharge TinyStories, tokenize, définit le GPT, entraîne et sauvegarde `out/model.pt` |
| `requirements.txt` | Déclare `torch`, `numpy`, `tiktoken` et `datasets` |
| `run_on_hf.sh` | Crée/synchronise le bucket, choisit le GPU, lance le job et monte le stockage |
| `sample.py` | Recharge le checkpoint et génère trois histoires |

### Configuration du modèle et de l'entraînement

Le code source fixe les paramètres suivants :

- 8 blocs Transformer, dimension d'embedding 512, 8 têtes ;
- contexte de 512 tokens et vocabulaire GPT-2 de 50 257 tokens ;
- environ 51 millions de paramètres, avec partage des poids entre embedding de tokens et tête de sortie ;
- embeddings positionnels appris (pas RoPE dans cet exemple) ;
- attention causale via `scaled_dot_product_attention` ;
- batch de 16 séquences, soit 8 192 tokens par mise à jour ;
- AdamW, taux maximal de (6\times10^{-4}), warm-up puis décroissance cosinus ;
- écrêtage de norme du gradient à 1 ;
- sur CUDA, `torch.compile` et autocast bfloat16.

Les données d'entraînement sont téléchargées depuis `roneneldan/TinyStories`, tokenisées avec l'encodage GPT-2, concaténées en un grand tableau puis découpées en fenêtres tirées aléatoirement. Le nombre de pas est calculé à partir du nombre total de tokens et de la taille d'un batch ; ce n'est donc pas un parcours séquentiel strict de chaque fenêtre.

## Préparer et lancer

### Prérequis

1. Un compte Hugging Face autorisé à utiliser Jobs, avec abonnement PRO ou crédits suffisants selon les conditions du compte.
2. Le CLI Hugging Face récent, `uv`, un shell Bash et une session authentifiée.
3. Un budget maximal défini avant le lancement.

Depuis le dossier du projet :

```bash
hf auth login
hf jobs hardware
```

La commande `hf jobs hardware` permet de consulter les flavors et leurs prix au moment du lancement. Le script n'impose volontairement aucun GPU par défaut : il faut en choisir un explicitement.

### Lancement distant

```bash
./run_on_hf.sh train.py a100-large
```

Le launcher utilise par défaut un timeout de deux heures. Il accepte une durée explicite et un autre flavor :

```bash
./run_on_hf.sh train.py l4x1 4h
```

Le script :
1. crée un bucket privé nommé d'après le dossier du projet ;
2. synchronise le code dans `code/`, en excluant les fichiers cachés, caches Python et sorties locales ;
3. lance un job détaché dans l'image `ghcr.io/astral-sh/uv:python3.12-bookworm` ;
4. monte le bucket dans le conteneur, relie `out/` au répertoire persistant du bucket ;
5. installe les dépendances depuis `requirements.txt` et exécute le même fichier Python.

Le job est asynchrone. Le launcher affiche son identifiant ; suivre les journaux avec :

```bash
hf jobs logs -f <job-id>
```

### Récupérer et utiliser le checkpoint

Après le job :

```bash
hf sync hf://buckets/<utilisateur>/nanogpt-jobs/out ./out
uv run --with-requirements requirements.txt sample.py "Once upon a time"
```

Le nom du bucket dépend du nom du dossier local et de l'utilisateur Hugging Face. Vérifier le chemin réel avant de synchroniser.

## Adapter le patron à un autre projet

Le launcher est volontairement générique. Pour le réutiliser :

- le programme doit enregistrer ses résultats dans `out/` (ou il faut modifier la variable `OUT`) ;
- le code et les dépendances doivent être dans le dossier synchronisé ;
- les données doivent être téléchargeables depuis le Hub ou une URL, ou être explicitement placées dans un stockage accessible au job ;
- le script doit être compatible avec l'image, la version de Python et le flavor GPU choisis ;
- le chemin de sortie doit pointer vers le volume persistant monté.

Le slogan « sans modifier le code » est donc conditionnel : il suppose que le programme est déjà portable, que ses chemins et dépendances sont compatibles et que ses données sont accessibles.

## Contrôles avant et après exécution

### Avant de dépenser du crédit

- Lancer le script localement sur CPU/MPS/GPU avec une configuration réduite.
- Vérifier les imports, le téléchargement des données, les dimensions des tenseurs et la création effective de `out/`.
- Vérifier que le checkpoint peut être rechargé par `sample.py`.
- Lire le prix du flavor, son type de GPU et le timeout ; fixer une limite de coût.
- Ne jamais placer un token personnel dans le dépôt ou dans le script. Utiliser les mécanismes de secrets documentés par le fournisseur lorsque le job doit accéder à une ressource privée.

### Pendant le job

- Vérifier le statut, les logs, le GPU effectivement visible et l'utilisation mémoire.
- Contrôler le débit de tokens, les pertes, les erreurs OOM et la progression vers le prochain checkpoint.
- Prévoir le comportement en cas de timeout, d'échec ou d'interruption ; un job détaché n'est pas un job garanti jusqu'à son terme.

### Après le job

- Vérifier la présence, la taille et la date du checkpoint dans le bucket.
- Télécharger les artefacts et tester le chargement local.
- Enregistrer le commit du code, les versions des dépendances, le dataset, le flavor, le timeout, les logs, la durée facturée, le coût et les métriques.
- Conserver séparément les données d'entraînement, de validation et de test.

## Limites scientifiques du dépôt

Cette démonstration est surtout un exemple d'orchestration et de portabilité. Le code examiné présente plusieurs limites qu'il faut rendre explicites :

1. **Pas de validation indépendante.** La loss imprimée est celle du batch d'entraînement courant ; aucun jeu de validation séparé ni métrique de test n'est implémenté.
2. **Pas de preuve de généralisation.** Une loss d'entraînement qui baisse ou des histoires générées ne suffisent pas à établir la qualité du modèle.
3. **Mémoire hôte.** Le script tokenise le corpus entier et le concatène en mémoire avant l'entraînement ; la RAM du conteneur compte autant que la VRAM.
4. **Checkpoint périodique.** Le modèle est sauvegardé toutes les 2 000 étapes et à la fin. Une interruption entre deux sauvegardes peut faire perdre le travail depuis le dernier checkpoint.
5. **Reproductibilité incomplète.** Les graines aléatoires, les versions exactes des paquets et une configuration complète de l'expérience ne sont pas fixées par le dépôt.
6. **Évaluation de la durée et du coût.** Le « ~1 $ » dépend du flavor et de la durée réellement facturée ; ce n'est pas un tarif universel.

La page officielle consultée pour A100-large indiquait 2,50 $/heure pour un A100 80 Go, facturé à la minute pendant les états Starting et Running. À ce tarif, 30 minutes représentent environ 1,25 $, hors éventuels autres frais. Toujours reconsulter la [tarification Jobs](https://huggingface.co/docs/hub/en/jobs-pricing).

## Expérience pédagogique proposée pour LLM Lab

Comparer les trois environnements avec exactement le même code et le même protocole :

| Variante | Question |
|---|---|
| CPU local | Le pipeline fonctionne-t-il sans accélérateur ? |
| GPU local (si disponible) | Quel gain apporte l'accélération locale ? |
| GPU managé (Jobs) | Quel gain de temps obtient-on, et à quel coût total ? |

Pour que la comparaison soit interprétable :
- fixer le commit, les données, les dimensions, le batch et le nombre de pas ;
- mesurer le temps de préparation des données séparément du temps d'entraînement ;
- mesurer tokens/seconde, loss d'entraînement et loss de validation ;
- enregistrer le coût réellement facturé, pas seulement le prix horaire affiché ;
- répéter les mesures si l'on veut comparer les performances ;
- distinguer le temps de démarrage, le téléchargement du corpus, la compilation et le calcul GPU.

**Hypothèse testable :** le GPU distant réduit fortement le temps d'entraînement pour un budget borné, mais le bénéfice réel dépend du temps de démarrage, du transfert/chargement des données, de la compilation et du coût facturé.

## Sources

- [Dépôt NanoGPT Jobs](https://github.com/scienceetonnante/nanogpt-jobs) — README, `train.py`, `run_on_hf.sh`, `requirements.txt`, `sample.py`.
- [Hugging Face Jobs : exécuter et gérer des jobs](https://huggingface.co/docs/huggingface_hub/en/guides/jobs).
- [Configuration des Jobs](https://huggingface.co/docs/hub/en/jobs-configuration).
- [Tarification des Jobs](https://huggingface.co/docs/hub/en/jobs-pricing).

**Niveau de preuve :** dépôt source inspecté statiquement ; aucune exécution du job ni dépense de crédit effectuée par LLM Lab.
