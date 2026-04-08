from googleapiclient.discovery import build
from core.auth import get_credentials
from loguru import logger

def get_service():
    return build('calendar', 'v3', credentials=get_credentials())
