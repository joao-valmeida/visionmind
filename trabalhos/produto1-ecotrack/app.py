import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fictional emission factors (kg CO2 per unit)
EMISSION_FACTORS = {
    "flight_km": 0.115,
    "electricity_kwh": 0.475,
    "car_km": 0.170
}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    activity = data.get("activity")
    amount = data.get("amount", 0)
    
    factor = EMISSION_FACTORS.get(activity)
    if not factor:
        return jsonify({"error": f"Activity '{activity}' not supported"}), 400
    
    result = amount * factor
    
    # In a real app, we would save this to a database here
    # db.save({"activity": activity, "amount": amount, "co2": result})
    
    return jsonify({
        "product": "EcoTrack",
        "activity": activity,
        "amount": amount,
        "co2_kg": round(result, 2),
        "status": "success"
    })

# Handler for AWS Lambda (using mangum or similar is common, but here's a direct logic)
def lambda_handler(event, context):
    # Simplified logic for demonstration
    body = json.loads(event.get('body', '{}'))
    activity = body.get("activity")
    amount = body.get("amount", 0)
    factor = EMISSION_FACTORS.get(activity, 0)
    result = amount * factor
    return {
        "statusCode": 200,
        "body": json.dumps({"co2_kg": round(result, 2)})
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
