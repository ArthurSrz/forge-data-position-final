"""
Questionnaire Interface - La Forge à Data Position
Progressive disclosure questionnaire with adaptive profiling
"""

import sys
sys.path.insert(0, '..')

import pandas as pd
import streamlit as st
import requests
from datetime import datetime
from styles import inject_styles

# Page configuration
st.set_page_config(
    page_title="Questionnaire - Forge Data Position",
    page_icon="📝",
    layout='centered',
    initial_sidebar_state='collapsed'
)

# Inject custom styles (hide sidebar for candidates)
inject_styles(hide_sidebar=True)

# Banner - seamless integration
st.components.v1.html("""
<div style="width:100%;height:120px;display:flex;justify-content:center;align-items:center;padding:10px;background:transparent;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true&v=2"
         style="max-width:100%;max-height:100%;background:transparent;" alt="La Forge Data Position">
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


def generate_results_markdown(user_info, profile_results, selected_profiles):
    """Generate a colorful markdown file with results."""
    qualified = [p for p, r in profile_results.items() if r.get('passed', False)]
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")

    # Build markdown content
    md = f"""# 🔥 La Forge à Data Position
## Résultats de l'évaluation

---

### 👤 Participant
| | |
|---|---|
| **Nom** | {user_info['nom']} |
| **Prénom** | {user_info['prenom']} |
| **Email** | {user_info['mail']} |
| **Date** | {date_str} |

---

### 📊 Synthèse

| Métrique | Valeur |
|----------|--------|
| Profils évalués | **{len(selected_profiles)}** |
| Profils qualifiés | **{len(qualified)}** |
| Taux de réussite | **{len(qualified)*100//len(selected_profiles) if selected_profiles else 0}%** |

"""

    if qualified:
        md += f"""
> ✅ **Félicitations !** Vous êtes qualifié(e) pour : {', '.join(qualified)}

"""
    else:
        md += """
> ⚠️ Aucun profil qualifié. N'hésitez pas à réessayer !

"""

    md += """---

### 📋 Détail par profil

"""

    section_icons = {'screening': '🔍', 'expertise': '💡', 'mastery': '🎓'}
    section_names = {'screening': 'Screening', 'expertise': 'Expertise', 'mastery': 'Maîtrise'}

    for profile in selected_profiles:
        results = profile_results.get(profile, {})
        passed = results.get('passed', False)
        status_badge = "✅ QUALIFIÉ" if passed else "❌ Non qualifié"

        md += f"""
#### {'🏆' if passed else '📌'} {profile}

**Statut : {status_badge}**

| Section | Score | Résultat |
|---------|-------|----------|
"""

        for section in ['screening', 'expertise', 'mastery']:
            if section in results:
                score = results[section] * 100
                icon = section_icons[section]
                name = section_names[section]
                bar = "🟩" * int(score // 10) + "⬜" * (10 - int(score // 10))
                result = "✅ Réussi" if score >= 75 else "❌ < 75%"
                md += f"| {icon} {name} | {bar} **{score:.0f}%** | {result} |\n"

        md += "\n"

    md += """---

### ℹ️ À propos

Cette évaluation a été réalisée via **La Forge à Data Position**, un outil développé par [Datactivist](https://datactivist.coop).

Le seuil de qualification est de **75%** par section. Pour être qualifié sur un profil, il faut réussir toutes les sections (Screening → Expertise → Maîtrise).

---

*Document généré automatiquement*
"""

    return md


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
    'submitted': False
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
        if st.button("✅ Enregistrer mes résultats", type="primary"):
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

    qualified = [p for p, r in st.session_state.profile_results.items() if r.get('passed', False)]

    st.markdown(f"""
    ### Récapitulatif

    - **Nom** : {st.session_state.user_info['nom']} {st.session_state.user_info['prenom']}
    - **Profils évalués** : {len(st.session_state.selected_profiles)}
    - **Profils qualifiés** : {len(qualified)} ({', '.join(qualified) if qualified else 'Aucun'})

    Votre responsable pourra consulter vos résultats détaillés.
    """)

    st.divider()

    # Generate and offer markdown download
    st.subheader("📥 Télécharger vos résultats")

    results_md = generate_results_markdown(
        st.session_state.user_info,
        st.session_state.profile_results,
        st.session_state.selected_profiles
    )

    filename = f"resultats_{st.session_state.user_info['nom']}_{st.session_state.user_info['prenom']}.md"
    filename = filename.replace(" ", "_").lower()

    st.download_button(
        label="📄 Télécharger mes résultats (.md)",
        data=results_md,
        file_name=filename,
        mime="text/markdown",
        type="primary"
    )

    st.caption("Ce fichier contient le détail de vos scores par profil et par section.")

    st.divider()

    if st.button("🔄 Nouvelle évaluation"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        st.rerun()
