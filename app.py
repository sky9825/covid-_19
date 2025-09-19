import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

# ---- App Title ----
st.title("COVID-19 Research Papers Explorer")
st.write("This app allows you to explore the CORD-19 metadata dataset interactively.")

# ---- Load Data ----
file_path = r"C:\Users\pc\Downloads\unzipped\metadata.csv"

@st.cache_data
def load_data(path, nrows=5000):
    return pd.read_csv(path, nrows=nrows, low_memory=False)

df = load_data(file_path)

# ---- Show Sample Data ----
if st.checkbox("Show Raw Data Sample"):
    st.write(df.head())

# ---- Basic Information ----
st.subheader("Dataset Information")
st.write(f"Number of Rows: {df.shape[0]}")
st.write(f"Number of Columns: {df.shape[1]}")

# ---- Handle Missing Data ----
missing_info = df.isnull().sum().sort_values(ascending=False)
if st.checkbox("Show Missing Values Info"):
    st.write(missing_info.head(10))

# ---- Convert Dates ----
if "publish_time" in df.columns:
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year

# ---- Publications Over Time ----
if "year" in df.columns:
    st.subheader("Publications by Year")
    year_counts = df["year"].value_counts().sort_index()
    st.bar_chart(year_counts)

# ---- Top Journals ----
if "journal" in df.columns:
    st.subheader("Top Journals")
    top_journals = df["journal"].value_counts().head(10)
    st.bar_chart(top_journals)

# ---- Word Cloud ----
st.subheader("Word Cloud of Paper Titles")
if "title" in df.columns:
    titles_text = " ".join(str(title) for title in df["title"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles_text)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# ---- Interactive Filter ----
if "year" in df.columns:
    year_filter = st.slider("Select Year", int(df["year"].min()), int(df["year"].max()), int(df["year"].min()))
    st.write(f"Papers from Year: {year_filter}")
    filtered_df = df[df["year"] == year_filter]
    st.write(filtered_df.head(10))
