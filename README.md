# Skills

A workspace for authoring, building, and testing [Cursor Agent Skills](https://docs.cursor.com).

## Layout

```
skills/                  # one directory per skill (the source of truth)
  git-commit-helper/     # KIND 1: text-only (high freedom)
  report-generator/      # KIND 2: template-based (medium freedom)
  csv-summarizer/        # KIND 3: script-backed (low freedom) + tests
scripts/                 # repo tooling (validate, scaffold, sync) — not skills
tests/                   # cross-cutting tests
```

## The three kinds of skills

| Kind | Freedom | Contents |
|------|---------|----------|
| Instructional | High | `SKILL.md` only |
| Template | Medium | `SKILL.md` + `templates/` (+ `reference.md`) |
| Script-backed | Low | `SKILL.md` + `scripts/` + `requirements.txt` + `tests/` |

## Workflow

```bash
make new name=my-skill   # scaffold a new skill dir
make validate            # lint every SKILL.md (frontmatter, size, paths)
make build               # install per-skill requirements.txt into .venv
make test                # validate + run all pytest suites
make install             # symlink skills/* into ./.cursor/skills/ for live use
```

## Making skills usable in Cursor

These are **project skills**. Run `make install` to symlink each skill into
`.cursor/skills/`, which is where Cursor discovers project-scoped skills. The
symlinks point back at `skills/`, so edits are picked up live.
