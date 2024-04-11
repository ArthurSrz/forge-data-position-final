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
    {'icon': "far fa-copy", 'label': "Recrutement"}
]

## Set the default tab of the app to "Qualification"
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Qualification"

#initialize selected_data in session state.
if 'selected_data' not in st.session_state:
    st.session_state.selected_data = {}
                
## create a tab to gather the answers from the population to questions added to the database
def gatherizer_tab():
    
    st.title("Recrutement des profils data")
    st.markdown("Bienvenue sur le formulaire de recrutement. Répondez aux questions pour valider votre candidature. Nous reviendrons vers vous très vite.")
    
    
    
    ## create an empty dataframe to store the answers
    df_answers = pd.DataFrame(columns=['nom', 'prenom', 'mail', 'question', 'reponse', 'score','profile_type'])
    
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
    
    
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables/{table_id}/records"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data0 = response.json()
        columns = data0['records'][0]['fields'].keys()
        #print(list(columns)[0])
        # Process the data as needed
    else:
        print(f"Request failed with status code {response.status_code}")

    records = data0['records']
    grist_question_df = pd.json_normalize(records, sep='_')

    ## clean the column names to display them in a nice way in the app
    grist_question_df.columns = [col.replace('fields_', '') for col in grist_question_df.columns]
    print(grist_question_df)
    
    
    
    ## If google spreadsheet was chosen, add content from the google spreadsheet 
    #question_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
    #spreadsheet_question_df = pd.DataFrame(question_data)
    
   
    grist_question_df = grist_question_df 
    
    
    profiles = config['profiles'].iloc[-1]
    selected_profiles = profiles.split(", ")
    
    #get the list of selected profils present in st.session_state.profiles
    #selected_profiles = st.session_state.profiles
    st.write(selected_profiles)
    ## from the database, select the screening questions
    introduction_question_df = grist_question_df[(grist_question_df.question_type == "screening") & (grist_question_df.profile_type.isin(selected_profiles))]
    unique_introduction_questions = introduction_question_df.question.unique()

    #from the data, filter only the expertise data related to the selected profiles
    unique_expertise_questions = grist_question_df[(grist_question_df.question_type == "expertise") & (grist_question_df.profile_type.isin(selected_profiles))]
    
    #from the data, filter only the mastery data related to the selected profiles
    unique_mastery_questions = grist_question_df[(grist_question_df.question_type == "mastery") & (grist_question_df.profile_type.isin(selected_profiles))]
    
    ## from the data, select the unique questions
    unique_questions = grist_question_df[grist_question_df.question_type == "expertise"].question.unique()
    unique_reponse = grist_question_df[grist_question_df.question_type == "expertise"].reponse.unique()
    
    
    ## create a form to get respondent name and email
    st.header("Qui êtes-vous ? :disguised_face:")
    nom = st.text_input("Nom", key='nom')
    prenom = st.text_input("Prenom", key='prenom')
    mail = st.text_input("Mail", key='mail')
    #append the values of the inputs to the df_answers
    # df_answers = df_answers.append({'nom': nom, 'prenom': prenom, 'mail': mail}, ignore_index=True)
    
    ## create a form to do some profiling
    st.header("Quel(s) profil(s) data êtes-vous ?:male-detective:")
    
    for i, question_people in enumerate(unique_introduction_questions):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i+1000)
        question_type = grist_question_df[grist_question_df.reponse == answer_people].question_type.values
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_vals = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        profile_type_vals = profile_type_vals.tolist()
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people],'question_type':[question_type], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_vals]})
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
        

    
    #if error continue
    
    #df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: x[0])
    
    try:
        df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: x[0])
    except IndexError as e:
        print(f"An IndexError occurred: {e}")
        pass  # continue execution even if an IndexError occurs
    except Exception as e:
        print(f"An error occurred: {e}")
        pass  # continue execution for any other exception
    
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['question_type'] = df_answers['question_type'].apply(lambda x: str(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (str)) else str(x) if isinstance(x, (str)) else str(x))
    
    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
    ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        response = requests.post(url, headers=headers, json=data)
    
    if st.button("Je valide", key=78):
        add_answers_to_grist_table(df_answers, config['table_id'])
        #st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    # Create a form to assess the level of expertise of each respondent
    st.header("Parlons de vous (et de data) :floppy_disk: ")
    
    
    #define what the unique questions are depending on the score for each profile
    df_analyst = grist_question_df[grist_question_df['profile_type'] == 'Data Analyst']
    df_scientist = grist_question_df[grist_question_df['profile_type'] == 'Data Scientist']
    df_dpo = grist_question_df[grist_question_df['profile_type'] == 'Data Protection Officer']
    
    
    
    ############### create a logic to display questionns based on previous response
    
    unique_questions = np.array([])
    
    if df_answers[df_answers['profile_type'] == 'Data Analyst']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_analyst[df_analyst['question_type'] == 'expertise'].question.unique())
    
    if df_answers[df_answers['profile_type'] == 'Data Scientist']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_scientist[df_scientist['question_type'] == 'expertise'].question.unique())
    
    if df_answers[df_answers['profile_type'] == 'Data Protection Officer']['score'].sum() >= 4:
        unique_questions = np.append(unique_questions, df_dpo[df_dpo['question_type'] == 'expertise'].question.unique())
    
    ################ end 
    
    ## for each question, display the question and the possible answers
    for i, question_people in enumerate(unique_questions):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i)
        question_type = grist_question_df[grist_question_df.reponse == answer_people].question_type.values
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_val = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people],'question_type':[question_type], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        
    
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['question_type'] = df_answers['question_type'].apply(lambda x: str(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (str)) else str(x) if isinstance(x, (str)) else str(x))

    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
   ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"],"question_type": record["question_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        response = requests.post(url, headers=headers, json=data)
        
        
    
    
    ## Create a button to add the answers to the Grist table
    if st.button("Je valide"):
        
        add_answers_to_grist_table(df_answers, config['table_id'])])
        st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    st.header("Qu'en est-il de votre expertise (toujours data) :smile: ")
    
    
    #define what the unique questions are depending on the score for each profile
    df_analyst = grist_question_df[grist_question_df['profile_type'] == 'Data Analyst']
    df_scientist = grist_question_df[grist_question_df['profile_type'] == 'Data Scientist']
    df_dpo = grist_question_df[grist_question_df['profile_type'] == 'Data Protection Officer']
    
    ############### create a logic to display questionns based on previous response
    

    unique_questions_mastery = np.array([])

    score_analyst_df = df_answers[df_answers['profile_type'] == 'Data Analyst'] 
    score_scientist_df = df_answers[df_answers['profile_type'] == 'Data Scientist'] 
    score_dpo_df = df_answers[df_answers['profile_type'] == 'Data Protection Officer'] 

    
    
    for score_df in [score_analyst_df, score_scientist_df, score_dpo_df]:
        sum_expertise_score = score_df[score_df['question_type'] == 'expertise']['score'].sum()

        if sum_expertise_score > 6:
            if score_df is score_analyst_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_analyst[df_analyst['question_type'] == 'mastery'].question.unique())
            elif score_df is score_scientist_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_scientist[df_scientist['question_type'] == 'mastery'].question.unique())
            elif score_df is score_dpo_df:
                unique_questions_mastery = np.append(unique_questions_mastery, df_dpo[df_dpo['question_type'] == 'mastery'].question.unique())
    
    
    
    
    ################ end 
    
    ## for each question, display the question and the possible answers
    for i, question_people in enumerate(unique_questions_mastery):
        st.write(question_people)
        answer_people = st.selectbox("Votre réponse", grist_question_df[grist_question_df.question == question_people].reponse.unique(), index=None, key = i+104)
        score = grist_question_df[grist_question_df.reponse == answer_people].score.values
        profile_type_val = grist_question_df[grist_question_df.reponse == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people], 'reponse': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        
    
        # Append the data to the df_answers DataFrame
        df_answers = pd.concat([df_answers, df], ignore_index=True)
    
    # convert the score and profile_type columns to int and string
    df_answers['score'] = df_answers['score'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    df_answers['profile_type'] = df_answers['profile_type'].apply(lambda x: int(x[0]) if isinstance(x, np.ndarray) and len(x) > 0 and isinstance(x[0], (int, np.integer)) else int(x) if isinstance(x, (int, np.integer)) else str(x))
    #remove "[]" and " ' " from the profile type column
    df_answers['profile_type'] = df_answers['profile_type'].str.strip('[]').str.strip("'")
    
    
   ## get the names of the tables inside Grist
    subdomain = "docs"
    doc_id = "nSV5r7CLQCWzKqZCz7qBor"
    table_id = "Form3"
    url = f"https://{subdomain}.getgrist.com/api/docs/{doc_id}/tables"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tables = response.json()
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    #create a function to add the answers to the st.session_state
    def add_answers_to_grist_table(df_answers, table_id):

        # Convert DataFrame to list of records
        records = [{"fields": {"nom":record["nom"],"prenom":record["prenom"],"question":record["question"],"reponse":record["reponse"],"mail":record["mail"],"score": record["score"], "profile_type": record["profile_type"]}} for record in df_answers.to_dict(orient='records')]
        
        # Prepare the request body
        data = {"records": records}
        docId = "nSV5r7CLQCWzKqZCz7qBor"
        tableId = table_id

        # Use the Grist API to add the new rows to the specified Grist table
        url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
        
        
        response = requests.post(url, headers=headers, json=data)
        
        
    
    
    ## Create a button to add the answers to the Grist table
    if st.button("Je valide", key = 201):
        
        add_answers_to_grist_table(df_answers, config['table_id'])
        st.session_state.selected_data = df_answers
        #conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    
    # Now, outside the loop, you can display the complete df_answers DataFrame
    #st.dataframe(df_answers)
    
# Le vent souffla plus fort alors que le programmeur invoquait le puissant radar graph pour analyser la distribution des profils. 
# Des profils émergeaient, formant des constellations dans le ciel de données.


# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Recrutement":
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
