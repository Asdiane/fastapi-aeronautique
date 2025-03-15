from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Initialisation de l'API
app = FastAPI()

# Définition du modèle d'entrée (JSON)
class FlightData(BaseModel):
    statut: int
    retard_depart: int
    retard_arrivee: int

# Chargement et Préparation des Données
df = pd.read_csv("../vols_grand_dataset.csv")

# Nettoyage
df_clean = df.dropna(subset=["Retard_Depart"]).copy()
df_clean["Retard_Arrivee"] = df_clean["Retard_Arrivee"].fillna(0)

df_clean["Retard_Depart"] = df_clean["Retard_Depart"].astype(int)
df_clean["Retard_Arrivee"] = df_clean["Retard_Arrivee"].astype(int)

# Conversion des statuts en nombres
df_clean["Statut"] = df_clean["Statut"].map({
    "scheduled": 0, "active": 1, "landed": 2, "cancelled": -1
}).fillna(0).astype(int)

# Sélection des variables pour l'entraînement
df_ml = df_clean[["Statut", "Retard_Depart", "Retard_Arrivee"]]

# Entraînement des Modèles
model_iso = IsolationForest(contamination=0.05, random_state=42)
model_iso.fit(df_ml)

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_ml)
model_dbscan = DBSCAN(eps=2, min_samples=3).fit(df_scaled)

# Endpoint pour détecter les anomalies
@app.post("/detect_anomaly/")
async def detect_anomaly(data: FlightData):
    """Analyse un vol et détecte s'il est suspect ou non."""
    data_np = np.array([[data.statut, data.retard_depart, data.retard_arrivee]])

    # Prédiction avec Isolation Forest
    anomaly_iso = int(model_iso.predict(data_np)[0])  # Convertir numpy.int en int standard

    # Prédiction avec DBSCAN
    data_scaled = scaler.transform(data_np)
    anomaly_dbscan = int(model_dbscan.fit_predict(data_scaled)[0])  # Convertir numpy.int en int standard

    # Déterminer si c'est une anomalie finale
    anomaly_final = int(-1 if (anomaly_iso == -1 and anomaly_dbscan == -1) else 1)

    return {
        "statut": int(data.statut),
        "retard_depart": int(data.retard_depart),
        "retard_arrivee": int(data.retard_arrivee),
        "anomaly_isolation_forest": anomaly_iso,
        "anomaly_dbscan": anomaly_dbscan,
        "anomaly_final": anomaly_final
    }

