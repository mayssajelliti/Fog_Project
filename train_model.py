from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

# Créer des données factices : [nombre de ports, durée en secondes]
normal = np.random.uniform([1, 0.1], [5, 3], size=(200, 2))
anomalies = np.random.uniform([8, 0.5], [30, 5], size=(40, 2))
X = np.vstack([normal, anomalies])

# Entraîner le modèle
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X)

# Sauvegarder
joblib.dump(model, 'isolation_forest_model.pkl')
print("✅ Modèle IA créé et sauvegardé !")
