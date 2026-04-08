import time
from loguru import logger
from core.config import load_config, save_config
from src.email_monitor.utils.gmail_client import get_recent_emails
from src.email_monitor.utils.openai_classifier import is_job_related, classify_email
from src.job_intake.handlers.write_to_sheet import get_jobs, update_job_status
from src.email_monitor.handlers.create_event import create_interview_event

STATUS_MAP = {
    'rejection': 'Rejected',
    'interview_request': 'Interview Scheduled',
    'online_assessment': 'Online Assessment',
    'offer': 'Offer',
    'application_confirmation': 'Applied',
    'other': None
}

def match_company(classification, jobs):
    company = classification.get('company', '').lower()
    if not company:
        return None
    for job in jobs:
        if company in job.get('Company', '').lower():
            return job
    return None

def run():
    config = load_config()
    sheet_id = config.get('sheet_id')
    if not sheet_id:
        logger.warning("No sheet found in config — add a job first via the web app")
        return

    last_checked = config.get('last_email_check', time.time() - 86400)
    logger.info(f"Checking emails since {last_checked}")

    emails = get_recent_emails(last_checked)
    logger.info(f"Found {len(emails)} emails to process")

    jobs = get_jobs(sheet_id)
    processed = 0

    for email in emails:
        logger.info(f"Checking: {email['subject']}")

        if not is_job_related(email):
            logger.info("Not job-related, skipping")
            continue

        classification = classify_email(email)
        category = classification.get('category')
        status = STATUS_MAP.get(category)
        logger.info(f"Classified as: {category} — {classification.get('company')}")

        if not status or category == 'other':
            continue

        job = match_company(classification, jobs)
        if job:
            update_job_status(sheet_id, job['row'], status, classification.get('notes', ''))
            logger.info(f"Updated {job['Company']} to {status}")

            if category == 'interview_request' and classification.get('interview_date'):
                create_interview_event(job['Company'], job['Job Title'], classification['interview_date'])
        else:
            logger.warning(f"Could not match company: {classification.get('company')}")

        processed += 1

    config['last_email_check'] = time.time()
    save_config(config)
    logger.info(f"Done. Processed {processed} job-related emails.")

if __name__ == '__main__':
    run()
