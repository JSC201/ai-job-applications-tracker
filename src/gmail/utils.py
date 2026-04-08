from googleapiclient.discovery import build
from core.auth import get_credentials
from loguru import logger



def get_service():
    return build('gmail', 'v1', credentials=get_credentials())
