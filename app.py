from flask import Flask, request

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