from datetime import date
from src.parser.utils import extract_job_fields
from loguru import logger



def parse_job_posting(text):
    logger.info("Parsing job posting")
    data = extract_job_fields(text)
    data['date_applied'] = date.today().strftime('%Y-%m-%d')
    data['status'] = 'Applied'
    data['notes'] = ''
    logger.info(f"Parsed: {data.get('title')} at {data.get('company')}")
    return data
