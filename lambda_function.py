import boto3
import os
import zipfile
import io

# AWS Clients
s3 = boto3.client('s3')

# Define constants
EFS_MOUNT_PATH = "/mnt/artifacts"
DEFAULT_BUCKET_NAME = "main-branch-airflow-ecs-demo-copies"
DEFAULT_FILE_NAME = DEFAULT_BUCKET_NAME + "/aws-ecs-airflow-demo.zip"


def get_latest_s3_file(bucket_name):
    """Get the latest uploaded file from the S3 bucket"""
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        return None

    # Sort files by LastModified timestamp
    sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)

    # Return the latest file
    return sorted_files[0]['Key']


def download_s3_file(bucket_name, object_key):
    try:
        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        s3_object = s3.get_object(Bucket=bucket_name, Key=object_key)
        zip_content = io.BytesIO(s3_object['Body'].read())
        return zip_content
    except Exception as e:
        raise Exception({'statusCode': 500, 'body': f"Error downloading {object_key} from S3.", 'error': str(e)})


def extract_to_efs(zip: io.BytesIO):
    try:
        with zipfile.ZipFile(zip, 'r') as zip_ref:
            zip_ref.extractall(EFS_MOUNT_PATH)
        print(f"Extracted object to {EFS_MOUNT_PATH}")
    except Exception as e:
        raise Exception({'statusCode': 500, 'body': f"Error extracting object.", 'error': str(e)})


def lambda_handler(event, context):
    # Try to extract bucket and object key from event
    bucket_name = event.get('Records', [{}])[0].get('s3', {}).get('bucket', {}).get('name', DEFAULT_BUCKET_NAME)
    object_key = event.get('Records', [{}])[0].get('s3', {}).get('object', {}).get('key')

    # If no object key is provided (manual trigger), get the latest file
    if not object_key:
        print("No specific file in event. Fetching the latest file from S3...")
        object_key = get_latest_s3_file(bucket_name) or DEFAULT_FILE_NAME
        print(f"Latest file in S3: {object_key}")
        if not object_key:
            print("No files found to process.")
            return {'statusCode': 404, 'body': "No files available in S3."}

    zip_content = download_s3_file(bucket_name, object_key)
    extract_to_efs(zip_content)
    return {
        'statusCode': 200,
        'body': f"Successfully processed {object_key}"
    }
