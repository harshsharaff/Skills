#!/usr/bin/env python3
"""Scaffold a new skill directory.

Usage:
    python scripts/new_skill.py my-skill --kind text|template|script
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

SKILL_MD = """---
name: {name}
description: >-
  TODO one-line WHAT this does and WHEN to use it (third person, trigger terms).
disable-model-invocation: true
---
# {title}

## Instructions

TODO: step-by-step guidance for the agent.
"""

SCRIPT_PY = '''#!/usr/bin/env python3
"""Helper script for the {name} skill."""


def run() -> str:
    return "TODO"


if __name__ == "__main__":
    print(run())
'''

TEST_PY = '''from scripts.example import run


def test_run():
    assert run() == "TODO"
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--kind", choices=["text", "template", "script"], default="text")
    args = ap.parse_args()

    name = args.name
    if not re.match(r"^[a-z0-9-]{1,64}$", name):
        ap.error("name must be lowercase letters/digits/hyphens, <=64 chars")

    dest = SKILLS_DIR / name
    if dest.exists():
        ap.error(f"{dest} already exists")
    dest.mkdir(parents=True)

    title = name.replace("-", " ").title()
    (dest / "SKILL.md").write_text(SKILL_MD.format(name=name, title=title), encoding="utf-8")

    if args.kind == "template":
        (dest / "templates").mkdir()
        (dest / "templates" / "output.md").write_text("# {{ title }}\n", encoding="utf-8")
        (dest / "reference.md").write_text(f"# {title} reference\n", encoding="utf-8")
    elif args.kind == "script":
        (dest / "scripts").mkdir()
        (dest / "scripts" / "__init__.py").write_text("", encoding="utf-8")
        (dest / "scripts" / "example.py").write_text(SCRIPT_PY.format(name=name), encoding="utf-8")
        (dest / "tests").mkdir()
        (dest / "tests" / "__init__.py").write_text("", encoding="utf-8")
        (dest / "tests" / "test_example.py").write_text(TEST_PY, encoding="utf-8")
        (dest / "requirements.txt").write_text("", encoding="utf-8")

    print(f"Created {args.kind} skill at {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
