from flask import Flask, jsonify

app = Flask(__name__)

# Define your data offers
offers = [
    {"id": 1, "data": "350MB", "price": 49, "validity": "24hrs"},
    {"id": 2, "data": "250MB", "price": 20, "validity": "24hrs"},
    {"id": 3, "data": "160MB", "price": 15, "validity": "24hrs"},
    {"id": 4, "data": "1GB", "price": 99, "validity": "24hrs"},
    {"id": 5, "data": "2GB", "price": 100, "validity": "Till midnight"},
]

# Endpoint to get the list of offers
@app.route('/offers', methods=['GET'])
def get_offers():
    return jsonify({"status": "success", "offers": offers})from flask import Flask, request
import time

app = Flask(__name__)

# Cache to prevent duplicate sending
sent_log = {}
cooldown_seconds = 30 * 60  # 30 mins

# === 🔁 Bundle Offers ===
bundle_offers = {
    50:  {"mb": 1500, "label": "1.5GB, 3hrs"},
    49:  {"mb": 350,  "label": "350MB, 7 days"},
    300: {"mb": 2500, "label": "2.5GB, 7 days"},
    700: {"mb": 6000, "label": "6GB, 7 days"},
    19:  {"mb": 1000, "label": "1GB, 1hr"},
    20:  {"mb": 250,  "label": "250MB, 24hrs"},
    99:  {"mb": 1000, "label": "1GB, 24hrs"},
    55:  {"mb": 1250, "label": "1.25GB, till midnight"},
    25:  {"mb": 1000, "label": "1GB, 1hr"},
    10:  {"mb": 70,   "label": "70MB, 24hrs"},
    991: {"mb": 2000, "label": "2GB, 24hrs"},
    501: {"mb": 300,  "label": "300MB, 24hrs"}
}

# === ✅ Test Root Route ===
@app.route('/')
def home():
    return "✅ Flask app is running."

# === 📥 C2B Confirmation Endpoint ===
@app.route('/confirmation', methods=['POST'])
def confirmation():
    data = request.get_json()
    phone = data.get('MSISDN')
    amount = int(float(data.get('TransAmount', 0)))
    current_time = time.time()

    # Special logic if two bundles have same price
    if amount == 99:
        offer = bundle_offers[991]
    elif amount == 50:
        offer = bundle_offers[501]
    else:
        offer = bundle_offers.get(amount)

    if offer:
        last_time = sent_log.get(phone, 0)
        if current_time - last_time >= cooldown_seconds:
            sent_log[phone] = current_time
            try:
                with open("send_bundle.txt", "w") as f:
                    f.write(f"{phone},{offer['mb']},{offer['label']}")
                print(f"✔ Sent {offer['label']} to {phone}")
            except Exception as e:
                print("❌ Error writing file:", e)
        else:
            print(f"⏳ Skipped {phone} (recently sent).")
    else:
        print(f"❌ No bundle match for KES {amount}")

    return {"ResultCode": 0, "ResultDesc": "Accepted"}from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "M-PESA API is live"

@app.route('/confirmation', methods=['POST'])
def confirmation():
    data = request.json
    print("Confirmation received:", data)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}

@app.route('/validation', methods=['POST'])
def validation():
    data = request.json
    print("Validation received:", data)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}

if __name__ == '__main__':
    app.run()
