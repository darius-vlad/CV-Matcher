package com.example.be_accesa.Model;

import jakarta.persistence.*;

@Entity
@Table(name = "job_embeddings")
public class JobEmbedding {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name="embedding", nullable = false)
    private double[] embedding;

    public JobEmbedding(double[] embedding) {
        this.embedding = embedding;
    }

    public JobEmbedding() {}

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public double[] getEmbedding() {
        return embedding;
    }

    public void setEmbedding(double[] embedding) {
        this.embedding = embedding;
    }
}
