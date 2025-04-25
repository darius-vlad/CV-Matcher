package com.example.be_accesa.Service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

@Service
public class RedisService {
    private static final Logger logger = LoggerFactory.getLogger(RedisService.class);

    @Autowired
    private StringRedisTemplate template;
    private static final String CV_QUEUE   = "queue:cvs";
    private static final String JOB_QUEUE  = "queue:jobs";

    public boolean enqueueCvId(String cvId) {
        try {
            template.opsForList().leftPush(CV_QUEUE, cvId);
            logger.info("Pushed CV id : " + cvId);
            return true;
        }
        catch (Exception e) {
            logger.error("Error pushing CV id :" + cvId);
            return false;
        }
    }
    public boolean enqueueJobId(String jobId) {
        try {
            template.opsForList().leftPush(JOB_QUEUE, jobId);
            logger.info("Pushed Job id : " + jobId);
            return true;
        }
        catch (Exception e) {
            logger.error("Error pushing Job id :" + jobId);
            return false;
        }
    }
}
