import os, io
from minio import Minio
from minio.error import S3Error

ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
BUCKET = os.getenv("MINIO_BUCKET", "lexisumm")

client = Minio(ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

def ensure_bucket():
    found = client.bucket_exists(BUCKET)
    if not found:
        client.make_bucket(BUCKET)

def store_file(key: str, content: bytes):
    ensure_bucket()
    data = io.BytesIO(content)
    client.put_object(BUCKET, key, data, length=len(content), content_type="application/octet-stream")

def get_file(key: str) -> bytes:
    resp = client.get_object(BUCKET, key)
    return resp.read()
