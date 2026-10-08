import tomllib
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    watchlist_file: Path
    output_dir: Path
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    whisper_compute: str = "int8"
    @property
    def state_file(self):
        return self.output_dir / ".tubescribe-state.json"

def load(path=None):
    p = Path(path or "config.toml").resolve()
    if not p.is_file():
        raise ValueError("Configuration absente. Lancez INSTALLER-VIDEOS.cmd.")
    with p.open("rb") as f:
        data = tomllib.load(f)
    def relative(value):
        v = Path(value)
        return (p.parent / v).resolve() if not v.is_absolute() else v.resolve()
    w = data.get("whisper", {})
    return Config(relative(data.get("watchlist", {}).get("file", "../../youtube.md")),
                  relative(data.get("output", {}).get("dir", "../../raw/youtube")),
                  w.get("model", "base"), w.get("device", "cpu"),
                  w.get("compute_type", "int8"))
