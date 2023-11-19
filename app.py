import streamlit as st
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from folium.plugins import HeatMap

EMISSION_FACTORS = {
    "India": {
        "name": "India",
        "Road Freight": 0.00016667,
        "Rail Freight": 0.00002273,
        "Sea Freight": 0.00004167,
        "Air Freight": 0.00083333,
        "Electricity": 0.82,
    },
    "Indonesia": {
        "name": "Indonesia",
        "Road Freight": 0.00016667,
        "Rail Freight": 0.00002273,
        "Sea Freight": 0.00004167,
        "Air Freight": 0.00083333,
        "Electricity": 0.6,
    },
    "US": {
        "name": "US",
        "Road Freight": 0.00016667,
        "Rail Freight": 0.00002273,
        "Sea Freight": 0.00004167,
        "Air Freight": 0.00083333,
        "Electricity": 0.45,
    },
    "UK": {
        "name": "UK",
        "Road Freight": 0.00016667,
        "Rail Freight": 0.00002273,
        "Sea Freight": 0.00004167,
        "Air Freight": 0.00083333,
        "Electricity": 0.75,
    },
}

st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

st.title("Calculate total emission from your company ⚠️")

st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["India", "Indonesia", "US", "UK"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

    st.subheader("🚗 Road Freight")
    distance_road_weight = st.slider(
        "Total weight of goods transported with road freight (kg)",
        0.0,
        100.0,
        key="distance_road_weight_input",
    )
    distance_road_distance = st.slider(
        "Total distance of goods transported with road freight (km)",
        0.0,
        100.0,
        key="distance_road_distance_input",
    )

    st.subheader("🚂 Rail Freight")
    distance_rail_weight = st.slider(
        "Total weight of goods transported with Rail freight (kg)",
        0.0,
        100.0,
        key="distance_rail_weight_input",
    )
    distance_rail_distance = st.slider(
        "Total distance of goods transported with Rail freight (km)",
        0.0,
        100.0,
        key="distance_rail_distance_input",
    )

with col2:
    st.subheader("🛩️ Air Freight")
    distance_air_weight = st.slider(
        "Total weight of goods transported with Air freight (kg)",
        0.0,
        100.0,
        key="distance_air_weight_input",
    )
    distance_air_distance = st.slider(
        "Total distance of goods transported with Air freight (km)",
        0.0,
        100.0,
        key="distance_air_distance_input",
    )

    st.subheader("🚢 Sea Freight")
    distance_sea_weight = st.slider(
        "Total weight of goods transported with Sea freight (kg)",
        0.0,
        100.0,
        key="distance_sea_weight_input",
    )
    distance_sea_distance = st.slider(
        "Total distance of goods transported with Sea freight (km)",
        0.0,
        100.0,
        key="distance_sea_distance_input",
    )

# Normalize inputs
if electricity > 0:
    electricity = electricity * 12  # Convert monthly electricity to yearly


# Calculate carbon emissions
road_freight_emissions = (
    EMISSION_FACTORS[country]["Road Freight"]
    * distance_road_distance
    * distance_road_weight
)
rail_freight_emissions = (
    EMISSION_FACTORS[country]["Rail Freight"]
    * distance_rail_distance
    * distance_rail_weight
)
sea_freight_emissions = (
    EMISSION_FACTORS[country]["Sea Freight"]
    * distance_sea_distance
    * distance_sea_weight
)
air_freight_emissions = (
    EMISSION_FACTORS[country]["Air Freight"]
    * distance_air_distance
    * distance_air_weight
)
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity


# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = (
    road_freight_emissions
    + rail_freight_emissions
    + sea_freight_emissions
    + air_freight_emissions
)

transportation_emissions = round(transportation_emissions / 1, 2)
electricity_emissions = round(electricity_emissions / 1000000, 2)

total_emissions = round(
    transportation_emissions + electricity_emissions,
    2,
)

if st.button("Calculate CO2 Emissions"):
    # Display results
    st.header("Results")

    # # Data
    categories = [
        "Road Freight",
        "Rail Freight",
        "Sea Freight",
        "Air Freight",
        "Electricity",
    ]
    co2_emissions = [
        road_freight_emissions,
        rail_freight_emissions,
        sea_freight_emissions,
        air_freight_emissions,
        electricity_emissions,
    ]

    # # Data
    # locations = {
    #     "Transportation": {"latitude": 37.7749, "longitude": -122.4194},
    #     "Electricity": {"latitude": 34.0522, "longitude": -118.2437},
    #     "Diet": {"latitude": 40.7128, "longitude": -74.0060},
    #     "Waste": {"latitude": 41.8781, "longitude": -87.6298},
    # }
    # emissions = [1.52, 2.68, 0.91, 0.02]

    # Create two columns
    col1, col2 = st.columns(2)

    # Column 1: Bar Chart
    col1.write("## CO2 Emissions by Category (Bar Chart)")
    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(
        categories, co2_emissions, color=["skyblue", "lightgreen", "lightcoral", "gold"]
    )
    ax_bar.set_ylabel("CO2 Emissions (tonnes per year)")
    col1.pyplot(fig_bar)

    # Column 2: Pie Chart
    col2.write("## CO2 Emissions by Category (Pie Chart)")
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(
        co2_emissions,
        labels=categories,
        autopct="%1.1f%%",
        startangle=70,
        colors=["skyblue", "lightgreen", "lightcoral", "gold"],
    )
    ax_pie.axis("equal")
    col2.pyplot(fig_pie)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} kg CO2e CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(
            f"""🌍 Your total carbon footprint is: {total_emissions} kg CO2e per year"""
        )
        st.warning(
            f"""In 2021, CO2 emissions per capita for {EMISSION_FACTORS[country]["name"]} was 1.9 tons of CO2 per capita. Between 1972 and 2021, CO2 emissions per capita of {EMISSION_FACTORS[country]["name"]} grew substantially from 0.39 to 1.9 tons of CO2 per capita rising at an increasing annual rate that reached a maximum of 9.41% in 2021"""
        )
