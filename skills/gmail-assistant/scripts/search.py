"""Search Gmail messages and print results as JSON.

Uses Gmail's native search syntax via -q, or convenience flags that are
combined into a query (--from, --subject, --keyword, --unread, --newer-than).

Examples:
  python scripts/search.py --from amazon.com --max 5
  python scripts/search.py --unread --newer-than 7d
  python scripts/search.py -q "from:boss@work.com is:important"
"""

import argparse
import json
import sys

from auth import get_service
from gmail_utils import get_message_meta, list_message_ids


def build_query(args):
    if args.query:
        return args.query
    parts = []
    if args.sender:
        parts.append(f"from:{args.sender}")
    if args.subject:
        parts.append(f"subject:({args.subject})")
    if args.keyword:
        parts.append(args.keyword)
    if args.unread:
        parts.append("is:unread")
    if args.newer_than:
        parts.append(f"newer_than:{args.newer_than}")
    return " ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Search Gmail messages.")
    parser.add_argument("-q", "--query", help="Raw Gmail search query.")
    parser.add_argument("--from", dest="sender", help="Filter by sender.")
    parser.add_argument("--subject", help="Filter by subject text.")
    parser.add_argument("--keyword", help="Free-text keyword to match.")
    parser.add_argument("--unread", action="store_true", help="Only unread messages.")
    parser.add_argument(
        "--newer-than", help="Relative age, e.g. 7d, 2m, 1y (Gmail syntax)."
    )
    parser.add_argument(
        "--max", type=int, default=10, help="Max messages to return (default 10)."
    )
    args = parser.parse_args()

    query = build_query(args)
    service = get_service()
    ids = list_message_ids(service, query=query, max_results=args.max)
    results = [get_message_meta(service, mid) for mid in ids]

    print(
        json.dumps(
            {"query": query, "count": len(results), "messages": results}, indent=2
        )
    )
    if not results:
        print("No messages matched.", file=sys.stderr)


if __name__ == "__main__":
    main()
