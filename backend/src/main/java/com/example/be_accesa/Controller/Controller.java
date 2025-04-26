package com.example.be_accesa.Controller;

import com.example.be_accesa.DTO.CvSimilarityDTO;
import com.example.be_accesa.Model.CvHash;
import com.example.be_accesa.Model.JobHash;
import com.example.be_accesa.Service.*;
import com.example.be_accesa.Utils.FileHasher;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.nio.charset.StandardCharsets;
import java.util.*;

@RestController
@RequestMapping("/api")
public class Controller {

    private final FilebaseService filebaseService;
    private final PGService pgService;
    private final RedisService redisService;
    private final CvHashService cvHashService;
    private final JobHashService jobHashService;

    @Autowired
    public Controller(FilebaseService filebaseService,
                      PGService pgService,
                      RedisService redisService,
                      CvHashService cvHashService,
                      JobHashService jobHashService) {
        this.filebaseService = filebaseService;
        this.pgService = pgService;
        this.redisService = redisService;
        this.cvHashService = cvHashService;
        this.jobHashService = jobHashService;
    }

    @PostMapping("/upload-cv-batch")
    public ResponseEntity<Object> uploadBatch(@RequestParam("files") MultipartFile[] files) {
        Map<String, String> map = new HashMap<>();

        for(MultipartFile file : files) {
            String cvHash = FileHasher.hashMultipartFile(file);

            if(cvHash == null){
                return ResponseEntity.badRequest().body("Error hashing cv " + file.getOriginalFilename());
            }

            CvHash newCvHash;

            try{
                newCvHash = cvHashService.save(cvHash);
            } catch (Exception e){
                // TODO: handle multiple different exceptions
                continue;
            }

            String fileHashed = newCvHash.getId().toString() + ".docx";
            String cvId = "cv-raw/" + fileHashed;

            if(!filebaseService.uploadFile(cvId, file)) {
                return ResponseEntity.badRequest().body("Error uploading raw cv " + file.getOriginalFilename());
            }

            if(!redisService.enqueueCvId(fileHashed)) {
                return ResponseEntity.badRequest().body("Error adding cv id to queue" + file.getOriginalFilename());
            }

            map.put(file.getOriginalFilename(), cvId);
        }

        return ResponseEntity.ok(map);
    }

    @PostMapping("/upload-job-batch")
    public ResponseEntity<Object> addJobs(@RequestParam("files") List<MultipartFile> files) {
        Map<String, String> map = new HashMap<>();

        for(MultipartFile file : files) {
            String jobHash = FileHasher.hashMultipartFile(file);

            if(jobHash == null){
                return ResponseEntity.badRequest().body("Error hashing job " + file.getOriginalFilename());
            }

            JobHash newJobHash;

            try{
                newJobHash = jobHashService.save(jobHash);
            } catch (Exception e){
                // TODO: handle multiple different exceptions
                continue;
            }

            String fileHashed = newJobHash.getId().toString() + ".docx";
            String jobId = "jobs/" + fileHashed;

            if(!filebaseService.uploadFile(jobId, file)) {
                return ResponseEntity.badRequest().body("Error uploading raw job " + file.getOriginalFilename());
            }

            if(!redisService.enqueueJobId(fileHashed)) {
                return ResponseEntity.badRequest().body("Error adding job id to queue " + file.getOriginalFilename());
            }

            map.put(file.getOriginalFilename(), jobId);
        }

        return ResponseEntity.ok(map);
    }

    @GetMapping("/get-job-top")
    public ResponseEntity<Object> getJobTopCv(@RequestParam("jobId") Long jobId, @RequestParam("limit") int limit) {
        List<String> cvList = new ArrayList<>();

        List<CvSimilarityDTO> topCvList = pgService.getTopCvForJobId(jobId, limit);

        for(CvSimilarityDTO cv : topCvList) {
            String cvId = cv.getId() + ".docx";

            byte[] cvJsonBytes = filebaseService.getFile(cvId);

            if(cvJsonBytes == null) {
                return ResponseEntity.badRequest().body("Error fetching cv with id " + cvId);
            }

            String cvJson = new String(cvJsonBytes, StandardCharsets.UTF_8);

            cvList.add(cvJson);
        }

        return ResponseEntity.ok(cvList);
    }

    @DeleteMapping("delete-job")
    public ResponseEntity<?> deleteJob(@RequestParam("jobId") String jobId) {
        if(filebaseService.deleteFile(jobId)) {
            return ResponseEntity.ok("Deleted " + jobId);
        }

        return ResponseEntity.badRequest().body("Error deleting " + jobId);
    }
}
