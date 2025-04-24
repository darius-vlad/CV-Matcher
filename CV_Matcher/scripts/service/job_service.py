from scripts.repo.abstract_file_repo import get_connection
from scripts.repo.cv_repo import get_cvs_df
from scripts.repo.job_repo import save_job_embeddings
from scripts.repo.sim_matrix_repo import insert_new_column
from scripts.util.job_util import process_job


def add_jobs(jobs): # actual text from docx/pdf file
    print('Started processing')
    # retrieve all cv vector embeddings
    id = 5
    df_cvs_embeddings = get_cvs_df()
    for job in jobs:
        job_embedding, sim_measures = process_job(df_cvs_embeddings, job, id)
        print(job_embedding)
        # save job_vector_embedding in db
        save_job_embeddings(job_embedding)
        # insert new sim_measure 'column'
        insert_new_column(get_connection(), str(id), sim_measures)
