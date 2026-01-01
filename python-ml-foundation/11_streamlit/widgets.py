import streamlit as st
import pandas as pd

st.title("TEXT INPUT")

name=st.text_input("enter you name bachaa")

age=st.slider("select you age:",0,100)
st.write(f"your age is {age}")

options=["python","java","c++","only python"]
choice=st.selectbox("choose you fav language:", options)
st.write(f"your fav lang is {choice}")
if name:
    st.write(f"hello, {name}")

df=pd.DataFrame({
    'firstcol': [1,2,3,4],
    'secondcol':[10,11,12,13]
})

st.write(df)

uploaded_file=st.file_uploader("CHOOSE A CSV FILR", type="csv")

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write(df)