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

# Banner - seamless integration
st.components.v1.html("""
<div style="width:100%;height:200px;display:flex;justify-content:center;align-items:center;padding:20px;background:transparent;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true&v=2"
         style="max-width:100%;max-height:100%;background:transparent;" alt="La Forge Data Position">
</div>
""", height=220)

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

st.caption("Développé par Datactivist")
