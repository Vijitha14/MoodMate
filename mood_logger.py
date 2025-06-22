import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Mood Insights 📊", page_icon="📈")

st.title("📈 MoodMate – Mood Insights Dashboard")
st.write("Explore how you’ve been feeling recently 💫")

# Load mood logs
try:
    df = pd.read_csv("data/mood_logs.csv")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Show latest entries
    st.subheader("📝 Recent Conversations")
    st.dataframe(df.tail(10))

    # Plot mood frequency over time
    df['date'] = df['timestamp'].dt.date

    st.subheader("📅 Mood Usage Over Time")
    mood_counts = df.groupby("date").size()
    st.line_chart(mood_counts)

    # Word frequency cloud (optional)
    st.subheader("💭 Frequently Used Words")
    all_text = " ".join(df['user_input'].dropna().astype(str))
    from wordcloud import WordCloud
    wc = WordCloud(width=800, height=300, background_color='white').generate(all_text)
    st.image(wc.to_array())

except FileNotFoundError:
    st.error("Mood logs not found. Use MoodMate to record interactions first.")
