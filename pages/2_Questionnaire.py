"""
Questionnaire Interface - La Forge à Data Position
Progressive disclosure questionnaire with adaptive profiling
"""

import pandas as pd
import streamlit as st
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(
    page_title="Questionnaire - Forge Data Position",
    page_icon="📝",
    layout='centered',
    initial_sidebar_state='collapsed'
)

# Custom CSS
st.markdown("""
<style>
    .stProgress > div > div > div > div { background-color: #1c3f4b; }
    .pass-badge { background-color: #28a745; color: white; padding: 5px 15px; border-radius: 20px; }
    .fail-badge { background-color: #dc3545; color: white; padding: 5px 15px; border-radius: 20px; }
    .score-display { font-size: 24px; font-weight: bold; text-align: center; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# Banner
st.components.v1.html("""
<div style="width:100%;height:120px;display:flex;justify-content:center;align-items:center;padding:10px;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true"
         style="max-width:100%;max-height:100%;" alt="La Forge Data Position">
</div>
""", height=140)

# Constants
PASS_THRESHOLD = 0.75  # 75% to pass a section

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
            data = response.json()
            if 'records' not in data:
                return {"records": []}, None
            return data, None
        return {"records": []}, f"Erreur {response.status_code}"
    except Exception as e:
        return {"records": []}, str(e)


def save_answers_to_grist(answers_list):
    """Save answers to Grist Form3."""
    try:
        records = [{"fields": a} for a in answers_list]
        url = f"https://{subdomain}.getgrist.com/api/docs/{DOC_ID}/tables/Form3/records"
        response = requests.post(url, headers=headers, json={"records": records})
        return response.status_code == 200
    except:
        return False


def send_results_email(user_info, profile_results, selected_profiles):
    """Send results email to participant."""
    try:
        # Get SMTP config from secrets
        smtp_server = st.secrets.get("smtp", {}).get("server", "smtp.gmail.com")
        smtp_port = st.secrets.get("smtp", {}).get("port", 587)
        smtp_user = st.secrets.get("smtp", {}).get("user", "")
        smtp_password = st.secrets.get("smtp", {}).get("password", "")
        from_email = st.secrets.get("smtp", {}).get("from_email", smtp_user)

        if not smtp_user or not smtp_password:
            return False, "Configuration email manquante"

        # Calculate qualified profiles
        qualified = [p for p, r in profile_results.items() if r.get('passed', False)]

        # Build email content
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vos résultats - La Forge à Data Position"
        msg['From'] = from_email
        msg['To'] = user_info['mail']

        # Plain text version
        text_content = f"""
Bonjour {user_info['prenom']} {user_info['nom']},

Merci d'avoir complété l'évaluation de compétences data !

RÉSULTATS
---------
Profils évalués : {len(selected_profiles)}
Profils qualifiés : {len(qualified)}

"""
        for profile in selected_profiles:
            results = profile_results.get(profile, {})
            passed = results.get('passed', False)
            status = "✓ QUALIFIÉ" if passed else "✗ Non qualifié"
            text_content += f"\n{profile} - {status}\n"
            for section in ['screening', 'expertise', 'mastery']:
                if section in results:
                    score = results[section] * 100
                    text_content += f"  • {section.capitalize()}: {score:.0f}%\n"

        text_content += """
---
La Forge à Data Position
Développé par Datactivist
"""

        # HTML version
        html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #1c3f4b; padding: 20px; text-align: center;">
        <h1 style="color: white; margin: 0;">La Forge à Data Position</h1>
    </div>

    <div style="padding: 20px;">
        <p>Bonjour <strong>{user_info['prenom']} {user_info['nom']}</strong>,</p>

        <p>Merci d'avoir complété l'évaluation de compétences data !</p>

        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h2 style="margin-top: 0;">📊 Vos Résultats</h2>
            <p><strong>Profils évalués :</strong> {len(selected_profiles)}</p>
            <p><strong>Profils qualifiés :</strong> {len(qualified)}</p>
        </div>
"""

        for profile in selected_profiles:
            results = profile_results.get(profile, {})
            passed = results.get('passed', False)
            bg_color = "#d4edda" if passed else "#f8d7da"
            status_text = "✓ QUALIFIÉ" if passed else "✗ Non qualifié"

            html_content += f"""
        <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h3 style="margin: 0 0 10px 0;">{profile}</h3>
            <p style="margin: 0; font-weight: bold;">{status_text}</p>
            <table style="width: 100%; margin-top: 10px;">
"""
            for section in ['screening', 'expertise', 'mastery']:
                if section in results:
                    score = results[section] * 100
                    bar_color = "#28a745" if score >= 75 else "#dc3545"
                    html_content += f"""
                <tr>
                    <td style="width: 100px;">{section.capitalize()}</td>
                    <td>
                        <div style="background-color: #e9ecef; border-radius: 4px; height: 20px; width: 100%;">
                            <div style="background-color: {bar_color}; width: {score}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </td>
                    <td style="width: 50px; text-align: right;">{score:.0f}%</td>
                </tr>
"""
            html_content += """
            </table>
        </div>
"""

        html_content += """
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
        <p style="color: #666; font-size: 12px;">
            La Forge à Data Position - Développé par Datactivist
        </p>
    </div>
</body>
</html>
"""

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return True, "Email envoyé"
    except Exception as e:
        return False, str(e)


def calculate_section_score(answers, questions_df, profile, section_type):
    """Calculate score percentage for a section."""
    section_questions = questions_df[
        (questions_df['profile_type'] == profile) &
        (questions_df['question_type'] == section_type)
    ]['question'].unique()

    if len(section_questions) == 0:
        return 1.0  # No questions = auto-pass

    total_score = 0
    max_score = len(section_questions) * 4  # Max 4 points per question

    for q in section_questions:
        if q in answers:
            total_score += answers[q]['score']

    return total_score / max_score if max_score > 0 else 0


# Initialize session state
defaults = {
    'step': 'welcome',
    'user_info': {},
    'selected_profiles': [],
    'current_profile_idx': 0,
    'current_section': 'screening',
    'answers': {},
    'profile_results': {},  # {profile: {'screening': score, 'expertise': score, 'mastery': score, 'passed': bool}}
    'submitted': False,
    'email_sent': False,
    'email_error': None
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

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
section_order = ['screening', 'expertise', 'mastery']
section_labels = {'screening': '🔍 Screening', 'expertise': '💡 Expertise', 'mastery': '🎓 Maîtrise'}

# =============================================================================
# WELCOME STEP
# =============================================================================
if st.session_state.step == 'welcome':
    st.title("Évaluez vos compétences data")

    st.markdown("""
    Ce questionnaire adaptatif évalue vos compétences pour plusieurs profils data.

    **Comment ça marche ?**
    - Sélectionnez les profils qui vous intéressent
    - Pour chaque profil, répondez aux questions par niveau (Screening → Expertise → Maîtrise)
    - Si vous obtenez **75% ou plus** sur une section, vous passez à la suivante
    - Sinon, le questionnaire passe au profil suivant

    **Durée estimée** : 10-15 minutes
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

    st.subheader("🎯 Profils à évaluer")
    st.caption("Sélectionnez un ou plusieurs profils (il est courant d'avoir des compétences dans plusieurs domaines)")

    selected = st.multiselect(
        "Profils",
        available_profiles,
        default=st.session_state.selected_profiles or None,
        label_visibility="collapsed"
    )

    st.divider()

    can_proceed = nom and prenom and mail and len(selected) > 0

    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Commencer →", type="primary", disabled=not can_proceed):
            st.session_state.user_info = {'nom': nom, 'prenom': prenom, 'mail': mail}
            st.session_state.selected_profiles = selected
            st.session_state.current_profile_idx = 0
            st.session_state.current_section = 'screening'
            st.session_state.step = 'questions'
            st.session_state.profile_results = {p: {} for p in selected}
            st.rerun()

    if not can_proceed:
        st.info("Remplissez vos informations et sélectionnez au moins un profil.")

# =============================================================================
# QUESTIONS STEP
# =============================================================================
elif st.session_state.step == 'questions':
    profiles = st.session_state.selected_profiles
    current_idx = st.session_state.current_profile_idx
    current_section = st.session_state.current_section

    # Check if we're done with all profiles
    if current_idx >= len(profiles):
        st.session_state.step = 'results'
        st.rerun()

    current_profile = profiles[current_idx]

    # Get questions for current profile and section
    section_df = questions_df[
        (questions_df['profile_type'] == current_profile) &
        (questions_df['question_type'] == current_section)
    ]
    unique_questions = section_df['question'].unique()

    # If no questions for this section, skip to next
    if len(unique_questions) == 0:
        # Auto-pass empty sections
        st.session_state.profile_results[current_profile][current_section] = 1.0

        # Move to next section or profile
        section_idx = section_order.index(current_section)
        if section_idx < len(section_order) - 1:
            st.session_state.current_section = section_order[section_idx + 1]
        else:
            st.session_state.profile_results[current_profile]['passed'] = True
            st.session_state.current_profile_idx += 1
            st.session_state.current_section = 'screening'
        st.rerun()

    # Progress indicator
    total_profiles = len(profiles)
    total_sections = len(section_order)
    section_idx = section_order.index(current_section)
    overall_progress = (current_idx * total_sections + section_idx) / (total_profiles * total_sections)

    st.progress(overall_progress)
    st.caption(f"Profil {current_idx + 1}/{total_profiles} • Section {section_idx + 1}/{total_sections}")

    st.title(f"{current_profile}")
    st.subheader(f"{section_labels.get(current_section, current_section)}")

    section_descriptions = {
        'screening': "Questions générales pour évaluer votre familiarité avec ce domaine.",
        'expertise': "Questions techniques pour évaluer vos compétences pratiques.",
        'mastery': "Questions avancées pour évaluer votre niveau d'expertise."
    }
    st.caption(section_descriptions.get(current_section, ""))

    st.divider()

    # Display questions
    all_answered = True
    section_key = f"{current_profile}_{current_section}"

    for i, question in enumerate(unique_questions):
        st.markdown(f"**Question {i+1}/{len(unique_questions)}**")
        st.markdown(f"*{question}*")

        # Get possible answers sorted by score (highest first)
        q_data = section_df[section_df['question'] == question].sort_values('score', ascending=False)
        possible_answers = q_data['reponse'].tolist()
        scores = q_data['score'].tolist()

        # Get current answer if any
        current_answer = st.session_state.answers.get(question, {}).get('reponse', None)
        default_idx = possible_answers.index(current_answer) if current_answer in possible_answers else None

        selected_answer = st.radio(
            f"q_{section_key}_{i}",
            possible_answers,
            index=default_idx,
            label_visibility="collapsed",
            key=f"radio_{section_key}_{i}"
        )

        if selected_answer:
            score_idx = possible_answers.index(selected_answer)
            st.session_state.answers[question] = {
                'reponse': selected_answer,
                'score': scores[score_idx],
                'profile': current_profile,
                'section': current_section
            }
        else:
            all_answered = False

        st.divider()

    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])

    with col3:
        if st.button("Valider cette section →", type="primary", disabled=not all_answered):
            # Calculate score for this section
            score_pct = calculate_section_score(
                st.session_state.answers, questions_df, current_profile, current_section
            )
            st.session_state.profile_results[current_profile][current_section] = score_pct

            passed = score_pct >= PASS_THRESHOLD

            if passed:
                # Move to next section
                if section_idx < len(section_order) - 1:
                    st.session_state.current_section = section_order[section_idx + 1]
                else:
                    # Completed all sections for this profile
                    st.session_state.profile_results[current_profile]['passed'] = True
                    st.session_state.current_profile_idx += 1
                    st.session_state.current_section = 'screening'
            else:
                # Failed - move to next profile
                st.session_state.profile_results[current_profile]['passed'] = False
                st.session_state.current_profile_idx += 1
                st.session_state.current_section = 'screening'

            st.rerun()

    if not all_answered:
        st.warning("Répondez à toutes les questions pour continuer.")

    # Show current section progress
    with st.expander("📊 Votre progression"):
        for profile in profiles[:current_idx + 1]:
            results = st.session_state.profile_results.get(profile, {})
            if results:
                st.markdown(f"**{profile}**")
                for section in section_order:
                    if section in results:
                        score = results[section]
                        status = "✅" if score >= PASS_THRESHOLD else "❌"
                        st.write(f"  {section_labels[section]}: {score*100:.0f}% {status}")

# =============================================================================
# RESULTS STEP
# =============================================================================
elif st.session_state.step == 'results':
    st.title("📊 Résultats de votre évaluation")

    # Calculate qualified profiles
    qualified_profiles = []
    for profile, results in st.session_state.profile_results.items():
        if results.get('passed', False):
            qualified_profiles.append(profile)

    if qualified_profiles:
        st.success(f"🎉 Félicitations ! Vous êtes qualifié(e) pour **{len(qualified_profiles)}** profil(s) data.")
    else:
        st.info("Vous n'avez pas atteint le seuil de 75% pour les profils évalués. N'hésitez pas à réessayer !")

    st.divider()

    # Detailed results
    st.subheader("Détail par profil")

    for profile in st.session_state.selected_profiles:
        results = st.session_state.profile_results.get(profile, {})
        passed = results.get('passed', False)

        with st.expander(f"{'✅' if passed else '❌'} {profile}", expanded=True):
            cols = st.columns(3)
            for i, section in enumerate(section_order):
                with cols[i]:
                    score = results.get(section, 0)
                    st.metric(
                        section_labels[section],
                        f"{score*100:.0f}%",
                        delta="Réussi" if score >= PASS_THRESHOLD else "Non atteint"
                    )

            if passed:
                st.success("Profil validé ! Toutes les sections complétées avec succès.")
            elif any(section in results for section in section_order):
                failed_section = None
                for section in section_order:
                    if section in results and results[section] < PASS_THRESHOLD:
                        failed_section = section
                        break
                if failed_section:
                    st.warning(f"Évaluation arrêtée à la section {section_labels[failed_section]} (score < 75%)")

    st.divider()

    # Submit results
    st.subheader("Enregistrer vos résultats")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Recommencer"):
            for key in defaults:
                st.session_state[key] = defaults[key]
            st.rerun()

    with col2:
        if st.button("✅ Envoyer mes résultats", type="primary"):
            # Prepare answers for Grist
            final_answers = []
            for question, data in st.session_state.answers.items():
                final_answers.append({
                    'nom': st.session_state.user_info['nom'],
                    'prenom': st.session_state.user_info['prenom'],
                    'mail': st.session_state.user_info['mail'],
                    'question': question,
                    'reponse': data['reponse'],
                    'score': data['score'],
                    'profile_type': data['profile']
                })

            if save_answers_to_grist(final_answers):
                # Try to send email with results
                email_success, email_msg = send_results_email(
                    st.session_state.user_info,
                    st.session_state.profile_results,
                    st.session_state.selected_profiles
                )
                st.session_state.email_sent = email_success
                st.session_state.email_error = email_msg if not email_success else None
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Erreur lors de l'enregistrement. Veuillez réessayer.")

# =============================================================================
# SUBMITTED
# =============================================================================
elif st.session_state.submitted:
    st.balloons()
    st.title("🎉 Merci !")

    st.success("Vos résultats ont été enregistrés avec succès.")

    # Show email status
    if st.session_state.email_sent:
        st.info(f"📧 Un email récapitulatif a été envoyé à **{st.session_state.user_info['mail']}**")
    elif st.session_state.email_error:
        st.warning(f"📧 L'email n'a pas pu être envoyé ({st.session_state.email_error}). Vos résultats ont tout de même été enregistrés.")

    qualified = [p for p, r in st.session_state.profile_results.items() if r.get('passed', False)]

    st.markdown(f"""
    ### Récapitulatif

    - **Nom** : {st.session_state.user_info['nom']} {st.session_state.user_info['prenom']}
    - **Profils évalués** : {len(st.session_state.selected_profiles)}
    - **Profils qualifiés** : {len(qualified)} ({', '.join(qualified) if qualified else 'Aucun'})

    Votre responsable pourra consulter vos résultats détaillés.
    """)

    if st.button("Nouvelle évaluation"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        st.rerun()
