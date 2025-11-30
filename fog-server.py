from flask import Flask, request, Response
import joblib
from datetime import datetime
import json
import os  # Optional: for safety

app = Flask(__name__)

# --- LOAD MODEL HERE ---
MODEL_PATH = 'isolation_forest_model.pkl'  # <-- CHANGE IF NEEDED
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print(f"✅ Model loaded from {MODEL_PATH}")

ALERT_THRESHOLD = -0.1

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    if not data:
        return Response(json.dumps({"error": "No JSON received"}), status=400, mimetype='application/json')
    
    src_ip = data.get('src_ip')
    ports = data.get('unique_ports')
    duration = data.get('duration')

    if ports is None or duration is None:
        return Response(json.dumps({"error": "Missing 'unique_ports' or 'duration'"}), status=400, mimetype='application/json')

    # Get anomaly score
    score_array = model.decision_function([[ports, duration]])[0]
    score = float(score_array)
    is_anomaly = bool(score < ALERT_THRESHOLD)

    if is_anomaly:
        print(f"\n🚨 FOG ALERT [{datetime.now().strftime('%H:%M:%S')}]")
        print(f" Source: {src_ip} | Ports: {ports} | Durée: {duration:.2f}s\n")

    response_data = {"alert": is_anomaly, "score": score}
    return Response(json.dumps(response_data), mimetype='application/json')

if __name__ == "__main__":
    print("📡 Nœud Fog démarré sur http://192.168.1.136:5000")
    app.run(host='0.0.0.0', port=5000)