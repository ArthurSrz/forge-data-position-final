import requests
import os

# Load credentials from environment variables
# Set these before running: export GRIST_API_KEY="your_key" && export GRIST_DOC_ID="your_doc_id"
subdomain = "docs"
docId = os.environ.get("GRIST_DOC_ID", "YOUR_DOC_ID_HERE")
tableId = "Form2"
api_url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
api_key = os.environ.get("GRIST_API_KEY", "YOUR_API_KEY_HERE")
# Set up the API key for authorization
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Prepare the request body
records = [
    {
        "fields": {"nom": "value1", "prenom": "value2"}
    },
    {
        "fields": {"nom": "value3", "prenom": "value4"}
    }
    # Add more records as needed in the same format
]

data = {
    "records": records
}

# Make the POST request
response = requests.post(api_url, headers=headers, json=data)
# Check the response status
if response.status_code == 200:
    print("Records added successfully!")
else:
    print("Error adding records. Status code:", response.status_code)
    print("Error message:", response.text)