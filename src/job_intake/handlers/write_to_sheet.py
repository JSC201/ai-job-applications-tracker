from src.job_intake.utils.sheets_client import create_spreadsheet, append_row, get_all_rows, update_cell, HEADERS, col_letter
from core.config import save_config
from loguru import logger

def get_or_create_sheet(config):
    if 'sheet_id' in config:
        return config['sheet_id']
    logger.info("No sheet found, creating new one")
    sheet_id = create_spreadsheet()
    config['sheet_id'] = sheet_id
    save_config(config)
    return sheet_id

def add_job(sheet_id, job):
    row = [
        job.get('company', ''),
        job.get('title', ''),
        job.get('location', ''),
        job.get('work_type', ''),
        job.get('salary', ''),
        job.get('date_posted', ''),
        job.get('job_post_id', ''),
        job.get('source', ''),
        job.get('recruiter', ''),
        job.get('contact_link', ''),
        job.get('easy_apply', ''),
        job.get('cover_letter', ''),
        job.get('date_applied', ''),
        job.get('follow_up_date', ''),
        job.get('status', 'Applied'),
        job.get('url', ''),
        job.get('summary', ''),
        job.get('requirements', ''),
        job.get('notes', ''),
    ]
    append_row(sheet_id, row)
    logger.info(f"Added: {job.get('title')} at {job.get('company')}")

def get_jobs(sheet_id):
    rows = get_all_rows(sheet_id)
    jobs = []
    for i, row in enumerate(rows):
        row += [''] * (len(HEADERS) - len(row))
        job = dict(zip(HEADERS, row))
        job['row'] = i + 2
        jobs.append(job)
    return jobs

def update_follow_up_date(sheet_id, row_num, follow_up_date):
    update_cell(sheet_id, row_num, col_letter('Follow Up Date'), follow_up_date)
    logger.info(f"Set follow-up date for row {row_num}: {follow_up_date}")

def update_job_status(sheet_id, row_num, status, notes=''):
    update_cell(sheet_id, row_num, col_letter('Status'), status)
    if notes:
        update_cell(sheet_id, row_num, col_letter('Notes'), notes)
    logger.info(f"Updated row {row_num} to status: {status}")
