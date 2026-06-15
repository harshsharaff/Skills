"""Repo-wide test: every skill directory passes validation."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skill import validate_skill  # noqa: E402

SKILL_DIRS = sorted(
    d for d in (ROOT / "skills").iterdir() if (d / "SKILL.md").exists()
)


def test_at_least_one_skill():
    assert SKILL_DIRS, "no skills found under skills/"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda d: d.name)
def test_skill_is_valid(skill_dir):
    errors = validate_skill(skill_dir)
    assert not errors, "\n".join(errors)
