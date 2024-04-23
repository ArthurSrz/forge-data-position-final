import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import hydralit_components as hc
from streamlit_elements import nivo, elements, mui, html
from grist_api import GristDocAPI
import requests
import json
import streamlit as st
import numpy as np
import json
import time
import altair as alt
import st_static_export as sse

## Set the page title and favicon of the app
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
custom_html = """
<div class="banner">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge_vf.png?raw=true" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        padding: 10px;
        
    }
    .banner img {
        max-width: 100%;
        max-height: 100%;
    }
</style>
"""

##Instantiate the static export class
css_text = """
table, th, td {
border: 1px solid black;
border-collapse: collapse;
}
tr:nth-child(even) {background-color: #f2f2f2;}
.table{
    width:100%;
}
.footn{
color:#c0c0c0;
}
"""

static_html = sse.StreamlitStaticExport(css=css_text)

## Display the custom HTML
st.components.v1.html(custom_html)

## Set up the Google Sheets connection in case the user wants to handle its Data Position from a google sheet
conn = st.connection("gsheets", type=GSheetsConnection)

## Set up the Grist API connection in case the user wants to handle its Data Position from a Grist database
SERVER = "https://docs.getgrist.com"
DOC_ID = "nSV5r7CLQCWzKqZCz7qBor"
API_KEY = "3a00dc02645f6f36f4e1c9449dd4a8529b5e9149"

## Initialize GristDocAPI with document ID, server, and API key
api = GristDocAPI(DOC_ID, server=SERVER, api_key=API_KEY)

## Load the data from Grist
#api_key = st.secrets["grist_api_key"]
api_key = "3a00dc02645f6f36f4e1c9449dd4a8529b5e9149"

headers = {
    "Authorization": f"Bearer {api_key}"
}

## Load Form2 from Grist
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_2 = "Form2"
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_2}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    #print("Houra")
    columns = data['records'][0]['fields'].keys()
    #print(list(columns)[0])
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")

## Load Form3 from Grist
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_3 = "Form3"
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_3}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data2 = response.json()
    #print("Houra")
    columns = data2['records'][0]['fields'].keys()
    #print(list(columns)[0])
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")

## Load Form0 from Grist
subdomain = "docs"
doc_id = "nSV5r7CLQCWzKqZCz7qBor"
table_id_0 = "Form0"
url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id_0}/records"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data0 = response.json()
    columns = data0['records'][0]['fields'].keys()
    #print(list(columns)[0])
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")


## generate the different tabs of the app
menu_data = [
    {'icon': "far fa-copy", 'label': "Position"},
]

## Set the default tab of the app to "Qualification"
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Qualification"

#initialize selected_data in session state.
if 'selected_data' not in st.session_state:
    st.session_state.selected_data = {}
# La mission était claire : sauver le royaume des données...
# ...en recrutant les profils data les plus qualifiés.


