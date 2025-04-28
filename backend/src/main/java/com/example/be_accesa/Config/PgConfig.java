package com.example.be_accesa.Config;

import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class PgConfig {
    private final Logger logger = LoggerFactory.getLogger(PgConfig.class);

    @Autowired
    private JdbcTemplate template;

    @PostConstruct
    public void init() {
        createTablesIfNotExist();
    }

    public void createTablesIfNotExist() {
        try {
            String createJobHashTable = "CREATE TABLE IF NOT EXISTS job_hashes (" +
                    "id BIGSERIAL PRIMARY KEY, " +
                    "hash VARCHAR(255) NOT NULL" +
                    ");";

            String createCvHashTable = "CREATE TABLE IF NOT EXISTS cv_hashes (" +
                    "id BIGSERIAL PRIMARY KEY, " +
                    "hash VARCHAR(255) NOT NULL" +
                    ");";

            String createSimMatrixTable = "CREATE TABLE IF NOT EXISTS sim_matrix (" +
                    "id BIGSERIAL PRIMARY KEY" +
                    ");";

            template.execute(createJobHashTable);
            template.execute(createCvHashTable);
            template.execute(createSimMatrixTable);
        }
        catch (Exception e) {
            logger.error(e.getMessage());
        }
    }
}
