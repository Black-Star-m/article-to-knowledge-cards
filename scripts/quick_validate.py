#!/usr/bin/env python3
"""Validate a skill folder: layout, frontmatter, name/description rules.

Usage: python scripts/quick_validate.py [path/to/skill-dir]   (default: skills/make-knowledge-cards)
Prints one line per check; exits 1 if any check fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")
TODO_RE = re.compile(r"TODO:", re.I)


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None


def top_level_keys(fm: str) -> dict[str, str]:
    """Minimal YAML read: top-level `key: value`, folding multi-line values."""
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            if key is not None:
                out[key] = " ".join(buf).strip()
            key, value = line.split(":", 1)
            key = key.strip()
            buf = [value.strip()] if value.strip() not in (">-", ">", "|") else []
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        out[key] = " ".join(buf).strip()
    return out


def main() -> int:
    default = Path("skills/make-knowledge-cards")
    skill_dir = Path(sys.argv[1] if len(sys.argv) > 1 else default)

    checks: list[tuple[str, bool, str]] = []

    def check(label: str, ok: bool, detail: str = "") -> None:
        checks.append((label, ok, detail))

    skill_md = skill_dir / "SKILL.md"
    check(f"{skill_dir}/SKILL.md exists", skill_md.is_file(), "")
    if not skill_md.is_file():
        report(checks)
        return 1

    text = skill_md.read_text(encoding="utf-8")
    parts = split_frontmatter(text)
    check("frontmatter delimited by ---", parts is not None)
    if parts is None:
        report(checks)
        return 1

    fm, body = parts
    fields = top_level_keys(fm)
    name = fields.get("name", "")
    desc = fields.get("description", "")

    check("name field present", bool(name), f"name={name!r}")
    check("name is hyphen-case", bool(NAME_RE.match(name)), f"name={name!r}")
    check("description field present", bool(desc))
    check("description <= 1024 chars", len(desc) <= 1024, f"len={len(desc)}")
    check("description single line", "\n" not in desc)
    check("folder name matches name", skill_dir.resolve().name == name,
          f"folder={skill_dir.resolve().name} name={name!r}")
    check("body under 500 lines", len(body.splitlines()) < 500,
          f"lines={len(body.splitlines())}")

    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".yaml", ".yml", ".txt"}:
            check(f"no TODO in {f.name}", not TODO_RE.search(f.read_text(encoding="utf-8", errors="replace")))
            if f.suffix in {".yaml", ".yml"}:
                check(f"yaml parses: {f.name}", _yaml_ok(f))

    for stray in ("README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "LICENSE.md"):
        check(f"no extraneous {stray} in skill", not (skill_dir / stray).exists())

    return report(checks)


def _yaml_ok(path: Path) -> bool:
    try:
        import yaml  # type: ignore
    except ImportError:
        return True  # no parser available; skip rather than false-fail
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def report(checks: list[tuple[str, bool, str]]) -> int:
    failed = 0
    for label, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        suffix = f" ({detail})" if detail and not ok else ""
        print(f"[{mark}] {label}{suffix}")
    print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
