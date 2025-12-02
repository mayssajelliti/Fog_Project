# train_model.py
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

normal = np.random.uniform([1, 0.1], [5, 3], size=(200, 2))
anomalies = np.random.uniform([10, 0.2], [40, 4], size=(50, 2))
X = np.vstack([normal, anomalies])

model = IsolationForest(contamination=0.25, random_state=42)
model.fit(X)

joblib.dump(model, 'isolation_forest_model.pkl')
print(" Modèle IA sauvegardé")