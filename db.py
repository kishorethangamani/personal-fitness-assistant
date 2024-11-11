from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ENDPOINT="https://7abd12d4-664a-4187-9e73-37ca6d25ce2c-us-east-2.apps.astra.datastax.com"
TOKEN="AstraCS:xhnTsmQogcOoHcSPZZQrgEZl:02e9875379abadfa799021fb9ae2bcc2ab728817543f80190b0c8cb3355a3e55"


@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

db = get_db()
collection_names = ["personal_data", "notes"]

for collection in collection_names:
    try:
        db.create_collection(collection)
    except:
        pass
    
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")