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

# Logo in sidebar at top
with st.sidebar:
    st.image("resource/logo_forge.png", use_container_width=True)

st.markdown("# Bienvenue sur <span style='color:#002FA7'>La Forge</span> à Data Position", unsafe_allow_html=True)

st.markdown("""
### Qu'est-ce qu'un <span style='color:#002FA7'>Data Position</span> ?

Un **Data Position** est un référentiel de compétences data qui permet de :

- <span style='color:#002FA7;font-weight:600'>Cartographier</span> les profils data de votre organisation
- <span style='color:#002FA7;font-weight:600'>Évaluer</span> les compétences de vos collaborateurs
- <span style='color:#002FA7;font-weight:600'>Visualiser</span> la répartition des expertises
""", unsafe_allow_html=True)

# Animated radar chart - "Perfect Team" visualization
st.markdown("### <span style='color:#002FA7'>L'équipe data idéale</span>", unsafe_allow_html=True)

ANIMATED_RADAR_HTML = """
<div style="display:flex;justify-content:center;align-items:center;padding:20px;">
<svg viewBox="0 0 500 500" width="100%" style="max-width:600px;max-height:500px;">
  <defs>
    <style>
      .grid-line { stroke: #e7e5e4; stroke-width: 1; fill: none; }
      .axis-line { stroke: #e7e5e4; stroke-width: 1; }
      .label { font-family: 'IBM Plex Sans', sans-serif; font-size: 11px; fill: #1c1917; }
      .team-area { fill: #002FA7; fill-opacity: 0; stroke: #002FA7; stroke-width: 2; }
      .dot { fill: #002FA7; opacity: 0; }
      .legend { font-family: 'IBM Plex Sans', sans-serif; font-size: 12px; fill: #1c1917; }

      /* Animation keyframes */
      @keyframes fillIn {
        0% { fill-opacity: 0; }
        100% { fill-opacity: 0.3; }
      }
      @keyframes drawPath {
        0% { stroke-dashoffset: 1000; }
        100% { stroke-dashoffset: 0; }
      }
      @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
      }
      @keyframes pulse {
        0%, 100% { r: 6; }
        50% { r: 8; }
      }

      .team-area {
        stroke-dasharray: 1000;
        stroke-dashoffset: 1000;
        animation: drawPath 2s ease-out forwards, fillIn 1s ease-out 1.5s forwards;
      }
      .dot {
        animation: fadeIn 0.5s ease-out forwards, pulse 2s ease-in-out infinite;
      }
      .dot:nth-child(1) { animation-delay: 0.5s, 2.5s; }
      .dot:nth-child(2) { animation-delay: 0.7s, 2.7s; }
      .dot:nth-child(3) { animation-delay: 0.9s, 2.9s; }
      .dot:nth-child(4) { animation-delay: 1.1s, 3.1s; }
      .dot:nth-child(5) { animation-delay: 1.3s, 3.3s; }
      .dot:nth-child(6) { animation-delay: 1.5s, 3.5s; }
    </style>
  </defs>

  <!-- Grid circles -->
  <circle cx="250" cy="250" r="40" class="grid-line"/>
  <circle cx="250" cy="250" r="80" class="grid-line"/>
  <circle cx="250" cy="250" r="120" class="grid-line"/>
  <circle cx="250" cy="250" r="160" class="grid-line"/>
  <circle cx="250" cy="250" r="200" class="grid-line"/>

  <!-- Axis lines (6 axes for 6 profiles) -->
  <line x1="250" y1="250" x2="250" y2="50" class="axis-line"/>
  <line x1="250" y1="250" x2="423" y2="150" class="axis-line"/>
  <line x1="250" y1="250" x2="423" y2="350" class="axis-line"/>
  <line x1="250" y1="250" x2="250" y2="450" class="axis-line"/>
  <line x1="250" y1="250" x2="77" y2="350" class="axis-line"/>
  <line x1="250" y1="250" x2="77" y2="150" class="axis-line"/>

  <!-- Labels -->
  <text x="250" y="30" text-anchor="middle" class="label" font-weight="600">Data Analyst</text>
  <text x="440" y="145" text-anchor="start" class="label" font-weight="600">Data Scientist</text>
  <text x="440" y="360" text-anchor="start" class="label" font-weight="600">Data Engineer</text>
  <text x="250" y="475" text-anchor="middle" class="label" font-weight="600">ML Engineer</text>
  <text x="60" y="360" text-anchor="end" class="label" font-weight="600">Chef Projet Data</text>
  <text x="60" y="145" text-anchor="end" class="label" font-weight="600">Data Architect</text>

  <!-- Perfect team polygon - each member excels in one area (95%) but has basics everywhere (40%) -->
  <!-- Points calculated for: top=95%, others=40% for first member, rotating for each -->
  <polygon class="team-area" points="
    250,58
    385,168
    385,332
    250,442
    115,332
    115,168
  "/>

  <!-- Specialist dots - showing where each team member excels -->
  <circle cx="250" cy="58" r="6" class="dot" style="fill:#002FA7;"/>
  <circle cx="385" cy="168" r="6" class="dot" style="fill:#4A90D9;"/>
  <circle cx="385" cy="332" r="6" class="dot" style="fill:#7CB9E8;"/>
  <circle cx="250" cy="442" r="6" class="dot" style="fill:#002FA7;"/>
  <circle cx="115" cy="332" r="6" class="dot" style="fill:#4A90D9;"/>
  <circle cx="115" cy="168" r="6" class="dot" style="fill:#7CB9E8;"/>

  <!-- Legend -->
  <g transform="translate(30, 30)">
    <circle cx="8" cy="8" r="6" fill="#002FA7"/>
    <text x="20" y="12" class="legend">Équipe Idéale</text>
  </g>

  <!-- Tagline -->
  <text x="250" y="495" text-anchor="middle" class="label" style="font-size:10px;fill:#57534e;">
    Chaque membre excelle dans un domaine, maîtrise les bases partout
  </text>
</svg>
</div>
"""

st.components.v1.html(ANIMATED_RADAR_HTML, height=550)

st.divider()

st.markdown("### Choisissez votre <span style='color:#002FA7'>interface</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("""
        #### <span style='color:#002FA7'>Admin</span>
        **Pour les responsables data**

        - Créer et configurer un Data Position
        - Sélectionner les profils à évaluer
        - Visualiser les résultats (radar chart)
        - Analyser la répartition des compétences
        """, unsafe_allow_html=True)
        st.page_link("pages/1_Admin.py", label="Ouvrir l'interface Admin", icon="⚙️")

with col2:
    with st.container(border=True):
        st.markdown("""
        #### <span style='color:#002FA7'>Questionnaire</span>
        **Pour les collaborateurs**

        - Remplir le questionnaire d'évaluation
        - Auto-évaluer ses compétences data
        - Contribuer à la cartographie de l'équipe
        """, unsafe_allow_html=True)
        st.page_link("pages/2_Questionnaire.py", label="Ouvrir le Questionnaire", icon="📝")

st.divider()

st.markdown("""
### Comment ça <span style='color:#002FA7'>marche</span> ?

1. **Le responsable** crée un Data Position dans l'interface <span style='color:#002FA7'>Admin</span>
2. **Le responsable** partage le lien du <span style='color:#002FA7'>Questionnaire</span> avec son équipe
3. **Les collaborateurs** remplissent le questionnaire
4. **Le responsable** visualise les <span style='color:#002FA7'>résultats</span> dans l'onglet Position
""", unsafe_allow_html=True)

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
