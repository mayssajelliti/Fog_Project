# fog-server.py
from flask import Flask, request, jsonify
import joblib
from datetime import datetime
import os

app = Flask(__name__)

# Charger le modèle (crée-le si absent)
MODEL_PATH = "isolation_forest_model.pkl"
if not os.path.exists(MODEL_PATH):
    print(" Modèle absent. Exécute train_model.py d'abord.")
    exit(1)

model = joblib.load(MODEL_PATH)
ALERT_THRESHOLD = 0.0

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    src_ip = data['src_ip']
    ports = data['unique_ports']
    duration = data['duration']
    
    score = model.decision_function([[ports, duration]])[0]
    is_anomaly = bool(score < ALERT_THRESHOLD)
    
    if is_anomaly:
        print(f"\n FOG ALERT [{datetime.now().strftime('%H:%M:%S')}]")
        print(f"   Source: {src_ip} | Ports: {ports} | Durée: {duration:.2f}s\n")
    
    return jsonify({"alert": is_anomaly})

if __name__ == "__main__":
    print(" Nœud Fog (Windows) démarré sur http://localhost:5001")
    app.run(host='127.0.0.1', port=5001, threaded=True)  # ← changé à 5001