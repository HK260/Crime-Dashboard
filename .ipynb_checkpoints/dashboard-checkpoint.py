# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Load the dataset
df = pd.read_csv('df_merged.csv')

# Load the GeoJSON file for India's states
geojson_url = 'https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson'
gdf = gpd.read_file(geojson_url)

# Sidebar for user input
st.sidebar.title("Crime Data EDA")
selected_state = st.sidebar.selectbox("Select State", df['Area_Name'].unique())
analysis_type = st.sidebar.selectbox("Select Analysis Type", ["Overview", "Time-Series", "Geographical"])

# Filter data based on user selection
state_data = df[df['Area_Name'] == selected_state]

# Main dashboard area
st.title(f"Exploratory Data Analysis for {selected_state}")

if analysis_type == "Overview":
    st.header("Data Overview")
    st.write(state_data.describe())

elif analysis_type == "Time-Series":
    st.header("Time-Series Analysis")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Year', y='Recidivism_Total', data=state_data)
    plt.title(f"Recidivism Trend in {selected_state}")
    st.pyplot(plt)

elif analysis_type == "Geographical":
    st.header("Geographical Analysis")

    # Merge the state data with the GeoDataFrame
    gdf['state_name'] = gdf['STATE'].str.lower()  # Adjust 'STATE' to match the column name in your geojson
    merged_gdf = gdf[gdf['state_name'] == selected_state.lower()]
    if merged_gdf.empty:
        st.write("State not found in GeoJSON data.")
    else:
        merged_gdf = merged_gdf.assign(Recidivism_Total=state_data['Recidivism_Total'].values[0])

        # Create a folium map centered on the selected state
        state_center = [merged_gdf.geometry.centroid.y.mean(), merged_gdf.geometry.centroid.x.mean()]
        m = folium.Map(location=state_center, zoom_start=6)

        # Add state boundaries to the map
        folium.GeoJson(
            merged_gdf,
            name='geojson',
            tooltip=folium.features.GeoJsonTooltip(
                fields=['STATE', 'Recidivism_Total'],  # Update fields to include those you want to display
                aliases=['State', 'Recidivism Total'],  # Update aliases as needed
                localize=True
            )
        ).add_to(m)

        # Display the map
        folium_static(m)

# Run the dashboard
# streamlit run dashboard.py

