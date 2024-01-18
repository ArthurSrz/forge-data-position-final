
# Le vent glacial s'engouffrait dans le code balayant les lignes de pandas et les colonnes de Streamlit. 
# C'était une nuit sombre dans le monde virtuel de Forge Data, où les profils data se dissimulaient dans l'ombre du code.


## Import the required tool (libraries) to build the app

### pandas for data manipulation
import pandas as pd
### streamlit for the app
import streamlit as st
### streamlit_gsheets so to connect the app Google Sheets
from streamlit_gsheets import GSheetsConnection
### hydralit to display a nice navigation bar
import hydralit_components as hc
### streamlit_elements to display the radar graph where the position of individuals will be displayed
from streamlit_elements import nivo, elements, mui, html
### Grist API so to connect the app to a Grist database
from grist_api import GristDocAPI
### requests to use the Grist API
import requests
### json to transform json files returned by the Grist API into a dataframe
import json
import streamlit as st
import numpy as np
import json

# Le héros, un valeureux programmeur, maniait son clavier comme une épée..
#...naviguant entre les méandres de GSheets et les terres inexplorées de Streamlit.


## Set the page title and favicon of the app
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
custom_html = """
<div class="banner">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true" alt="Banner Image">
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
    print("Houra")
    columns = data['records'][0]['fields'].keys()
    print(list(columns)[0])
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
    print("Houra")
    columns = data2['records'][0]['fields'].keys()
    print(list(columns)[0])
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
    print(list(columns)[0])
    # Process the data as needed
else:
    print(f"Request failed with status code {response.status_code}")


## generate the different tabs of the app
menu_data = [
    {'icon': "far fa-copy", 'label': "Qualification"},
    {'icon': "far fa-copy", 'label': "Recrutement"},
    {'icon': "far fa-copy", 'label': "Position"},
]

## Set the default tab of the app to "Qualification"
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Qualification"

# La mission était claire : sauver le royaume des données...
# ...en recrutant les profils data les plus qualifiés.


## Create a tab to add the answers to the database
def colorizer_tab():
    st.title("Table de qualification des profils data")
    st.markdown("Vous envisagez de classer une population en différents profils _data_.")
    st.markdown("Chaque **profil data** correspond à un ensemble de compétences auxquelles sont associées un certain niveau de maitrise. ") 
    st.markdown("Pour évaluer le niveau de maitrise, vous poserez à la population des **questions** ")
    st.markdown("A chaque question est associé un ensemble de 4 **réponses** possibles.")
    st.markdown("Chaque réponse correspond à un certain **niveau de maîtrise**")
    
    st.header("Liste des questionnaires de la communauté")
    col1, col2, col3 = st.columns(3)
    
    # Create elements with the different data positions that can be used
    with col1:
        with st.container(border=True):
            st.text("Data Position Maitre")
            expander = st.expander("Description")
            expander.write("Hello")
            if st.button("Charger le data position",type="primary", key=1):
                st.session_state.selected_data = data2
                st.session_state.table_id = table_id_3
                st.success("Data position chargé 🚚")
        with st.container(border=True):
            st.text("Data Position pour Hackathon")
            expander = st.expander("Description")
            expander.write("Hello")
            if st.button("Charger le data position",type="primary", key=2):
                st.session_state.selected_data = data
                st.session_state.table_id = table_id_2
                st.success("Data position chargé 🚚")
        with st.container(border=True):
            st.text("k")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=3)
    with col2:
        with st.container(border=True):
            st.text("h")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=4)
        with st.container(border=True):
            st.text("w")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=5)
        with st.container(border=True):
            st.text("k")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=6)
    with col3:
        with st.container(border=True):
            st.text("h")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=7)
        with st.container(border=True):
            st.text("w")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=8)
        with st.container(border=True):
            st.text("k")
            expander = st.expander("Description")
            expander.write("Hello")
            st.button("Charger le data position",type="primary", key=9)
    


    col1, col2 = st.columns(2)
    
    ## Create a storage where the data will be stored dynamically
    if 'data' not in st.session_state:
        st.session_state.data = {
            'profile_type':[],
            'question': [],
            'answer': [],
            'score': []
        }
# Tandis que le programmeur avançait, les énigmes se dressaient sur son chemin. 
# Des questions sur les compétences, des réponses à choisir, des niveaux de maîtrise à déterminer. Chaque ligne de code était une bataille, chaque requête une épreuve.
    
    ## Create the form to add questions to the Grist table
    with col1:
        st.header('Ma :blue[table] :sunglasses:')
        profile_type = st.text_input("Le profil")
        question = st.text_input("La question")
        reponse = st.text_input("Une réponse possible")
        score = st.selectbox("Le niveau de maitrise associé", [1, 2, 3, 4])
        
        # Le héros se heurta à une forteresse appelée Grist API, où des clés secrètes ouvraient les portes des données convoitées. 
        # Les réponses étaient extraites, les colonnes alignées, et le programmeur se fraya un chemin à travers le labyrinthe des requêtes HTTP.
        
        ## Create a function to add the answers to the Grist table
        def add_data_to_grist_table(profile_type, question, reponse, score):
            # Create a new row with the provided data
            new_records = [
                {'profile_type': profile_type, 'question': question, 'reponse': reponse, 'score': score}
                ]

            # Use the Grist API to add the new row to the Grist table
            api.add_records('Form0', new_records)
        
        ## Button to add questions to Grist
        if st.button("Ajouter", key=78):
            # Add the input values to Grist table
            add_data_to_grist_table(profile_type, question, reponse, score)
            st.session_state.selected_data = data0
            st.session_state.table_id = table_id_0
            st.success("Data added to Grist table")
        
        ## Button to add questions Google spreadsheet

        #if st.button("Ajouter", key=10):
        #    st.session_state.data['profile_type'].append(profile_type)
        #    st.session_state.data['question'].append(question)
        #    st.session_state.data['answer'].append(answer)
        #    st.session_state.data['score'].append(score)
        #    # Combine the existing data from Google Sheets and new data
        #    existing_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
        #    existing_df = pd.DataFrame(existing_data)
        #    #st.write("Existing Data:")
        #    #st.dataframe(existing_df)
        #    new_df = pd.DataFrame(st.session_state.data)
        #    #st.write("New Data:")
        #    #st.dataframe(new_df)
        #    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        #    #st.write("Combined Data:")
        #    #st.dataframe(combined_df)
        #    conn.update(worksheet="Colorizer", data=combined_df)
        #    st.success("Data added to Google Sheets")
        #    st.session_state.data = {
        #        'profile_type': [],
        #        'question': [],
        #        'answer': [],
        #        'score': []
        #    }

    
    with col2:
        ## display an image with inspiration for the question that can be asked
        st.header(':blue[Inspiration] :star-struck:')
        st.image("resource/skills_framework.png")
         
                    
## create a tab to gather the answers from the population to questions added to the database
def gatherizer_tab():
    st.title("Recrutement des profils data")
    st.markdown("Bienvenue sur le formulaire de recrutement. Répondez aux questions pour valider votre candidature. Nous reviendrons vers vous très vite.")
    
    ## Check if there are data available loaded
    if 'selected_data' not in st.session_state:
        st.warning("Please select data in the Colorizer tab first.")
        return

    
    
    ## create an empty dataframe to store the answers
    df_answers = pd.DataFrame(columns=['nom', 'prenom', 'mail', 'question', 'reponse', 'score','profile_type'])
    
    ## if grist was used, transform the json file into a dataframe
    grist_question_df = pd.json_normalize(st.session_state.selected_data['records'])
    
    ## clean the column names to display them in a nice way in the app
    grist_question_df.columns = [col.replace('fields.', '') for col in grist_question_df.columns]
    
    
    ## If google spreadsheet was chosen, add content from the google spreadsheet 
    #question_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
    #spreadsheet_question_df = pd.DataFrame(question_data)
    
   
    
    ## from the data, select the unique questions
    unique_questions = grist_question_df.question.unique()
    
    ## create a form to gather the answers from the population
    st.header("Qui êtes-vous ? :disguised_face:")
    nom = st.text_input("Nom", key='nom')
    prenom = st.text_input("Prenom", key='prenom')
    mail = st.text_input("Mail", key='mail')
    #append the values of the inputs to the df_answers
    df_answers = df_answers.append({'nom': nom, 'prenom': prenom, 'mail': mail}, ignore_index=True)
    st.header("Parlons de vous (et de data) :floppy_disk: ")

    ## for each question, display the question and the possible answers
    for question_people in unique_questions:
        st.write(question_people)
        answer_people = st.selectbox("Answers", grist_question_df[grist_question_df.question == question_people].reponse, index=None)
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_val = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        # Append the data to the df_answers DataFrame
        df_answers = df_answers.append(df, ignore_index=True)
    
    print(st.session_state)
    print(df_answers)
    
   #  
   ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        # get the names of the tables
        for table in tables["tables"]:
            print(table['id'])
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):
        st.dataframe(df_answers)
        # Convert the "score" and "profile_type" columns to a more suitable data type (e.g., list)
        df_answers["score"] = df_answers["score"].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
        df_answers["profile_type"] = df_answers["profile_type"].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

        # Fill NaN values with None for all columns
        df_answers = df_answers.applymap(lambda x: None if pd.isna(x) else x)
        
        st.write(str(table_id))
        
        # Convert DataFrame to list of records
        records = [{"fields": record} for record in df_answers.to_dict(orient='records')]
        st.write(records)
        # Prepare the request body
        data = {"records": records}
        st.write(data)
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        st.write(url)
        
        
        response = requests.post(url, headers=headers, json=data)
        st.write(response)
        st.write(response.text)
        
    print("The last table id" + str(st.session_state.table_id))
    
    ## Create a button to add the answers to the Grist table
    if st.button("Je valide"):
        add_answers_to_grist_table(df_answers, st.session_state.table_id)
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    # Now, outside the loop, you can display the complete df_answers DataFrame
    #st.dataframe(df_answers)
    
# Le vent souffla plus fort alors que le programmeur invoquait le puissant radar graph pour analyser la distribution des profils. 
# Des profils émergeaient, formant des constellations dans le ciel de données.

def dispenser_tab():
    st.header("Position des profils")
    st.markdown("Grâce au _radar graph_, analysez la distribution des profils au sein de votre population")
    with elements("nivo_charts"):
        form_data = conn.read(worksheet="Gatherizer", usecols=["nom","prenom","mail","question","answer","score","profile_type"],ttl=0, nrows=10) 
        # Obtenez les valeurs uniques de la colonne "nom"
        unique_noms = form_data['nom'].unique()

        # Créez la structure de données DATA
        DATA = []

        # Pour chaque profil unique, créez un dictionnaire
        for profile_type in form_data['profile_type'].unique():
            profile_data = {"profile": profile_type}

            # Parcourez les noms uniques
            for nom in unique_noms:
                # Filtrer le DataFrame pour obtenir les lignes correspondant au nom et profil
                filtered_data = form_data[(form_data['nom'] == nom) & (form_data['profile_type'] == profile_type)]
        
                # Vérifiez s'il y a des données pour le nom et le profil actuels
                if not filtered_data.empty:
                    score = int(filtered_data['score'].str.strip('[]').values[0])
                    profile_data[nom] = score

            DATA.append(profile_data)

        # Affichez la liste DATA
        #st.write(DATA)

        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=unique_noms,
                indexBy="profile",
                maxValue = 4,
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
# Mais la quête n'était pas terminée. Le héros se plongea dans la création des groupes, attribuant des profils à des cohortes spécifiques. 
# Le tableau se transforma en un champ de bataille stratégique, où chaque programmeur était assigné à sa place.

    #create a df that is form_data df but group by name
    form_data = form_data[form_data['score'].notna()]
    form_data['score'] = form_data['score'].str.strip('[]').astype(int)
    form_data_grouped = form_data.groupby(['nom', 'prenom'])['score'].mean().reset_index()
    form_data_grouped['groupe'] = pd.NA
    st.header("Constitution des groupes")
    st.markdown("Répartissez les profils au sein de groupes")
    groups = st.data_editor(
        form_data_grouped,
        column_config={
            "group": st.column_config.NumberColumn(
                "Group",
                help="What group",
                min_value=1,
                max_value=10,
                step=1,
                format="%d 👭",
        )
        }
    )
    #st.dataframe(groups)
    #st.write(st.session_state)
    if st.button("Assigner", key=8):
        conn.update(worksheet="Dispenser", data=groups)
        st.success("C'est fait !")
        



# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Qualification":
        colorizer_tab()
    elif tab_label == "Recrutement":
        gatherizer_tab()
    elif tab_label == "Position":
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