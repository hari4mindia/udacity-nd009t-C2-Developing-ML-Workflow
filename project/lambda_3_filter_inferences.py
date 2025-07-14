import json

THRESHOLD = 0.93

def lambda_handler(event, context):
    """Check if inference confidence exceeds threshold"""

    # Safely unpack 'body' key if it exists
    body = event.get("body", event)
    if isinstance(body, str):
        body = json.loads(body)

    # Get inference scores
    inferences = body["inferences"]

    # Check if any exceed the threshold
    if any(score > THRESHOLD for score in inferences):
        return {
            'statusCode': 200,
            'body': body  # Return plain dict for Step Function chaining
        }
    else:
        raise ValueError("THRESHOLD_CONFIDENCE_NOT_MET")
