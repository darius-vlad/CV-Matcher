package com.example.be_accesa.Service;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class FilebaseService {
    private final AmazonS3 amazonS3;

    @Value("${aws.s3.bucket}")
    private String bucket;

    @Autowired
    public FilebaseService(AmazonS3 amazonS3) {
        this.amazonS3 = amazonS3;
    }

    public boolean uploadFile(String cvId, MultipartFile file) {
        try {
            ObjectMetadata metadata = new ObjectMetadata();
            metadata.setContentLength(file.getSize());
            metadata.setContentType(file.getContentType());

            amazonS3.putObject(
                    new PutObjectRequest(
                            bucket,
                            cvId,
                            file.getInputStream(),
                            metadata
                    )
            );

            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public List<byte[]> getFolder(String foldername) {
        List<byte[]> folder = new ArrayList<>();

        ListObjectsV2Request request = new ListObjectsV2Request()
                .withBucketName(bucket)
                .withPrefix(foldername);

        var items = amazonS3.listObjectsV2(request);

        for(S3ObjectSummary item : items.getObjectSummaries()) {
            String key = item.getKey();
            byte[] content = getFile(key);

            if(key != null) {
                folder.add(content);
            }
        }

        return folder;
    }

    public byte[] getFile(String filename) {
        S3Object s3Object = amazonS3.getObject(bucket, filename);

        try(S3ObjectInputStream inputStream = s3Object.getObjectContent()) {
            return inputStream.readAllBytes();
        }
        catch (IOException e) {
            return null;
        }
    }

    public boolean deleteFile(String filename) {
        try {
            amazonS3.deleteObject(new DeleteObjectRequest(bucket, filename));
            return true;
        }
        catch (Exception e) {
            return false;
        }
    }
}
