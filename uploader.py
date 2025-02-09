import boto3
import requests
import os
from ftplib import FTP

def download_iso(url, filename):
    """Download an ISO file from a given URL and save it with a specified filename."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print("Failed to download ISO")

def upload_to_s3(file_path, bucket_name, object_name, access_key, secret_key, endpoint_url):
    """Upload a file to S3-compatible storage."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url
    )
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to {bucket_name}/{object_name}")
    except Exception as e:
        print("Upload failed:", str(e))

def upload_to_ftp(file_path, ftp_host, ftp_user, ftp_pass, ftp_dir):
    """Upload a file to an FTP server."""
    try:
        with FTP(ftp_host) as ftp:
            ftp.login(user=ftp_user, passwd=ftp_pass)
            ftp.cwd(ftp_dir)
            with open(file_path, 'rb') as f:
                ftp.storbinary(f'STOR {os.path.basename(file_path)}', f)
            print(f"Uploaded {file_path} to FTP server {ftp_host}/{ftp_dir}")
    except Exception as e:
        print("FTP upload failed:", str(e))

# User-defined parameters
ISO_URL = "https://example.com/sample.extention"  # Replace with actual URL
NEW_FILENAME = "renamed_file.extention"
BUCKET_NAME = "your-bucket-name"  # Replace with actual bucket name
S3_OBJECT_NAME = "uploaded_file.extention"
ACCESS_KEY = "<ACCESS_KEY>"
SECRET_KEY = "<SECRET_KEY>"
ENDPOINT_URL = "https://s3.link"

FTP_HOST = "ftp.example.com"  # Replace with actual FTP host
FTP_USER = "ftp_user"  # Replace with actual FTP username
FTP_PASS = "ftp_password"  # Replace with actual FTP password
FTP_DIR = "/upload"  # Replace with actual FTP directory

# Download the ISO file
download_iso(ISO_URL, NEW_FILENAME)

# Upload to S3-compatible storage
upload_to_s3(NEW_FILENAME, BUCKET_NAME, S3_OBJECT_NAME, ACCESS_KEY, SECRET_KEY, ENDPOINT_URL)

# Upload to FTP server
upload_to_ftp(NEW_FILENAME, FTP_HOST, FTP_USER, FTP_PASS, FTP_DIR)

# Cleanup (optional)
os.remove(NEW_FILENAME)
