import json
import re
import tempfile
from datetime import date
from pathlib import Path
from . import downloader, state, transcriber, watchlist

def _ts(n):
    m, s = divmod(int(n), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def _render(cfg, vid, record, summary=None):
    transcript_path = cfg.output_dir / f"{vid}.transcript.md"
    transcript = transcript_path.read_text(encoding="utf-8")
    title = str(record["titre"]).replace("\n", " ")
    lines = ["---", "source: youtube", f'url: {record["url"]}',
             f"titre: {json.dumps(title, ensure_ascii=False)}", "statut: brut", "---",
             f"# {title}", "",
             summary or "_Transcription disponible ; aucun résumé généré._", "",
             "## Transcription", "", transcript]
    state.atomic_write(cfg.output_dir / f"{vid}.md", "\n".join(lines) + "\n")

def process_url(url, cfg):
    vid = watchlist.video_id(url)
    if not vid:
        raise ValueError("URL invalide.")
    st = state.load(cfg.state_file)
    if vid in st and (cfg.output_dir / f"{vid}.md").exists():
        print("Déjà transcrite. Ouvrez votre assistant pour la résumer.")
        return vid
    if vid not in st or not (cfg.output_dir / f"{vid}.transcript.md").exists():
        with tempfile.TemporaryDirectory(prefix="cerveau-video-") as temp:
            wav, info = downloader.fetch_audio(url, Path(temp))
            segments, lang = transcriber.transcribe(wav, cfg.whisper_model, cfg.whisper_device, cfg.whisper_compute)
        transcript = "\n".join(f"[{_ts(s)}–{_ts(e)}] {t}" for s, e, t in segments)
        if not transcript.strip():
            raise RuntimeError("Transcription vide. Vidéo laissée en attente.")
        state.atomic_write(cfg.output_dir / f"{vid}.transcript.md", transcript)
        st[vid] = {"url": "https://www.youtube.com/watch?v="+vid,
                   "titre": str(info.get("title") or vid), "channel": str(info.get("uploader") or ""),
                   "note": vid, "date": date.today().isoformat(), "langue": lang, "summary": "pending"}
        state.save(cfg.state_file, st)
    record = st[vid]
    _render(cfg, vid, record)
    return vid

def watch(cfg):
    entries = watchlist.pending_entries(cfg.watchlist_file)
    failures = 0
    for entry in entries:
        try:
            note = process_url(entry.url, cfg)
            watchlist.mark_done(cfg.watchlist_file, entry, note, date.today().isoformat())
            print(f"Note prête : {note}.md")
        except Exception as exc:
            failures += 1
            print(f"Vidéo {entry.video_id} : {exc}")
    print(f"{len(entries)-failures} vidéo(s) traitée(s), {failures} échec(s).")
    if failures:
        raise RuntimeError("Lot incomplet. Les transcriptions déjà obtenues sont conservées. Relancez le lot pour retenter les téléchargements échoués.")
