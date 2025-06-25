# config.py
import os
from dotenv import load_dotenv

load_dotenv()
# Source: base existante
SOURCE_DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Target: base à créer automatiquement si elle n'existe pas
TARGET_DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    "database": os.getenv('NEW_DB')  # tu peux changer ça facilement
}

# Global settings
BATCH_SIZE = 1000
