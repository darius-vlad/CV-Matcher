package com.example.be_accesa.Service;

import com.example.be_accesa.Model.CvHash;
import com.example.be_accesa.Repository.ICvHashRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CvHashService {
    private ICvHashRepo cvRepo;

    @Autowired
    public CvHashService(ICvHashRepo cvRepo){
        this.cvRepo = cvRepo;
    }

    public CvHash add(CvHash cvHash){
        return cvRepo.save(cvHash);
    }
}
