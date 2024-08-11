import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title='Income Prediction Data', page_icon='📊', layout='wide')

# Set up page title
st.title('Income Prediction Data')

# Load Data
@st.cache_data(show_spinner='Data loading ...')
def load_data():
    data = pd.read_csv('./datafiles/Income trainset.csv')
    return data

# Load the data
data = load_data()

# Display data
st.subheader('Raw Dataset')
st.write(data)
