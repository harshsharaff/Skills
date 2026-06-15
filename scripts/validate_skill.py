#!/usr/bin/env python3
"""Validate Cursor skill directories.

Checks each SKILL.md for: well-formed frontmatter, a valid `name` and
`description`, body length, and one-level-deep / non-Windows references.

Usage:
    python scripts/validate_skill.py skills/*
Exit code is non-zero if any skill fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
MAX_BODY_LINES = 500
MAX_DESC = 1024


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Return (top-level frontmatter keys, body lines).

    Minimal stdlib-only parser: handles `key: value` and folded `key: >-`
    blocks, which is all skill frontmatter needs.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening '---' frontmatter fence")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("missing closing '---' frontmatter fence")

    fm: dict[str, str] = {}
    i = 1
    while i < end:
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in (">", ">-", "|", "|-"):  # folded/literal block
                block, i = [], i + 1
                while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    block.append(lines[i].strip())
                    i += 1
                fm[key] = " ".join(b for b in block if b).strip()
                continue
            fm[key] = val.strip().strip("\"'")
        i += 1
    return fm, lines[end + 1:]


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = md.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        return [f"{md}: {e}"]

    name = fm.get("name", "")
    if not name:
        errors.append(f"{md}: frontmatter missing 'name'")
    elif not NAME_RE.match(name):
        errors.append(f"{md}: invalid name '{name}' (lowercase/digits/hyphens, <=64)")
    elif name != skill_dir.name:
        errors.append(f"{md}: name '{name}' should match directory '{skill_dir.name}'")

    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{md}: frontmatter missing 'description'")
    elif len(desc) > MAX_DESC:
        errors.append(f"{md}: description too long ({len(desc)} > {MAX_DESC})")

    if len(body) > MAX_BODY_LINES:
        errors.append(f"{md}: body too long ({len(body)} > {MAX_BODY_LINES} lines)")

    for m in re.finditer(r"\]\(([^)]+)\)", text):
        link = m.group(1)
        if "\\" in link:
            errors.append(f"{md}: Windows-style path in reference '{link}'")
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if link.count("/") > 1:
            errors.append(f"{md}: reference not one level deep '{link}'")

    return errors


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in argv[1:]] or [Path("skills")]
    skill_dirs = [p for p in paths if p.is_dir() and (p / "SKILL.md").exists()]
    if not skill_dirs:
        print("No skill directories found.")
        return 0

    all_errors: list[str] = []
    for d in sorted(skill_dirs):
        errs = validate_skill(d)
        status = "FAIL" if errs else "ok"
        print(f"[{status}] {d}")
        all_errors.extend(errs)

    if all_errors:
        print("\nValidation errors:")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print(f"\nAll {len(skill_dirs)} skill(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
