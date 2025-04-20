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

    private static final String REDIS_CHANNEL = "queue";

    public boolean enqueueCvId(String cvId) {
        try {
            template.opsForList().leftPush(REDIS_CHANNEL, cvId);
            logger.info("Pushed CV id : " + cvId);
            return true;
        }
        catch (Exception e) {
            logger.error("Error pushing CV id :" + cvId);
            return false;
        }
    }
}
