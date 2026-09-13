import json
import subprocess
from pathlib import Path


class DownloadError(RuntimeError):
    pass


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        detail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else f"échec : {cmd[0]}"
        raise DownloadError(detail)


def fetch_audio(url: str, workdir: Path, cookies_browser: str = "") -> tuple[Path, dict]:
    """Télécharge l'audio + métadonnées ; renvoie (wav 16 kHz mono, info dict yt-dlp)."""
    workdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp", "--no-playlist", "--no-warnings",
        "-f", "bestaudio/best",
        "--write-info-json",
        "-o", str(workdir / "media.%(ext)s"),
        url,
    ]
    if cookies_browser:
        cmd[1:1] = ["--cookies-from-browser", cookies_browser]
    _run(cmd)

    info_path = next(workdir.glob("media.info.json"), None)
    info = json.loads(info_path.read_text(encoding="utf-8")) if info_path else {}
    media = next((p for p in workdir.glob("media.*") if p.suffix != ".json"), None)
    if media is None:
        raise DownloadError("aucun fichier audio téléchargé")

    wav = workdir / "audio.wav"
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(media), "-vn", "-ar", "16000", "-ac", "1", str(wav)])
    return wav, info
