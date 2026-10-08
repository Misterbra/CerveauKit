import json
import subprocess
import sys
from pathlib import Path
from .watchlist import video_id
class DownloadError(RuntimeError):
    pass
def _run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1200)
    except FileNotFoundError as exc:
        raise DownloadError("Outil vidéo absent. Relancez INSTALLER-VIDEOS.cmd.") from exc
    if p.returncode:
        raise DownloadError("Échec du téléchargement ou de la conversion. Vérifiez la disponibilité de la vidéo et les outils installés.")
def fetch_audio(url: str, workdir: Path):
    vid = video_id(url)
    if not vid:
        raise ValueError("URL YouTube invalide.")
    workdir.mkdir(parents=True, exist_ok=True)
    _run([sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-plugin-dirs",
          "--no-playlist", "--js-runtimes", "deno", "--socket-timeout", "30",
          "--retries", "2", "--max-filesize", "256M",
          "--match-filter", "!is_live & duration <= 7200", "-f", "bestaudio/best",
          "--write-info-json", "-o", str(workdir / "media.%(ext)s"),
          "--", "https://www.youtube.com/watch?v=" + vid])
    info_path = workdir / "media.info.json"
    if not info_path.exists():
        raise DownloadError("Vidéo indisponible, en direct ou supérieure à la limite de deux heures.")
    info = json.loads(info_path.read_text(encoding="utf-8"))
    media = next((p for p in workdir.glob("media.*") if p.suffix not in (".json", ".part", ".ytdl")), None)
    if not media:
        raise DownloadError("Aucun fichier audio complet.")
    wav = workdir / "audio.wav"
    _run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(media), "-vn", "-ar", "16000", "-ac", "1", str(wav)])
    return wav, info
