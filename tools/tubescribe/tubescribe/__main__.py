import argparse
import sys

from . import __version__
from . import config as config_mod
from . import pipeline, state, watchlist


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="tubescribe",
        description="YouTube → Whisper → résumé → note markdown (watchlist + dédup)",
    )
    parser.add_argument("--config", help="chemin du fichier config.toml")
    parser.add_argument("--version", action="version", version=f"tubescribe {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_watch = sub.add_parser("watch", help="traiter toutes les vidéos en attente de la watchlist")
    p_watch.add_argument("--no-summary", action="store_true", help="sauter l'étape résumé")

    p_add = sub.add_parser("add", help="ajouter une URL à la watchlist puis traiter")
    p_add.add_argument("url")
    p_add.add_argument("--no-summary", action="store_true")

    p_proc = sub.add_parser("process", help="traiter une ou plusieurs URLs (sans watchlist)")
    p_proc.add_argument("urls", nargs="+")
    p_proc.add_argument("--no-summary", action="store_true")

    sub.add_parser("status", help="vidéos traitées et en attente")

    args = parser.parse_args()
    cfg = config_mod.load(args.config)

    if args.command == "watch":
        created = pipeline.watch(cfg, args.no_summary)
        if created:
            print(f"\n{len(created)} note(s) créée(s) dans {cfg.output_dir}")
    elif args.command == "add":
        watchlist.append_url(cfg.watchlist_file, args.url)
        created = pipeline.watch(cfg, args.no_summary)
        if created:
            print(f"\n{len(created)} note(s) créée(s) dans {cfg.output_dir}")
    elif args.command == "process":
        for url in args.urls:
            print(f"> {url}")
            pipeline.process_url(url, cfg, args.no_summary)
    elif args.command == "status":
        st = state.load(cfg.state_file)
        pend = watchlist.pending_entries(cfg.watchlist_file)
        print(f"Traitées : {len(st)}")
        for vid, e in st.items():
            print(f"  [x] {e['date']}  {e['titre']}  ({vid})")
        print(f"En attente : {len(pend)}")
        for p in pend:
            print(f"  [ ] {p.url}")


if __name__ == "__main__":
    main()
