from pathlib import Path

_MODEL = None
_MODEL_KEY = None


def transcribe(
    wav: Path,
    model_size: str = "medium",
    device: str = "auto",
    compute_type: str = "auto",
) -> tuple[list[tuple[float, float, str]], str]:
    """Renvoie (segments [(début, fin, texte)], langue détectée)."""
    global _MODEL, _MODEL_KEY
    from faster_whisper import WhisperModel

    if device == "auto":
        attempts = [
            ("cuda", "float16" if compute_type == "auto" else compute_type),
            ("cpu", "int8" if compute_type == "auto" else compute_type),
        ]
    elif compute_type == "auto":
        attempts = [(device, "float16" if device == "cuda" else "int8")]
    else:
        attempts = [(device, compute_type)]

    key = (model_size, tuple(attempts))
    if _MODEL is None or _MODEL_KEY != key:
        last_err: Exception | None = None
        for dev, ct in attempts:
            try:
                _MODEL = WhisperModel(model_size, device=dev, compute_type=ct)
                _MODEL_KEY = key
                break
            except Exception as e:  # CUDA absent, VRAM insuffisante…
                last_err = e
        else:
            raise RuntimeError(f"impossible de charger le modèle Whisper : {last_err}")

    segs, info = _MODEL.transcribe(
        str(wav), vad_filter=True, vad_parameters={"min_silence_duration_ms": 400}
    )
    out = [(s.start, s.end, s.text.strip()) for s in segs]
    return out, info.language
