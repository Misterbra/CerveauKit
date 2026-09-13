# Cerveau Kit

> 🇬🇧 English version: [README.md](README.md)

Un second cerveau auto-alimenté : **Obsidian + Claude Code + ingestion automatique de vidéos YouTube**.

Vous déposez des sources (articles, PDF, liens YouTube) — l'agent les lit, les transcrit,
les résume, les relie entre elles et fait grandir votre base de connaissances à chaque
question posée. Basé sur le pattern « LLM Wiki » d'Andrej Karpathy, augmenté d'un pipeline
YouTube complet (téléchargement, transcription Whisper, résumé).

## Comment ça marche

```
sources ──▶  raw/        (jamais modifiées)
              │
   /ingest    │  /youtube (téléchargement → Whisper → résumé)
              ▼
            wiki/        ◀── l'agent écrit et maintient des pages reliées
              │
   ta question ──▶ l'agent lit le wiki, cite ses sources,
                   et propose de sauvegarder les nouveautés en page (la boucle)
```

## Prérequis

- **Python 3.11+** ([python.org](https://python.org) — cochez « Add Python to PATH »)
- **Claude Code** ([claude.com/claude-code](https://claude.com/claude-code)) — requis pour le
  bibliothécaire (wiki, questions, ingestion) ; la partie YouTube fonctionne sans.
- **Obsidian** (gratuit, [obsidian.md](https://obsidian.md)) — recommandé pour naviguer dans vos notes.
- **ffmpeg** et **yt-dlp** : l'installateur les vérifie et vous aide à les installer.

## Installation — 2 minutes

**Avec Claude Code (expérience complète) :**

1. Décompressez ce dossier où vous voulez (il devient votre cerveau).
2. Ouvrez un terminal dans ce dossier et lancez `claude`.
3. Tapez : **`/install`**

**Sans Claude Code (Windows, pipeline YouTube seul) :**

1. Décompressez ce dossier.
2. Double-cliquez **`INSTALLER.bat`** — il installe les dépendances et vous pose une seule
   question (comment résumer : Claude Code, clé API Anthropic, ou pas de résumé).
3. Collez vos liens dans `youtube.md`, puis double-cliquez **`TRAITER-VIDEOS.bat`**.

**Mac / Linux** — mêmes étapes en terminal :

```sh
pip install -r tools/tubescribe/requirements.txt
python tools/setup.py
cd tools/tubescribe && python -m tubescribe watch
```

Sans Claude Code vous obtenez : téléchargement, transcription Whisper, résumé (si clé API)
et notes markdown organisées — mais pas le bibliothécaire (le wiki auto-relié, les
questions-réponses, `/ingest`).

## Utilisation quotidienne

| Action | Comment |
|--------|---------|
| Ajouter un article/PDF | Déposez le fichier dans `raw/`, puis `/ingest` |
| Ajouter une vidéo YouTube | Collez le lien dans `youtube.md`, puis `/youtube` |
| Poser une question | Demandez simplement — l'agent lit le wiki et cite ses sources |
| Sauvegarder une bonne réponse | L'agent propose de la reverser comme nouvelle page (la boucle) |
| Entretien | `/lint` (cohérence) et `/digest` (résumé périodique) de temps en temps |

## Structure

```
raw/        vos sources brutes (jamais modifiées)
wiki/       les pages de synthèse générées par l'agent
youtube.md  watchlist de vidéos à traiter
index.md    catalogue de toutes les pages
log.md      journal de toutes les opérations
tools/      TubeScribe, le pipeline YouTube (Python)
```

## TubeScribe — le pipeline YouTube

Un outil Python autonome qui transforme une watchlist markdown de liens YouTube en notes
transcrites, résumées et prêtes à classer : watchlist → téléchargement (yt-dlp) →
transcription (faster-whisper, GPU ou CPU) → résumé (Claude) → une note markdown par
vidéo, puis la ligne est cochée pour ne jamais traiter deux fois la même.
Voir [`tools/tubescribe/README.md`](tools/tubescribe/README.md) pour les détails.

## Licence

MIT — voir [LICENSE](LICENSE). Les contributions sont bienvenues.
