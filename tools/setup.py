"""Configuration portable de la transcription locale. Aucune clé ni compte enregistré."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "tools/tubescribe/config.toml"
def main():
    if CONFIG.exists() and input("Remplacer la configuration ? [o/N] : ").strip().lower() != "o":
        print("Configuration conservée.")
        return
    CONFIG.write_text((ROOT / "tools/tubescribe/config.example.toml").read_text(encoding="utf-8"), encoding="utf-8")
    print("Transcription locale configurée. Whisper téléchargera son modèle au premier traitement.")
    print("Après le traitement, ouvrez Claude Code ou Codex pour résumer et classer les transcriptions.")
if __name__ == "__main__":
    main()
