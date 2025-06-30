import mysql.connector
from mysql.connector import errorcode
from config import SOURCE_DB_CONFIG, TARGET_DB_CONFIG


def get_source_connection():
    return mysql.connector.connect(**SOURCE_DB_CONFIG)


def create_database_if_not_exists():
    """Drop and recreate the target database."""
    temp_config = TARGET_DB_CONFIG.copy()
    db_name = temp_config.pop("database")

    conn = mysql.connector.connect(**temp_config)
    cursor = conn.cursor()
    try:
        cursor.execute("DROP DATABASE IF EXISTS kutniti_clean")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Target database dropped and recreated: {db_name}")
    except mysql.connector.Error as err:
        print(f"Database creation error: {err}")
    finally:
        cursor.close()
        conn.close()


def get_target_connection():
    """Establish connection to the target database (assumes it already exists)."""
    return mysql.connector.connect(**TARGET_DB_CONFIG)
