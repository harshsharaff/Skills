"""Shared helpers for reading Gmail messages."""

import base64


def list_message_ids(service, query="", max_results=10):
    """Return up to max_results message ids matching a Gmail search query."""
    ids = []
    request = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=min(max_results, 500))
    )
    while request is not None and len(ids) < max_results:
        response = request.execute()
        for msg in response.get("messages", []):
            ids.append(msg["id"])
            if len(ids) >= max_results:
                break
        request = (
            service.users()
            .messages()
            .list_next(previous_request=request, previous_response=response)
        )
    return ids[:max_results]


def _header(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def get_message_meta(service, msg_id):
    """Fetch lightweight metadata (from/subject/date/snippet) for a message."""
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=msg_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        )
        .execute()
    )
    headers = msg.get("payload", {}).get("headers", [])
    return {
        "id": msg_id,
        "from": _header(headers, "From"),
        "subject": _header(headers, "Subject"),
        "date": _header(headers, "Date"),
        "snippet": msg.get("snippet", ""),
        "labels": msg.get("labelIds", []),
    }


def _walk_parts(payload):
    """Yield all parts of a message payload, depth-first."""
    stack = [payload]
    while stack:
        part = stack.pop()
        yield part
        for child in part.get("parts", []) or []:
            stack.append(child)


def get_message_body(service, msg_id):
    """Fetch the plain-text body of a message (falls back to snippet)."""
    msg = (
        service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    )
    payload = msg.get("payload", {})
    for part in _walk_parts(payload):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    return msg.get("snippet", "")
