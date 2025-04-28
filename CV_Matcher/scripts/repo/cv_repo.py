import threading

import pandas as pd

from scripts.repo.abstract_file_repo import save_embeddings, get_df

table_name = "cv_embeddings"

# Save cv embeddings from DataFrame
def save_cv_embeddings(df_orig: pd.DataFrame) -> pd.DataFrame:
    return save_embeddings(df_orig, table_name)

# Get all cv embeddings as DataFrame
def get_cvs_df() -> pd.DataFrame:
    return get_df(table_name)