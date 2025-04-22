from google import genai
from google.genai import types
import pandas as pd

GOOGLE_API_KEY = 'AIzaSyAXllQXKvQmkAz5mK0oSabwMDzmmLCb4qI'
client = genai.Client(api_key=GOOGLE_API_KEY)

def embed_json(json):
    embedding = client.models.embed_content(
        model='models/text-embedding-004',
        contents=[json],
        config=types.EmbedContentConfig(task_type='semantic_similarity'))

    df_embedding = pd.DataFrame([e.values for e in embedding.embeddings], index=[i for i in range(0, 1)])
    return df_embedding

def calc_sim_measure(df_cv, df_job):
    sim = df_cv @ df_job.T
    return sim