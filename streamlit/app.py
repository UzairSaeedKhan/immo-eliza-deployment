import os
import requests
import streamlit as st
from dotenv import load_dotenv
from styles import get_custom_styles, get_header_card, get_form, get_result_card, get_fun_facts

load_dotenv()

try: # error handling so that st.secrets doesnt send any error if it doesnt find api_url
    API_URL = st.secrets["API_URL"] 
except (FileNotFoundError, KeyError):
    API_URL = "http://localhost:8000"

API_URL = API_URL + "/predict"
# st.title("Immo Eliza Price Predictor")


st.set_page_config(layout="wide", page_title="Immo Eliza Price Predictor")

# Inject Custom CSS for the Hero banner, Grids, and Result Card
get_custom_styles()

# ßRender the Hero Section at the top
get_header_card()


# Render Form Section
submitted, payload = get_form()


# Handling Response and rendering custom Layout Output
if submitted:
    
    # Create a clean container for the loading state layout
    loading_container = st.empty()
    fact_container = st.empty()
    
    # Display the loading spinner and the fun fact card side-by-side or stacked
    with loading_container:
        st.spinner("Crunching data and analyzing regional Belgian trends... Please wait.")
        
    # Render fun facts while waiting for the result
    with fact_container:
        get_fun_facts()
        
    try:
        # Trigger actual backend calculation
        response = requests.post(API_URL, json=payload)
        
        # Clear loading placeholders once data returns safely
        loading_container.empty()
        fact_container.empty()
        
        if response.status_code == 200:
            prediction_value = response.json()['prediction']
            
            # Render result card
            get_result_card(prediction_value)
            
        else:
            st.error(f"Error: {response.json().get('detail')}")
            
    except Exception as e:
        loading_container.empty()
        fact_container.empty()
        st.error(f"Could not connect to backend API: {e}")