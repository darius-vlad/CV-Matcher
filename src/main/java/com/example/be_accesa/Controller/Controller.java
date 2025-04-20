package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvDTO;
import com.example.be_accesa.Service.FilebaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api")
public class Controller {

    private final FilebaseService filebaseService;

    @Autowired
    public Controller(FilebaseService filebaseService) {
        this.filebaseService = filebaseService;
    }

    @PostMapping("/upload-batch")
    public void uploadBatch(@RequestParam("files") MultipartFile[] files) {
        for(MultipartFile file : files) {
            String randomId = "cv-raw/" + UUID.randomUUID().toString() + ".pdf";
            filebaseService.uploadRawCv(randomId, file);
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
