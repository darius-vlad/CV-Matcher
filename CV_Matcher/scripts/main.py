from google import genai
from google.genai import types

from json_matcher import read_folder

GOOGLE_API_KEY = 'AIzaSyB5c78qm-K4J7U5xjpQwgsPxhH6YGMqPyo'
client = genai.Client(api_key=GOOGLE_API_KEY)

cv_ids, cv_texts, cv_titles = read_folder('../text_files/candidates')
job_ids, job_texts, job_titles = read_folder('../text_files/jobs')

cv_embeddings = client.models.embed_content(
    model='models/text-embedding-004',
    contents=cv_texts,
    config=types.EmbedContentConfig(task_type='semantic_similarity'))
job_embeddings = client.models.embed_content(
    model='models/text-embedding-004',
    contents=job_texts,
    config=types.EmbedContentConfig(task_type='semantic_similarity'))

import pandas as pd
import seaborn as sns

# Set up the embeddings in a dataframe.
df_cv = pd.DataFrame([e.values for e in cv_embeddings.embeddings], index=['cv_' + str(cur_id) for cur_id in cv_ids])
df_job = pd.DataFrame([e.values for e in job_embeddings.embeddings], index=['job_' + str(cur_id) for cur_id in job_ids])

# Perform the similarity calculation
sim = df_cv @ df_job.T
mini = sim.min().min()
maxi = sim.max().max()

sns.heatmap(sim, vmin=mini, vmax=maxi, cmap='Greens')
