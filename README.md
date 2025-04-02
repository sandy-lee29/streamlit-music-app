🎵 You can checkout my streamlit dashboard [here](https://music-app-review-dashboard.streamlit.app/)🎵

### 🎵 App Review Analysis Dashboard – Features Overview <br>
#### 1. File Upload & Default Dataset
- Users can upload a custom CSV file
- If no file is uploaded, a default dataset (music_500.csv) is automatically loaded

#### 2. Key Metrics Summary
- Total number of reviews, Number of unique apps (companies), Average user rating, Time range covered by the reviews

#### 3. Average Rating Comparison by Category
- Horizontal bar chart showing average ratings grouped by: Sentiment, Topic, Company, Year, Data Source

#### 4. Yearly & Monthly Trend Analysis
- Filter reviews by topic or company.
- Visualize: Yearly average rating trends & Monthly trends (latest 6 months)

#### 5. Similar Review Finder
- Select a negative/neutral issue (aspect), and it will randomly display one sample review
- Uses TF-IDF and cosine similarity to find 5 similar reviews
- Reviews are displayed in expandable cards

#### 6. Topic-Based Deep Dive (with OpenAI GPT-4o)
- Sidebar lets users select a topic (e.g., pricing, usability)
- For each issue (aspect) under the selected topic:
  - Number of reviews, average rating, and percentage share shown
  - AI generates clear, two-sentence insights per issue:
      - What the issue is (brief definition of the issue)
      - How it affects user experience or product performance
- Shows 3 sample user reviews per issue

  
