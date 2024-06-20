import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.bottom_container import bottom
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(
    page_title="SIM Vehicle Activity Identification",
    page_icon="🛻",
    layout='wide',
    initial_sidebar_state = "collapsed"
)


st.write("# Vehicle Activity Identification 🚘")


#st.balloons()



with st.sidebar.container():
    st.write("Vehicel Activity Identification (VAI)",)
    col1, col2 = st.columns([2,2])
    col1.image("Misc/RIDER.png", use_column_width=True) 
    col2.image("Misc/College.png", use_column_width=True)
    col1, col2 = st.columns([2,2])
    #col1.page_link("./pages/05_About.py",use_container_width = True)
    #col2.page_link("./pages/04_Help.py",use_container_width = True)


st.divider()

# Get time        
container = st.container()
col1, col2, col3, col4 = container.columns([1,1,1,1])
col1.write("### 🕒 Time")
col1.write("Initial time step")
machine_name = col2.text_input("Machine name", value="Car 1")
date = col3.date_input("Start Date")
now = datetime.now()
col41, col42, col43 = col4.columns([1,1,1])
hours = col41.number_input("Hours", min_value=0, max_value=23, value= 12)
minutes = col42.number_input("Minutes", min_value=0, max_value=59)
seconds = col43.number_input("Seconds", min_value=0, max_value=59)
time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)
#st.write("Current time:", time)
st.divider()

# Environmental Sensor Data Cleaning

def environmental_sensor_cleaning(df, initial_time ):
    df.columns = ['AX', 'AY', 'AZ', 'CO2','Temp',"Humidity",'Time',"File"]
    df.drop(columns=["File"], inplace=True)

    temp = np.isnan(df.CO2)==False
    first_rec = temp[temp==True].index[0]
    df.iloc[0][['CO2','Temp',"Humidity",'Time']] = list(df.iloc[first_rec][['CO2','Temp',"Humidity"]])+[0]

    for col in ['CO2','Temp',"Humidity",'Time']:
        df[col].interpolate(method='linear', inplace=True) 

    df['Time'] = df['Time'].apply(lambda x: initial_time + pd.Timedelta(milliseconds=x))
    return(df)

col1 , col2 = st.columns([2,2],gap="medium")
col1.write("### 😶‍🌫️ Environmental sensors")
col1.write("The data used in this project was collected from a variety of sensors installed on a vehicle. This includes Inertial Measurement Unit (IMU) sensors, Global Positioning System (GPS) sensors, and Environmental sensors. The environmental sensors record data such as temperature, humidity, and air quality. In this section, we will focus on cleaning and preprocessing the environmental sensor data. In this step, we are going to upload the environmental sensor data. The data should be in CSV format and contain the following columns:")
ENV = col2.file_uploader("Upload your environmental sensor data", type=['csv'])
convert_button = st.button("Convert",use_container_width=True)
with st.expander("**📊 Results**"):
    if convert_button:
        try:
            ENV = pd.read_csv(ENV)
            # Display the data
            col1, col2 = st.columns([1,2], gap=  "large")
            ENV = environmental_sensor_cleaning(ENV, time)
            col1.dataframe(ENV, height=800)
            fig_CO2 = px.area(ENV, x='Time', y="CO2",labels={"CO2":"CO2 (ppm)"}, height=400)
            fig_Temp = px.area(ENV, x='Time', y="Temp",labels={"Temp":"Temperature (°C)"}, height=400)
            fig_Humidity = px.area(ENV, x='Time', y="Humidity",labels={"Humidity":"Humidity (%)"}, height=400)
            fig_acc = px.line(ENV, x='Time', y=["AX", "AY", "AZ"],labels={"value":"Acceleration (m/s^2)"}, height=400)
            col21,col22 = col2.columns([1,1])
            col21.plotly_chart(fig_CO2)
            col22.plotly_chart(fig_Temp)
            col21,col22 = col2.columns([1,1])
            col21.plotly_chart(fig_Humidity)
            col22.plotly_chart(fig_acc)
        except:
            st.error("Please upload the file first 🤨!")
st.divider()
# IMU Sensor Data Cleaning

col1 , col2 = st.columns([2,2],gap="medium")
col1.write("### 🎢 IMU sensors")
col1.write("In this step, we are going to upload the IMU sensor data. The data should be in TXT format:")
number_of_sensors = col2.number_input("Number of IMU sensors", min_value=1, max_value=10, value=1)

