package com.example.be_accesa.Repository;

import com.example.be_accesa.Model.JobEmbedding;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JobEmbeddingsRepo extends JpaRepository<JobEmbedding, Long> {
}