def dispenser_tab():
    
    #Load config data from Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Config"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        config = response.json()
        columns = config['records'][0]['fields'].keys()
        #print(list(columns)[0])
        # Process the data as needed
    else:
        print(f"Request failed with status code {response.status_code}")

    config = config['records']
    config = pd.json_normalize(config, sep='_')
    config.columns = [col.replace('fields_', '') for col in config.columns]
    
    ## Load Data from Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = config['table_id'].iloc[-1]
    
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Houra")
        columns = data['records'][0]['fields'].keys()
        #print(list(columns)[0])
        # Process the data as needed
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #turn data into a dataframe with columns "nom","prenom","mail","question","answer","score","profile_type"
    records = data['records']
    data = pd.json_normalize(records, sep='_')
    data.columns = [col.replace('fields_', '') for col in data.columns]
    
    
    st.header("Position des profils")
    st.markdown("Grâce au _radar graph_, analysez la distribution des profils au sein de votre population")
    with elements("nivo_charts"):
        form_data = data
        #filter form data so to delete all rows where "nom" is empty
        # Assuming 'nom' is the column name where you want to check for empty values
        form_data_filtered = form_data[form_data['mail'].str.contains('@')]
        # Obtenez les valeurs uniques de la colonne "nom"
        unique_noms = form_data_filtered['nom'].unique()

        # Créez la structure de données DATA
        DATA = []

        # Pour chaque profil unique, créez un dictionnaire
        for profile_type in form_data_filtered['profile_type'].unique():
            profile_data = {"profile": profile_type}

            # Parcourez les noms uniques
            for nom in unique_noms:
                # Filtrer le DataFrame pour obtenir les lignes correspondant au nom et profil
                filtered_data = form_data_filtered[(form_data_filtered['nom'] == nom) & (form_data_filtered['profile_type'] == profile_type)]
        
                # Vérifiez s'il y a des données pour le nom et le profil actuels
                if not filtered_data.empty:
                    score = filtered_data['score'].tolist()
                    score = [int(x) for x in score if isinstance(x, (int, np.integer))]
                    total_score = sum(score)
                    profile_data[nom] = total_score
            
            DATA.append(profile_data)

            
        
        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=unique_noms,
                indexBy="profile",
                maxValue = 40,
                valueFormat=">-.2f",
                curve="linearClosed",
                margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                borderColor={ "theme": "grid.line.stroke" },
                gridLabelOffset=36,
                dotSize=8,
                dotColor={ "theme": "background" },
                dotBorderWidth=2,
                motionConfig="wobbly",
                legends=[
                    {
                        "anchor": "top-left",
                        "direction": "column",
                        "translateX": -50,
                        "translateY": -40,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ],
                theme={
                    "background": "#FFFFFF",
                    "textColor": "#31333F",
                    "tooltip": {
                        "container": {
                            "background": "#FFFFFF",
                            "color": "#31333F",
                        }
                    }
                }
            )
    
    
    st.markdown("#### Niveau d'expertise des profils")
    st.markdown("Grâce aux histogrammes, analysez la distribution des scores pour chaque profil")
    
    #make an altair chart to display the data
    df = pd.DataFrame(DATA)
    
    # Filter out rows with empty profile names
    df = df[df['profile'] != ""]
    # Melt the DataFrame to long format for Altair
    df_melted = df.melt(id_vars='profile', var_name='Name', value_name='Value')
    # Create histograms for the distribution of scores for each profile
    charts = alt.Chart(df_melted).mark_bar(opacity=0.7).encode(
        x=alt.X('Value', bin=alt.Bin(maxbins=10), title='Score'),
        y='count()',
        color=alt.Color('profile:N', legend=None)
    ).facet(column='profile', spacing=80, title=None).properties(
        title=''
    ).resolve_axis(x='independent',y='independent')
    
    st.altair_chart(charts)
        
        
        
        
        
        
    
    
# Mais la quête n'était pas terminée. Le héros se plongea dans la création des groupes, attribuant des profils à des cohortes spécifiques. 
# Le tableau se transforma en un champ de bataille stratégique, où chaque programmeur était assigné à sa place.

    #create a df that is form_data df but group by name
    #form_data = form_data[form_data['score'].notna()]
    #form_data['score'] = form_data['score'].astype(int)
    #form_data_grouped = form_data.groupby(['nom', 'prenom'])['score'].mean().reset_index()
    #form_data_grouped['groupe'] = pd.NA
    #st.header("Constitution des groupes")
    #st.markdown("Répartissez les profils au sein de groupes")
    #groups = st.data_editor(
    #    form_data_grouped,
    #    column_config={
    #        "group": st.column_config.NumberColumn(
    #            "Group",
    #            help="What group",
    #            min_value=1,
    #            max_value=10,
    #            step=1,
    #            format="%d 👭",
    #    )
    #    }
    #)
    #st.dataframe(groups)
    #st.write(st.session_state)
    #if st.button("Assigner", key=8):
    #    conn.update(worksheet="Dispenser", data=groups)
    #    st.success("C'est fait !")
        



# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Position":
        dispenser_tab()
#
over_theme = {'txc_inactive': 'white','menu_background':'#1c3f4b','txc_active':'#e95459','option_active':''}
# Create the navigation bar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #home_name='Home',
    #login_name='Logout',
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned'
)

# Get the selected tab label from the menu
selected_tab_label = menu_id

# Display the selected tab content
display_tab_content(selected_tab_label)


# Store the selected tab in the session state
if selected_tab_label != st.session_state.selected_tab:
    st.session_state.selected_tab = selected_tab_label

# Get the id of the menu item clicked
#st.info(f"Selected tab: {selected_tab_label}")
#st.info(f"Menu {menu_id}")

# Et ainsi se termina cette saga épique, où le codeur du monde virtuel triompha des énigmes, manipula les données et forgea un chemin vers la victoire. 
# Un conte de programmation, où chaque ligne de code était une ligne de l'histoire, tissée dans le tissu du royaume virtuel.
