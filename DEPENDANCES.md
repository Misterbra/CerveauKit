# Dépendances — version 1.1.0
## Documents : choisissez un assistant
Claude Code (conditions Anthropic) : https://code.claude.com/docs/en/setup.
Ou Codex (conditions OpenAI) : https://developers.openai.com/codex/cli.
Accès personnel compatible et connexion Internet. Le kit ne redistribue aucun assistant et n’inclut pas d’abonnement.
Installation proposée : Claude Code natif via WinGet ; Codex déjà installé ou paquet @openai/codex via npm et Node.js LTS (22 minimum pour le parcours du kit). Node n’est pas une dépendance du stockage des notes.
Obsidian (https://obsidian.md) et Git sont facultatifs.

## Option vidéo Windows
Python 3.12 (PSF) ; FFmpeg (licence selon le build) ; Deno 2 (MIT).
Dans .venv : yt-dlp[default] (Unlicense et composants sous leurs licences), faster-whisper (MIT), dépendances transitives installées par pip.
Deno exécute les traitements JavaScript de yt-dlp ; aucun serveur JavaScript n’est lancé.
Le modèle Whisper est téléchargé au premier usage, pas inclus dans le ZIP.
Les versions directes et transitives sont fixées dans tools/tubescribe/constraints-windows-py312.txt, utilisé par requirements.txt. Leur résolution PyPI a été vérifiée pour Windows x64 et Python 3.12 ; cela ne remplace pas un essai complet de transcription. Les versions effectivement installées sont enregistrées dans .venv/installed-requirements.txt. Une mise à jour exige de régénérer les contraintes et de revalider les traitements.
Aucun SDK Anthropic ou OpenAI ni clé API n’est nécessaire au script de transcription. Demandez le résumé ensuite dans votre assistant.
Sources : https://github.com/yt-dlp/yt-dlp ; https://github.com/SYSTRAN/faster-whisper ; https://www.python.org ; https://ffmpeg.org ; https://deno.com.

## Installateur
Il vérifie les outils avant de proposer leur installation, avec accord interactif. Les modules Python sont isolés dans .venv ; les logiciels système suivent leurs installateurs officiels. Il ne crée pas de service, ne change pas la politique PowerShell permanente et n’enregistre aucune clé. Les fichiers .cmd et tools/windows.ps1 sont consultables avant exécution.
