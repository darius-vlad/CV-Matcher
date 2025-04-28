import pandas as pd

from scripts.repo.abstract_file_repo import save_embeddings, get_df

table_name = "job_embeddings"

# Save Job embeddings from DataFrame
def save_job_embeddings(df_orig: pd.DataFrame) -> pd.DataFrame:
    return save_embeddings(df_orig, table_name)

# Get all Job embeddings as DataFrame
def get_jobs_df() -> pd.DataFrame:
    return get_df(table_name)

