#  Fog Computing – Surveillance Réseau Universitaire

Détection d’anomalies réseau (ex: scans de ports) en **fog computing**.

- **Nœud Fog** : Ubuntu (`192.168.1.136`) – analyse locale avec IA.
- **Client** : Windows/WSL2 (`192.168.1.130`) – simule un étudiant.

## Démarrage

### Sur le nœud Fog ()
```bash
pip3 install flask scikit-learn joblib
python3 train_model.py
python3 fog-server.py
