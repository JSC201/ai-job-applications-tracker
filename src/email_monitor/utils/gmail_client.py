import base64
from googleapiclient.discovery import build
from core.auth import get_credentials
from loguru import logger

def get_service():
    return build('gmail', 'v1', credentials=get_credentials())

def get_recent_emails(since_timestamp):
    service = get_service()
    query = f'after:{int(since_timestamp)}'
    response = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=50
    ).execute()
    messages = response.get('messages', [])
    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()
        emails.append(parse_email(detail))
    return emails

def parse_email(detail):
    headers = {h['name']: h['value'] for h in detail['payload']['headers']}
    body = extract_body(detail['payload'])
    return {
        'id': detail['id'],
        'from': headers.get('From', ''),
        'subject': headers.get('Subject', ''),
        'date': headers.get('Date', ''),
        'body': body[:3000]
    }

def extract_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        for part in payload['parts']:
            result = extract_body(part)
            if result:
                return result
    else:
        data = payload['body'].get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ''
