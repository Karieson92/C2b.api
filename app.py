from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# 🟢 Updated bundle offers to match payment amounts
offers = [
    {"id": 1, "data": "350MB", "price": 49, "validity": "24hrs"},
    {"id": 2, "data": "250MB", "price": 20, "validity": "24hrs"},
    {"id": 3, "data": "160MB", "price": 15, "validity": "24hrs"},
    {"id": 4, "data": "1GB", "price": 99, "validity": "24hrs"},
    {"id": 5, "data": "2GB", "price": 100, "validity": "Till midnight"},
]

@app.route('/')
def home():
    return "✅ Welcome to the M-PESA Bundle API!"

# Endpoint to view available bundle offers
@app.route('/offers', methods=['GET'])
def get_offers():
    return jsonify({"status": "success", "offers": offers})

# Endpoint to receive confirmation from M-PESA
@app.route('/c2b/confirmation', methods=['POST'])
def c2b_confirmation():
    data = request.get_json()

    trans_id = data.get("TransID")
    trans_amount = float(data.get("TransAmount", 0))
    phone = data.get("MSISDN")
    time = data.get("TransTime")

    # 🔍 Match the amount paid with the correct bundle offer
    matched_offer = next((offer for offer in offers if offer["price"] == int(trans_amount)), None)

    if matched_offer:
        # 💡 Here you would integrate bundle sending via USSD/API
        print(f"[{datetime.datetime.now()}] ✅ Match found! {phone} bought {matched_offer['data']} for KES {trans_amount}")

        response_message = f"Bundle matched: {matched_offer['data']} ({matched_offer['validity']}) sent to {phone}"
    else:
        print(f"[{datetime.datetime.now()}] ❌ No bundle found for KES {trans_amount} from {phone}")
        response_message = f"No matching bundle for KES {trans_amount}. Please follow up."

    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted", "Message": response_message})

# Optional: Validation route (used by Daraja if enabled)
@app.route('/c2b/validation', methods=['POST'])
def c2b_validation():
    return jsonify({"ResultCode": 0, "ResultDesc": "Validation passed successfully"})

# Health check
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"msg": "App is working!"})