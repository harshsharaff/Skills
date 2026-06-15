#!/usr/bin/env python3
"""Symlink each skill in skills/ into ./.cursor/skills/ for live use in Cursor."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
DEST = ROOT / ".cursor" / "skills"


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    count = 0
    for skill in sorted(SRC.iterdir()):
        if not (skill / "SKILL.md").exists():
            continue
        link = DEST / skill.name
        if link.is_symlink() or link.exists():
            if link.is_symlink():
                link.unlink()
            else:
                print(f"skip (not a symlink): {link}")
                continue
        link.symlink_to(Path("../../skills") / skill.name)
        print(f"linked {link} -> {link.readlink()}")
        count += 1
    print(f"Synced {count} skill(s) into {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
