from googleapiclient.discovery import build
from core.auth import get_credentials
from loguru import logger

HEADERS = [
    'Company', 'Job Title', 'Location', 'Work Type', 'Salary',
    'Date Posted', 'Job Post ID', 'Source', 'Recruiter/HM',
    'Recruiter/HM Contact', 'Easy Apply', 'Cover Letter', 'Date Applied',
    'Follow Up Date', 'Status', 'URL', 'Summary', 'Requirements', 'Notes'
]

def col_letter(header_name):
    idx = HEADERS.index(header_name)
    return chr(ord('A') + idx)

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
        range=f'Applications!A2:{col_letter(HEADERS[-1])}'
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
