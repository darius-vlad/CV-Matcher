package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvDTO;
import com.example.be_accesa.Service.FilebaseService;
import com.example.be_accesa.Service.RedisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
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
    public ResponseEntity<Object> uploadBatch(@RequestParam("files") MultipartFile[] files) {
        Map<String, String> map = new HashMap<>();

        for(MultipartFile file : files) {
            String cvId = "cv-raw/" + UUID.randomUUID().toString() + ".docx";

            if(!filebaseService.uploadFile(cvId, file)) {
                return ResponseEntity.badRequest().body("Error uploading raw cv " + file.getOriginalFilename());
            }

            if(!redisService.enqueueCvId(cvId)) {
                return ResponseEntity.badRequest().body("Error adding cv id to queue" + file.getOriginalFilename());
            }

            map.put(file.getOriginalFilename(), cvId);
        }

        return ResponseEntity.ok(map);
    }

    @GetMapping("/get-job-cvs")
    public ResponseEntity<List<CvDTO>> getJobTopCv(@RequestParam("jobId") Long jobId) {
        return null;
    }

    @PostMapping("/add-job")
    public ResponseEntity<Object> addJobs(@RequestParam("files") List<MultipartFile> files) {
        Map<String, String> map = new HashMap<>();

        for(MultipartFile file : files) {
            String jobId = "jobs/" + file.getOriginalFilename();

            if(!filebaseService.uploadFile(jobId, file)) {
                return ResponseEntity.badRequest().body("Error adding job" + file.getOriginalFilename());
            }

            map.put(file.getOriginalFilename(), jobId);
        }

        return ResponseEntity.ok(map);
    }

    @DeleteMapping("delete-job")
    public ResponseEntity<?> deleteJob(@RequestParam("jobId") String jobId) {
        if(filebaseService.deleteFile(jobId)) {
            return ResponseEntity.ok("Deleted " + jobId);
        }

        return ResponseEntity.badRequest().body("Error deleting " + jobId);
    }
}
