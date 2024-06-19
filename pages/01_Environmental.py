import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="SIM VAI: Environmental Sensor Data Cleaning",
    page_icon="😶‍🌫️",
    layout='wide',
    initial_sidebar_state = "collapsed"
)
st.write("# Environmental Sensor Data Cleaning 😶‍🌫️")
st.write("### Importing the data")
st.write("The data used in this project was collected from a variety of sensors installed on a vehicle. This includes Inertial Measurement Unit (IMU) sensors, Global Positioning System (GPS) sensors, and Environmental sensors. The environmental sensors record data such as temperature, humidity, and air quality. In this section, we will focus on cleaning and preprocessing the environmental sensor data.")


# Get time        
st.write("### 🕒 Time")
container = st.container()
col1, col2, col3 = container.columns([1,1,1])
col1.write("Initial time step")
date = col2.date_input("Start Date")
now = datetime.now()
col31, col32, col33 = col3.columns([1,1,1])
hours = col31.selectbox("Hours", list(range(0,24)), index=now.hour)
minutes = col32.selectbox("Minutes", list(range(0,60)), index=now.minute)
seconds = col33.selectbox("Seconds", list(range(0,60)), index=now.second)
time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)
#st.write("Current time:", time)

# Get CSV file
st.write("### 📱 Environmental sensor data")
ENV = st.file_uploader("Upload your environmental sensor data", type=['csv'])
if ENV != None:
    ENV = pd.read_csv(ENV)
    # Display the data
    st.dataframe(ENV, width=1000, height=500)
