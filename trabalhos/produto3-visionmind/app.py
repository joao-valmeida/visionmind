import os
import time
from urllib.parse import unquote_plus
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

rekognition_client = boto3.client('rekognition')
dynamodb_resource = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ImageMetadata')
table = dynamodb_resource.Table(TABLE_NAME)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

def analyze_and_store(bucket, key):
    _, ext = os.path.splitext(key.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {ext}")

    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MaxLabels=10,
        MinConfidence=75.0
    )

    labels = [
        {'Name': label['Name'], 'Confidence': str(round(label['Confidence'], 2))}
        for label in response.get('Labels', [])
    ]

    item = {
        'imageId': key,
        'bucket': bucket,
        'uploadTimestamp': int(time.time()),
        'tags': labels
    }

    table.put_item(Item=item)
    return item

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json(silent=True) or {}
    bucket = data.get("bucket")
    key = data.get("key")

    if not bucket or not key:
        return jsonify({"error": "Missing bucket or key parameters"}), 400

    try:
        result = analyze_and_store(bucket, key)
        return jsonify({
            "product": "VisionMind",
            "analysis": result,
            "status": "completed"
        }), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as err:
        return jsonify({"error": "Internal server error", "details": str(err)}), 500

def lambda_handler(event, context):
    results = []
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        res = analyze_and_store(bucket, key)
        results.append(res)

    return {
        "statusCode": 200,
        "body": results
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))