---
description: Traiter les nouvelles vidéos YouTube de youtube.md (TubeScribe)
---

Traite les nouvelles vidéos de la watchlist :

1. Lance TubeScribe (peut prendre plusieurs minutes par vidéo — télécharge, transcrit avec Whisper, résume) :
   `cd tools/tubescribe && python -m tubescribe watch`
2. Les nouvelles notes arrivent dans `raw/youtube/` et les lignes de `youtube.md` sont cochées automatiquement.
3. Pour chaque nouvelle note produite, propose de l'ingérer dans le wiki (workflow « Ingérer une source » de CLAUDE.md — la note de `raw/youtube/` est la source, ne la modifie pas).
4. Termine par une entrée dans log.md + commit.

Si la commande échoue (yt-dlp, ffmpeg, Whisper), montre l'erreur exacte et propose `python -m tubescribe status` pour diagnostiquer. Si `tools/tubescribe/config.toml` n'existe pas, propose de relancer `/install`.
