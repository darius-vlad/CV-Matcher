from scripts.repo.job_repo import save_job_embeddings
from scripts.util.job_util import process_job


def add_jobs(jobs): # actual text from docx/pdf file
    print('Started processing')
    # retrieve all cv vector embeddings
    for job in jobs:
        # TODO: pass in cv_embeddings
        job_embedding, _ = process_job(job, None)
        print(job_embedding)
        save_job_embeddings(job_embedding)
        # save job_vector_embedding in db
        # insert new sim_measure 'column'
    pass