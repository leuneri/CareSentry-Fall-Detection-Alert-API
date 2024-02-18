from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def detect_fall():
    # Simulate fall detection processing here
    # For now, we just return a mock response
    return jsonify({"fall_detected": True, "message": "Fall detected in the received frame"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
