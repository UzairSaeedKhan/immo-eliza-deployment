import os
import requests
import streamlit as st
from dotenv import load_dotenv
from labels import (
    PROVINCE_OPTIONS, TYPE_PROPERTY_OPTIONS, SUBTYPE_PROPERTY_OPTIONS,
    SUN_EXPOSURE_LABELS, HEATING_TYPE_LABELS, STATE_OF_PROPERTY_LABELS,
    EPC_SCORE_LABELS, FLOODING_AREA_LABELS,
)

load_dotenv()
try: # error handling so that st.secrets doesnt send any error if it doesnt find api_url
    API_URL = st.secrets["API_URL"]
except (FileNotFoundError, KeyError):
    API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.title("Immo Eliza Price Predictor")

def label_select(label, options_dict):
    """Show human-readable labels, return the underlying raw value."""
    display = st.selectbox(label, list(options_dict.values()))
    return next(k for k, v in options_dict.items() if v == display)

with st.form("property_form"):
    province = st.selectbox("Province", PROVINCE_OPTIONS)
    type_property = st.selectbox("Property Type", TYPE_PROPERTY_OPTIONS)
    subtype_property = st.selectbox("Property Subtype", SUBTYPE_PROPERTY_OPTIONS)

    livable_surface = st.number_input("Livable Surface (m²)", min_value=0.0)
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    facades = st.number_input("Facades", min_value=0, step=1)
    bedrooms = st.number_input("Bedrooms", min_value=0.0, step=1.0)
    bathrooms = st.number_input("Bathrooms", min_value=0, step=1)
    toilets = st.number_input("Toilets", min_value=0, step=1)
    construction_year = st.number_input("Construction Year", min_value=1800, max_value=2026, step=1)

    heating_type = label_select("Heating Type", HEATING_TYPE_LABELS)
    sun_exposure = label_select("Sun Exposure", SUN_EXPOSURE_LABELS)
    state_of_property = label_select("State of Property", STATE_OF_PROPERTY_LABELS)
    epc_score = label_select("EPC Score", EPC_SCORE_LABELS)
    flooding_area_type = label_select("Flooding Area Type", FLOODING_AREA_LABELS)

    terrace = st.checkbox("Terrace")
    garden = st.checkbox("Garden")
    garage = st.checkbox("Garage")
    swimming_pool = st.checkbox("Swimming Pool")

    submitted = st.form_submit_button("Predict Price")

if submitted:
    payload = {
        "province": province, "type_property": type_property,
        "subtype_property": subtype_property, "livable_surface": livable_surface,
        "latitude": latitude, "longitude": longitude, "facades": facades,
        "bedrooms": bedrooms, "bathrooms": bathrooms, "toilets": toilets,
        "construction_year": construction_year, "heating_type": heating_type,
        "sun_exposure": sun_exposure, "state_of_property": state_of_property,
        "epc_score": epc_score, "flooding_area_type": flooding_area_type,
        "terrace": int(terrace), "garden": int(garden),
        "garage": int(garage), "swimming_pool": int(swimming_pool),
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        st.success(f"Estimated price: €{response.json()['prediction']:,.2f}")
    else:
        st.error(f"Error: {response.json().get('detail')}")