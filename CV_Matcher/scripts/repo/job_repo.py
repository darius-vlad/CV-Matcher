import pandas as pd
import psycopg2
import numpy as np
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "CV_Matcher",
    "user": "postgres",
    "password": "changeme",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Save Job embeddings from DataFrame
def save_job_embeddings(df: pd.DataFrame) -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cur:
            ids = []
            for embedding in df['embedding']:
                cur.execute(
                    "INSERT INTO job_embeddings (embedding) VALUES (%s) RETURNING job_id",
                    (embedding.tolist(),))
                ids.append(cur.fetchone()[0])
            conn.commit()
    df['job_id'] = ids
    return df

# Get all Job embeddings as DataFrame
def get_jobs_df() -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql("SELECT * FROM job_embeddings", conn)
    df['embedding'] = df['embedding'].apply(np.array)
    return df