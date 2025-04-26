package com.example.be_accesa.Service;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Repository.SimMatrixRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PGService {
    private final SimMatrixRepo simMatrixRepo;

    @Autowired
    public PGService(SimMatrixRepo simMatrixRepo) {
        this.simMatrixRepo = simMatrixRepo;
    }

    public List<CvSimilarityDTO> getTopCvForJobId(Long jobId, int limit) {
        return simMatrixRepo.getTopCvForJobId(jobId, limit);
    }
}
