import os
import json
from dotenv import load_dotenv
from core.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

CONFIG_FILE = 'config.json'

def get_openai_key():
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        raise ValueError("OPENAI_API_KEY not found in .env")
    return key

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    logger.info("Config saved")
