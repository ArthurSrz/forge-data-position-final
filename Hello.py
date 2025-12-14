"""
La Forge à Data Position - Landing Page
"""

import streamlit as st
from styles import inject_styles

# Page configuration
st.set_page_config(
    page_title="La Forge à Data Position",
    page_icon="🔥",
    layout='wide',
    initial_sidebar_state='expanded'
)

# Inject custom styles
inject_styles()

# Banner - full width logo
st.image("resource/logo_forge.png", use_container_width=True)

st.title("Bienvenue sur La Forge à Data Position")

st.markdown("""
### Qu'est-ce qu'un Data Position ?

Un **Data Position** est un référentiel de compétences data qui permet de :

- **Cartographier les profils data** de votre organisation (Data Analyst, Data Scientist, ML Engineer, etc.)
- **Évaluer les compétences** de vos collaborateurs via un questionnaire standardisé
- **Visualiser la répartition** des expertises grâce à un radar de compétences
""")

st.divider()

st.markdown("### Choisissez votre interface")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("""
        #### Admin
        **Pour les responsables data**

        - Créer et configurer un Data Position
        - Sélectionner les profils à évaluer
        - Visualiser les résultats (radar chart)
        - Analyser la répartition des compétences
        """)
        st.page_link("pages/1_Admin.py", label="Ouvrir l'interface Admin", icon="⚙️")

with col2:
    with st.container(border=True):
        st.markdown("""
        #### Questionnaire
        **Pour les collaborateurs**

        - Remplir le questionnaire d'évaluation
        - Auto-évaluer ses compétences data
        - Contribuer à la cartographie de l'équipe
        """)
        st.page_link("pages/2_Questionnaire.py", label="Ouvrir le Questionnaire", icon="📝")

st.divider()

st.markdown("""
### Comment ça marche ?

1. **Le responsable** crée un Data Position dans l'interface Admin
2. **Le responsable** partage le lien du Questionnaire avec son équipe
3. **Les collaborateurs** remplissent le questionnaire
4. **Le responsable** visualise les résultats dans l'onglet Position
""")

st.divider()

# Footer with social links
st.components.v1.html("""
<div style="display:flex;justify-content:center;align-items:center;gap:12px;padding:20px;font-family:system-ui,-apple-system,sans-serif;font-size:14px;color:#666;">
    <span>Developed with ❤️ by Arthur Sarazin</span>
    <a href="https://www.linkedin.com/in/arthursarazin/" target="_blank" style="text-decoration:none;color:#0077B5;">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
    </a>
    <a href="https://github.com/ArthurSrz" target="_blank" style="text-decoration:none;color:#333;">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
    </a>
</div>
""", height=70)
