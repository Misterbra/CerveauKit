# CerveauKit — B2Labs
Version 1.1.0 · [Guide français](README.fr.md) · [Start here / Commencer](COMMENCER.html)

A reusable folder of source documents, cited notes and open questions, guided by **Claude Code or Codex**. Choose one assistant; both use the same files and instructions. The kit is free, but does not include an AI subscription or credits.

## What you get
Keep originals in raw/, ask your assistant to create cited notes in wiki/, then ask questions, prepare a brief or review unresolved points. Instructions live in CLAUDE.md and AGENTS.md with identical rules. The included example is fictional and prewritten.
This is a folder of files and scripts, not a standalone AI application. Nothing monitors your computer or runs automatically. Adding a file does not ingest it until you ask. For an occasional question on a single document, a normal chat may be enough.

## First run on Windows
1. Extract the entire archive, then open COMMENCER.html. The guide is in French and works offline.
2. Run VERIFIER.cmd to check available tools without installing them.
3. Run INSTALLER.cmd if necessary. Choose **1 — Claude Code** or **2 — Codex**; each installation asks for confirmation. One assistant is enough.
4. Run OUVRIR-CERVEAU.cmd, select your assistant and sign in with your own compatible account: Claude for Claude Code, ChatGPT with Codex access for Codex. Authorize only your copy of this folder.
5. Ask: “Read raw/exemple-atelier.md. What delivery time is planned and what remains to be confirmed? Cite the source passage.”
6. Add a .txt or .md source, then ask to file it in your knowledge library. Check the generated note against its original.

The historical INSTALLER.bat and TRAITER-VIDEOS.bat files forward to the new launchers.

## Requirements
- Claude Code **or** Codex, Internet and a compatible account. An ordinary browser chat does not automatically connect this folder.
- Claude Code uses the native installer, without requiring Node.js. A free Claude account alone does not provide Claude Code access.
- The Codex installer checks Node.js LTS (22 or newer for this installation path) and npm. An already installed Codex does not need to be reinstalled. Access depends on your ChatGPT plan; API-key usage can incur separate charges. Do not store keys in this kit.
- Obsidian and Git are optional. Any text editor can read the notes. No remote repository or cloud sync is created.
- Python is **not needed for text documents**. The optional video path uses Python 3.12, FFmpeg, Deno and Python modules isolated in .venv. See DEPENDANCES.md for the pinned Windows x64 dependency set.

Official installation: [Claude Code](https://code.claude.com/docs/en/setup) · [Codex](https://developers.openai.com/codex/cli).

## Daily use with either assistant
Ask to file a named source, answer a question with citations, summarize your library or check its references. Claude Code also has /ingest, /digest, /lint and /youtube shortcuts; these are not Codex commands.
Switch assistants between sessions without moving your files. Conversation histories do not transfer. Close one editing session before editing the same notes with the other.
Start with text and Markdown. PDF scans and office formats may need conversion that is not included. Responses can be wrong: check original sources, and request updates after changing or removing a source.

## Optional video workflow
Run INSTALLER-VIDEOS.cmd, add permitted YouTube URLs to youtube.md, then run TRAITER-VIDEOS.cmd. Audio is downloaded and transcribed locally with Whisper on CPU; the model downloads on first use. Notes go to raw/youtube/.
Then open **either assistant** and ask it to summarize and file the transcript with timestamp references. The Python pipeline does not use an AI account or make hidden summarization API calls.
The command named watch processes a batch and exits. It does not watch a directory. Limits: no live streams, two hours per video, downloaded media up to 256 MB. YouTube restrictions can prevent downloads; no browser-cookie import or restriction bypass. Only process material you are authorized to download.
See [TubeScribe instructions](tools/tubescribe/README.md) for commands, failures and migration.

## Data and limitations
Files stay in your local folder, but content processed by Claude Code may be sent to Anthropic, and content processed by Codex may be sent to OpenAI. This is not offline AI. B2Labs receives no documents through the kit and adds no telemetry; third-party software has its own terms and settings.
The instruction files are guidance, not a security sandbox. Check assistant permissions and avoid unnecessary connectors. Never add passwords, keys or confidential material you are not authorized to process. Back up your folder and share the original archive, not a used copy containing your data.
No shared-team access controls, email/CRM connector, scheduled task or remote backup is included.

## Existing users
Back up your notes and any ignored configuration before updating. The installer does not overwrite a video configuration without asking. Version 1.1 removes automatic Claude/API video summaries: generate the transcript, then request the summary in Claude Code or Codex. Old CLI add/process commands are replaced by the watchlist workflow. Existing transcripts and notes should be kept; see the video migration guide.
For macOS/Linux, install your chosen assistant from its official documentation and run claude or codex from this directory. The supplied launchers target Windows; other platforms have not been validated.

## Maintainers: package and test
Run these commands from the repository root with Python 3.11 or later (the end-user video installer specifically targets 3.12):

    python scripts/package-cerveau.py
    python -B -m unittest discover -s tests -p "test_cerveau*.py"

The packager reads a fixed allowlist, scans for common secret/private-path patterns, and writes dist/cerveau-kit-1.1.0.zip with per-file hashes. It never recursively packages your notes. Review any new allowlisted content manually; pattern checks are not a guarantee.
Tests cover failure recovery, URL validation, preservation of existing files, package integrity and both Windows launchers with mock commands. They do not validate a live AI account or a full YouTube transcription on a clean machine.

MIT — see [LICENSE](LICENSE).
