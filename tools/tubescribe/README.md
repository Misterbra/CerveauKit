# TubeScribe — transcription locale à la demande
Version 1.1.0. Le script télécharge l’audio de liens YouTube autorisés, transcrit avec Whisper et conserve une note Markdown avec repères horodatés. Il traite un lot puis s’arrête.

## Installation Windows
Depuis la racine du kit, lancez INSTALLER-VIDEOS.cmd. Le lanceur vérifie Python 3.12, FFmpeg et Deno, propose les outils manquants avec votre accord et installe les modules dans .venv. Le fichier de contraintes fixe 33 versions résolues pour Windows x64/Python 3.12. La résolution ne constitue pas un essai complet de transcription.
La configuration créée garde des chemins relatifs. Le modèle Whisper se télécharge au premier usage ; le profil par défaut utilise le CPU.

## Traitement
Ajoutez une ligne dans youtube.md :

    - [ ] https://www.youtube.com/watch?v=XXXXXXXXXXX

Remplacez XXXXXXXXXXX par un véritable identifiant vidéo. Lancez ensuite TRAITER-VIDEOS.cmd. La note et sa transcription restent dans raw/youtube/. La ligne est cochée après succès. Les autres vidéos continuent si une vidéo échoue ; le lot renvoie alors une erreur. Relancez pour retenter les liens non cochés.
Pour résumer, ouvrez Claude Code ou Codex et demandez de résumer et classer la note en citant ses horodatages. Le script Python ne contacte aucun fournisseur IA de résumé et ne demande aucune clé API.

## Commandes manuelles Windows
Depuis la racine du kit :

    .venv\Scripts\python.exe tools\setup.py
    cd tools\tubescribe
    ..\..\.venv\Scripts\python.exe -m tubescribe --config config.toml status
    ..\..\.venv\Scripts\python.exe -m tubescribe --config config.toml watch

watch traite le lot une fois, sans surveillance permanente. status ne télécharge rien.

## Limites et incidents
Pas de direct, deux heures maximum et 256 Mo de média téléchargé. Utilisez uniquement des contenus autorisés. Les restrictions de YouTube peuvent bloquer un téléchargement ; aucun contournement ou import de cookies du navigateur.
Un journal corrompu n’est pas écrasé. Gardez-le et restaurez une sauvegarde. Après un arrêt brutal, ne retirez raw/youtube/.run.lock qu’après avoir vérifié qu’aucun traitement ne tourne. Les modifications concurrentes de la liste sont signalées, sans les remplacer.

## Migration depuis la première version
Sauvegardez d’abord le dossier, notamment raw/youtube/ et config.toml. Le nouvel installateur demande avant de remplacer la configuration. Les anciens réglages summary/api_key ne servent plus : supprimez les clés de votre configuration après sauvegarde appropriée et gérez vos accès dans l’assistant choisi.
Les anciennes notes avec un nom terminé par un titre ne sont pas renommées ni supprimées. Ne décochez pas tous les anciens liens : seuls les nouveaux liens non cochés doivent être traités. Si vous souhaitez retraiter une ancienne vidéo, archivez d’abord sa note ; la version 1.1 écrit IDENTIFIANT.md et IDENTIFIANT.transcript.md.
Les anciennes commandes add, process et les résumés automatiques sont remplacés par youtube.md, watch et un résumé demandé dans l’assistant. Les anciens .bat restent des raccourcis vers les nouveaux lanceurs.

MIT — voir ../../LICENSE.
