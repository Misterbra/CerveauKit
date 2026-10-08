import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from .state import atomic_write
PENDING = re.compile(r"^\s*-\s*\[ \]\s*(\S+)")
@dataclass
class Entry:
    line_no: int
    raw_line: str
    url: str
    video_id: str

def video_id(url):
    try:
        u = urlparse(url)
        if u.scheme not in ("http", "https") or u.username or u.password:
            return None
        host = (u.hostname or "").lower()
        if host == "youtu.be":
            candidate = u.path.strip("/")
        elif host in ("youtube.com", "www.youtube.com", "m.youtube.com"):
            if u.path == "/watch":
                candidate = parse_qs(u.query).get("v", [""])[0]
            elif u.path.startswith(("/shorts/", "/live/")):
                candidate = u.path.split("/")[2]
            else:
                return None
        else:
            return None
        return candidate if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate) else None
    except (ValueError, IndexError):
        return None

def pending_entries(path: Path):
    entries = []
    if not path.exists():
        raise ValueError("youtube.md introuvable.")
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        m = PENDING.match(line)
        if m:
            vid = video_id(m.group(1))
            if not vid:
                raise ValueError(f"Ligne {i+1} : URL YouTube invalide. Corrigez la ligne avant de relancer.")
            entries.append(Entry(i, line, "https://www.youtube.com/watch?v=" + vid, vid))
    return entries

def mark_done(path, entry, note_name, date):
    lines = path.read_text(encoding="utf-8").splitlines()
    if entry.line_no < len(lines) and lines[entry.line_no] == entry.raw_line:
        lines[entry.line_no] = f"- [x] {entry.url} → [[{note_name}]] ({date})"
        atomic_write(path, "\n".join(lines) + "\n")
    else:
        raise RuntimeError("La liste a changé pendant le traitement. La transcription est conservée ; vérifiez youtube.md.")
