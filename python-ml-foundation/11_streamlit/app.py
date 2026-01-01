import streamlit as st
import pandas as pd
import numpy as np

##title of applicatiion
st.title("Hello Streamlit")

##display a simple text
st.write("this is very easy")

##create a data frame

df=pd.DataFrame({
    'firstcol': [1,2,3,4],
    'secondcol':[10,11,12,13]
})

##display the data frame
st.write("here is the data frame")
st.write(df)

##create a line chart

chart_data=pd.DataFrame(
    np.random.randn(20,3),columns=['a','b','c']
)
st.line_chart(chart_data)