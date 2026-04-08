import os
import json
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

CONFIG_FILE = 'config.json'
SHEET_TAB = 'Applications'

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
