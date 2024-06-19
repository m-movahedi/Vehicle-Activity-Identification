import streamlit as st
import pandas as pd
import numpy as np

#st.balloons()
st.title('Vehicle Activity Identification: Data Cleaning')
st.subheader('Research Experiences for Undergraduates (REU)')
st.link_button('More about REU',url='https://www.nsf.gov/crssprgm/reu/')
st.link_button('RIDER Center', url='https://rider.eng.famu.fsu.edu/')
st.link_button('SIM Lab', url='https://rider.eng.famu.fsu.edu/research/laboratory-sustainable-infrastructure-management')

st.sidebar.title('Navigation')
st.sidebar.markdown('1. [Upload Data](#upload-data)')
st.sidebar.markdown('2. [Data Cleaning](#data-cleaning)')
st.sidebar.markdown('3. [Data Exploration](#data-exploration)')
st.sidebar.markdown('4. [Data Preprocessing](#data-preprocessing)')
st.sidebar.markdown('5. [Model Building](#model-building)',)

st.markdown("# Step 1: Upload Data")

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

