#import boto3
#bucket_name = 'your-bucket-name'
#object_key = 'folder/filename.txt'
#s3 = boto3.client('s3')  # Will use credentials from environment or config
# Download object
#s3.download_file(bucket_name, object_key, 'local_filename.txt')
#print("Download complete.")