---
name: git-commit-helper
description: >-
  Generate Conventional Commits messages by analyzing staged git diffs. Use when
  the user asks for help writing a commit message or reviewing staged changes.
disable-model-invocation: true
---
# Git Commit Helper

## Instructions

1. Inspect the staged changes with `git diff --cached`.
2. Pick the type that matches the dominant change: `feat`, `fix`, `refactor`,
   `docs`, `test`, `chore`, `perf`, `build`, `ci`.
3. Infer a short scope from the touched area (e.g. `auth`, `api`). Omit if unclear.
4. Write a `<type>(<scope>): <summary>` subject in the imperative mood, <=50 chars.
5. Add a body only when the "why" is non-obvious. Wrap at 72 chars.

## Format

```
<type>(<scope>): <summary>

<optional body explaining why, not what>
```

## Examples

Input: Added JWT login endpoint and token middleware
```
feat(auth): add JWT login and token validation

Introduce /login endpoint and middleware so protected routes can
verify bearer tokens.
```

Input: Fixed dates rendering in the wrong timezone
```
fix(reports): use UTC timestamps for date formatting
```
