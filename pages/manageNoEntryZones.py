import streamlit as st
import pandas as pd
import folium

from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_folium import st_folium
from shapely.geometry import shape

from utils.storageHandling import get_files_from_github, load_file_from_github, delete_github_file
from pages.addNoEntryZone import add_no_entry_zone

# Session state to track if add is in process
if "add_area" not in st.session_state:
    st.session_state.add_area = False

st.title("Manage No Entry Zones Around the World")
if st.button("Add Area"):
    st.session_state.add_area = True

path = "areas"
area_files = get_files_from_github(path)

if not area_files:
    st.warning("No areas with no entry zones were found.")
    st.stop()
else:
    # Table data
    table_data = []

    for file_name in area_files:
        zones = load_file_from_github(path,file_name)
        zone_count = len(zones)
        
        # Add to table
        table_data.append({"Area": file_name.replace("_area.json", ""), "# of Zones": zone_count})

    # Convert to DataFrame without index
    df = pd.DataFrame(table_data)

    if st.session_state.add_area:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection(selection_mode="disabled", use_checkbox=False)
        gb.configure_grid_options(suppressCellFocus=True)
        grid_options = gb.build()
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=False,
            height=200
        )
        add_no_entry_zone()
        st.stop()
    else:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection(selection_mode="single", use_checkbox=False)
        gb.configure_grid_options(suppressCellFocus=True)
        grid_options = gb.build()
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=False,
            height=200
        )

    selected_list = grid_response.get('selected_rows', [])
    selected = pd.DataFrame(selected_list)
    
    # Delete Buttons and Map of selected area
    if not selected.empty:
        selected_file = selected.iloc[0]["Area"] + "_area.json"
        if st.button("Delete Area"):
            if delete_github_file("areas", selected_file):
                st.session_state.confirm_delete = None
                st.rerun()
        # Draw map of selected area
        zones_data = load_file_from_github(path, selected_file)
        #st.write(zones_data)
        if not zones_data or len(zones_data) == 0:
            st.write("No zones found in the selected area: " + selected_file)
            st.stop()
        
        zone_index = 1

        for zone in zones_data:
            geometry = zone.get("geometry", {})
            if geometry.get("type") == "Polygon":
                if zone_index == 1:
                    geom = shape(zone["geometry"])
                    centroid = geom.centroid
                    center = (centroid.y, centroid.x)
                    if len(zones_data) > 1:
                        zoom_level = 5
                    else:
                        zoom_level = 7
                    m = folium.Map(location=center, zoom_start=zoom_level)          

                coords = geometry.get("coordinates")[0]  # Outer ring coords
                coords_latlng = [(lat, lng) for lng, lat in coords]

                folium.Polygon(
                    locations=coords_latlng,
                    #color="blue",
                    fill=True,
                    fill_opacity=0.4,
                    popup=f"No Entry Zone"
                ).add_to(m)
                zone_index += 1
        st_folium(m, width=1200, height=450)
