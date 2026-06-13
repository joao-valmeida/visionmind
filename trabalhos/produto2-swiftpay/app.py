import os
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/payment', methods=['POST'])
def payment_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    
    transaction_id = data.get("transaction_id")
    status = data.get("status")
    
    print(f"Processing payment {transaction_id} with status {status}")
    
    # Simulate processing delay
    time.sleep(0.5)
    
    # Logic to send notification or update DB
    # notify_user(transaction_id, status)
    
    return jsonify({
        "product": "SwiftPay",
        "processed_at": time.time(),
        "transaction_id": transaction_id,
        "status": "acknowledged"
    }), 202

def lambda_handler(event, context):
    # For SQS trigger
    for record in event.get('Records', []):
        body = json.loads(record['body'])
        print(f"SwiftPay processing SQS message: {body}")
    
    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
