from googleapiclient.discovery import build
from core.auth import get_credentials
from core.logger import get_logger

logger = get_logger(__name__)

def get_service():
    return build('gmail', 'v1', credentials=get_credentials())
