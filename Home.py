import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.bottom_container import bottom

st.set_page_config(
    page_title="SIM VAI",
    page_icon="🚘",
    layout='wide',
    initial_sidebar_state = "collapsed"
)


st.write("# Vehicle Activity Identification 🚘")


#st.balloons()



with st.sidebar.container(border=True):
    st.write("Vehicel Activity Identification (VAI)",)
    col1, col2 = st.columns([2,2])
    col1.image("Misc/RIDER.png", use_column_width=True) 
    col2.image("Misc/College.png", use_column_width=True)
    col1, col2 = st.columns([2,2])
    col1.page_link("pages/05_About.py",use_container_width = True)
    col2.page_link("pages/04_Help.py",use_container_width = True)

