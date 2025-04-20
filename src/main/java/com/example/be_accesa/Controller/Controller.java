package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvDTO;
import com.example.be_accesa.Service.FilebaseService;
import com.example.be_accesa.Service.RedisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.cache.CacheProperties;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api")
public class Controller {

    private final FilebaseService filebaseService;
    private final RedisService redisService;

    @Autowired
    public Controller(FilebaseService filebaseService,
                      RedisService redisService) {
        this.filebaseService = filebaseService;
        this.redisService = redisService;
    }

    @PostMapping("/upload-batch")
    public void uploadBatch(@RequestParam("files") MultipartFile[] files) {
        for(MultipartFile file : files) {
            String cvId = "cv-raw/" + UUID.randomUUID().toString() + ".pdf";
            filebaseService.uploadRawCv(cvId, file);
            redisService.enqueueCvId(cvId);
        }
    }

    @GetMapping("/get-job-cvs")
    public ResponseEntity<List<CvDTO>> getJobTopCv(@RequestParam("jobId") Long jobId) {
        return null;
    }

    @PostMapping("/add-job")
    public ResponseEntity<?> addJob(@RequestParam("name") String name,
                                    @RequestParam("description") String description) {
        return null;
    }

    @DeleteMapping("delete-job")
    public ResponseEntity<?> deleteJob(@RequestParam("jobId") Long jobId) {
        return null;
    }
}
