import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# ----------------------------
# 🚀 Drug Recommendation Section
# ----------------------------
def show(df):
    st.title("💊 Drug Recommendation System")

    # Step 1: Select a condition first
    selected_condition = st.selectbox("Select a condition", ["All"] + sorted(df["condition"].dropna().unique()))

    # Step 2: Filter drugs based on the selected condition
    if selected_condition == "All":
        filtered_drugs = df["drugName"].unique()
    else:
        filtered_drugs = df[df["condition"] == selected_condition]["drugName"].unique()

    # Step 3: Select a drug from the filtered list
    selected_drug = st.selectbox("Select a drug", ["All"] + sorted(filtered_drugs))

    # Function to recommend similar drugs
    def recommend_drugs(selected_drug, selected_condition, df):
        if selected_drug == "All":
            return ["Select a drug to see recommendations."]

        # Filter drugs for the selected condition (or all conditions if not specified)
        condition_drugs = df[df["condition"] == selected_condition] if selected_condition != "All" else df

        if condition_drugs.empty or condition_drugs["drugName"].nunique() < 2:
            return ["No similar drugs found."]

        # TF-IDF Vectorization & Cosine Similarity
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(condition_drugs["drugName"])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Ensure the selected drug is in condition_drugs
        if selected_drug not in condition_drugs["drugName"].values:
            return ["Error: Could not find recommendations for this drug."]

        # Locate the drug index
        drug_index = condition_drugs[condition_drugs["drugName"] == selected_drug].index[0]
        drug_loc = condition_drugs.index.get_loc(drug_index)

        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim[drug_loc]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Extract top recommended drugs
        similar_drugs = [condition_drugs.iloc[i[0]]["drugName"] for i in sim_scores[1:6]]

        return similar_drugs if similar_drugs else ["No similar drugs found."]

    # Display drug details if a drug is selected
    if selected_drug != "All":
        recommended_drugs = recommend_drugs(selected_drug, selected_condition, df)

        # Drug Information
        st.subheader(f"🔍 **Drug Details: {selected_drug}**")
        drug_info = df[df["drugName"] == selected_drug].iloc[0]
        st.write(f"- **Condition:** {drug_info['condition']}")
        st.write(f"- **Average Rating:** {drug_info['rating']:.1f} ⭐")
        st.write(f"- **Total Reviews:** {df[df['drugName'] == selected_drug].shape[0]}")

        # Top Reviews
        st.subheader("📝 **Top Reviews:**")
        filtered_reviews = df[(df["drugName"] == selected_drug) & (df["condition"] == selected_condition)]
        top_reviews = filtered_reviews.sort_values(by="usefulCount", ascending=False).head(3)

        for _, row in top_reviews.iterrows():
            st.write(f"💬 *\"{row['review']}\"* (👍 {row['usefulCount']} helpful)")

        # Possible Side Effects
        if "sideEffects" in df.columns:
            st.subheader("⚠️ **Possible Side Effects:**")
            side_effects = df[df["drugName"] == selected_drug]["sideEffects"].unique()
            st.write(", ".join(side_effects) if side_effects else "No data available.")

        # Recommended Drugs
        st.subheader(f"🔹 **Drugs similar to {selected_drug}:**")
        st.write(", ".join(recommended_drugs))

        # User Feedback on Recommendations
        st.subheader("👍 **Was this recommendation helpful?**")
        if st.button("✅ Yes"):
            st.success("Thanks for your feedback! 😊")
        if st.button("❌ No"):
            st.warning("We'll improve this feature! 🚀")

    else:
        st.write("Select a drug to see recommendations.")
