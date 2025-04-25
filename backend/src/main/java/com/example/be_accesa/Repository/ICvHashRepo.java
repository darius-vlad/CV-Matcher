package com.example.be_accesa.Repository;

import com.example.be_accesa.Model.CvHash;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ICvHashRepo extends JpaRepository<CvHash, Long> {
}
