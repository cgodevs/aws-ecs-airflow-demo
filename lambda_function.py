import boto3
import os
import zipfile
import io

# AWS Clients
s3 = boto3.client('s3')

# Define where EFS is mounted inside Lambda
EFS_MOUNT_PATH = "/mnt/artifacts"


def get_latest_s3_file(bucket_name):
    """Get the latest uploaded file from the S3 bucket"""
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return None

    # Sort files by LastModified timestamp
    sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)

    # Return the latest file
    return sorted_files[0]['Key']


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    # Get the latest file from S3
    latest_file_key = get_latest_s3_file(bucket_name)
    if not latest_file_key:
        print("No files found in S3 bucket.")
        return

    print(f"Processing latest file: {latest_file_key}")

    # Download the ZIP file
    s3_object = s3.get_object(Bucket=bucket_name, Key=latest_file_key)
    zip_content = io.BytesIO(s3_object['Body'].read())

    # Extract the contents to EFS
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        zip_ref.extractall(EFS_MOUNT_PATH)

    print(f"Extracted {latest_file_key} to {EFS_MOUNT_PATH}")

    return {
        'statusCode': 200,
        'body': f"Successfully processed {latest_file_key}"
    }
