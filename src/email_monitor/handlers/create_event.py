from src.email_monitor.utils.calendar_client import get_service
from loguru import logger

def create_interview_event(company, job_title, datetime_str):
    try:
        service = get_service()
        event = {
            'summary': f'Interview — {company}',
            'description': f'Job: {job_title}\nCompany: {company}',
            'start': {
                'dateTime': f'{datetime_str}:00',
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': f'{datetime_str}:00',
                'timeZone': 'America/New_York',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'popup', 'minutes': 10},
                ]
            }
        }
        service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f"Calendar event created for {company} on {datetime_str}")
    except Exception as e:
        logger.error(f"Failed to create calendar event: {e}")
