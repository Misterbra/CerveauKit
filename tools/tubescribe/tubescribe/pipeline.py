import re
import shutil
import tempfile
import unicodedata
from datetime import date
from pathlib import Path

from . import downloader, state, summarizer, transcriber, watchlist
from .config import Config


def _slug(text: str, maxlen: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return text[:maxlen].rstrip("-") or "video"


def _ts(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def process_url(url: str, cfg: Config, no_summary: bool = False) -> str | None:
    """Traite une vidéo ; renvoie le nom de la note créée (sans .md), ou None."""
    vid = watchlist.video_id(url)
    if not vid:
        print(f"  ! URL non reconnue comme vidéo YouTube : {url}")
        return None
    st = state.load(cfg.state_file)
    if vid in st:
        print(f"  = déjà traitée ({st[vid]['note']})")
        return None

    tmp = Path(tempfile.mkdtemp(prefix=f"tubescribe-{vid}-"))
    try:
        print("  - téléchargement audio…")
        wav, info = downloader.fetch_audio(url, tmp, cfg.cookies_browser)
        title = info.get("title") or vid
        channel = info.get("uploader") or info.get("channel") or "?"

        print("  - transcription Whisper…")
        segments, lang = transcriber.transcribe(
            wav, cfg.whisper_model, cfg.whisper_device, cfg.whisper_compute
        )
        transcript = "\n".join(f"[{_ts(s)}-{_ts(e)}] {t}" for s, e, t in segments)

        summary = None
        if not no_summary:
            print(f"  - résumé ({cfg.summary_mode})…")
            summary = summarizer.summarize(
                transcript, title, channel, cfg.summary_mode, cfg.summary_model,
                cfg.summary_language, cfg.summary_api_key,
            )

        note_name = f"{vid}-{_slug(title)}"
        note_path = cfg.output_dir / f"{note_name}.md"
        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        today = date.today().isoformat()
        dur = info.get("duration")
        safe_title = title.replace('"', "'")
        fm = [
            "---",
            "source: youtube",
            f"url: {url}",
            f"video_id: {vid}",
            f'titre: "{safe_title}"',
            f'chaine: "{channel}"',
            f"duree: {_ts(dur) if dur else '?'}",
            f"publiee: {info.get('upload_date', '?')}",
            f"traitee: {today}",
            f"langue: {lang}",
            "tags: [youtube]",
            "statut: brut",
            "---",
        ]
        body = [f"# {title}", ""]
        if summary:
            body += [summary, ""]
        body += ["## Transcription", "", transcript, ""]
        note_path.write_text("\n".join(fm + [""] + body), encoding="utf-8")

        st[vid] = {"url": url, "titre": title, "note": note_name, "date": today}
        state.save(cfg.state_file, st)
        print(f"  + note : {note_path}")
        return note_name
    finally:
        if cfg.keep_media:
            keep_dir = cfg.output_dir / "media" / vid
            keep_dir.parent.mkdir(parents=True, exist_ok=True)
            if not keep_dir.exists():
                shutil.move(str(tmp), str(keep_dir))
        else:
            shutil.rmtree(tmp, ignore_errors=True)


def watch(cfg: Config, no_summary: bool = False) -> list[str]:
    entries = watchlist.pending_entries(cfg.watchlist_file)
    if not entries:
        print("Rien à traiter — aucune vidéo en attente dans la watchlist.")
        return []
    created: list[str] = []
    for e in entries:
        print(f"> {e.url}")
        note = process_url(e.url, cfg, no_summary)
        if note:
            watchlist.mark_done(cfg.watchlist_file, e, note, date.today().isoformat())
            created.append(note)
        else:
            st = state.load(cfg.state_file)
            if e.video_id in st:  # déjà traitée : coche quand même la ligne
                watchlist.mark_done(cfg.watchlist_file, e, st[e.video_id]["note"], st[e.video_id]["date"])
    return created
