import pandas as pd
import streamlit as st
import re
# ----------------------------
# 🚀 Step 3: Load & Preprocess Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("drugs.csv")  
    # Step 1: Clean HTML tags
    df["condition"] = df["condition"].astype(str).apply(lambda x: re.sub(r"<.*?>", "", x).strip())
    # Step 2: Remove rows with invalid 'condition' values
    # # For example: if 'condition' contains the word "users", it's likely junk
    df = df[~df["condition"].str.contains("users found this comment helpful", case=False, na=False)]
    df["date"] = pd.to_datetime(df["date"])  
    df["Year-Month"] = df["date"].dt.to_period("M").astype(str)  
    df["condition"].fillna("Unknown", inplace=True)  
    df["condition"] = df["condition"].astype(str).str.strip()  
    return df


