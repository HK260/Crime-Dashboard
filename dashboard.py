import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load the dataset
file_path = 'df_merged.csv'  # Update this path
df = pd.read_csv(file_path)

# Approximate coordinates for Indian states (latitude, longitude)
state_coordinates = {
    'Andaman & Nicobar Islands': [11.7401, 92.6586],
    'Andhra Pradesh': [15.9129, 79.7400],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Assam': [26.2006, 92.9376],
    'Bihar': [25.0961, 85.3131],
    'Chandigarh': [30.7333, 76.7794],
    'Chhattisgarh': [21.2787, 81.8661],
    'Dadra and Nagar Haveli': [20.1809, 73.0169],
    'Daman and Diu': [20.3974, 72.8328],
    'Delhi': [28.7041, 77.1025],
    'Goa': [15.2993, 74.1240],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'Himachal Pradesh': [31.1048, 77.1734],
    'Jammu and Kashmir': [34.0837, 74.7973],
    'Jharkhand': [23.6102, 85.2799],
    'Karnataka': [15.3173, 75.7139],
    'Kerala': [10.8505, 76.2711],
    'Ladakh': [34.1526, 77.5770],
    'Lakshadweep': [10.3280, 72.7846],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Maharashtra': [19.7515, 75.7139],
    'Manipur': [24.6637, 93.9063],
    'Meghalaya': [25.4670, 91.3662],
    'Mizoram': [23.1645, 92.9376],
    'Nagaland': [26.1584, 94.5624],
    'Odisha': [20.9517, 85.0985],
    'Puducherry': [11.9416, 79.8083],
    'Punjab': [31.1471, 75.3412],
    'Rajasthan': [27.0238, 74.2179],
    'Sikkim': [27.5330, 88.5122],
    'Tamil Nadu': [11.1271, 78.6569],
    'Telangana': [18.1124, 79.0193],
    'Tripura': [23.9408, 91.9882],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Uttarakhand': [30.0668, 79.0193],
    'West Bengal': [22.9868, 87.8550]
}

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
    if selected_state in state_coordinates:
        state_center = state_coordinates[selected_state]
        m = folium.Map(location=state_center, zoom_start=6)
        folium.Marker(
            location=state_center,
            popup=(
                f"State: {selected_state}<br>"
                f"Recidivism Total: {state_data['Recidivism_Total'].values[0]}<br>"
                f"Economic Setup Total: {state_data['Economic_Set_up_Total'].values[0]}"
            ),
            tooltip=selected_state
        ).add_to(m)
        folium_static(m)
    else:
        st.write("Coordinates for the selected state are not available.")

