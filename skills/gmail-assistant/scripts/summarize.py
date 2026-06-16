"""Fetch recent or matching emails with their bodies, as JSON.

This script does NOT write the prose summary itself: it gathers the structured
content (sender, subject, date, trimmed body) and the agent turns that into a
summary. Use -q to scope to a search, otherwise it grabs the most recent mail.

Examples:
  python scripts/summarize.py --max 5
  python scripts/summarize.py -q "is:unread newer_than:3d" --max 10
"""

import argparse
import json

from auth import get_service
from gmail_utils import get_message_body, get_message_meta, list_message_ids

BODY_CHAR_LIMIT = 2000


def main():
    parser = argparse.ArgumentParser(
        description="Fetch emails with bodies for summarization."
    )
    parser.add_argument(
        "-q", "--query", default="", help="Gmail search query (default: all mail)."
    )
    parser.add_argument(
        "--max", type=int, default=5, help="Max messages to fetch (default 5)."
    )
    parser.add_argument(
        "--body-limit",
        type=int,
        default=BODY_CHAR_LIMIT,
        help="Trim each body to this many characters.",
    )
    args = parser.parse_args()

    service = get_service()
    ids = list_message_ids(service, query=args.query, max_results=args.max)

    messages = []
    for mid in ids:
        meta = get_message_meta(service, mid)
        body = get_message_body(service, mid)
        if args.body_limit and len(body) > args.body_limit:
            body = body[: args.body_limit] + "\n...[truncated]"
        meta["body"] = body
        messages.append(meta)

    print(
        json.dumps(
            {"query": args.query, "count": len(messages), "messages": messages},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
