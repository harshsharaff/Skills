---
name: gmail-assistant
description: >-
  Read, search, and summarize a user's personal Gmail via the Gmail API.
  Use when the user wants to find emails, get an inbox overview, or summarize
  recent/matching messages. Requires a one-time OAuth setup.
disable-model-invocation: true
---
# Gmail Assistant

## Setup (one time)

1. Place the OAuth client file from Google Cloud Console at
   `credentials.json` in this skill folder.
2. Install dependencies: `pip install -r requirements.txt`.
3. First run opens a browser to authorize; a `token.json` is cached so later
   runs are silent. Verify auth with:

```bash
python scripts/auth.py
```

Both `credentials.json` and `token.json` are git-ignored. The configured scope
is full access (`https://mail.google.com/`).

## Instructions

Run the helper scripts; do not hand-build API calls. All scripts print JSON.

- **Search** for messages (returns metadata only):

```bash
python scripts/search.py --from amazon.com --max 5
python scripts/search.py -q "is:unread newer_than:7d"
```

- **Summarize**: fetch recent or matching emails *with bodies*, then write the
  summary yourself from the JSON (the script intentionally does not summarize):

```bash
python scripts/summarize.py --max 5
python scripts/summarize.py -q "is:unread newer_than:3d" --max 10
```

Present results as a short table (sender, subject, date) and call out anything
notable. For summaries, group by topic/sender and keep it concise.

## Utility scripts

- **auth.py** — builds the authenticated Gmail service; run directly to test login.
- **search.py** — search by `-q` raw query or `--from/--subject/--keyword/--unread/--newer-than`.
- **summarize.py** — fetch emails with trimmed bodies as JSON for summarization.
- **gmail_utils.py** — shared helpers (listing ids, reading metadata/bodies).

## Requirements

Google API client libraries (see [requirements.txt](requirements.txt)).
