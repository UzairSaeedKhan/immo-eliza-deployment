import os
import requests
import streamlit as st
from dotenv import load_dotenv
from labels import (
    PROVINCE_OPTIONS, TYPE_PROPERTY_OPTIONS, SUBTYPE_PROPERTY_OPTIONS,
    SUN_EXPOSURE_LABELS, HEATING_TYPE_LABELS, STATE_OF_PROPERTY_LABELS,
    EPC_SCORE_LABELS, FLOODING_AREA_LABELS, CITY_OPTIONS

)
load_dotenv()

try: # error handling so that st.secrets doesnt send any error if it doesnt find api_url
    API_URL = st.secrets["API_URL"] 
except (FileNotFoundError, KeyError):
    API_URL = "http://localhost:8000/predict"

API_URL = API_URL + "/predict"
# st.title("Immo Eliza Price Predictor")

def label_select(label, options_dict):
    """Show human-readable labels, return the underlying raw value."""
    display = st.selectbox(label, list(options_dict.values()))
    return next(k for k, v in options_dict.items() if v == display)


st.set_page_config(layout="wide", page_title="Immo Eliza Price Predictor")

# Inject Custom CSS for the Hero banner, Grids, and Result Card
st.markdown("""
<style>
    /* Global Background (Secondary 30%: Pure Off-White) */
    .stApp {
        background-color: #f1f5f9; 
    }

    /* Customized Form Container: Now a distinct, soft light-blue shade */
    div[data-testid="stForm"] {
        background-color: linear-gradient(135deg, #7A91B1 0%, #4A6288 100%);
        border-radius: 16px;
        padding: 35px;
        border: 1px solid rgba(93, 117, 153, 0.2); 
        box-shadow: 0px 10px 30px rgba(93, 117, 153, 0.08); 
    }

    /* Form Section Headings (Primary 60%: Slate Blue) */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #5D7599; 
        margin-top: 35px;
        margin-bottom: 20px;
        border-bottom: 2px solid rgba(93, 117, 153, 0.25);
        padding-bottom: 8px;
    }
    
    /* Input Labels (Dark Text: Deep Black) */
    .stWidget label p {
        color: #0F172A !important; 
        font-weight: 600; 
        font-size: 0.95rem;
    }
    
    /* Centers the button container within the Streamlit form */
    div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 1.5rem !important; /* Adds breathing room above the button */
        margin-bottom: 1.5rem !important; /* Adds breathing room below the button */
    }

    /* Extra large, high-impact action button */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #5E769A !important; 
        color: #FFFFFF !important;
        font-weight: 700 !important; /* Bumped to bold for high legibility */
        font-size: 1.4rem !important; /* Substantially larger text */
        letter-spacing: 0.5px !important; /* Subtle spacing makes large text look premium */
        border: none !important;
        border-radius: 50px !important; /* Perfect pill shape */
        width: auto !important; 
        padding: 1.1rem 4rem !important; /* Generous padding for a massive, clickable hit-box */
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); /* Smoother, high-end animation transition */
        
        /* Layered drop shadow to make the button look like it physically floats */
        box-shadow: 0px 10px 25px rgba(94, 118, 154, 0.4), 
                    0px 4px 10px rgba(94, 118, 154, 0.2) !important; 
        cursor: pointer !important;
    }

    /* Eye-catching hover animation */
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #4A5D7B !important; 
        transform: translateY(-3px); /* Lifts higher off the screen when hovered */
        
        /* Deepens shadow on hover to simulate moving closer to the user */
        box-shadow: 0px 15px 30px rgba(94, 118, 154, 0.5), 
                    0px 6px 15px rgba(94, 118, 154, 0.3) !important;
    }

    /* Satisfying click animation */
    div[data-testid="stFormSubmitButton"] button:active {
        transform: translateY(-1px); /* Sinks down slightly when physically clicked */
        box-shadow: 0px 6px 15px rgba(94, 118, 154, 0.4) !important;
    }

            

    /* High-Impact Popping Valuation Output Card */
    .result-card {
        background-color: #e2e8f0; 
        border-left: 8px solid #10B981; /* Green accent bar to symbolize money/valuation */
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-top: 35px;
        
        /* This forces the element to pop outward visually */
        transform: scale(1.02); 
        box-shadow: 0px 15px 40px rgba(16, 185, 129, 0.15); /* Vibrant green glow shadow effect */
        
        /* Smooth entry animation */
        animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes popUp {
        from { transform: scale(0.95); opacity: 0; }
        to { transform: scale(1.02); opacity: 1; }
    }
    
    .result-price {
        font-size: 3.5rem; /* Larger font size to stand out */
        font-weight: 800;
        color: #10b981; /* Premium Emerald Green */065f46
        margin: 10px 0;
        letter-spacing: -1px;
    }

    /* Original Hero Banner Layout (Unchanged) */
    .hero-container {
        background: linear-gradient(135deg, #7A91B1 0%, #4A6288 100%);
        padding: 50px;
        border-radius: 20px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 40px;
    }
    .hero-text {
        flex: 1.2;
        padding-right: 30px;
    }
    .hero-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 15px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        line-height: 1.5;
    }
    .hero-image-container {
        flex: 0.8;
        display: flex;
        justify-content: center;
    }
    .hero-image {
        max-width: 100%;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
    }
    /* Custom Fun Facts Card Styling */
    .fun-fact-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px 25px;
        margin-top: 20px;
        border: 1px dashed #5D7599;
        box-shadow: 0px 4px 15px rgba(93, 117, 153, 0.05);
    }
    .fun-fact-title {
        color: #3B82F6;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .fun-fact-text {
        color: #4A5568;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ßRender the Hero Section at the top
hero_html = """
<div class="hero-container">
    <div class="hero-text">
        <div class="hero-title">We’ll estimate the price of your Dream House</div>
        <div class="hero-subtitle">Fill out the structural details and location parameters below. Our machine learning model will calculate an instant, realistic Belgian market valuation.</div>
    </div>
    <div class="hero-image-container">
        <img class="hero-image" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=700&q=80">
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)


