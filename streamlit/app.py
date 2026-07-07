import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/predict") # defaults to the localhost if api_url is not found

st.title("Immo Eliza Price Predictor")

with st.form("property_form"):
    province = st.selectbox("Province", ["brussels", "antwerp", "..."])  # full list later
    type_property = st.selectbox("Property Type", ["house", "apartment"])
    livable_surface = st.number_input("Livable Surface (m²)", min_value=0.0)
    bedrooms = st.number_input("Bedrooms", min_value=0.0)
    submitted = st.form_submit_button("Predict Price")

if submitted:
    payload = {
        "province": province,
        "type_property": type_property,
        "livable_surface": livable_surface,
        "bedrooms": bedrooms,
        # remaining required fields...
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        st.success(f"Estimated price: €{response.json()['prediction']:,.2f}")
    else:
        st.error(f"Error: {response.json().get('detail')}")