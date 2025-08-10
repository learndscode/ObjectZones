import streamlit as st

from utils.geolocate import geoLocateObject, islocationwithinnoentryzone
from utils.displayProximityResult import display_results

st.title("Object Location Info")

object_name = st.text_input(
    label="Enter Object Name",
    placeholder="(Optional)", 
    value="My Object"  # default value
)

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
        if not object_name:
            object_name = "Object"
        # check if the object is within a no entry zone
        result = islocationwithinnoentryzone(object_name, lat_value, lon_value)
        if result[0]:
            st.error(result[1], icon="🚫")
                #f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Object is within a no entry zone.</span>", 
        else:
            st.success(result[1], icon="✅")
                #f"<span style='color: #00c000; background-color: #c7ffc7; padding: 4px;'>Object is not within a no entry zone.</span>",

        # display proximity to border
        display_results(geoLocateObject(lat_value, lon_value), lat_value, lon_value, object_name)
else:
    st.markdown(
            f"<span style='color: #c00000; background-color: #ffc7cf; padding: 4px;'>Enter a latitude and longitude</span>",
            unsafe_allow_html=True
    )