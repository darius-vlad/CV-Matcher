package com.example.be_accesa.Service;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Model.JobEmbedding;
import com.example.be_accesa.Repository.JobEmbeddingsRepo;
import com.example.be_accesa.Repository.JobHashRepo;
import com.example.be_accesa.Repository.SimMatrixRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PGService {
    private final SimMatrixRepo simMatrixRepo;
    private final JobEmbeddingsRepo jobEmbeddingsRepo;
    private final JobHashRepo jobHashRepo;

    @Autowired
    public PGService(SimMatrixRepo simMatrixRepo,
                     JobEmbeddingsRepo jobEmbeddingsRepo,
                     JobHashRepo jobHashRepo) {
        this.simMatrixRepo = simMatrixRepo;
        this.jobEmbeddingsRepo = jobEmbeddingsRepo;
        this.jobHashRepo = jobHashRepo;
    }

    public List<CvSimilarityDTO> getTopCvForJobId(Long jobId, int limit) {
        return simMatrixRepo.getTopCvForJobId(jobId, limit);
    }

    public void dropJobIdColumn(Long jobId) {
        simMatrixRepo.dropJobIdColumn(jobId);
    }

    public void deleteJobEmbeddingsRowById(Long jobId) {
        jobEmbeddingsRepo.deleteById(jobId);
    }

    public void deleteJobHashRowById(Long jobId) {
        jobHashRepo.deleteById(jobId);
    }
}
