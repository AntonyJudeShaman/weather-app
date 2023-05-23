import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
from dateutil import parser

owm = pyowm.OWM('fbe1c93ce010fc592ace7e5823166fba')
mgr = owm.weather_manager()

buff, col, buff2 = st.columns([1,5,1])

col.markdown("<h1 style='text-align: center;'>Weather Forecasting</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        color: Aliceblue;
        background-image: linear-gradient(to bottom left, #08307c, #013a45) !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    [data-testid="stVerticalBlock"]{
        background-color: linear-gradient(to bottom left, #2193b0 ,#6dd5ed) !important;
        
        padding-bottom: 40px;
    }
    
    
    </style>
    """,
    unsafe_allow_html=True
)
place = col.text_input("Enter a city:", "")

if place == '':
    col.write("Please enter a city")

unit = col.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = col.selectbox("Select Graph Type", ("Line Chart", "Bar Graph","Scatter Plot"))

submit_button = col.button("Submit")

if submit_button:
    if place != "":
        forecast = mgr.forecast_at_place(place, '3h')

        dates_list = []
        temperatures = []
        for weather in forecast.forecast:
            date_str = weather.reference_time('iso')
            date = parser.isoparse(date_str).date()
            temperature = weather.temperature(unit=unit.lower())['temp']
            dates_list.append(date)
            temperatures.append(temperature)

        col1, col2 = st.columns(2)

        with col1:
            for date, temp in zip(dates_list, temperatures):
                st.write(f"Date: {date}, Temperature: {temp} {unit}")

        with col2:
            if g_type == "Line Chart":
                plt.plot(dates_list, temperatures)
                plt.xlabel('Date')
                plt.ylabel('Temperature (' + unit + ')')
                plt.title('Temperature Variation')
                plt.xticks(rotation=90)
                st.pyplot(plt)
            elif g_type == "Bar Graph":
                plt.bar(dates_list, temperatures)
                plt.xlabel('Date')
                plt.ylabel('Temperature (' + unit + ')')
                plt.title('Temperature Variation')
                plt.xticks(rotation=90)
                st.pyplot(plt)    
            elif g_type == "Scatter Plot":
                plt.scatter(dates_list, temperatures)
                plt.xlabel('Date')
                plt.ylabel('Temperature (' + unit + ')')
                plt.title('Temperature Variation')
                plt.xticks(rotation=90)
                st.pyplot(plt)
            else:
                st.write("Invalid graph type selected.")
