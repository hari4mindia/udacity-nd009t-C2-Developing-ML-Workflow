import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the S3 bucket and key from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the data from S3 to /tmp/image.png
    download_path = '/tmp/image.png'
    s3.download_file(bucket, key, download_path)

    # Read and encode the image in base64
    with open(download_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Return the updated event structure for the next step
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }