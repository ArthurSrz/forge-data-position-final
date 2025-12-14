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
    initial_sidebar_state='collapsed'
)

# Inject custom styles
inject_styles()

# Logo at top left
col_logo, col_spacer = st.columns([1, 4])
with col_logo:
    st.image("resource/logo_forge.png", width=150)

st.markdown("# Composez votre <span style='color:#002FA7'>Dream Team</span> Data", unsafe_allow_html=True)
st.markdown("### <span style='color:#57534e'>L'outil de cartographie des compétences pour les Chief Data Officers</span>", unsafe_allow_html=True)

# Animated radar with overlapping team members
ANIMATED_RADAR_HTML = """
<div style="display:flex;justify-content:center;align-items:center;padding:20px;">
<svg viewBox="0 0 600 550" width="100%" style="max-width:700px;">
  <defs>
    <style>
      .grid-line { stroke: #e7e5e4; stroke-width: 1; fill: none; }
      .axis-line { stroke: #e7e5e4; stroke-width: 1; }
      .label { font-family: 'IBM Plex Sans', sans-serif; font-size: 12px; fill: #1c1917; font-weight: 600; }
      .legend-text { font-family: 'IBM Plex Sans', sans-serif; font-size: 11px; fill: #1c1917; }

      /* Team member areas with different colors */
      .member-a { fill: #002FA7; stroke: #002FA7; stroke-width: 2; }
      .member-b { fill: #E63946; stroke: #E63946; stroke-width: 2; }
      .member-c { fill: #2A9D8F; stroke: #2A9D8F; stroke-width: 2; }
      .member-d { fill: #F4A261; stroke: #F4A261; stroke-width: 2; }
      .member-e { fill: #9B5DE5; stroke: #9B5DE5; stroke-width: 2; }
      .member-f { fill: #00B4D8; stroke: #00B4D8; stroke-width: 2; }

      /* Animation */
      @keyframes drawMember {
        0% { opacity: 0; transform: scale(0.8); }
        100% { opacity: 1; transform: scale(1); }
      }
      @keyframes fillMember {
        0% { fill-opacity: 0; }
        100% { fill-opacity: 0.25; }
      }

      .team-member {
        transform-origin: 300px 270px;
        opacity: 0;
        fill-opacity: 0;
      }
      .member-a { animation: drawMember 0.6s ease-out 0.2s forwards, fillMember 0.4s ease-out 0.6s forwards; }
      .member-b { animation: drawMember 0.6s ease-out 0.5s forwards, fillMember 0.4s ease-out 0.9s forwards; }
      .member-c { animation: drawMember 0.6s ease-out 0.8s forwards, fillMember 0.4s ease-out 1.2s forwards; }
      .member-d { animation: drawMember 0.6s ease-out 1.1s forwards, fillMember 0.4s ease-out 1.5s forwards; }
      .member-e { animation: drawMember 0.6s ease-out 1.4s forwards, fillMember 0.4s ease-out 1.8s forwards; }
      .member-f { animation: drawMember 0.6s ease-out 1.7s forwards, fillMember 0.4s ease-out 2.1s forwards; }
    </style>
  </defs>

  <!-- Grid circles -->
  <circle cx="300" cy="270" r="40" class="grid-line"/>
  <circle cx="300" cy="270" r="80" class="grid-line"/>
  <circle cx="300" cy="270" r="120" class="grid-line"/>
  <circle cx="300" cy="270" r="160" class="grid-line"/>
  <circle cx="300" cy="270" r="200" class="grid-line"/>

  <!-- Axis lines (6 axes) -->
  <line x1="300" y1="270" x2="300" y2="70" class="axis-line"/>
  <line x1="300" y1="270" x2="473" y2="170" class="axis-line"/>
  <line x1="300" y1="270" x2="473" y2="370" class="axis-line"/>
  <line x1="300" y1="270" x2="300" y2="470" class="axis-line"/>
  <line x1="300" y1="270" x2="127" y2="370" class="axis-line"/>
  <line x1="300" y1="270" x2="127" y2="170" class="axis-line"/>

  <!-- Profile Labels -->
  <text x="300" y="50" text-anchor="middle" class="label">Data Analyst</text>
  <text x="490" y="165" text-anchor="start" class="label">Data Scientist</text>
  <text x="490" y="380" text-anchor="start" class="label">Data Engineer</text>
  <text x="300" y="495" text-anchor="middle" class="label">ML Engineer</text>
  <text x="110" y="380" text-anchor="end" class="label">Chef Projet</text>
  <text x="110" y="165" text-anchor="end" class="label">Data Architect</text>

  <!-- Team Member A - Expert Data Analyst (high on Analyst, medium elsewhere) -->
  <polygon class="team-member member-a" points="300,78 380,200 380,340 300,390 220,340 220,200"/>

  <!-- Team Member B - Expert Data Scientist (high on Scientist, medium elsewhere) -->
  <polygon class="team-member member-b" points="300,150 460,185 380,340 300,390 220,340 160,200"/>

  <!-- Team Member C - Expert Data Engineer (high on Engineer, medium elsewhere) -->
  <polygon class="team-member member-c" points="300,150 380,200 460,355 300,390 220,340 160,200"/>

  <!-- Team Member D - Expert ML Engineer (high on ML, medium elsewhere) -->
  <polygon class="team-member member-d" points="300,150 380,200 380,340 300,462 220,340 160,200"/>

  <!-- Team Member E - Expert Chef Projet (high on PM, medium elsewhere) -->
  <polygon class="team-member member-e" points="300,150 380,200 380,340 300,390 140,355 160,200"/>

  <!-- Team Member F - Expert Data Architect (high on Architect, medium elsewhere) -->
  <polygon class="team-member member-f" points="300,150 380,200 380,340 300,390 220,340 140,185"/>

  <!-- Legend -->
  <g transform="translate(20, 20)">
    <rect x="0" y="0" width="12" height="12" rx="2" fill="#002FA7"/>
    <text x="18" y="10" class="legend-text">Alice - Data Analyst</text>

    <rect x="0" y="20" width="12" height="12" rx="2" fill="#E63946"/>
    <text x="18" y="30" class="legend-text">Bob - Data Scientist</text>

    <rect x="0" y="40" width="12" height="12" rx="2" fill="#2A9D8F"/>
    <text x="18" y="50" class="legend-text">Clara - Data Engineer</text>

    <rect x="0" y="60" width="12" height="12" rx="2" fill="#F4A261"/>
    <text x="18" y="70" class="legend-text">David - ML Engineer</text>

    <rect x="0" y="80" width="12" height="12" rx="2" fill="#9B5DE5"/>
    <text x="18" y="90" class="legend-text">Emma - Chef Projet</text>

    <rect x="0" y="100" width="12" height="12" rx="2" fill="#00B4D8"/>
    <text x="18" y="110" class="legend-text">Fabien - Data Architect</text>
  </g>

</svg>
</div>
"""

st.components.v1.html(ANIMATED_RADAR_HTML, height=550)

st.markdown("""
<div style="text-align:center;color:#57534e;font-size:14px;margin-top:-20px;">
<strong>6 experts</strong> · Chacun excelle dans son domaine · Ensemble, ils couvrent tous les besoins data
</div>
""", unsafe_allow_html=True)

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