def IMU_sensor_add (i):
    col1, col2, col3, col4, col51,col52,col53, col6 = st.columns([1,1,1,1,0.5,0.5,0.5,2])
    type_ = col1.selectbox(f"Type of sensor", options=["Bucket","Arm","Boom","Inside"]           , index=3, key=f"IMU_{i}Type")
    X_ori = col2.selectbox(f"X orientation",  options=["Up","Front","Down","Back","Left","Right"], index=2, key=f"IMU_{i}X")
    Y_ori = col3.selectbox(f"Y orientation",  options=["Up","Front","Down","Back","Left","Right"], index=1, key=f"IMU_{i}Y")
    Z_ori = col4.selectbox(f"Z orientation",  options=["Up","Front","Down","Back","Left","Right"], index=4, key=f"IMU_{i}Z")
        
    hours   = col51.number_input("Hours"  , min_value=0, max_value=23, value=12, key=f"IMU_{i}H")
    minutes = col52.number_input("Minutes", min_value=0, max_value=59, value=0 , key=f"IMU_{i}M")
    seconds = col53.number_input("Seconds", min_value=0, max_value=59, value=0 , key=f"IMU_{i}S")
    time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    IMU  = col6.file_uploader(f"IMU {i+1}", type=['txt'], key=f"IMU_{i}")
    if IMU !=None:
        IMU  = pd.read_csv(IMU, sep=",", header=0)
    else:
        IMU = pd.DataFrame()
    return([type_, X_ori, Y_ori, Z_ori, time, IMU])

def IMU_sensor_cleaning(IMU, time, i):   
    if type(IMU)!=None:    
        IMU= IMU[IMU.columns[:13]]
        IMU['Time'] = pd.to_datetime(IMU['rtcDate']+ ' ' + IMU['rtcTime'])
        IMU['Time'] = IMU['Time']- IMU.iloc[0]['Time']
        IMU['Time'] = IMU['Time'].dt.total_seconds()
        IMU['Time'] = IMU['Time'].apply(lambda x: time + pd.Timedelta(milliseconds=x))
        IMU = IMU[['Time']+list(IMU.columns[2:-2])]
        IMU.set_index('Time', inplace=False)
        IMU.columns = [str(i)+'_'+str(col) for col in IMU.columns]
    else:
        IMU = None
    return(IMU)

imu_df = pd.DataFrame(columns = ['Type', 'X_ori', 'Y_ori', 'Z_ori', 'Time', 'IMU'])

for i in range(number_of_sensors):
            imu_df.loc[i] = IMU_sensor_add (i)
col1, col2 = st.columns([1,1])

IMU_button = col1.button("Convert",use_container_width=True,key="IMU")
with st.expander("**📊 Results**"):
    with st.spinner('Wait for it...'):
        IMU_ed = []
        if IMU_button:
            for i in range(number_of_sensors):
                time = imu_df.loc[i]['Time']
                IMU  = imu_df.loc[i]['IMU']
                IMU  = IMU_sensor_cleaning(IMU, time, i)   
                IMU_ed.append( IMU )
            imu_df ['IMU_ed'] = IMU_ed
            IMU_df = pd.concat([df for df in list(imu_df['IMU_ed'])], axis=1)
            st.dataframe(IMU_df, height=400)

IMU_button_plot = col2.button("Plot",use_container_width=True,key="IMU_plot",disabled=(IMU_button==False))
with st.spinner('Wait for it...'):
    with st.expander("**📊 Plots**"):
        if IMU_button:
            for i in range(number_of_sensors):
                col1, col2, col3 = st.columns([1,1,1])
                AX= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_aX",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col1.plotly_chart(AX)
                AY= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_aY",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col2.plotly_chart(AY)
                AZ= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_aZ",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col3.plotly_chart(AZ)

            for i in range(number_of_sensors):
                col1, col2, col3 = st.columns([1,1,1])
                AX= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_gX",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col1.plotly_chart(AX)
                AY= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_gY",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col2.plotly_chart(AY)
                AZ= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_gZ",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col3.plotly_chart(AZ)

            for i in range(number_of_sensors):
                col1, col2, col3 = st.columns([1,1,1])
                AX= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_mX",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col1.plotly_chart(AX)
                AY= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_mY",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col2.plotly_chart(AY)
                AZ= px.line(IMU_df, x=str(i)+'_Time', y=str(i)+"_mZ",labels={"value":"Acceleration (m/s^2)"}, height=300)
                col3.plotly_chart(AZ)
st.divider()

#GPS Data Cleaning
col1 , col2 = st.columns([2,2],gap="medium")
col1.write("### 🧭 GPS")
col1.write("In this step, we are going to upload the GPS files extracted from the vehicle's dashcam.")
GPS_files = col2.file_uploader("Select all your GPS files!", type=['TXT'], key="GPS", accept_multiple_files=True)
GPS_button_plot = st.button("Analyze",use_container_width=True,key="GPS_file convert")
