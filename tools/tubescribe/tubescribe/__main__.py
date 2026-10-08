import argparse
import os
import sys
from . import config, pipeline, state, watchlist

def main():
    parser = argparse.ArgumentParser(description="CerveauKit — traitement manuel des vidéos")
    parser.add_argument("--config", default="config.toml")
    parser.add_argument("command", choices=["watch", "status"])
    args = parser.parse_args()
    lock = None
    fd = None
    try:
        cfg = config.load(args.config)
        if args.command == "status":
            print(f"Transcriptions : {len(state.load(cfg.state_file))} ; vidéos en attente : {len(watchlist.pending_entries(cfg.watchlist_file))}")
            return 0
        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        lock = cfg.output_dir / ".run.lock"
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise RuntimeError("Un traitement est déjà actif. Après un arrêt brutal, vérifiez qu'aucun traitement ne tourne avant de retirer raw/youtube/.run.lock.")
        os.write(fd, str(os.getpid()).encode())
        pipeline.watch(cfg)
        return 0
    except Exception as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    finally:
        if fd is not None:
            os.close(fd)
            lock.unlink(missing_ok=True)
if __name__ == "__main__":
    raise SystemExit(main())
