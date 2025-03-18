# fastapi-aeronautique
# ✈️ Détection d'Anomalies dans des Données Aéronautiques

Ce projet détecte les **anomalies dans les vols aériens** à partir de données telles que les retards et le statut du vol. Il utilise **Machine Learning (Isolation Forest & DBSCAN)** et propose une interface web pour l’analyse.

---

## 📦 Technologies utilisées
- **Backend** : FastAPI, Scikit-learn, Pandas, NumPy
- **Frontend** : Streamlit, Requests, Matplotlib
- **Déploiement** : Railway (API), Streamlit Cloud (Interface)

---

## 🚀 Fonctionnalités
- Détection automatique d’anomalies sur les vols
- Sauvegarde des anomalies détectées dans un fichier CSV
- Visualisation des anomalies sous forme de graphiques
- Téléchargement de l’historique


## 📡 Backend - FastAPI (Détection d'anomalies)

### ▶️ Fonctionnement :
1. Charge les données de vols.
2. Entraîne deux modèles ML :
   - Isolation Forest
   - DBSCAN
3. Fournit un endpoint POST `/detect_anomaly/` :
   - Reçoit : statut, retard_depart, retard_arrivee
   - Retourne : détection avec chaque modèle + résultat final

### Exemple d'appel (JSON) :
 Variables envoyées (JSON en entrée)
L’API attend trois variables envoyées au format JSON dans le corps de la requête :

statut : un entier représentant l’état du vol. Les valeurs possibles sont :

0 → vol prévu (scheduled)
1 → vol en cours (active)
2 → vol atterri (landed)
-1 → vol annulé (cancelled)
retard_depart : un entier indiquant le retard au départ du vol en minutes.

retard_arrivee : un entier représentant le retard à l’arrivée du vol en minutes. Cette valeur peut être 0 si le retard à l’arrivée n’est pas encore connu.


```json
POST /detect_anomaly/
{
  "statut": 1,
  "retard_depart": 50,
  "retard_arrivee": 20
}

Reponse attendu


📤 Variables retournées (JSON en sortie)
L’API retourne les mêmes données reçues, accompagnées de trois résultats de détection d’anomalies :

anomaly_isolation_forest : un entier indiquant le résultat du modèle Isolation Forest :

-1 → anomalie détectée
1 → vol considéré comme normal
anomaly_dbscan : un entier indiquant le résultat du modèle DBSCAN :

-1 → anomalie détectée
1 ou autre → vol considéré comme normal
anomaly_final : un entier représentant le verdict global :

-1 → anomalie confirmée par les deux modèles
1 → vol considéré comme normal

{
  "statut": 1,
  "retard_depart": 50,
  "retard_arrivee": 20,
  "anomaly_isolation_forest": -1,
  "anomaly_dbscan": -1,
  "anomaly_final": -1
}


Backend FastAPI :

cd app
pip install -r requirements.txt
uvicorn api:app --reload

Frontend Streamlit :

cd interface
pip install -r requirements.txt
streamlit run app.py

Déploiement
API FastAPI : Déployée sur Railway url=https://fastapi-aeronautique-production.up.railway.app/detect_anomaly/
Interface Streamlit : Déployée sur Streamlit Cloud url=https://fastapi-aeronautique-adwsd8ck7sk5r7ptypnpgt.streamlit.app/

📥 Données utilisées
Fichier : vols_grand_dataset.csv
Colonnes clés : Statut, Retard_Depart, Retard_Arrivee


✨ Auteur
Ahmed Sekou Diane


