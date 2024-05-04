import pandas as pd
import streamlit as st
import pydeck as pdk

# read in data
def read_data():
    # Sample data
    data = {
        '3 - County Name': ['Chatham County', 'Chatham County', 'Bibb County', 'Bibb County'],
        'CAT10 - Bridge Condition': ['Fair', 'Poor', 'Fair', 'Poor'],
        '16 - Latitude (decimal)': [32.0804, 32.0855, 32.8354, 32.8456],
        '17 - Longitude (decimal)': [-81.0912, -81.0952, -83.7123, -83.7245]
    }

    df = pd.DataFrame(data)
    return df 

# filter for all bridges in <3 - County Name> with <CAT10 - Bridge Condition>
def filter1(df, countyLst, conditionLst):
    # create a new df with only the necessary columns
    df1 = df[["3 - County Name","CAT10 - Bridge Condition", "16 - Latitude (decimal)", "17 - Longitude (decimal)"]]
    # check if the updated df has the selected conditions
    df1 = df1[(df1["3 - County Name"].isin(countyLst)) & (df1["CAT10 - Bridge Condition"].isin(conditionLst))]
    return df1

def plot1(df1):
    # Define the scatterplot layer
    scatterplot = pdk.Layer(
        "ScatterplotLayer",
        data=df1,
        get_position=["17 - Longitude (decimal)", "16 - Latitude (decimal)"],
        get_radius=100,
        get_fill_color=[255, 0, 0],  # Red color
        pickable=True
    )

    # Set the initial viewport with static values
    view_state = pdk.ViewState(
        latitude=df1["16 - Latitude (decimal)"].mean(),
        longitude=df1["17 - Longitude (decimal)"].mean(),
        zoom=6,
        pitch=0
    )

    # Create the Deck object
    deck = pdk.Deck(
        layers=[scatterplot],
        initial_view_state=view_state,
    )
    return deck

# Call the read_data function
df = read_data()

#HARDCODED DATA
countyLst = ['Chatham County', 'Bibb County']
conditionLst = ['Fair', 'Poor']

# Call the filter1 function with the read data
df1 = filter1(df, countyLst, conditionLst)

# Call the plot1 function with the filtered dataframe
deck = plot1(df1)

# Display the PyDeck chart
st.pydeck_chart(deck)
