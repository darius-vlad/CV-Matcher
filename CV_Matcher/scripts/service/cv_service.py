# imports
import seaborn as sns
import matplotlib.pyplot as plt

from scripts.repo.abstract_file_repo import get_connection
from scripts.repo.cv_repo import save_cv_embeddings
from scripts.repo.job_repo import get_jobs_df
from scripts.repo.sim_matrix_repo import insert_new_row
from scripts.util.cv_util import process_cv

def add_cvs(cvs): # actual texts form docx/pdf files
    # retrieve all JOB vector embeddings
    job_vector_embeddings = get_jobs_df()
    id = 1
    for cv in cvs:
        cv_embedding, sim_measures = process_cv(cv, job_vector_embeddings)
        mini = sim_measures.min().min()
        maxi = sim_measures.max().max()
        sns.heatmap(sim_measures, vmin=mini, vmax=maxi, cmap='Greens')
        plt.savefig(f"simpler_similarity_heatmap_{id}.png")
        plt.close()
        # save cv_vector_embedding in db
        save_cv_embeddings(cv_embedding)
        id += 1
        # insert new sim_measure 'row'
        insert_new_row(get_connection(), id, sim_measures)
