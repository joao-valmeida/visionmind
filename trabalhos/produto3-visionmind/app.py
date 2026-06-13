import os
import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulating AI Tagging
AI_TAGS = ["nature", "urban", "person", "vehicle", "animal", "landscape"]

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json()
    image_url = data.get("image_url")
    
    if not image_url:
        return jsonify({"error": "No image URL"}), 400
    
    # Simulate calling an AI Vision Service
    detected_tags = random.sample(AI_TAGS, k=random.randint(2, 4))
    confidence = random.uniform(0.85, 0.99)
    
    print(f"VisionMind analyzed: {image_url}")
    
    return jsonify({
        "product": "VisionMind",
        "image_url": image_url,
        "analysis": {
            "tags": detected_tags,
            "confidence": round(confidence, 4)
        },
        "status": "completed"
    })

def lambda_handler(event, context):
    # For S3 Trigger
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"VisionMind processing file from S3: {bucket}/{key}")
    
    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
