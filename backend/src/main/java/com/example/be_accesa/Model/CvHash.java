package com.example.be_accesa.Model;

import jakarta.persistence.*;

@Entity
@Table(name = "cv_hashes")
public class CvHash {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name="hash", nullable = false, unique = true)
    private String hash;

    public CvHash(String hash) {
        this.hash = hash;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }
}
