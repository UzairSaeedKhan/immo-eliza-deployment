import requests
import streamlit as st
import random
from styles import get_custom_styles, get_header_card, get_form, get_result_card, get_fun_facts

try: # error handling so that st.secrets doesnt send any error if it doesnt find api_url
    API_URL = st.secrets["API_URL"] 
except (FileNotFoundError, KeyError):
    API_URL = "http://localhost:8000"

API_URL = API_URL + "/predict"

st.set_page_config(layout="wide", page_title="Immo Eliza Price Predictor")

# Inject Custom CSS for the Hero banner, Grids, and Result Card
get_custom_styles()

# Render the header section
get_header_card()

# Render Form Section
submitted, payload = get_form()


# Handling Response and rendering custom Layout Output
if submitted:
    
    # Hardcoded facts
    facts = [
        "Brussels and Flemish Brabant consistently rank as the most expensive regions for property in Belgium. Conversely, you'll generally find the most budget-friendly prices in the beautiful, rural areas of Namur and Luxembourg.",
        "Property value in Belgium is heavily influenced by energy performance. Homes with an 'A' or 'B' EPC score sell significantly faster and can fetch up to a 10-15% premium compared to similar energy-inefficient properties.",
        "Historical charm comes at a price! Many Belgian cities feature protected facades or historic zoning regulations. While stunning, renovating a designated heritage property can introduce structural requirements that impact overall valuation."
    ]
    
    # Pick a random fact
    selected_fact = random.choice(facts)
    
    # Create a clean container for the loading state layout
    loading_container = st.empty()
    fact_container = st.empty()
    
    # Display the loading spinner and the fun fact card side-by-side or stacked
    with loading_container:
        st.spinner("Crunching data and analyzing regional Belgian trends... Please wait.")
        
    # Pass the randomly selected fact straight into your style function
    with fact_container:
        get_fun_facts(selected_fact)
        
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