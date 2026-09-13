"""Assistant de configuration du Cerveau Kit — génère tools/tubescribe/config.toml."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "tools" / "tubescribe" / "config.toml"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if CONFIG.is_file():
        answer = input("Une configuration existe déjà. La refaire ? [o/N] : ").strip().lower()
        if answer not in ("o", "oui", "y", "yes"):
            print("Configuration conservée.")
            return

    print()
    print("Comment générer les résumés des vidéos ?")
    print("  [1] Claude Code installé sur cette machine (recommandé — aucune clé à saisir)")
    print("  [2] Clé API Anthropic (paiement à l'usage, sans abonnement — console.anthropic.com)")
    print("  [3] Pas de résumé (transcription seule ; vous pourrez changer plus tard)")
    choice = input("Choix [1/2/3] : ").strip() or "1"

    mode, api_key = "claude-cli", ""
    if choice == "2":
        mode = "api"
        api_key = input("Collez votre clé API (sk-ant-…) : ").strip()
    elif choice == "3":
        mode = "none"

    key_line = f'api_key = "{api_key}"\n' if api_key else ""
    CONFIG.write_text(
        f"""[watchlist]
file = "{(ROOT / 'youtube.md').as_posix()}"

[output]
dir = "{(ROOT / 'raw' / 'youtube').as_posix()}"

[whisper]
model = "medium"
device = "auto"
compute_type = "auto"

[summary]
mode = "{mode}"
model = "claude-opus-4-8"
language = "fr"
{key_line}
[download]
keep_media = false
cookies_browser = ""
""",
        encoding="utf-8",
    )
    print(f"\nConfiguration écrite : {CONFIG}")
    if api_key:
        print("(votre clé reste en local, dans ce fichier — ne partagez pas ce dossier configuré)")
    print("Note : le modèle de transcription Whisper (~1,5 Go) se télécharge au premier traitement.")


if __name__ == "__main__":
    main()
