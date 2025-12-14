"""
Questionnaire Interface - La Forge à Data Position
Public interface for collaborators to fill out the questionnaire
"""

import pandas as pd
import streamlit as st
import requests
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Questionnaire - Forge Data Position",
    page_icon="📝",
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Banner
st.components.v1.html("""
<div style="width:100%;height:150px;display:flex;justify-content:center;align-items:center;padding:10px;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true"
         style="max-width:100%;max-height:100%;" alt="La Forge Data Position">
</div>
""")

# Load secrets
DOC_ID = st.secrets["grist"]["doc_id"]
API_KEY = st.secrets["grist"]["api_key"]
subdomain = st.secrets["grist"]["subdomain"]
headers = {"Authorization": f"Bearer {API_KEY}"}


def load_grist_table(table_name):
    """Load a table from Grist."""
    url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/{table_name}/records"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), None
        return {"records": []}, f"Erreur {response.status_code}"
    except Exception as e:
        return {"records": []}, str(e)


def add_answers_to_grist(df_answers, table_id):
    """Submit answers to Grist."""
    try:
        records = [{
            "fields": {
                "nom": r["nom"],
                "prenom": r["prenom"],
                "mail": r["mail"],
                "question": r["question"],
                "reponse": r["reponse"],
                "score": r["score"],
                "profile_type": r["profile_type"]
            }
        } for r in df_answers.to_dict(orient='records')]

        url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/{table_id}/records"
        response = requests.post(url, headers=headers, json={"records": records})

        if response.status_code == 200:
            return True, "Réponses enregistrées avec succès !"
        return False, f"Erreur: {response.status_code}"
    except Exception as e:
        return False, str(e)


# Load master questions
data2, error = load_grist_table("Form2")
if error:
    st.error(f"Impossible de charger le questionnaire: {error}")
    st.stop()

# Convert to DataFrame
records = data2.get('records', [])
if not records:
    st.warning("Aucune question disponible. Contactez votre administrateur.")
    st.stop()

questions_df = pd.json_normalize(records, sep='_')
questions_df.columns = [col.replace('fields_', '') for col in questions_df.columns]

# Get available profiles
available_profiles = questions_df['profile_type'].dropna().unique()
available_profiles = [p for p in available_profiles if p and "'" not in p]  # Filter clean profiles

# =============================================================================
# QUESTIONNAIRE
# =============================================================================

st.title("Évaluation de vos compétences data")

with st.expander("ℹ️ Comment remplir ce questionnaire ?", expanded=False):
    st.markdown("""
    Ce questionnaire permet d'évaluer vos compétences data pour mieux positionner
    les talents de l'équipe.

    **Instructions :**
    1. Renseignez vos informations personnelles
    2. Indiquez votre profil data principal
    3. Répondez aux questions d'expertise
    4. Validez vos réponses

    Vos réponses seront transmises à votre responsable qui pourra visualiser
    la répartition des compétences dans l'équipe.
    """)

st.divider()

# Initialize answers storage
if 'answers' not in st.session_state:
    st.session_state.answers = []

# Profile selection for filtering questions
selected_profiles = st.multiselect(
    "Pour quels profils souhaitez-vous être évalué(e) ?",
    available_profiles,
    default=available_profiles[:3] if len(available_profiles) >= 3 else available_profiles,
    help="Sélectionnez les profils data qui correspondent à votre activité"
)

if not selected_profiles:
    st.warning("Veuillez sélectionner au moins un profil.")
    st.stop()

# Filter questions by selected profiles
filtered_df = questions_df[questions_df['profile_type'].isin(selected_profiles)]

# Separate screening and expertise questions
screening_df = filtered_df[filtered_df.get('question_type', '') == 'screening'] if 'question_type' in filtered_df.columns else pd.DataFrame()
expertise_df = filtered_df[filtered_df.get('question_type', '') == 'expertise'] if 'question_type' in filtered_df.columns else filtered_df

st.divider()

# =============================================================================
# PERSONAL INFO
# =============================================================================
st.header("🧑 Vos informations")

col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom *", key='nom')
    prenom = st.text_input("Prénom *", key='prenom')
with col2:
    mail = st.text_input("Email *", key='mail')

if not nom or not prenom or not mail:
    st.info("Veuillez remplir tous les champs obligatoires (*)")

st.divider()

# =============================================================================
# QUESTIONS
# =============================================================================
st.header("📚 Questions d'expertise")

# Collect answers
df_answers = pd.DataFrame(columns=['nom', 'prenom', 'mail', 'question', 'reponse', 'score', 'profile_type'])

# Get unique questions
unique_questions = expertise_df['question'].unique() if not expertise_df.empty else []

for i, question in enumerate(unique_questions):
    st.markdown(f"**{question}**")

    # Get possible answers for this question
    question_data = expertise_df[expertise_df['question'] == question]
    possible_answers = question_data['reponse'].unique()

    answer = st.selectbox(
        "Votre réponse",
        options=["-- Sélectionnez --"] + list(possible_answers),
        key=f"q_{i}",
        label_visibility="collapsed"
    )

    if answer != "-- Sélectionnez --":
        # Get score and profile for this answer
        answer_row = question_data[question_data['reponse'] == answer].iloc[0]
        score = answer_row.get('score', 0)
        profile_type = answer_row.get('profile_type', '')

        # Handle numpy arrays
        if isinstance(score, np.ndarray):
            score = int(score[0]) if len(score) > 0 else 0
        if isinstance(profile_type, np.ndarray):
            profile_type = str(profile_type[0]) if len(profile_type) > 0 else ''

        new_row = pd.DataFrame([{
            'nom': nom,
            'prenom': prenom,
            'mail': mail,
            'question': question,
            'reponse': answer,
            'score': score,
            'profile_type': profile_type
        }])
        df_answers = pd.concat([df_answers, new_row], ignore_index=True)

    st.divider()

# =============================================================================
# SUBMIT
# =============================================================================
st.header("✅ Validation")

answered_count = len(df_answers)
total_questions = len(unique_questions)

if answered_count < total_questions:
    st.warning(f"Vous avez répondu à {answered_count}/{total_questions} questions.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Envoyer mes réponses", type="primary", disabled=(not nom or not prenom or not mail)):
        if answered_count == 0:
            st.error("Veuillez répondre à au moins une question.")
        else:
            with st.spinner("Envoi en cours..."):
                success, message = add_answers_to_grist(df_answers, "Form3")

            if success:
                st.success("🎉 Merci ! Vos réponses ont été enregistrées.")
                st.balloons()
            else:
                st.error(f"Erreur lors de l'envoi : {message}")
