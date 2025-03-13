import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🎯 multipage
st.set_page_config(page_title="App Review Dashboard", layout="wide")

st.title("🎵 App Review Analysis Dashboard")
st.write("Navigate using the sidebar to switch between pages.")

DEFAULT_FILE_PATH = "music_500.csv"

 
uploaded_file = st.file_uploader(
    "📂 Upload an App Review Dataset (CSV)",
    type="csv",
    help="""
    - Please upload a **CSV file** containing app review data.  
    - **Data Source:** This review dataset can be **automatically extracted from [https://github.com/sandy-lee29/musicapp-review-analysis]**.
    """
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

else:
    df = pd.read_csv(DEFAULT_FILE_PATH)   
    st.info(f" No file uploaded yet. We've loaded the default dataset `{DEFAULT_FILE_PATH}`")

# Calculate Year Range
df['time'] = pd.to_datetime(df['time'])
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.strftime('%Y-%m')  # YYYY-MM format for monthly trends
min_year, max_year = df['year'].min(), df['year'].max()
year_range = f"{min_year} ~ {max_year}"

st.subheader("Sample Reviews")
st.write(df.head())

st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("✨Key Metrics from Review Data")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Reviews Collected", value=len(df))
    st.metric(label="Number of Apps Reviewed", value=df['company'].nunique())

with col2:
    st.metric(label="Overall User Satisfaction (average rating)", value=round(df['rating'].mean(), 1))
    st.metric(label="Time Range of Reviews", value=year_range)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Plot Data
st.subheader("⭐Average Rating by Category")
st.write("Below, you can visualize the **average rating** based on different categories such as sentiment, topic, and year.")


allowed_x_columns = ['sentiment', 'topic', 'company', 'year', 'data_source']
x_column_all = st.selectbox("Select a category to analyze average rating", allowed_x_columns, key="all_data_x")


fig, ax = plt.subplots()
sorted_df = df.groupby(x_column_all)['rating'].mean().sort_values(ascending=True)
colors = plt.cm.viridis(np.linspace(0, 1, len(sorted_df)))
sorted_df.plot(kind="barh", ax=ax, color=colors)
ax.set_ylabel(" ")
ax.set_xlabel("Average Rating")
ax.set_yticklabels(sorted_df.index, fontsize=8)
st.pyplot(fig)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Filter Data for Yearly & Monthly Trends
st.subheader("🔍 Filter Data to See Yearly & Monthly Trends")
st.write("You can filter the review by **topic** or **company** to analyze yearly and monthly trends in average rating.")
filter_column = st.selectbox("Select a category to filter by", ['topic', 'company'], key="filter_col")
unique_values = df[filter_column].unique()
selected_value = st.selectbox(f"Select a {filter_column} value", unique_values, key="filter_value")

filtered_df = df[df[filter_column] == selected_value][["review", "rating", "topic", "sentiment", "company", "year", "month"]]
st.write(filtered_df)

# 📈 Yearly & Monthly Trend of Average Rating (Side-by-Side Layout)
st.subheader("📊 Visual Trend Analysis of Average Rating")

# 두 개의 컬럼으로 배치
col1, col2 = st.columns(2)

with col1:
    st.write(f"📈 **Yearly Trend for `{selected_value}` under `{filter_column}`**")
    fig, ax = plt.subplots()
    yearly_avg = filtered_df.groupby("year")["rating"].mean().sort_index()
    ax.plot(yearly_avg.index, yearly_avg.values, marker='o', linestyle='-', color='b')
    ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.6)
    st.pyplot(fig)

with col2:
    st.write(f"📅 **Monthly Trend for `{selected_value}` under `{filter_column}` (latest 6 months)**")
    fig, ax = plt.subplots()
    latest_six_months = filtered_df["month"].sort_values().unique()[-6:]
    filtered_monthly_df = filtered_df[filtered_df["month"].isin(latest_six_months)]
    monthly_avg = filtered_monthly_df.groupby("month")["rating"].mean().sort_index()
    ax.plot(monthly_avg.index, monthly_avg.values, marker='o', linestyle='-', color='b')
    ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.6)
    st.pyplot(fig)


st.markdown("<br><br><br>", unsafe_allow_html=True)

st.subheader("🔍 Find Similar Reviews by Issue")

# Step 1: Select Issue (Exclude positive sentiment)
valid_aspects = df[(df["sentiment"] != "Positive") & df["aspect"].notna()]["aspect"].unique()
selected_aspect = st.selectbox("Choose an issue", valid_aspects)

# Step 2: Select a random review from the aspect I chose  
aspect_reviews = df[df["aspect"] == selected_aspect]["review"].dropna().tolist()
if aspect_reviews:
    selected_review = random.choice(aspect_reviews)
    st.write(f"**Sample Review for Issue '{selected_aspect}':**")
    st.write(f"📌 *{selected_review}*")

# Step 3: Suggest similar reviews for that aspect

def recommend_reviews(selected_review, df):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["review"].dropna())
    cosine_sim = cosine_similarity(tfidf_matrix)
    idx = df[df["review"] == selected_review].index[0]
    similar_reviews = df.iloc[cosine_sim[idx].argsort()[-6:-1]][["aspect", "review", "rating"]]  
    return similar_reviews.dropna(subset=["aspect"])  # Remove rows where aspect is NaN

recommended_reviews = recommend_reviews(selected_review, df)
st.subheader("🔗 Similar Reviews")

# Display reviews in a table with expandable full review
if not recommended_reviews.empty:
    for index, row in recommended_reviews.iterrows():
        with st.expander(f"🔹 {row['aspect']}"):
            st.write(f"**Review:** {row['review']}")
            st.write(f"⭐ Rating: {row['rating']}")
else:
    st.write("No similar reviews found.")
