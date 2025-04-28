import threading

import pandas as pd

from scripts.repo.abstract_file_repo import save_embeddings, get_df

table_name = "job_embeddings"

cached_data = None
cache_valid = False
cache_lock = threading.Lock()

# Save Job embeddings from DataFrame
def save_job_embeddings(df_orig: pd.DataFrame) -> pd.DataFrame:
    return save_embeddings(df_orig, table_name)

# Get all job embeddings as DataFrame
def get_jobs_df() -> pd.DataFrame:
    global cache_valid, cached_data

    with cache_lock:
        if not cache_valid:
            cached_data = get_df(table_name)
            cache_valid = True

    return cached_data

def invalidate_job_cache():
    with cache_lock:
        global cache_valid
        cache_valid = False

