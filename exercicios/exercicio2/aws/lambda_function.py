import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")
    
    # EventBridge event from S3 typically has 'detail' field
    detail = event.get('detail', {})
    bucket_name = detail.get('bucket', {}).get('name')
    object_key = detail.get('object', {}).get('key')
    
    logger.info(f"File uploaded! Bucket: {bucket_name}, Key: {object_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Event processed'})
    }
