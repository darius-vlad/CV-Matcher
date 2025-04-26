package com.example.be_accesa.Repository.RowMapper;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;

public class CvSimilarityRowMapper implements RowMapper<CvSimilarityDTO> {

    @Override
    public CvSimilarityDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
        return new CvSimilarityDTO(
                rs.getInt("id"),
                rs.getDouble("similarity")
        );
    }
}
