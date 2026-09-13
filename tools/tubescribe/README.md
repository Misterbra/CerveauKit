# TubeScribe

Turn a markdown watchlist of YouTube links into transcribed, summarized, ready-to-file knowledge notes.

**Pipeline:** watchlist (`youtube.md`) → download audio (yt-dlp) → transcribe (faster-whisper, GPU or CPU) → summarize (Claude) → one markdown note per video, with YAML frontmatter — then the watchlist line is checked off so nothing is ever processed twice.

Built to feed a personal knowledge vault (Obsidian, or any folder of markdown), but works standalone.

## Requirements

- Python 3.11+
- [ffmpeg](https://ffmpeg.org/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp) on PATH
- `pip install -r requirements.txt`
- For summaries: an Anthropic API key (`ANTHROPIC_API_KEY` or `ant auth login`), **or** the Claude Code CLI (`claude`) installed, **or** disable summaries (`mode = "none"`)

## Setup

```sh
cp config.example.toml config.toml
# edit paths: watchlist file + output dir
```

## Usage

```sh
python -m tubescribe watch          # process every unchecked link in the watchlist
python -m tubescribe add <url>      # append a link to the watchlist and process it
python -m tubescribe process <url>  # one-off, without touching the watchlist
python -m tubescribe status         # what's done, what's pending
```

Watchlist format — plain markdown checkboxes:

```markdown
# YouTube — to process
- [ ] https://www.youtube.com/watch?v=XXXXXXXXXXX
- [x] https://youtu.be/YYYYYYYYYYY → [[YYYYYYYYYYY-video-title]] (2026-07-17)
```

Already-processed videos are tracked by video ID in a state file (`.tubescribe-state.json` in the output dir), so re-adding a link is a no-op.

## Output

One note per video: `<video-id>-<slug>.md`

```markdown
---
source: youtube
url: https://www.youtube.com/watch?v=...
video_id: ...
titre: "..."
chaine: "..."
duree: 12:34
publiee: 20260101
traitee: 2026-07-17
langue: fr
tags: [youtube]
statut: brut
---

# Title

## TL;DR
...

## Points clés
...

## Transcription
[0:00-0:04] ...
```

## Configuration

See `config.example.toml`. Key options: Whisper model size/device (auto-falls back from CUDA to CPU), summary backend (`api` / `claude-cli` / `none`), summary language, browser cookies for restricted videos.

## License

MIT — part of [Cerveau Kit](../../README.md). See the repository's `LICENSE`.
