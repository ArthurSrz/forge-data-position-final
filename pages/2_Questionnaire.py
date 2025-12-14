"""
Questionnaire Interface - La Forge à Data Position
Clean, step-by-step questionnaire for collaborators
"""

import pandas as pd
import streamlit as st
import requests
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Questionnaire - Forge Data Position",
    page_icon="📝",
    layout='centered',
    initial_sidebar_state='collapsed'
)

# Custom CSS for better UX
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #1c3f4b;
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .step-indicator {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Banner
st.components.v1.html("""
<div style="width:100%;height:120px;display:flex;justify-content:center;align-items:center;padding:10px;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true"
         style="max-width:100%;max-height:100%;" alt="La Forge Data Position">
</div>
""", height=140)

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


def add_answers_to_grist(answers_list, table_id="Form3"):
    """Submit answers to Grist."""
    try:
        records = [{"fields": a} for a in answers_list]
        url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/{table_id}/records"
        response = requests.post(url, headers=headers, json={"records": records})
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)


# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'selected_profile' not in st.session_state:
    st.session_state.selected_profile = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Load questions
data2, error = load_grist_table("Form2")
if error:
    st.error(f"Impossible de charger le questionnaire: {error}")
    st.stop()

records = data2.get('records', [])
if not records:
    st.warning("Aucune question disponible.")
    st.stop()

questions_df = pd.json_normalize(records, sep='_')
questions_df.columns = [col.replace('fields_', '') for col in questions_df.columns]

# Get available profiles
available_profiles = sorted(questions_df['profile_type'].dropna().unique())

# =============================================================================
# STEP 0: Welcome & User Info
# =============================================================================
if st.session_state.step == 0:
    st.title("Évaluez vos compétences data")

    st.markdown("""
    Bienvenue ! Ce questionnaire permet d'évaluer vos compétences data
    pour mieux positionner les talents de l'équipe.

    **Durée estimée** : 5-10 minutes
    """)

    st.divider()

    st.subheader("🧑 Vos informations")

    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom", value=st.session_state.user_info.get('nom', ''))
        prenom = st.text_input("Prénom", value=st.session_state.user_info.get('prenom', ''))
    with col2:
        mail = st.text_input("Email", value=st.session_state.user_info.get('mail', ''))

    st.divider()

    st.subheader("🎯 Votre profil data principal")
    st.caption("Sélectionnez le profil qui correspond le mieux à votre activité")

    selected = st.radio(
        "Profil",
        available_profiles,
        index=None,
        label_visibility="collapsed"
    )

    st.divider()

    # Validation
    can_proceed = nom and prenom and mail and selected

    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Commencer →", type="primary", disabled=not can_proceed):
            st.session_state.user_info = {'nom': nom, 'prenom': prenom, 'mail': mail}
            st.session_state.selected_profile = selected
            st.session_state.step = 1
            st.rerun()

    if not can_proceed:
        st.info("Remplissez tous les champs et sélectionnez un profil pour continuer.")

