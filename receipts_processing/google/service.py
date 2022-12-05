import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials_dir = os.path.dirname(
    os.path.realpath(__file__))

CREDENTIALS_PATH = os.path.join(credentials_dir, 'credentials.json')
TOKEN_PATH = os.path.join(credentials_dir, 'token.json')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/drive']


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds


services = {
    'gmail': ('gmail', 'v1'),
    'drive': ('drive', 'v3')
}


def create_service(service):
    s = services[service]
    return build(s[0], s[1], credentials=get_credentials())
