import shutil
import subprocess

PROMPT = (
    "Tu es un analyste. Résume la transcription de vidéo YouTube ci-dessous en {language}.\n"
    "Structure exigée (markdown, commence directement par les sections) :\n"
    "## TL;DR — 2 ou 3 phrases\n"
    "## Points clés — liste à puces des idées principales\n"
    "## À retenir — citations ou faits marquants, avec leur horodatage\n"
    "Reste fidèle au contenu ; n'invente rien.\n\n"
    "Titre : {title}\nChaîne : {channel}\n\nTranscription :\n{transcript}"
)


def summarize(
    transcript: str, title: str, channel: str, mode: str, model: str, language: str,
    api_key: str = "",
) -> str | None:
    if mode == "none":
        return None
    prompt = PROMPT.format(language=language, title=title, channel=channel, transcript=transcript)
    try:
        if mode == "claude-cli":
            return _via_claude_cli(prompt)
        if mode == "api":
            return _via_api(prompt, model, api_key)
        raise ValueError(f"mode de résumé inconnu : {mode}")
    except Exception as e:
        print(f"  ! résumé impossible ({e}) — note générée sans résumé")
        return None


def _via_claude_cli(prompt: str) -> str:
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("commande 'claude' introuvable dans le PATH")
    proc = subprocess.run(
        [exe, "-p", "--output-format", "text"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "claude -p a échoué")
    return proc.stdout.strip()


def _via_api(prompt: str, model: str, api_key: str = "") -> str:
    import anthropic

    client = anthropic.Anthropic(**({"api_key": api_key} if api_key else {}))
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    )
    return "\n".join(b.text for b in response.content if b.type == "text").strip()
