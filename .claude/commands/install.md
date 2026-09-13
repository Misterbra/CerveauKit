---
description: Installer le Cerveau Kit (dépendances, configuration, git)
---

Tu installes le Cerveau Kit pour un nouvel utilisateur. Le dossier courant est son futur cerveau. Fais tout, dans l'ordre, et montre un point d'étape clair après chaque bloc. Adapte-toi à l'OS (Windows/macOS/Linux).

## 1. Vérifier les prérequis

- `python --version` → exige 3.11+. Sinon, guide l'utilisateur vers python.org et arrête-toi là.
- `ffmpeg -version` → si absent : propose l'installation (Windows : `winget install Gyan.FFmpeg` ; macOS : `brew install ffmpeg` ; Linux : gestionnaire de paquets) et exécute-la avec son accord.
- `yt-dlp --version` → si absent, il sera installé avec les dépendances Python (étape 2).

## 2. Installer les dépendances Python

```
pip install -r tools/tubescribe/requirements.txt
```

Attention : `faster-whisper` télécharge son modèle de transcription (~1,5 Go pour « medium ») au premier usage — préviens l'utilisateur.

## 3. Configurer TubeScribe

Crée `tools/tubescribe/config.toml` à partir de `tools/tubescribe/config.example.toml`, avec les chemins ABSOLUS du dossier courant :

- `[watchlist] file` → `<racine>/youtube.md`
- `[output] dir` → `<racine>/raw/youtube`
- `[summary] mode` → `"claude-cli"` (l'utilisateur a Claude Code, aucune clé API requise)
- `[whisper] model` → `"medium"` (propose `"small"` si la machine est modeste ou sans GPU)

## 4. Initialiser le suivi de versions

```
git init && git add -A && git commit -m "init: installation du Cerveau Kit"
```

Si git est absent, propose de l'installer ; s'il refuse, note dans log.md que le versioning est désactivé et continue.

## 5. Dater le journal

Remplace la ligne d'installation de `log.md` par la date du jour.

## 6. Test de fumée

```
cd tools/tubescribe && python -m tubescribe --version && python -m tubescribe status
```

Montre le résultat. En cas d'erreur, diagnostique avant de continuer.

## 7. Finaliser

- Demande à l'utilisateur ses 2-3 grands sujets d'intérêt et ajoute-les en commentaire en tête de `index.md` (l'aide à organiser plus tard).
- Recommande d'ouvrir ce dossier comme vault dans Obsidian (« Open folder as vault »).
- Termine par un mini-guide : déposer un fichier dans `raw/` puis `/ingest` ; coller un lien dans `youtube.md` puis `/youtube` ; poser des questions librement ; `/lint` et `/digest` pour l'entretien.
- Commit final : `install: configuration terminée`.
