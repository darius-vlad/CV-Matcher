package com.example.be_accesa.Repository;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Repository.RowMapper.CvSimilarityRowMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class SimMatrixRepo {

    @Autowired
    private JdbcTemplate template;

    public List<CvSimilarityDTO> getTopCvForJobId(Long jobId, int limit) {
        String sqlQuery = "SELECT id, \"" + jobId + "\" AS similarity " +
                "FROM sim_matrix " +
                "ORDER BY \"" + jobId + "\" DESC " +
                "LIMIT ?";

        return template.query(sqlQuery, new CvSimilarityRowMapper(), limit);
    }

    public void dropJobIdColumn(Long jobId) {
        String columnName = jobId.toString();
        String sqlQuery = "ALTER TABLE sim_matrix DROP COLUMN IF EXISTS \"" + columnName + "\";";

        try {
            template.update(sqlQuery);
        }
        catch (Exception e) {}
    }
}