# Form Section
with st.form("property_form"):
    
    # --- ROW 1: LOCATION & PROPERTY IDENTITY ---
    st.markdown('<div class="section-header">📍 Location & Property Identity</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        province = st.selectbox("Province", PROVINCE_OPTIONS)
        type_property = st.selectbox("Property Type", TYPE_PROPERTY_OPTIONS)
    with col2:
        selected_label = st.selectbox("City / Postal Code", sorted(CITY_OPTIONS.keys()))
        selected_entry = CITY_OPTIONS[selected_label]
        postal_code = int(selected_entry["zip"])
        city = selected_entry["city"]
        construction_year = st.number_input("Construction Year", min_value=1800, max_value=2026, step=1, value=2000)
    with col3:
        subtype_property = st.selectbox("Property Subtype", SUBTYPE_PROPERTY_OPTIONS)

    # --- ROW 2: STRUCTURE & DIMENSIONS ---
    st.markdown('<div class="section-header">📐 Structure & Dimensions</div>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        livable_surface = st.number_input("Livable Surface (m²)", min_value=0.0, value=120.0)
        facades = st.number_input("Facades", min_value=0, step=1, value=2)
    with col5:
        bedrooms = st.number_input("Bedrooms", min_value=0.0, step=1.0, value=3.0)
        toilets = st.number_input("Toilets", min_value=0, step=1, value=1)
        # latitude = st.number_input("Latitude", format="%.6f", value=50.8503) # Defaulting to Brussels coordinates
    with col6:
        bathrooms = st.number_input("Bathrooms", min_value=0, step=1, value=1)
        # longitude = st.number_input("Longitude", format="%.6f", value=4.3517)

    # --- ROW 3: QUALITY & RATINGS ---
    st.markdown('<div class="section-header">🛡️ Quality, Ratings & Utilities</div>', unsafe_allow_html=True)
    col7, col8, col9 = st.columns(3)
    
    with col7:
        state_of_property = label_select("State of Property", STATE_OF_PROPERTY_LABELS)
        heating_type = label_select("Heating Type", HEATING_TYPE_LABELS)
    with col8:
        epc_score = label_select("EPC Score", EPC_SCORE_LABELS)
        sun_exposure = label_select("Sun Exposure", SUN_EXPOSURE_LABELS)
    with col9:
        flooding_area_type = label_select("Flooding Area Type", FLOODING_AREA_LABELS)

    # --- ROW 4: AMENITIES (Clean Grid of Checkboxes) ---
    st.markdown('<div class="section-header">✨ Features & Amenities</div>', unsafe_allow_html=True)
    col_t, col_g, col_gar, col_p = st.columns(4)
    
    with col_t:
        terrace = st.checkbox("Terrace ☀️")
    with col_g:
        garden = st.checkbox("Garden 🏡")
    with col_gar:
        garage = st.checkbox("Garage 🚗")
    with col_p:
        swimming_pool = st.checkbox("Swimming Pool 🏊‍♂️")

    # Space formatting before button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Big, wide premium form submit button
    submitted = st.form_submit_button("🔮 Predict Valuation Price", use_container_width=True)


# Handling Response and rendering custom Layout Output
if submitted:
    payload = {
        "province": province, "type_property": type_property,
        "postal_code": postal_code,
        "city": city,
        "subtype_property": subtype_property, "livable_surface": livable_surface,
        "latitude": 0, "longitude": 0, 
        "facades": facades,
        "bedrooms": bedrooms, "bathrooms": bathrooms, "toilets": toilets,
        "construction_year": construction_year, "heating_type": heating_type,
        "sun_exposure": sun_exposure, "state_of_property": state_of_property,
        "epc_score": epc_score, "flooding_area_type": flooding_area_type,
        "terrace": int(terrace), "garden": int(garden),
        "garage": int(garage), "swimming_pool": int(swimming_pool),
    }
    
    # 1. Create a clean container for the loading state layout
    loading_container = st.empty()
    fact_container = st.empty()
    
    # 2. Display the loading spinner and the fun fact card side-by-side or stacked
    with loading_container:
        st.spinner("Crunching data and analyzing regional Belgian trends... Please wait.")
        
    # Inject the HTML + Self-Rotating JavaScript Card
    with fact_container:
        st.markdown("""
        <div class="fun-fact-card">
            <div class="fun-fact-title">💡 Did You Know? </div>
            <p id="fact-text" class="fun-fact-text">Loading insights...</p>
        </div>

        <script>
            // Define your array of fun facts
            const facts = [
                "Brussels and Flemish Brabant consistently rank as the most expensive regions for property in Belgium. Conversely, you'll generally find the most budget-friendly prices in the beautiful, rural areas of Namur and Luxembourg.",
                "Property value in Belgium is heavily influenced by energy performance. Homes with an 'A' or 'B' EPC score sell significantly faster and can fetch up to a 10-15% premium compared to similar energy-inefficient properties.",
                "Historical charm comes at a price! Many Belgian cities feature protected facades or historic zoning regulations. While stunning, renovating a designated heritage property can introduce structural requirements that impact overall valuation."
            ];

            // Pick a totally random starting index
            let currentIndex = Math.floor(Math.random() * facts.length);
            
            const factElement = document.getElementById('fact-text');
            
            // Set initial random fact immediately
            factElement.innerText = facts[currentIndex];

            // Set up a 10-second interval to gracefully swap facts
            setInterval(() => {
                currentIndex = (currentIndex + 1) % facts.length;
                factElement.innerText = facts[currentIndex];
            }, 10000); // 10000ms = 10 seconds
        </script>
        """, unsafe_allow_html=True)
        
    try:
        # Trigger actual backend calculation
        response = requests.post(API_URL, json=payload)
        
        # Clear loading placeholders once data returns safely
        loading_container.empty()
        fact_container.empty()
        
        if response.status_code == 200:
            prediction_value = response.json()['prediction']
            
            # Render your high-impact animated emerald-green result block
            st.markdown(f"""
            <div class="result-card">
                <h3 style="margin: 0; color: #5D7599; font-weight: 600; font-size: 1.3rem;">Estimated Market Valuation</h3>
                <div class="result-price">€{prediction_value:,.2f}</div>
                <p style="color: #64748B; margin: 0; font-size: 0.95rem; font-weight: 500;">
                    Calculated successfully using Immo Eliza AI algorithms.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error(f"Error: {response.json().get('detail')}")
            
    except Exception as e:
        loading_container.empty()
        fact_container.empty()
        st.error(f"Could not connect to backend API: {e}")