import streamlit as st
# ----------------------------
# 🚀 Step 1: Page Configuration
# ----------------------------
st.set_page_config(page_title="Drug Analysis & Recommendation", layout="wide")
import pandas as pd
import random
from bs4 import BeautifulSoup
import requests
from utils.data_processing import load_data
from importlib import import_module  # Dynamically import pages
from health_tips import get_health_tip  # Import the function

df = load_data()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Custom Dark Medical Theme for Streamlit with Synced Sidebar
st.markdown(
    """
    <style>
    /* Dark Background Gradient - Smoother */
    .stApp {
        background: linear-gradient(to right, #0A2A56, #011023);
        color: #d4d4d4;
        font-family: 'Arial', sans-serif;
    }

    /* Sidebar Styling - Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(25, 103, 167, 0.9);
        backdrop-filter: blur(12px);
        color: white !important;
        border-right: 3px solid #1e88e5;
        box-shadow: 4px 0px 10px rgba(30, 136, 229, 0.4);
    }

    /* Sidebar Headers */
    [data-testid="stSidebar"] h2 {
        color: #00e5ff !important;
        font-weight: bold;
        text-shadow: 1px 1px 8px rgba(0, 229, 255, 0.5);
    }

    /* Sidebar Labels */
    [data-testid="stSidebar"] .stRadio label {
        color: #FAF9FE !important;
        font-weight: bold;
        font-size: 16px;
    }

    /* Sidebar Hover Effect */
    .stButton > button:hover {
        background-color: #1a73e8 !important;
        transform: scale(1.05);
        transition: all 0.3s ease-in-out;
    }

    /* Headers - Neon Glow */
    h1, h2, h3, h4, h5, h6 {
        color: #00e5ff !important;
        font-weight: bold;
        text-shadow: 1px 1px 15px rgba(0, 229, 255, 0.7);
    }

    /* Streamlit Buttons - Neon Effect */
    .stButton > button {
        background: linear-gradient(to right, #00796b, #004d40);
        color: white !important;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        box-shadow: 2px 2px 12px rgba(0, 188, 212, 0.5);
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #004d40, #00251a);
        box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.6);
        transform: translateY(-2px);
    }

    /* Input Fields - Glassmorphism with Focus Glow */
    .stTextInput>div>div>input {
        background: rgba(10, 25, 47, 0.7) !important;
        backdrop-filter: blur(10px);
        color: white !important;
        border: 2px solid #00bcd4 !important;
        border-radius: 8px;
        padding: 8px;
        transition: all 0.3s ease-in-out;
    }

    .stTextInput>div>div>input:focus {
        box-shadow: 0px 0px 12px rgba(0, 255, 255, 0.6);
        border-color: #00e5ff;
        outline: none;
    }

    /* Chatbot Message Styling - Soft Glow */
    .stChatMessage {
        background: rgba(0, 31, 63, 0.85);
        padding: 12px;
        border-radius: 12px;
        color: white;
        box-shadow: 2px 2px 15px rgba(0, 188, 212, 0.6);
    }

    /* Metric Boxes - Raised Effect */
    .stMetric {
        background: rgba(0, 31, 63, 0.85);
        border-radius: 12px;
        padding: 10px;
        font-size: 18px;
        color: #00e5ff;
        border: 1px solid #00796b;
        box-shadow: 0px 6px 12px rgba(0, 255, 255, 0.4);
        transition: transform 0.3s ease-in-out;
    }

    .stMetric:hover {
        transform: scale(1.05);
    }

    /* Tables - Glassmorphism */
    .stDataFrame {
        background: rgba(10, 25, 47, 0.9) !important;
        color: white !important;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0, 229, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# 🚀 Sidebar: Styled Sections for Better Visibility
# ----------------------------

# 📌 Navigation Section
st.sidebar.title("📌 Navigation")  
# ✅ Custom CSS for Selectbox Inside Color Matching Sidebar Boxes
st.sidebar.markdown(
    """
    <style>
        /* Style the selectbox container */
        div[data-baseweb="select"] {
            background: linear-gradient(to right, #1e3c72, #2a5298) !important;
            border-radius: 10px !important;
            box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5) !important;
            padding: 10px !important;
            color: white !important;
        }

        /* Change background inside the selectbox */
        div[data-baseweb="select"] div {
            background: linear-gradient(to right, #1e3c72, #2a5298) !important;
            color: white !important;
        }

        /* Style dropdown items */
        div[data-baseweb="popover"] {
            background: linear-gradient(to right, #1e3c72, #2a5298) !important;
            border: 1px solid #2a5298 !important;
            border-radius: 10px !important;
        }

        /* Style the dropdown items */
        div[data-baseweb="option"] {
            color: white !important;
            font-weight: bold !important;
            background: linear-gradient(to right, #1e3c72, #2a5298) !important;
        }
        
        /* Hover effect on options */
        div[data-baseweb="option"]:hover {
            background-color: #2a5298 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# ✅ Use selectbox instead of radio (same functionality, but fits inside box)
page = st.sidebar.selectbox(
    "Select a Page:", 
    ["🏠 Home", "📊 Power BI Dashboard", "📈 Data Analysis", 
     "💊 Drug Recommendation", "🔍 Sentiment Analysis", 
     "📅 Forecast Reviews", "🤖 AI Chatbot"]
)

# 💡 Daily Health Tip Section
st.sidebar.title("💡 Daily Health Tip")
st.sidebar.markdown(
    f"""
    <div style="
        background: linear-gradient(to right, #1e3c72, #2a5298);
        padding: 12px;
        border-radius: 10px;
        color: white;
        box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5);
        text-align: center;">
        <p><strong>{get_health_tip()}</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔗 Quick Links Section
st.sidebar.title("🔗 Quick Links")
st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(to right, #1e3c72, #2a5298);
        padding: 12px;
        border-radius: 10px;
        color: white;
        box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5);
        text-align: center;">
        <p>🌐 <a href="https://www.drugs.com/" target="_blank" style="color:white; text-decoration: none;">Drugs.com - Drug Information</a></p>
        <p>🌐 <a href="https://www.webmd.com/" target="_blank" style="color:white; text-decoration: none;">WebMD - Medical Info</a></p>
        <p>🌐 <a href="https://www.mayoclinic.org/" target="_blank" style="color:white; text-decoration: none;">Mayo Clinic - Trusted Advice</a></p>
        <p>🌐 <a href="https://www.goodrx.com/" target="_blank" style="color:white; text-decoration: none;">GoodRx - Drug Discounts</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

# 👨‍💻 Developer Details Section
st.sidebar.title("👨‍💻 Developer Details")
st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(to right, #1e3c72, #2a5298);
        padding: 12px;
        border-radius: 10px;
        color: white;
        box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.5);
        text-align: center;">
        <p><strong>D ARUN KUMAR</strong></p>
        <p>📧 <a href="mailto:kumardarun11@gmail.com" style="color:white; text-decoration: none;">kumardarun11@gmail.com</a></p>
        <p>🔗 <a href="http://kumardarun11.github.io/portfolio" target="_blank" style="color:white; text-decoration: none;">Portfolio</a></p>
        <p>🐙 <a href="https://github.com/kumardarun11" target="_blank" style="color:white; text-decoration: none;">GitHub</a></p>
        <p>💼 <a href="https://linkedin.com/in/kumardarun11" target="_blank" style="color:white; text-decoration: none;">LinkedIn</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

page_modules = {
    "🏠 Home": "app_pages.home",
    "📊 Power BI Dashboard": "app_pages.powerbi_dashboard",
    "📈 Data Analysis": "app_pages.data_analysis",
    "💊 Drug Recommendation": "app_pages.drug_recommendation",
    "🔍 Sentiment Analysis": "app_pages.sentiment_analysis",
    "📅 Forecast Reviews": "app_pages.forecasting",
    "🤖 AI Chatbot": "app_pages.chatbot",
}

if page in page_modules:
    module = import_module(page_modules[page])
    module.show(df)  # ✅ Ensure each page script has a `show(df)` function
else:
    st.error("Invalid Page Selected!")