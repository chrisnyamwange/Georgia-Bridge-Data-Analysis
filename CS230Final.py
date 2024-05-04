'''
"Name: Chris Nyamwange
CS230: Section 2
Data: Georgia Bridges
Description:
This program ... (a few sentences about your program and the queries and charts)

'''

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os  
import pydeck as pdk

#read in data
def read_data():
    df = pd.read_csv('C:\\Users\\chris\\eclipse-workspace\\CS230FINAL\\FILES\\Georgia_Bridges_10000_sample.csv', low_memory=False).set_index('8 - Structure Number')
    return df 

#HARDCODED DATA
countyLst = ['Chatham County', 'Bibb County', 'Worth County']
conditionLst = ['Fair', 'Poor']



# filter for all bridges in <3 - County Name> with <CAT10 - Bridge Condition>
def filter1(df, countyLst, conditionLst):
    df = read_data()
    # create a new df with only the necessary columns
    df1 = df[["3 - County Name","CAT10 - Bridge Condition", "16 - Latitude (decimal)", "17 - Longitude (decimal)"]]
    # check if the updated df has the selected conditions
    df1 = df1[(df1["3 - County Name"].isin(countyLst)) & (df1["CAT10 - Bridge Condition"].isin(conditionLst))]
    return df1
print(filter1(df, countyLst, conditionLst))
df1 = filter1(df, countyLst, conditionLst)
def plot1(df1):
    # Create a Pydeck layer for the map
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df1,
        get_position=["17 - Longitude (decimal)", "16 - Latitude (decimal)"],
        get_radius=1000,  # Adjust the radius as needed
        get_fill_color=[255, 0, 0],  # Red color for points
        pickable=True
    )

    # Set the initial viewport for the map
    view_state = pdk.ViewState(
        longitude=float(df1["17 - Longitude (decimal)"].mean()),  # Set longitude of the center of the map
        latitude=float(df1["16 - Latitude (decimal)"].mean()),  # Set latitude of the center of the map
        zoom=5  # Set initial zoom level
    )

    # Create the Pydeck map
    map1 = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    )

    # Show the map
    st.pydeck_chart(map1)
plot1(df1)
