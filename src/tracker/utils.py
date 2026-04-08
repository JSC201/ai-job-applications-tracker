from googleapiclient.discovery import build
from core.auth import get_credentials
from core.logger import get_logger

logger = get_logger(__name__)

HEADERS = [
    'Company', 'Job Title', 'Location', 'Salary', 'Date Applied',
    'Status', 'URL', 'Summary', 'Requirements', 'Notes'
]

def get_service():
    return build('sheets', 'v4', credentials=get_credentials())

def create_spreadsheet():
    service = get_service()
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'Job Applications'},
        'sheets': [{'properties': {'title': 'Applications'}}]
    }).execute()
    sheet_id = spreadsheet['spreadsheetId']
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Applications!A1',
        valueInputOption='RAW',
        body={'values': [HEADERS]}
    ).execute()
    logger.info(f"Created spreadsheet: {sheet_id}")
    return sheet_id

def append_row(sheet_id, row):
    service = get_service()
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Applications!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [row]}
    ).execute()

def get_all_rows(sheet_id):
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range='Applications!A2:J'
    ).execute()
    return result.get('values', [])

def update_cell(sheet_id, row, col, value):
    service = get_service()
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f'Applications!{col}{row}',
        valueInputOption='RAW',
        body={'values': [[value]]}
    ).execute()
