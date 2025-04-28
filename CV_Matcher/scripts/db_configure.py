import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
load_dotenv()

PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_CONFIG = {
    "dbname": "CV_Matcher",
    "user": "postgres",
    "password": PASSWORD,
    "host": "localhost",
    "port": "5432"
}


def create_tables():
    """Create tables without timestamps or UUIDs"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS cv_embeddings (
            id SERIAL PRIMARY KEY,
            embedding FLOAT[] NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS job_embeddings (
            id SERIAL PRIMARY KEY,
            embedding FLOAT[] NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sim_matrix (
                    id INTEGER PRIMARY KEY)
        """
    )

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for command in commands:
        cursor.execute(command)

    conn.commit()
    # Verify tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name IN ('cv_embeddings', 'job_embeddings', 'sim_matrix')
    """)
    # print("Created tables:", [row[0] for row in cursor.fetchall()])

    if conn:
        cursor.close()
        conn.close()

def delete_cv_id_from_tables(id):
    """Delete a row from all tables"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    commands = ("""
        DELETE FROM cv_embeddings WHERE id = %s
        """,
        """
        DELETE FROM sim_matrix WHERE id = %s
        """)

    try:
        for command in commands:
            cursor.execute(command, (id,))
    except Exception as e:
        print(f"Error deleting CV ID {id}: {e}")

    conn.commit()

    if conn:
        cursor.close()
        conn.close()

def delete_job_id_from_tables(id):
    """Delete a row from all tables"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    commands = ("""
        DELETE FROM job_embeddings WHERE id = %s
        """,
        """
        ALTER TABLE sim_matrix DROP COLUMN IF EXISTS id
        """)

    try:
        for command in commands:
            cursor.execute(command, (id,))
    except Exception as e:
        print(f"Error deleting JOB ID {id}: {e}")
    conn.commit()

    if conn:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()