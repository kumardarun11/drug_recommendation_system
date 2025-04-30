import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from urllib.parse import quote
from difflib import get_close_matches
@st.cache_data
# # Function: Get drug side effects
# def get_drug_side_effects(drug_name):
#     url = f"https://www.drugs.com/sfx/{drug_name.lower().replace(' ', '-')}-side-effects.html"
#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             side_effects_section = soup.find("div", class_="contentBox")
#             if side_effects_section:
#                 side_effects = side_effects_section.text.strip().split("\n")[:5]
#                 return f"⚠️ **Common Side Effects:**\n- " + "\n- ".join(side_effects)
#     except Exception as e:
#         print("Error fetching side effects:", e)
    
#     return "⚠️ Side effects information is unavailable."
# Function: Get drug side effects using OpenFDA API
def get_drug_side_effects(drug_name):
    """Fetch common side effects using the OpenFDA API."""
    encoded_name = quote(drug_name.upper())
    url = f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{encoded_name}&limit=5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                reactions = [
                    event["reaction"][0]["reactionmeddrapt"]
                    for event in data["results"]
                    if "reaction" in event
                ]
                if reactions:
                    return f"⚠️ **Common Side Effects:**\n- " + "\n- ".join(reactions[:5])
    except Exception as e:
        print("Error fetching side effects:", e)
    
    return "⚠️ Side effects information is unavailable."


def get_drug_price(drug_name):
    """Scrape the price of a drug from GoodRx."""
    url = f"https://www.goodrx.com/{drug_name.replace(' ', '-')}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            price = soup.find("span", class_="price-value")
            if price:
                return f"💰 **Price of {drug_name}:** {price.text} (via GoodRx)"
    except Exception as e:
        print("Error fetching price:", e)
    
    return "❌ Price information unavailable."

def search_drug_online(drug_name):
    """Search drug info on Drugs.com as a fallback."""
    search_url = f"https://www.drugs.com/search.php?searchterm={drug_name}"
    try:
        response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            first_result = soup.select_one("ul.ddc-list-column-2 a")
            if first_result:
                drug_url = "https://www.drugs.com" + first_result["href"]
                return f"🌐 **Online Source:** [Read more about {drug_name} here]({drug_url})"
    except Exception as e:
        print("Error fetching online data:", e)
    
    return "I couldn't find this drug online. Please check a reliable medical website."


def check_symptoms_online(symptoms):
    """Redirect user to Mayo Clinic's symptom checker."""
    url = f"https://www.mayoclinic.org/symptom-checker?symptoms={symptoms.replace(' ', '%20')}"
    return f"🔍 **Possible conditions:** [Check on MayoClinic]({url})"

def chatbot_response(user_query, df):
    """Main chatbot response logic: matches drug or condition, or falls back online."""
    user_query = user_query.lower()

    # Fuzzy match drug name
    drug_names = df["drugName"].dropna().unique()
    matched_drugs = get_close_matches(user_query, drug_names, n=1, cutoff=0.6)

    if matched_drugs:
        drug = matched_drugs[0]
        drug_info = df[df["drugName"].str.lower() == drug.lower()].iloc[0]
        response = f"""
💊 **{drug_info['drugName']}** is commonly used for **{drug_info['condition']}**.
🌟 **Average Rating:** {drug_info['rating']:.1f}/10  
📝 **Most helpful review:**  
*"{drug_info['review'][:200]}..."*
        """.strip()

        # Add side effects if asked
        if "side effect" in user_query or "adverse effect" in user_query:
            response += "\n\n" + get_drug_side_effects(drug)

        # Add price if asked
        if "price" in user_query or "cost" in user_query:
            response += "\n\n" + get_drug_price(drug)

        return response

    # Fuzzy match condition
    conditions = df["condition"].dropna().unique()
    matched_conditions = get_close_matches(user_query, conditions, n=1, cutoff=0.6)

    if matched_conditions:
        condition = matched_conditions[0]
        condition_drugs = df[df["condition"].str.lower() == condition.lower()]["drugName"].unique()
        return f"📋 **Drugs for {condition}:**\n" + ", ".join(condition_drugs[:5]) + "..."

    # Check for symptom-related queries
    if "i feel" in user_query or "symptom" in user_query:
        return check_symptoms_online(user_query)

    # Fallback
    st.info("Searching online for more details... 🔍")
    return search_drug_online(user_query)