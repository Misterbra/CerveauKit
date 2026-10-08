"""Build a deterministic, allowlisted distribution. Never reads the author's live brain."""
from pathlib import Path
import hashlib, json, re, zipfile
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT
TARGET = ROOT / "dist/cerveau-kit-1.1.0.zip"
FILES = json.loads((ROOT / "scripts/cerveau-files.json").read_text(encoding="utf-8"))
PATTERNS = {
    "private-key": r"-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----",
    "service-token": r"\b(?:sk-[A-Za-z0-9_-]{20,}|re_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,})",
    "personal-path": r"(?i)(?:[A-Z]:[\\/](?:Users|Projet)|/Users/|/home/)",
    "personal-address": r"[A-Za-z0-9._%+-]+@(?:gmail|hotmail|outlook|yahoo)\.[A-Za-z]+",
}
def main():
    contents = {}
    for name in FILES:
        p = SOURCE / name
        if not p.resolve().is_relative_to(SOURCE.resolve()) or p.is_symlink():
            raise SystemExit("Unsafe package path: " + name)
        data = p.read_bytes()
        text = data.decode("utf-8")
        for kind, pattern in PATTERNS.items():
            if re.search(pattern, text):
                raise SystemExit("Distribution blocked: " + kind + " in " + name)
        contents[name] = data
    if contents["AGENTS.md"] != contents["CLAUDE.md"]:
        raise SystemExit("Assistant instructions differ")
    manifest = {"version": "1.1.0", "files": {n: hashlib.sha256(b).hexdigest() for n,b in sorted(contents.items())}}
    contents["MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False)+"\n").encode()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(TARGET, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents.items()):
            entry = zipfile.ZipInfo("CerveauKit/"+name, date_time=(2026,10,8,0,0,0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    with zipfile.ZipFile(TARGET) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(FILES)+1
        for name, expected in manifest["files"].items():
            assert hashlib.sha256(archive.read("CerveauKit/"+name)).hexdigest() == expected
    checksum = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    TARGET.with_suffix(".sha256").write_text(checksum+"  "+TARGET.name+"\n", encoding="ascii")
    print(f"Archive verified: {len(contents)} files, {TARGET.stat().st_size} bytes; SHA256 {checksum}")
if __name__ == "__main__": main()
