import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure necessary NLTK data is available
nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()  # Initialize the sentiment analyzer
# ----------------------------
# 🚀 Sentiment Analysis Section
# ----------------------------
def show(df):
    st.title("🔍 Sentiment Analysis of Drug Reviews")

    # Ensure necessary NLTK data is available
    nltk.download("vader_lexicon", quiet=True)

    # Initialize Sentiment Analyzer
    sia = SentimentIntensityAnalyzer()

    # **Cache sentiment scores to avoid recalculating every time**
    @st.cache_data
    def compute_sentiment(data):
        data["Sentiment"] = data["review"].fillna("").map(lambda x: sia.polarity_scores(x)["compound"])
        data["Sentiment Label"] = data["Sentiment"].apply(
            lambda x: "Positive" if x > 0.05 else "Negative" if x < -0.05 else "Neutral"
        )
        return data

    df = compute_sentiment(df.copy())  # Use cached computation

    # **Sentiment Distribution Pie Chart**
    st.subheader("📊 Sentiment Distribution")
    sentiment_counts = df["Sentiment Label"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment Label", "count"]  # Rename columns correctly

    fig_sentiment = px.pie(
        sentiment_counts,
        names="Sentiment Label",
        values="count",
        title="Sentiment Distribution of Reviews",
        color="Sentiment Label",
        color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"},
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

    # **Word Cloud of Reviews**
    st.subheader("☁️ Word Cloud of Reviews")
    
    # Sample up to 3000 reviews to avoid memory issues
    sample_reviews = df["review"].dropna().sample(min(3000, len(df)), random_state=42)
    text = " ".join(sample_reviews.astype(str))

    if text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig_wc, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig_wc)
    else:
        st.write("No text data available for word cloud.")