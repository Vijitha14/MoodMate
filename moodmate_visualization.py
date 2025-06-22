import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calplot
import matplotlib.pyplot as plt


st.set_page_config(page_title="MoodMate Analytics", layout="centered")

st.title("🧠 MoodMate Analytics Dashboard")
st.markdown("Track, visualize and understand your mood patterns!")

# Upload CSV or use sample
st.sidebar.header("📂 Upload your mood CSV")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("Or use sample data below 👇")
    if st.sidebar.button("Load Sample Data"):
        sample_data = {
            'Date': pd.date_range(start='2025-06-01', periods=15, freq='D'),
            'Mood': ['happy', 'neutral', 'sad', 'happy', 'sad', 'neutral', 'happy', 'neutral', 'sad', 'happy', 'sad', 'neutral', 'happy', 'neutral', 'happy']
        }
        df = pd.DataFrame(sample_data)
    else:
        st.warning("📁 Please upload a CSV file or load the sample to continue.")
        st.stop()

# Convert date column
df['Date'] = pd.to_datetime(df['Date'])

# Show raw data
st.subheader("🗂️ Raw Mood Data")
st.dataframe(df, use_container_width=True)

# Mood frequency bar chart
st.subheader("📊 Mood Frequency")
mood_counts = df['Mood'].value_counts()
st.bar_chart(mood_counts)

# Mood over time line chart
st.subheader("📈 Mood Over Time")
daily_mood = df.groupby('Date')['Mood'].apply(lambda x: x.mode()[0]).reset_index()
mood_to_num = {'sad': 1, 'neutral': 2, 'happy': 3}
daily_mood['Mood_Score'] = daily_mood['Mood'].map(mood_to_num)

fig, ax = plt.subplots()
sns.lineplot(data=daily_mood, x='Date', y='Mood_Score', marker='o', ax=ax)
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(['sad', 'neutral', 'happy'])
ax.set_title("Mood Trend Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Mood")
st.pyplot(fig)

# Convert mood to numeric for heatmap
df_heat = df.copy()
df_heat['MoodScore'] = df_heat['Mood'].map({'sad': 0, 'neutral': 1, 'happy': 2})
df_heat = df_heat.groupby('Date')['MoodScore'].mean()

# Show calendar heatmap
st.subheader("📆 Calendar Mood Heatmap")
fig, ax = calplot.calplot(df_heat, cmap='coolwarm', colorbar=True)
st.pyplot(fig)

# Weekly mood summary CSV download
st.subheader("📥 Download Weekly Mood Summary")
summary = df.groupby(['Date', 'Mood']).size().unstack(fill_value=0)
csv = summary.to_csv().encode('utf-8')
st.download_button("Download Summary as CSV", csv, "mood_summary.csv", "text/csv")
