import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
# ----------------------------
# 🚀 Data Analysis Section
# ----------------------------
def show(df):
    st.title("📈 Data Analysis & Visualizations")

    # Filter data only within Data Analysis
    selected_drug = st.selectbox("Select Drug", ["All"] + list(df["drugName"].unique()))
    selected_condition = st.selectbox("Select Condition", ["All"] + list(df["condition"].dropna().unique()))

    filtered_data = df.copy()
    if selected_drug != "All":
        filtered_data = filtered_data[filtered_data["drugName"] == selected_drug]
    if selected_condition != "All":
        filtered_data = filtered_data[filtered_data["condition"] == selected_condition]

    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Reviews", value=filtered_data.shape[0])
    col2.metric(label="Average Rating", value=round(filtered_data["rating"].mean(), 2))
    col3.metric(label="Most Useful Review", value=filtered_data["usefulCount"].max())

    # Top 10 Most Reviewed Drugs
    st.subheader("📊 Top 10 Most Reviewed Drugs")
    top_drugs = df["drugName"].value_counts().nlargest(10).reset_index()
    top_drugs.columns = ["Drug Name", "Total Reviews"]
    fig_bar = px.bar(top_drugs, x="Drug Name", y="Total Reviews", title="Top 10 Most Reviewed Drugs")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Ratings Distribution
    st.subheader("📊 Ratings Distribution")
    plt.style.use("dark_background")  # Apply dark background
    fig_hist, ax = plt.subplots()
    # Use a neon cyan color for bars and bright pink for the KDE curve]
    sns.histplot(filtered_data["rating"], bins=10, kde=True, ax=ax, 
                 color="#008BFF", edgecolor="#008BFF", alpha=0.6)  # Neon cyan with slight transparency
    ax.set_title("Ratings Distribution", color="white")
    ax.set_xlabel("Rating", color="white")
    ax.set_ylabel("Count", color="white")
    ax.spines["bottom"].set_color("#008BFF")
    ax.spines["left"].set_color("#008BFF")
    ax.spines["top"].set_color("#008BFF")
    ax.spines["right"].set_color("#008BFF")
    st.pyplot(fig_hist)

    # Treemap of Most Common Conditions
    st.subheader("🌳 Most Common Conditions")
    condition_counts = df.groupby("condition")["usefulCount"].sum().reset_index()
    fig_treemap = px.treemap(condition_counts, path=["condition"], values="usefulCount", title="Most Common Conditions")
    st.plotly_chart(fig_treemap, use_container_width=True)

    # Box Plot for Ratings Across Drugs
    st.subheader("📦 Rating Distribution Across Drugs")
    top_rated_drugs = df["drugName"].value_counts().nlargest(10).index
    fig_box = px.box(df[df["drugName"].isin(top_rated_drugs)], x="drugName", y="rating", title="Rating Distribution of Top 10 Drugs", color="drugName")
    fig_box.update_xaxes(tickangle=45, title_text="Drug Name")
    fig_box.update_yaxes(title_text="Rating")
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Reviews Over Time
    st.subheader("📈 Reviews Over Time")
    reviews_over_time = filtered_data.groupby("Year-Month").size().reset_index(name="Total Reviews")
    reviews_over_time["Year-Month"] = reviews_over_time["Year-Month"].astype(str)
    fig_line = px.line(reviews_over_time, x="Year-Month", y="Total Reviews", title="Reviews Over Time")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Correlation Heatmap
    st.subheader("🔗 Correlation Between Features")
    # Set dark theme for the plot
    plt.style.use("dark_background")
    fig_corr, ax = plt.subplots(figsize=(5, 4))
    corr_matrix = filtered_data[["rating", "usefulCount"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, linewidths=0.5,
                annot_kws={"color": "white"}, cbar_kws={'shrink': 0.8})
    st.pyplot(fig_corr)


    # Top 5 Most Reviewed Conditions
    st.subheader("📌 Top 5 Most Reviewed Conditions")
    top_conditions = df["condition"].value_counts().nlargest(5).reset_index()
    top_conditions.columns = ["Condition", "Total Reviews"]
    fig_cond = px.bar(top_conditions, y="Condition", x="Total Reviews", title="Top 5 Most Reviewed Conditions", orientation="h", color="Total Reviews", color_continuous_scale="magma")
    st.plotly_chart(fig_cond, use_container_width=True)

    # Monthly Review Trends
    st.subheader("📅 Monthly Review Trends")
    df["Year-Month"] = pd.to_datetime(df["Year-Month"])
    monthly_reviews = df.groupby(df["Year-Month"].dt.to_period("M")).size().reset_index(name="Total Reviews")
    monthly_reviews["Year-Month"] = monthly_reviews["Year-Month"].astype(str)  # Convert Period to string
    fig_monthly = px.line(monthly_reviews, x="Year-Month", y="Total Reviews", title="Monthly Reviews Trend", markers=True)
    st.plotly_chart(fig_monthly, use_container_width=True)
