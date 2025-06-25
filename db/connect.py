import mysql.connector
from mysql.connector import errorcode
from config import SOURCE_DB_CONFIG, TARGET_DB_CONFIG


def get_source_connection():
    return mysql.connector.connect(**SOURCE_DB_CONFIG)


def create_database_if_not_exists():
    """Créer la base cible si elle n'existe pas."""
    temp_config = TARGET_DB_CONFIG.copy()
    db_name = temp_config.pop("database")

    conn = mysql.connector.connect(**temp_config, )
    cursor = conn.cursor()
    try:
        cursor.execute(f"drop database if exists kutniti_clean")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✔ Base créée ou déjà existante : {db_name}")
    except mysql.connector.Error as err:
        print(f"Erreur création base : {err}")
    finally:
        cursor.close()
        conn.close()


def get_target_connection():
    """Connexion à la base cible (assume qu'elle existe déjà)."""
    return mysql.connector.connect(**TARGET_DB_CONFIG)
