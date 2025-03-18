from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Initialisation de l'API
app = FastAPI()

# Modèle d'entrée JSON
class FlightData(BaseModel):
    statut: int
    retard_depart: int
    retard_arrivee: int

# Chargement des données
df = pd.read_csv("vols_grand_dataset.csv")

# Nettoyage des données
df_clean = df.dropna(subset=["Retard_Depart"]).copy()
df_clean["Retard_Arrivee"] = df_clean["Retard_Arrivee"].fillna(0)

df_clean["Retard_Depart"] = df_clean["Retard_Depart"].astype(int)
df_clean["Retard_Arrivee"] = df_clean["Retard_Arrivee"].astype(int)

# Conversion des statuts
df_clean["Statut"] = df_clean["Statut"].map({
    "scheduled": 0, "active": 1, "landed": 2, "cancelled": -1
}).fillna(0).astype(int)

# Données pour l'entraînement
df_ml = df_clean[["Statut", "Retard_Depart", "Retard_Arrivee"]]

# Modèle Isolation Forest
model_iso = IsolationForest(contamination=0.05, random_state=42)
model_iso.fit(df_ml)

# Standardisation + DBSCAN
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_ml)
model_dbscan = DBSCAN(eps=2, min_samples=3).fit(df_scaled)

# Endpoint API
@app.post("/detect_anomaly/")
async def detect_anomaly(data: FlightData):
    """Analyse un vol et détecte s'il est suspect ou non."""
    
    # Créer DataFrame avec noms de colonnes pour éviter les warnings
    data_df = pd.DataFrame([[data.statut, data.retard_depart, data.retard_arrivee]], 
                           columns=["Statut", "Retard_Depart", "Retard_Arrivee"])

    # Prédiction Isolation Forest
    anomaly_iso = int(model_iso.predict(data_df)[0])

    # Standardisation + Prédiction DBSCAN
    data_scaled = scaler.transform(data_df)
    anomaly_dbscan = int(model_dbscan.fit_predict(data_scaled)[0])

    # Anomalie finale : -1 = suspect, 1 = normal
    anomaly_final = int(-1 if (anomaly_iso == -1 and anomaly_dbscan == -1) else 1)

    return {
        "statut": int(data.statut),
        "retard_depart": int(data.retard_depart),
        "retard_arrivee": int(data.retard_arrivee),
        "anomaly_isolation_forest": anomaly_iso,
        "anomaly_dbscan": anomaly_dbscan,
        "anomaly_final": anomaly_final
    }
