import streamlit as st
import pandas as pd

st.title("🔍 Topic-Based Review Breakdown")
st.markdown("📌 Select a topic from the left panel to explore its key issues and related user reviews (negative & neutral only).")

# Load Default Data
DEFAULT_FILE_PATH = "music_500.csv"
df = pd.read_csv(DEFAULT_FILE_PATH)

# Remove positive & NA
df_filtered = df[(df["sentiment"] != "Positive") & df["topic"].notna() & df["aspect"].notna()]

# Make Topic List
topics = df_filtered["topic"].unique()
selected_topic = st.sidebar.selectbox("Select a Topic", topics)

# Filter issues to the selected topic  
issues_df = df_filtered[df_filtered["topic"] == selected_topic]

# Topic List with purple theme
st.sidebar.subheader("📌 Topics Overview")

for topic in topics:
    topic_df = df_filtered[df_filtered["topic"] == topic]
    total_reviews = len(topic_df)
    avg_rating = round(topic_df["rating"].mean(), 2)
    review_percentage = round((total_reviews / len(df_filtered)) * 100, 2)

    with st.sidebar.container():
        st.markdown(
            f"""
            <div style="padding:10px; border-radius:10px; background-color:#EDE7F6; border-left: 5px solid #673AB7; margin-bottom:10px;">
            <strong style="font-size:16px; color:#4A148C;">{topic.capitalize()}</strong>  
            <br>📊 <strong>{total_reviews}</strong> reviews ({review_percentage}%)  
            <br>⭐ Avg. Rating: <strong>{avg_rating}/5</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

# Right Part: show list of selected topic  
st.subheader(f"💜 Key Issues in '{selected_topic}'")

for issue_number, issue in enumerate(issues_df["aspect"].unique(), start=1): 
    issue_df = issues_df[issues_df["aspect"] == issue]
    total_reviews = len(issue_df)
    avg_rating = round(issue_df["rating"].mean(), 2)
    review_percentage = round((total_reviews / len(issues_df)) * 100, 2)

    st.markdown("<br>", unsafe_allow_html=True)

    # ✅ Summary Box with Purple Theme (Updated)
    st.markdown(
        f"""
        <div style="background-color:#EDE7F6; padding:18px; border-radius:8px; border-left: 6px solid #673AB7;">
            <h4 style="color:#4A148C;">🎵 Issue {issue_number}. {issue}</h4>
            <p style="font-size:16px; color:#555; font-weight:500;">
            <strong>Review#:</strong> {total_reviews} &nbsp;/&nbsp;
            <strong>Review%:</strong> {review_percentage}% &nbsp;/&nbsp;
            <strong>Avg. Rating:</strong> {avg_rating}/5  
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🔹 Show 3 sample reviews of specific issue (add rating & aspect_index for each)
    for _, row in issue_df.sample(min(3, len(issue_df))).iterrows():
        st.markdown(f"""
        <div style="border: 1px solid #B39DDB; border-radius:8px; padding:10px; margin-top:10px;">
        <p> <em>{row['review']}</em></p>
        <p><strong>⭐ Rating:</strong> {row['rating']}/5  &nbsp;&nbsp;
         <strong>🟣 Issue Index:</strong> <span style="color:#7E57C2;">{row['aspect_index']}</span></p>
        </div>
        """, unsafe_allow_html=True)
