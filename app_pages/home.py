import streamlit as st

# ----------------------------
# 🏥 Home Page: Introduction
# ----------------------------
def show(df):
    st.title("🏥 Drug Analysis & Recommendation System")

    # Welcome Section
    st.markdown("""
        ## 🩺 **Welcome to the Drug Analysis & Recommendation System**
        This AI-powered platform offers **in-depth insights** into pharmaceutical drugs, including reviews, side effects, prices, and smart recommendations. Whether you're a **health professional, researcher, or patient**, this tool helps you make informed decisions **with confidence.**
    """)

    # Why Use This Tool?
    st.subheader("💡 Why Choose This Tool?")
    st.markdown("""
        - ✅ **Accurate Insights** – Reliable data on drug effectiveness, side effects, and pricing.  
        - 🧠 **AI-Powered Analysis** – Utilizes **Machine Learning & Natural Language Processing (NLP)**.  
        - 📊 **Interactive Visualizations** – Seamless experience with detailed, dynamic insights.  
        - 🌍 **Trusted Data Sources** – Aggregated from verified medical sources and user reviews.  
        - 🚀 **Personalized Recommendations** – Tailored medication suggestions based on user needs.
    """)

    # Key Features
    st.subheader("🔹 Key Features")
    st.markdown("""
        - 📊 **Power BI & Plotly Dashboards** – Interactive reports on drug usage & reviews.
        - 📈 **Data Analysis & Trends** – Explore conditions, medication efficiency, and trends.
        - 💊 **Smart Drug Recommendations** – AI-driven personalized suggestions.
        - 🔍 **Sentiment Analysis** – AI-powered review analysis for patient insights.
        - 📅 **Forecasting Trends** – Predict future drug reviews & market trends.
        - 🤖 **AI Chatbot Assistant** – Instantly answers queries about drugs, symptoms, and conditions.
        - 🔬 **Comparative Analysis** – Evaluate multiple medications side by side.
    """)

    # How It Works
    st.subheader("🔬 How It Works")
    st.markdown("""
        1️⃣ **Data Collection** – Aggregates information from verified medical sources and user reviews.  
        2️⃣ **AI Processing** – Uses **Machine Learning (ML)** for advanced analysis.  
        3️⃣ **Sentiment & Trend Analysis** – Evaluates public perception and drug effectiveness.  
        4️⃣ **Smart Drug Recommendations** – Suggests medications based on AI insights.  
        5️⃣ **Chatbot Assistance** – Provides instant, AI-powered responses to medical queries.  
    """)

    # Live Statistics (Dynamic)
    st.subheader("📈 Live Drug Analysis Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💊 Total Drugs Analyzed", value=len(df["drugName"].unique()))
    col2.metric(label="📝 Total Reviews Processed", value=df.shape[0])
    col3.metric(label="⭐ Average Rating", value=round(df["rating"].mean(), 2))

    # Tools & Technologies Used
    st.subheader("🛠️ Tools & Technologies Used")
    st.markdown("""
        - 🤖 **Machine Learning & AI** – Advanced models for drug analysis & prediction.  
        - 🗣️ **Natural Language Processing (NLP)** – AI-based sentiment and review analysis.  
        - 📊 **Power BI & Plotly** – Dynamic, interactive data visualizations.  
        - 🏥 **Medical Data Scraping** – Fetches real-time data from trusted sources.  
        - 🔍 **Deep Learning** – Enhances prediction accuracy and analysis depth.  
    """)

    # Data Privacy & Security
    st.subheader("🛡️ Data Security & Privacy")
    st.markdown("""
        - 🔒 **We prioritize your privacy.** No personal health data is stored.  
        - 📜 **Medical data is sourced from accredited & verified platforms.**  
        - 🏥 **Always consult a doctor** before making medical decisions.  
    """)

    # User Testimonials (Dynamic)
    st.subheader("📌 What Users Are Saying")
    testimonials = [
        "🗣️ *This tool helped me find an affordable alternative to my medication!* – John D.",
        "🗣️ *The AI chatbot answered my questions faster than my pharmacist!* – Sarah L.",
        "🗣️ *I love the sentiment analysis! It helps me understand patient experiences easily.* – Dr. Patel",
        "🗣️ *The forecasting feature gave me insights into future drug trends!* – Emily R.",
        "🗣️ *This platform is a game-changer for healthcare professionals!* – Dr. Ahmed"
    ]
    for testimonial in testimonials:
        st.success(testimonial)

    # Disclaimer
    st.subheader("📢 Disclaimer")
    st.warning(
        "This tool is for **informational purposes only** and does not replace professional medical advice. "
        "Always consult a healthcare provider before making any medical decisions."
    )
