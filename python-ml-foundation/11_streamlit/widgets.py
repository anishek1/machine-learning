import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Interactive Widgets Demo",
    page_icon="🎛️",
    layout="centered"
)

# Header section
st.title("🎛️ Interactive Widgets Demo")
st.markdown("---")

# User Info Section
st.header("👤 User Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("📝 Enter your name", placeholder="Type your name here...")

with col2:
    age = st.slider("🎂 Select your age", min_value=0, max_value=100, value=25)

if name:
    st.success(f"👋 Hello, **{name}**! You are **{age}** years old.")

st.markdown("---")

# Programming Preferences Section
st.header("💻 Programming Preferences")

options = ["Python 🐍", "Java ☕", "C++ ⚡", "Only Python 💯"]
choice = st.selectbox("🔧 Choose your favorite language", options)

st.info(f"Great choice! Your favorite language is: **{choice}**")

st.markdown("---")

# Sample Data Section
st.header("📊 Sample Data")

df = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'First Column': [1, 2, 3, 4],
    'Second Column': [10, 11, 12, 13]
})

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")

# File Upload Section
st.header("📁 File Upload")

uploaded_file = st.file_uploader(
    "Choose a CSV file to upload",
    type="csv",
    help="Upload a CSV file to view its contents"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ File uploaded successfully! ({len(df)} rows)")
    st.dataframe(df, use_container_width=True)
else:
    st.caption("No file uploaded yet. Drag and drop or click to browse.")