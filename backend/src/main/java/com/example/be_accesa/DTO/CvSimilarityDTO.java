package com.example.be_accesa.DTO;

public class CvSimilarityDTO {
    private int id;
    private double similarity;

    public CvSimilarityDTO() {}

    public CvSimilarityDTO(int id, double similarity) {
        this.id = id;
        this.similarity = similarity;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getSimilarity() {
        return similarity;
    }

    public void setSimilarity(double similarity) {
        this.similarity = similarity;
    }
}
