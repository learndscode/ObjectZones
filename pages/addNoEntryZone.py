import streamlit as st
import folium
import json

from streamlit_folium import st_folium
from folium.plugins import Draw
from utils.storageHandling import save_to_github

def add_no_entry_zone():
    st.write("Create or Update No Entry Zones")

    if st.button("Cancel"):
        st.session_state.add_area = False
        st.rerun()
        return

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

    user_input = st.text_input("Provide a Name for Area:")

    if st.button("Save Area"):
        features = output.get("all_drawings")
        if user_input:
            if not features:
                st.error("Please define at least one zone before saving area.")
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
                zone_count = len(polygon_features)

                # Create a new GeoJSON object
                new_geojson = {
                    "area_name": user_input,
                    "zone_count": zone_count,
                    "zones": polygon_features
                }
                # Save to new JSON file
                # Convert to string
                json_str = json.dumps(new_geojson, indent=2)

                # Upload to GitHub "area" folder
                path = f"areas/{user_input}_area.json"  # file path in repo
                commit_message = f"Add area file {user_input}_area.json from app"

                with st.spinner("Saving area..."):
                    #time.sleep(0.1)  # slight delay gives Streamlit time to render spinner
                    response = save_to_github(path, json_str, commit_message)

                    if response.status_code in (200, 201):
                        st.success(f"{user_input} area saved successfully.")
                    else:
                        st.error(f"Failed to save area: {response.status_code} - {response.text}")
        else:
            st.error("Please provide a name for the area.")