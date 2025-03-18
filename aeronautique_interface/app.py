import streamlit as st 
import requests


# Titre
st.title("Détection d'anomalies - Données Aronautiques ✈️")

st.markdown("**Entrez les données de vol pour analyser une anomalie :**")

# Formulaire du saisie
statut = st.selectbox("Statut du vol :", options=["scheduled", "active", "landed", "canceled", "incident", "diverted"])
retard_depart = st.number_input("Retard au départ (min)", min_value=0, value=0)
retard_arrivee = st.number_input("Retard à l'arrivée (min)", min_value=0, value=0)

# convertir statut en code numérique
statut_map = {
    "scheduled": 0,
    "active": 1,
    "landed": 2,
    "cancelled": 3,
    "incident": 4,
    "diverted": 5 
}

statut_code = statut_map[statut]

if st.button("Analyser le vol"):
    with st.spinner("Analyse en cours..."):
        try:

            # Appel à ton API Railway
            url = "https://fastapi-aeronautique-production.up.railway.app/detect_anomaly/"
            params = {
                "statut": statut_code,
                "retard_depart": retard_depart,
                "retard_arrivee": retard_arrivee
            }
            response = requests.post(url, json=params)
            data = response.json()

            # Resultat
            if data["anomaly_final"] == -1:
                st.error("⚠️ Anomalie détectée sur ce vol !")
                st.json(data)
            else:
                st.success("✅ Aucun comportement anormal détecté.")
                st.json(data)
            
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API: {e}")