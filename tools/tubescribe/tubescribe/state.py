import json
import os
from pathlib import Path
def load(path: Path):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError()
        return data
    except (ValueError, TypeError) as exc:
        raise RuntimeError("Journal vidéo illisible. Conservez-le et restaurez une sauvegarde avant de reprendre.") from exc
def atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
def save(path: Path, data: dict):
    atomic_write(path, json.dumps(data, indent=2, ensure_ascii=False))
