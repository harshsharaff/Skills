"""Gmail OAuth helper.

Builds an authenticated Gmail API service object. On first run a browser
opens for consent and a token is cached to token.json; subsequent runs reuse
(and silently refresh) that token.

Files are resolved relative to the skill folder (one level up from scripts/),
unless overridden by the GMAIL_CREDENTIALS / GMAIL_TOKEN env vars.
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Full access (read, send, modify, delete). Chosen for this project.
SCOPES = ["https://mail.google.com/"]

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.environ.get(
    "GMAIL_CREDENTIALS", os.path.join(_SKILL_DIR, "credentials.json")
)
TOKEN_FILE = os.environ.get("GMAIL_TOKEN", os.path.join(_SKILL_DIR, "token.json"))


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing OAuth client file: {CREDENTIALS_FILE}\n"
                    "Download it from Google Cloud Console (APIs & Services -> "
                    "Credentials) and save it there as credentials.json."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def get_service():
    """Return an authenticated Gmail API service client."""
    return build("gmail", "v1", credentials=get_credentials())


if __name__ == "__main__":
    service = get_service()
    profile = service.users().getProfile(userId="me").execute()
    print("Authenticated as:", profile.get("emailAddress"))
    print("Total messages:", profile.get("messagesTotal"))
