import streamlit as st
# ----------------------------
# 🚀 Power BI Dashboard Section
# ----------------------------
def show(df):
    st.title("📊 Power BI Dashboard")
    st.subheader("🔗 Embedded Power BI Report")
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=c3302025-d2b4-4105-9844-e409b97c3c85&autoAuth=true&ctid=f1ea55ea-1f7f-4734-913e-b70b9dd2408d"
    st.components.v1.iframe(powerbi_url, width=1000, height=600)
    st.write("Above is the Power BI dashboard embedded in Streamlit.")