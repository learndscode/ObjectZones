import streamlit as st
import folium
import json

from streamlit_folium import st_folium
from folium.plugins import Draw

st.title("Create / Update No Entry Zone(s)")

# Create a Folium map centered somewhere
m = folium.Map(location=[40, -100], zoom_start=4)

# Add drawing controls
draw = Draw(
    draw_options={
        'polyline': False,    # Disable polyline drawing
        'polygon': True,
        'circle': False,      # Disable circle drawing
        'rectangle': True,
        'marker': False,
        'circlemarker': False
    },
    edit_options={'edit': True}
)
#draw = Draw(export=True)
draw.add_to(m)
m.save('map.html')

# Display map with drawing enabled
output = st_folium(m, width=1200, height=500)

user_input = st.text_input("Provide a Name for Zone(s):")

if st.button("Save Zone(s)"):
    features = output.get("all_drawings")
    if user_input:
        if not features:
            st.error("Please define at least one zone before saving.")
        else:
            # Rename the top-level feature type to "Zone": 
            for feature in features:
                if feature.get("type") == "Feature":
                    feature["type"] = "Zone"
            
            # Filter only Polygon features
            polygon_features = [
                feature for feature in features
                if feature.get("geometry", {}).get("type") == "Polygon"
            ]

            # Create a new GeoJSON object
            new_geojson = {
                "zone_name": user_input,
                "zones": polygon_features
            }
            # Save to new JSON file
                       

            st.success(f"Zone '{user_input}' saved successfully!")
            st.write("GeoJSON Data:", new_geojson)
    else:
        st.error("Please provide a name for the zone.")