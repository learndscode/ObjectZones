import streamlit as st

from utils.geolocate import geoLocateObject
from utils.displayProximityResult import display_results

st.title("Object Location Info")

# Get longitude and latitude coordinates
lat_value = st.number_input(
    label="Enter Object's Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=32.7767,     # default
    step=1.0
)

lon_value = st.number_input(
    label="Enter Object's Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=-96.797,     # default
    step=1.0
)

if isinstance(lat_value, (int, float)) and isinstance(lon_value, (int, float)):
    if st.button("Check No Entry Zone"):
        display_results(geoLocateObject(lat_value, lon_value), lat_value, lon_value)
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )