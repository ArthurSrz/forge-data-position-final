"""
Admin Interface - La Forge à Data Position
For data team leads to create and manage Data Positions
"""

import sys
sys.path.insert(0, '..')

import pandas as pd
import streamlit as st
from streamlit_elements import nivo, elements, mui
from grist_api import GristDocAPI
import requests
import numpy as np
from styles import inject_styles

# Page configuration
st.set_page_config(
    page_title="Admin - Forge Data Position",
    page_icon="⚙️",
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Inject custom styles
inject_styles()

# Banner - large logo centered
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.image("resource/logo_forge.png", use_container_width=True)

# Load secrets
SERVER = st.secrets["grist"]["server"]
DOC_ID = st.secrets["grist"]["doc_id"]
API_KEY = st.secrets["grist"]["api_key"]
subdomain = st.secrets["grist"]["subdomain"]

api = GristDocAPI(DOC_ID, server=SERVER, api_key=API_KEY)
headers = {"Authorization": f"Bearer {API_KEY}"}


def load_grist_table(table_name):
    """Load a table from Grist with error handling."""
    url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/{table_name}/records"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Ensure records key exists
            if 'records' not in data:
                return {"records": []}, None
            return data, None
        return {"records": []}, f"Erreur {response.status_code}"
    except Exception as e:
        return {"records": []}, str(e)


# Load data
data2, _ = load_grist_table("Form2")  # Master questions
data3, _ = load_grist_table("Form3")  # Responses
data0, _ = load_grist_table("Form0")  # Custom questions

# Session state
if 'selected_data' not in st.session_state:
    st.session_state.selected_data = {}
if 'profiles' not in st.session_state:
    st.session_state.profiles = []

# Tabs
tab1, tab2 = st.tabs(["📋 Qualification", "📊 Position"])

# =============================================================================
# TAB 1: QUALIFICATION
# =============================================================================
with tab1:
    st.title("Créer votre Data Position")

    # Explanatory section
    with st.expander("ℹ️ Qu'est-ce qu'un Data Position ?", expanded=True):
        st.markdown("""
        ### Un **Data Position** est un référentiel de compétences data

        Il permet de :
        - **Définir les profils data** dont votre équipe a besoin (Data Analyst, Data Scientist, etc.)
        - **Évaluer les compétences** de vos collaborateurs via un questionnaire
        - **Visualiser la répartition** des expertises dans votre équipe

        **Comment ça marche ?**
        1. **Choisissez un Data Position** existant ou créez le vôtre
        2. **Partagez le lien du questionnaire** avec vos collaborateurs
        3. **Analysez les résultats** dans l'onglet Position
        """)

    st.divider()

    st.header("Utiliser un Data Position existant")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("Data Position Maître")
            st.caption("Le référentiel par défaut créé par Datactivist")

            # Get available profiles from Grist
            available_profiles = ["Data Analyst", "Data Scientist", "Machine Learning Engineer",
                                  "Geomaticien", "Data Engineer", "Data Protection Officer",
                                  "Chef de Projet Data"]

            profiles = st.multiselect(
                "Profils à évaluer",
                available_profiles,
                default=available_profiles,
                key="master_profiles"
            )

            if st.button("Charger ce Data Position", type="primary", key="load_master"):
                st.session_state.profiles = profiles
                st.session_state.selected_data = data2
                st.session_state.table_id = "Form3"
                st.success("Data Position chargé ! Partagez maintenant le lien Questionnaire avec vos collaborateurs.")

    with col2:
        with st.container(border=True):
            st.subheader("Data Position Hackathon")
            st.caption("Pour organiser les équipes d'un hackathon")
            st.button("Charger ce Data Position", type="primary", key="load_hackathon", disabled=True)
            st.info("Bientôt disponible")

    with col3:
        with st.container(border=True):
            st.subheader("Créer un nouveau")
            st.caption("Personnalisez vos propres questions")
            st.button("Créer", type="primary", key="create_new", disabled=True)
            st.info("Bientôt disponible")

    st.divider()

    # Show current selection
    if st.session_state.get('profiles'):
        st.success(f"**Data Position actif** : {len(st.session_state.profiles)} profil(s) sélectionné(s)")
        st.write("Profils :", ", ".join(st.session_state.profiles))

        # Generate questionnaire link
        st.info("**Lien à partager avec vos collaborateurs** : Ouvrez l'onglet 'Questionnaire' dans le menu latéral")

# =============================================================================
# TAB 2: POSITION (Radar Chart)
# =============================================================================
with tab2:
    st.title("Position de votre équipe")

    if 'table_id' not in st.session_state:
        st.warning("Veuillez d'abord charger un Data Position dans l'onglet Qualification")
    else:
        # Load responses
        table_id = st.session_state.table_id
        url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/{table_id}/records"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            st.error(f"Erreur lors du chargement : {response.status_code}")
        else:
            data = response.json()
            if not data.get('records'):
                st.info("Aucune réponse pour le moment. Partagez le questionnaire avec vos collaborateurs.")
            else:
                records = data['records']
                form_data = pd.json_normalize(records, sep='_')
                form_data.columns = [col.replace('fields_', '') for col in form_data.columns]

                # Filter by selected profiles if any
                if st.session_state.get('profiles'):
                    form_data = form_data[form_data['profile_type'].isin(st.session_state.profiles)]

                if form_data.empty:
                    st.info("Aucune donnée pour les profils sélectionnés.")
                else:
                    st.markdown("### Radar de compétences")
                    st.caption("Visualisez la distribution des profils data de votre équipe")

                    # Build radar data
                    unique_noms = form_data['nom'].unique()
                    unique_noms = [n for n in unique_noms if n]  # Remove empty names

                    if not unique_noms:
                        st.info("Aucun participant identifié dans les réponses.")
                    else:
                        DATA = []
                        for profile_type in form_data['profile_type'].unique():
                            if not profile_type:
                                continue
                            profile_data = {"profile": profile_type}
                            for nom in unique_noms:
                                filtered = form_data[(form_data['nom'] == nom) & (form_data['profile_type'] == profile_type)]
                                if not filtered.empty:
                                    score = filtered['score'].mean() if 'score' in filtered.columns else 0
                                    profile_data[nom] = score
                            DATA.append(profile_data)

                        with elements("radar_chart"):
                            with mui.Box(sx={"height": 500}):
                                nivo.Radar(
                                    data=DATA,
                                    keys=list(unique_noms),
                                    indexBy="profile",
                                    maxValue=4,
                                    valueFormat=">-.2f",
                                    curve="linearClosed",
                                    margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                                    borderColor={"theme": "grid.line.stroke"},
                                    gridLabelOffset=36,
                                    dotSize=8,
                                    dotColor={"theme": "background"},
                                    dotBorderWidth=2,
                                    motionConfig="wobbly",
                                    legends=[{
                                        "anchor": "top-left",
                                        "direction": "column",
                                        "translateX": -50,
                                        "translateY": -40,
                                        "itemWidth": 80,
                                        "itemHeight": 20,
                                        "itemTextColor": "#999",
                                        "symbolSize": 12,
                                        "symbolShape": "circle",
                                    }],
                                    theme={
                                        "background": "#FFFFFF",
                                        "textColor": "#31333F",
                                    }
                                )

                        # Summary table
                        st.markdown("### Participants")
                        summary = form_data.groupby(['nom', 'prenom']).agg({
                            'score': 'mean',
                            'profile_type': lambda x: ', '.join(x.unique())
                        }).reset_index()
                        summary.columns = ['Nom', 'Prénom', 'Score moyen', 'Profils']
                        st.dataframe(summary, use_container_width=True)
