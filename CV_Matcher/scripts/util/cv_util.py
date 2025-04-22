from scripts.util.json_parser import summary_cv_and_write_files
from scripts.util.vector_embedding_util import embed_json, calc_sim_measure


def process_cv(cv, df_job_embeddings):
    # convert cv docx to json
    cv_json = summary_cv_and_write_files(cv)
    # create vector embedding for cv
    df_cv_embedding = embed_json(cv_json)
    # calculate sim measure
    new_sims = calc_sim_measure(df_cv_embedding, df_job_embeddings)
    # return cv_vector_embedding, sim_measure
    return df_cv_embedding, new_sims