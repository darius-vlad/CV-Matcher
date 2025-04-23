from scripts.util.json_parser import summary_job
from scripts.util.vector_embedding_util import embed_json, calc_sim_measure

def process_job(df_cv_embeddings, job):
    # convert cv docx to json
    job_json = summary_job(job)
    # create vector embedding for cv
    df_job_embedding = embed_json(job_json)
    # calculate sim measure
    # TODO: calculate sim
    # new_sims = calc_sim_measure(df_cv_embedding, df_job_embedding)
    # return cv_vector_embedding, sim_measure
    return df_job_embedding, None