# =============================================================================
# STEP 1+: Questions by type
# =============================================================================
elif not st.session_state.submitted:
    # Filter questions for selected profile
    profile_df = questions_df[questions_df['profile_type'] == st.session_state.selected_profile]

    # Group by question type
    question_types = ['screening', 'expertise', 'mastery']
    available_types = [qt for qt in question_types if qt in profile_df['question_type'].values]

    if not available_types:
        st.error("Aucune question disponible pour ce profil.")
        if st.button("← Retour"):
            st.session_state.step = 0
            st.rerun()
        st.stop()

    # Calculate current question type index
    type_index = st.session_state.step - 1

    if type_index >= len(available_types):
        # All questions answered - show summary
        st.title("📋 Récapitulatif")

        st.success(f"Vous avez répondu à toutes les questions pour le profil **{st.session_state.selected_profile}**")

        # Show summary
        st.subheader("Vos réponses")
        for q_type in available_types:
            type_label = {'screening': '🔍 Screening', 'expertise': '💡 Expertise', 'mastery': '🎓 Maîtrise'}.get(q_type, q_type)
            st.markdown(f"**{type_label}**")

            type_questions = profile_df[profile_df['question_type'] == q_type]['question'].unique()
            for q in type_questions:
                if q in st.session_state.answers:
                    ans = st.session_state.answers[q]
                    st.markdown(f"- {q[:50]}... → Score: {ans['score']}")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Modifier mes réponses"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("✅ Envoyer mes réponses", type="primary"):
                # Prepare final answers
                final_answers = []
                for question, data in st.session_state.answers.items():
                    final_answers.append({
                        'nom': st.session_state.user_info['nom'],
                        'prenom': st.session_state.user_info['prenom'],
                        'mail': st.session_state.user_info['mail'],
                        'question': question,
                        'reponse': data['reponse'],
                        'score': data['score'],
                        'profile_type': st.session_state.selected_profile
                    })

                with st.spinner("Envoi en cours..."):
                    success, msg = add_answers_to_grist(final_answers)

                if success:
                    st.session_state.submitted = True
                    st.rerun()
                else:
                    st.error(f"Erreur: {msg}")
    else:
        # Show questions for current type
        current_type = available_types[type_index]
        type_questions = profile_df[profile_df['question_type'] == current_type]
        unique_questions = type_questions['question'].unique()

        # Header with progress
        type_labels = {'screening': 'Screening', 'expertise': 'Expertise', 'mastery': 'Maîtrise'}
        type_icons = {'screening': '🔍', 'expertise': '💡', 'mastery': '🎓'}

        progress = (type_index) / len(available_types)
        st.progress(progress)
        st.markdown(f"<div class='step-indicator'>Étape {type_index + 1}/{len(available_types)} • {st.session_state.selected_profile}</div>", unsafe_allow_html=True)

        st.title(f"{type_icons.get(current_type, '📝')} {type_labels.get(current_type, current_type)}")

        # Type description
        type_descriptions = {
            'screening': "Ces questions permettent d'évaluer votre niveau général dans ce domaine.",
            'expertise': "Ces questions évaluent vos compétences techniques spécifiques.",
            'mastery': "Ces questions mesurent votre niveau de maîtrise avancée."
        }
        st.caption(type_descriptions.get(current_type, ""))

        st.divider()

        # Questions
        all_answered = True
        for i, question in enumerate(unique_questions):
            st.markdown(f"**Question {i+1}/{len(unique_questions)}**")
            st.markdown(f"*{question}*")

            # Get possible answers sorted by score (descending)
            q_data = type_questions[type_questions['question'] == question].sort_values('score', ascending=False)
            possible_answers = q_data['reponse'].tolist()
            scores = q_data['score'].tolist()

            # Create answer options with score indicators
            current_answer = st.session_state.answers.get(question, {}).get('reponse', None)

            # Find index of current answer
            default_idx = None
            if current_answer in possible_answers:
                default_idx = possible_answers.index(current_answer)

            selected_answer = st.radio(
                f"q_{i}",
                possible_answers,
                index=default_idx,
                label_visibility="collapsed",
                key=f"{current_type}_{i}"
            )

            if selected_answer:
                # Save answer
                score_idx = possible_answers.index(selected_answer)
                st.session_state.answers[question] = {
                    'reponse': selected_answer,
                    'score': scores[score_idx]
                }
            else:
                all_answered = False

            st.divider()

        # Navigation
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if type_index > 0:
                if st.button("← Précédent"):
                    st.session_state.step -= 1
                    st.rerun()

        with col3:
            btn_label = "Suivant →" if type_index < len(available_types) - 1 else "Voir le récapitulatif →"
            if st.button(btn_label, type="primary", disabled=not all_answered):
                st.session_state.step += 1
                st.rerun()

        if not all_answered:
            st.warning("Répondez à toutes les questions pour continuer.")

# =============================================================================
# SUBMITTED: Thank you page
# =============================================================================
else:
    st.balloons()

    st.title("🎉 Merci !")

    st.success("Vos réponses ont été enregistrées avec succès.")

    st.markdown(f"""
    ### Récapitulatif

    - **Nom** : {st.session_state.user_info['nom']} {st.session_state.user_info['prenom']}
    - **Profil évalué** : {st.session_state.selected_profile}
    - **Questions répondues** : {len(st.session_state.answers)}

    Votre responsable pourra visualiser vos résultats dans le radar de compétences.
    """)

    if st.button("Recommencer avec un autre profil"):
        # Reset state
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.selected_profile = None
        st.rerun()
