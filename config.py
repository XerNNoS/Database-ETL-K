# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Source: existing database
SOURCE_DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Target: database to be created automatically if it does not exist
TARGET_DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('NEW_DB')  # Easily changeable if needed
}

# Global settings
BATCH_SIZE = 1000

