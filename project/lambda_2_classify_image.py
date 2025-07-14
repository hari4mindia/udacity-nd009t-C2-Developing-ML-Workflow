import json
import base64
import boto3

ENDPOINT = "image-classification-2025-07-11-13-02-32-743"
runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    """Invoke the SageMaker endpoint with base64 image data"""

    # ✅ Safe fallback whether 'body' exists or not
    body = event.get("body", event)
    if isinstance(body, str):
        body = json.loads(body)

    # Decode image and invoke SageMaker
    image_data = base64.b64decode(body["image_data"])
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType="image/png",
        Body=image_data
    )

    # Append inference results
    inferences = json.loads(response['Body'].read().decode('utf-8'))
    body["inferences"] = inferences

    return {
        "statusCode": 200,
        "body": body
    }
