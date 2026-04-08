from googleapiclient.discovery import build
from core.auth import get_credentials
from core.config import SHEET_TAB
from loguru import logger

HEADERS = [
    'Company', 'Job Title', 'Date Applied', 'Status', 'Location', 'Work Type',
    'Salary', 'Date Posted', 'Job Post ID', 'Source', 'Recruiter/HM',
    'Recruiter/HM Contact', 'Easy Apply', 'Cover Letter',
    'Follow Up Date', 'URL', 'Summary', 'Requirements', 'Notes'
]

COL_WIDTHS = {
    'Company': 120, 'Job Title': 160, 'Date Applied': 100, 'Status': 110,
    'Location': 100, 'Work Type': 80, 'Salary': 130, 'Date Posted': 100,
    'Job Post ID': 100, 'Source': 90, 'Recruiter/HM': 130,
    'Recruiter/HM Contact': 160, 'Easy Apply': 80, 'Cover Letter': 90,
    'Follow Up Date': 100, 'URL': 80, 'Summary': 350, 'Requirements': 350, 'Notes': 180
}

STATUS_COLORS = {
    'Applied':              {'red': 0.80, 'green': 0.91, 'blue': 0.98},
    'Interview Scheduled':  {'red': 0.80, 'green': 0.96, 'blue': 0.85},
    'Online Assessment':    {'red': 1.0,  'green': 0.95, 'blue': 0.72},
    'Rejected':             {'red': 1.0,  'green': 0.82, 'blue': 0.82},
    'Offer':                {'red': 0.75, 'green': 0.96, 'blue': 0.82},
}

def col_letter(header_name):
    idx = HEADERS.index(header_name)
    return chr(ord('A') + idx)

def get_service():
    return build('sheets', 'v4', credentials=get_credentials())

def create_spreadsheet():
    service = get_service()
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'Job Applications'},
        'sheets': [{'properties': {'title': SHEET_TAB}}]
    }).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']
    tab_id = spreadsheet['sheets'][0]['properties']['sheetId']
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f'{SHEET_TAB}!A1',
        valueInputOption='RAW',
        body={'values': [HEADERS]}
    ).execute()
    format_spreadsheet(spreadsheet_id, tab_id)
    logger.info(f"Created spreadsheet: {spreadsheet_id}")
    return spreadsheet_id

def format_spreadsheet(spreadsheet_id, tab_id):
    service = get_service()
    num_cols = len(HEADERS)
    status_col = col_letter('Status')

    requests = [
        # Freeze header row and company column
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': tab_id,
                    'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 2}
                },
                'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
            }
        },
        # Bold header row
        {
            'repeatCell': {
                'range': {'sheetId': tab_id, 'startRowIndex': 0, 'endRowIndex': 1,
                          'startColumnIndex': 0, 'endColumnIndex': num_cols},
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True}
                    }
                },
                'fields': 'userEnteredFormat.textFormat'
            }
        },
        # Text wrapping, white background, non-bold on all data rows
        {
            'repeatCell': {
                'range': {'sheetId': tab_id, 'startRowIndex': 1,
                          'startColumnIndex': 0, 'endColumnIndex': num_cols},
                'cell': {
                    'userEnteredFormat': {
                        'wrapStrategy': 'WRAP',
                        'backgroundColor': {'red': 1, 'green': 1, 'blue': 1},
                        'textFormat': {'bold': False}
                    }
                },
                'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.bold'
            }
        },
        # Enable filter
        {
            'setBasicFilter': {
                'filter': {
                    'range': {'sheetId': tab_id, 'startRowIndex': 0,
                              'startColumnIndex': 0, 'endColumnIndex': num_cols}
                }
            }
        }
    ]

    # Fixed row height for data rows (~3 lines of text)
    requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': tab_id, 'dimension': 'ROWS', 'startIndex': 1},
            'properties': {'pixelSize': 60},
            'fields': 'pixelSize'
        }
    })

    # Column widths
    for header, width in COL_WIDTHS.items():
        idx = HEADERS.index(header)
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': tab_id, 'dimension': 'COLUMNS',
                          'startIndex': idx, 'endIndex': idx + 1},
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })

    # Conditional formatting by status (colors entire row)
    for status_val, color in STATUS_COLORS.items():
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{'sheetId': tab_id, 'startRowIndex': 1,
                                'startColumnIndex': 0, 'endColumnIndex': num_cols}],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{'userEnteredValue': f'=${status_col}2="{status_val}"'}]
                        },
                        'format': {'backgroundColor': color}
                    }
                },
                'index': 0
            }
        })

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()
    logger.info("Spreadsheet formatted")

def append_row(sheet_id, row):
    service = get_service()
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f'{SHEET_TAB}!A1',
        valueInputOption='RAW',
        insertDataOption='OVERWRITE',
        body={'values': [row]}
    ).execute()

def get_all_rows(sheet_id):
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=f'{SHEET_TAB}!A2:{col_letter(HEADERS[-1])}'
    ).execute()
    return result.get('values', [])

def update_cell(sheet_id, row, col, value):
    service = get_service()
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f'{SHEET_TAB}!{col}{row}',
        valueInputOption='RAW',
        body={'values': [[value]]}
    ).execute()
