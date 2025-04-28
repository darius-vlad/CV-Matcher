import pandas as pd
import numpy as np

def convert_wide_to_compact(df_wide: pd.DataFrame):
    return pd.DataFrame({
        'id': df_wide.index,
        'embedding': df_wide.apply(lambda row: np.array(row, dtype=np.float32), axis=1)
    }).reset_index(drop=True)

def convert_compact_to_wide(df_compact: pd.DataFrame):
    return pd.DataFrame(
        df_compact['embedding'].tolist(),
        index=df_compact.index
    ).rename_axis('id')