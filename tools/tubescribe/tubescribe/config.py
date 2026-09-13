import os
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    watchlist_file: Path
    output_dir: Path
    whisper_model: str = "medium"
    whisper_device: str = "auto"
    whisper_compute: str = "auto"
    hf_home: str = ""
    summary_mode: str = "api"  # api | claude-cli | none
    summary_model: str = "claude-opus-4-8"
    summary_language: str = "fr"
    summary_api_key: str = ""  # optionnel : sinon ANTHROPIC_API_KEY / profil ant
    keep_media: bool = False
    cookies_browser: str = ""

    @property
    def state_file(self) -> Path:
        return self.output_dir / ".tubescribe-state.json"


def load(path: str | None) -> Config:
    candidates = [Path(path)] if path else [Path("config.toml"), Path.home() / ".tubescribe.toml"]
    data: dict = {}
    for p in candidates:
        if p.is_file():
            with open(p, "rb") as f:
                data = tomllib.load(f)
            break
    else:
        if path:
            sys.exit(f"Config introuvable : {path}")

    wl = data.get("watchlist", {})
    out = data.get("output", {})
    wh = data.get("whisper", {})
    su = data.get("summary", {})
    dl = data.get("download", {})

    cfg = Config(
        watchlist_file=Path(wl.get("file", "youtube.md")),
        output_dir=Path(out.get("dir", "output")),
        whisper_model=wh.get("model", "medium"),
        whisper_device=wh.get("device", "auto"),
        whisper_compute=wh.get("compute_type", "auto"),
        hf_home=wh.get("hf_home", ""),
        summary_mode=su.get("mode", "api"),
        summary_model=su.get("model", "claude-opus-4-8"),
        summary_language=su.get("language", "fr"),
        summary_api_key=su.get("api_key", ""),
        keep_media=bool(dl.get("keep_media", False)),
        cookies_browser=dl.get("cookies_browser", ""),
    )
    if cfg.hf_home:
        os.environ.setdefault("HF_HOME", cfg.hf_home)
    return cfg
