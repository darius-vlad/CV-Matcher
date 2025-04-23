import io
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from docx import Document

load_dotenv()
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION            = os.getenv("AWS_REGION")
S3_BUCKET_NAME        = os.getenv("S3_BUCKET_NAME")
S3_ENDPOINT_URL       = os.getenv("S3_ENDPOINT_URL")

missing = [name for name,val in {
    "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
    "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
    "AWS_REGION": AWS_REGION,
    "S3_BUCKET_NAME": S3_BUCKET_NAME}.items() if not val]
if missing:
    raise ValueError(f"Missing env vars: {', '.join(missing)}")  # fail fast

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=None,
    region_name=AWS_REGION
)
s3 = session.client("s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"))

def get_object(key: str) -> str:
    try:
        resp = s3.get_object(Bucket=S3_BUCKET_NAME, Key=key)
        body = resp["Body"].read()

        text = []
        doc = Document(io.BytesIO(body))
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except ClientError as err:
        code = err.response["Error"]["Code"]
        msg  = err.response["Error"]["Message"]
        print(f"S3 ClientError [{code}]: {msg}")
        return None

def put_object(key: str, content: str) -> None:
    try:
        if not key.endswith(".json"):
            key += ".json"
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=key, Body=content, ContentType="application/json")
    except ClientError as err:
        code = err.response["Error"]["Code"]
        msg  = err.response["Error"]["Message"]
        print(f"S3 ClientError [{code}]: {msg}")

if __name__ == "__main__":
    object_key = "cv-raw/0a0d3536-dfec-483e-8cce-3aef7ed9bad5.docx"
    content = get_object(object_key)
    if content is not None:
        print("Successfully retrieved object:")
        print(content)

    else:
        print("Failed to retrieve object.")
