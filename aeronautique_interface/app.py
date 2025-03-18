import streamlit as st
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt

st.title("Détection d'anomalies - Données Aéronautiques ✈️")

st.markdown("**Entrez les données de vol pour analyser une anomalie :**")

# Saisie utilisateur
statut = st.selectbox("Statut du vol :", options=["scheduled", "active", "landed", "cancelled"])
retard_depart = st.number_input("Retard au départ (min)", min_value=0, value=0)
retard_arrivee = st.number_input("Retard à l'arrivée (min)", min_value=0, value=0)

statut_map = {"scheduled": 0, "active": 1, "landed": 2, "cancelled": -1}
statut_code = statut_map[statut]

# Dossier CSV
csv_file = "historique_anomalies.csv"

if st.button("Analyser le vol"):
    with st.spinner("Analyse en cours..."):
        try:
            url = "https://fastapi-aeronautique-production.up.railway.app/detect_anomaly/"
            payload = {
                "statut": statut_code,
                "retard_depart": retard_depart,
                "retard_arrivee": retard_arrivee
            }
            response = requests.post(url, json=payload)
            data = response.json()

            if data["anomaly_final"] == -1:
                st.error("⚠️ Anomalie détectée sur ce vol !")
            else:
                st.success("✅ Aucun comportement anormal détecté.")
            st.json(data)

            # Sauvegarde CSV si anomalie
            if data["anomaly_final"] == -1:
                df_new = pd.DataFrame([data])
                if os.path.exists(csv_file):
                    df_new.to_csv(csv_file, mode='a', index=False, header=False)
                else:
                    df_new.to_csv(csv_file, index=False)
                st.info("📁 Anomalie sauvegardée dans l'historique.")

        except Exception as e:
            st.error(f"Erreur API : {e}")

# Afficher l'historique
st.markdown("---")
st.subheader("📊 Historique des vols suspects détectés")
if os.path.exists(csv_file):
    df_hist = pd.read_csv(csv_file)
    st.dataframe(df_hist)
    st.download_button("📥 Télécharger le CSV", data=df_hist.to_csv(index=False), file_name="anomalies.csv")
else:
    st.info("Aucune anomalie détectée pour le moment.")







st.markdown("---")
st.subheader("📈 Analyse graphique des anomalies")

if os.path.exists(csv_file):
    fig, ax = plt.subplots()
    df_hist["retard_depart"].plot(kind='hist', bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title("Distribution des Retards au Départ (Vols suspects)")
    ax.set_xlabel("Minutes")
    st.pyplot(fig)
else:
    st.info("Graphique indisponible - pas encore d'anomalies.")
