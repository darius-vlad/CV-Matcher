package com.example.be_accesa.Service;

import com.example.be_accesa.Model.CvHash;
import com.example.be_accesa.Model.JobHash;
import com.example.be_accesa.Repository.ICvHashRepo;
import com.example.be_accesa.Repository.JobHashRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class JobHashService {
    private final JobHashRepo jobRepo;

    @Autowired
    public JobHashService(JobHashRepo jobRepo){
        this.jobRepo = jobRepo;
    }

    public JobHash save(String fileHash){
        return jobRepo.save(new JobHash(fileHash));
    }
}
