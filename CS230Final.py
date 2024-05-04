import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

# read in data
def read_data():
    df = pd.read_csv('C:\\Users\\chris\\eclipse-workspace\\CS230FINAL\\FILES\\Georgia_Bridges_10000_sample.csv', low_memory=False).set_index('8 - Structure Number')
    return df 

def filter1(df, countyLst, conditionLst):
    # Filter the data based on countyLst and conditionLst
    df_filtered = df[(df["3 - County Name"].isin(countyLst)) & (df["CAT10 - Bridge Condition"].isin(conditionLst))]
    return df_filtered

def plot1(df):
    if not df.empty:
        # Rename columns to simpler names without spaces
        df = df.rename(columns={"16 - Latitude (decimal)": "latitude", "17 - Longitude (decimal)": "longitude"})

        # Define color mapping for bridge conditions
        color_mapping = {
            'Poor': [255, 0, 0, 255],  # Red color for Poor condition
            'Fair': [255, 255, 0, 255],  # Yellow color for Fair condition
            'Good': [0, 255, 0, 255]  # Green color for Good condition
        }

        # Map condition to color for each data point
        df['color'] = df['CAT10 - Bridge Condition'].map(color_mapping)

        # Create a PyDeck ScatterplotLayer
        scatterplot = pdk.Layer(
            "ScatterplotLayer",
            df,
            get_position=["longitude", "latitude"],
            get_radius=500,
            get_fill_color="color",  # Fill color based on condition
            stroked=True,  # Enable stroke (outline)
            get_line_color=[0, 0, 0],  # Outline color (black)
            get_line_width=10,  # Width of the outline
            pickable=True,
            auto_highlight=True
        )

        # Set the viewport for the map
        view_state = pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=7
        )

        # Render the map with PyDeck
        r = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            layers=[scatterplot],
            initial_view_state=view_state
        )

        # Display the map using Streamlit
        st.pydeck_chart(r)
    else:
        st.warning("No data available with the selected filters.")

def filter2(df, startYr, endYr):
    # Filter data based on start year and end year
    df_filtered = df[(df["27 - Year Built"] >= startYr) & (df["27 - Year Built"] <= endYr)]
    return df_filtered

def plot2(df_filtered, startYr, endYr):
    # Create a DataFrame with all years in the range
    all_years = pd.DataFrame(index=range(int(startYr), int(endYr) + 1))

    # Count occurrences of each year
    year_counts = df_filtered["27 - Year Built"].value_counts().sort_index()

    # Merge with all_years DataFrame to ensure all years are included
    merged_counts = all_years.join(year_counts, how="left").fillna(0)

    # Create a bar chart
    plt.bar(merged_counts.index, merged_counts.values.flatten())
    plt.xlabel('Year')
    plt.ylabel('Number of Bridges')
    plt.title('Number of Bridges Built Each Year')

    # Set x-axis tick locations and labels for integer years
    num_years = int(endYr) - int(startYr) + 1
    if num_years <= 20:
        # Show all years if the range is small
        plt.xticks(np.arange(startYr, endYr + 1, 1), rotation=90)
    elif num_years <= 50:
        # Show every other year if the range is medium
        plt.xticks(np.arange(startYr, endYr + 1, 2), rotation=90)
    else:
        # Show only every 5th year if the range is large
        plt.xticks(np.arange(startYr, endYr + 1, 5), rotation=90)

    # Display the chart in Streamlit
    st.pyplot()

def filter3(df, minLength, maxLength=None):
    # If maxLength is not provided, set it to the maximum value in the DataFrame
    if maxLength is None:
        maxLength = df["49 - Structure Length (ft.)"].max()
    
    # Filter data based on minimum and maximum structure lengths
    df_filtered = df[(df["49 - Structure Length (ft.)"] >= minLength) & (df["49 - Structure Length (ft.)"] <= maxLength)]
    return df_filtered

def plot3(df_filtered):
    # Create a scatterplot
    plt.scatter(df_filtered["49 - Structure Length (ft.)"], df_filtered["29 - Average Daily Traffic"], s=4)
    plt.xlabel('Structure Length (ft.)')
    plt.ylabel('Average Daily Traffic')
    plt.title('Correlation between Structure Length and Average Daily Traffic')
    
    # Display the chart in Streamlit
    st.pyplot()

def homepage():
    st.title("Georgia Bridges Data Analysis")
    st.text("Navigate the side menu to learn more ! :)")
    st.image("C:\\Users\\chris\\eclipse-workspace\\CS230FINAL\\FILES\\goku-jumping-goku.gif", use_column_width=True)

def main():
    # Read data
    df = read_data()

    page = st.sidebar.selectbox("Select Page", ["Home", "Bridge Conditions", "Bridge Years", "Bridge Length"])

    if page == "Home":
        homepage()
    elif page == "Bridge Conditions":
        # Multiselect for county selection
        countyLst = st.multiselect("Select County(s)", sorted(df["3 - County Name"].unique()))

        # Slider for condition selection
        conditionLst = st.multiselect("Select Condition(s)", df["CAT10 - Bridge Condition"].unique())

        # Filter data using filter1
        filtered_df = filter1(df, countyLst, conditionLst)

        # Plot filtered data using plot1
        plot1(filtered_df)
    elif page == "Bridge Years":
        # Number input boxes for start year and end year
        startYr = st.number_input("Enter Start Year", min_value=int(df["27 - Year Built"].min()), max_value=int(df["27 - Year Built"].max()))
        endYr = st.number_input("Enter End Year", min_value=int(df["27 - Year Built"].min()), max_value=int(df["27 - Year Built"].max()))

        # Filter data using filter2
        filtered_df2 = filter2(df, startYr, endYr)

        # Plot filtered data using plot2, passing startYr and endYr as arguments
        plot2(filtered_df2, startYr, endYr)
    elif page == "Bridge Length":
        # Slider for minimum and maximum structure lengths
        minLength, maxLength = st.slider("Select Minimum and Maximum Structure Lengths", min_value=df["49 - Structure Length (ft.)"].min(), max_value=df["49 - Structure Length (ft.)"].max(), value=(df["49 - Structure Length (ft.)"].min(), df["49 - Structure Length (ft.)"].max()))

        # Check if the minimum length is larger than the maximum length
        if minLength > maxLength:
            st.warning("Minimum length cannot be larger than maximum length. Please adjust the sliders.")
            return

        # Filter data based on minimum and maximum structure lengths
        filtered_df3 = filter3(df, minLength, maxLength)

        # Plot filtered data using plot3, passing filtered_df3 as argument
        plot3(filtered_df3)

if __name__ == "__main__":
    main()
