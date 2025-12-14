"""
La Forge à Data Position - Landing Page
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="La Forge à Data Position",
    page_icon="🔥",
    layout='wide',
    initial_sidebar_state='expanded'
)

# Banner
st.components.v1.html("""
<div style="width:100%;height:200px;display:flex;justify-content:center;align-items:center;padding:20px;">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true"
         style="max-width:100%;max-height:100%;" alt="La Forge Data Position">
</div>
""")

st.title("Bienvenue sur La Forge à Data Position")

st.markdown("""
### Qu'est-ce qu'un Data Position ?

Un **Data Position** est un référentiel de compétences data qui permet de :

- **Cartographier les profils data** de votre organisation (Data Analyst, Data Scientist, ML Engineer, etc.)
- **Évaluer les compétences** de vos collaborateurs via un questionnaire standardisé
- **Visualiser la répartition** des expertises grâce à un radar de compétences

---

### Choisissez votre interface

Utilisez le **menu latéral** (à gauche) pour accéder à l'interface adaptée à votre besoin :
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### ⚙️ Admin
    **Pour les responsables data**

    - Créer et configurer un Data Position
    - Sélectionner les profils à évaluer
    - Visualiser les résultats (radar chart)
    - Analyser la répartition des compétences

    👉 Ouvrez **Admin** dans le menu latéral
    """)

with col2:
    st.markdown("""
    #### 📝 Questionnaire
    **Pour les collaborateurs**

    - Remplir le questionnaire d'évaluation
    - Auto-évaluer ses compétences data
    - Contribuer à la cartographie de l'équipe

    👉 Ouvrez **Questionnaire** dans le menu latéral
    """)

st.divider()

st.markdown("""
### Comment ça marche ?

1. **Le responsable** crée un Data Position dans l'interface Admin
2. **Le responsable** partage le lien du Questionnaire avec son équipe
3. **Les collaborateurs** remplissent le questionnaire
4. **Le responsable** visualise les résultats dans l'onglet Position

---

*Développé avec Streamlit et Grist par Datactivist*
""")
