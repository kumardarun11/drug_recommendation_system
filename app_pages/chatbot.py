import streamlit as st
import pandas as pd
from streamlit_chat import message
from utils.voice import voice_input  # Handles voice input
from utils.web_scrapping import chatbot_response, search_drug_online, get_drug_side_effects, get_drug_price


# ----------------------------
# 🚀 AI Chatbot for Drug Advice
# ----------------------------
def show(df):
    st.title("🤖 AI Chatbot for Drug Queries")
    st.write("Ask about **drug names, conditions, ratings, side effects, prices, or symptoms!**")
    # User input field
    user_input = st.text_input("💬 Type your question here:")
    if st.button("🎙️ Ask with Voice"):
        user_input = voice_input()
        st.write(f"💬 **You said:** {user_input}")
    if user_input:
        response = chatbot_response(user_input, df)
        # 🛠️ NEW: Detect if user asks for side effects
        if "side effect" in user_input.lower() or "adverse effect" in user_input.lower():
            response += "\n\n" + get_drug_side_effects(user_input)
        # 🛠️ NEW: Detect if user asks for drug prices
        if "price" in user_input.lower() or "cost" in user_input.lower():
            response += "\n\n" + get_drug_price(user_input)
        # If no match is found in the dataset, search online
        if "I couldn't find" in response:
            response += "\n\n" + search_drug_online(user_input)
        # Ensure chat history exists
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        st.session_state["chat_history"].append((user_input, response))
        # Display chat history with unique keys to avoid duplicate ID errors
        for i, (user_msg, bot_msg) in enumerate(reversed(st.session_state["chat_history"])):
            message(user_msg, is_user=True, key=f"user_{i}")  # Unique key for user message
            message(bot_msg, key=f"bot_{i}")  # Unique key for bot response
        # User health form for personalized drug recommendations
        st.subheader("📋 Get Personalized Drug Recommendations")
        with st.form(key="user_health_form"):
            age = st.number_input("Enter your age:", min_value=1, max_value=120)
            condition = st.text_input("What medical condition do you have?")
            allergy = st.text_input("Any drug allergies? (Optional)")
            submitted = st.form_submit_button("Get Drug Recommendations")
        # Ensure safe_drugs is always defined
        safe_drugs = pd.DataFrame()  # Define as an empty DataFrame to avoid errors
        if submitted:
            recommended_drugs = df.dropna(subset=["condition"])  # Ensure no NaN conditions
            recommended_drugs = df[(df["condition"].str.lower() == condition.lower())]
             # Check for allergies (only if user provided input)
            if allergy:
                allergy_list = [a.strip().lower() for a in allergy.split(",")]  # Convert to list
                safe_drugs = recommended_drugs[~recommended_drugs["drugName"].str.lower().isin(allergy_list)]
            else:
                safe_drugs = recommended_drugs  # No allergy filtering if empty
        # Display recommendations only if safe_drugs is defined and not empty
        if not safe_drugs.empty:
            st.success(f"✅ **Recommended drugs for {condition}:**\n- " + "\n- ".join(safe_drugs["drugName"].unique()))
        else:
            st.warning("⚠️ No safe drugs found based on your allergies. Please consult a doctor.")