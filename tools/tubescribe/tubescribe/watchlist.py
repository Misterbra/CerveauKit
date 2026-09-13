import re
from dataclasses import dataclass
from pathlib import Path

YOUTUBE_ID = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:[^\s]*&)?v=|shorts/|live/)|youtu\.be/)([\w-]{11})"
)
PENDING = re.compile(r"^\s*-\s*\[ \]\s*(\S+)")


@dataclass
class Entry:
    line_no: int
    raw_line: str
    url: str
    video_id: str


def video_id(url: str) -> str | None:
    m = YOUTUBE_ID.search(url)
    return m.group(1) if m else None


def pending_entries(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    if not path.is_file():
        return entries
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        m = PENDING.match(line)
        if not m:
            continue
        url = m.group(1)
        vid = video_id(url)
        if vid:
            entries.append(Entry(i, line, url, vid))
    return entries


def mark_done(path: Path, entry: Entry, note_name: str, date: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if entry.line_no < len(lines) and lines[entry.line_no] == entry.raw_line:
        lines[entry.line_no] = f"- [x] {entry.url} → [[{note_name}]] ({date})"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_url(path: Path, url: str) -> None:
    text = path.read_text(encoding="utf-8") if path.is_file() else "# YouTube — à traiter\n"
    if url in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + f"- [ ] {url}\n", encoding="utf-8")
