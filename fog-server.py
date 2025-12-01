# fog-server.py
from flask import Flask, request, jsonify
import joblib
from datetime import datetime
import os

app = Flask(__name__)

# Vérifie que le modèle existe
MODEL_PATH = "isolation_forest_model.pkl"
if not os.path.exists(MODEL_PATH):
    print(" Modèle introuvable. Exécute train_model.py d'abord.")
    exit(1)

model = joblib.load(MODEL_PATH)
ALERT_THRESHOLD = 0.0  # Ajuste pour plus/moins de sensibilité

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    src_ip = data['src_ip']
    unique_ports = data['unique_ports']
    duration = data['duration']
    
    # Prédire avec le modèle
    score = model.decision_function([[unique_ports, duration]])[0]
    is_anomaly = bool(score < ALERT_THRESHOLD)
    
    # Afficher l'alerte locale
    if is_anomaly:
        print(f"\n FOG ALERT [{datetime.now().strftime('%H:%M:%S')}]")
        print(f"   Source: {src_ip} | Ports: {unique_ports} | Durée: {duration:.2f}s\n")
    
    return jsonify({"alert": is_anomaly})

if __name__ == "__main__":
    print(" Nœud Fog démarré sur http://localhost:5000")
    app.run(host='127.0.0.1', port=5000, threaded=True)