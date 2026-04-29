import streamlit as st 
import pandas as pd 

st.set_page_config(
  page_title = "Olympic Performance Analyzer", 
  layout = "wide",
)

st.title("Olympic Performance Analyzer")
st.write("Olympic medal trends, country performance and sport specialization using historical athlete and medal data.")