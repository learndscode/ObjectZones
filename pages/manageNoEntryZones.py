import streamlit as st
import pandas as pd

from st_aggrid import AgGrid, GridOptionsBuilder
from utils.storageHandling import get_area_files_from_github, load_area_file_from_github, delete_github_file

st.title("Manage No Entry Zones Around the World")
if st.button("Add Area"):
    st.write("Add button clicked")


# Session state to track which file is awaiting deletion confirmation
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

path = "areas"
area_files = get_area_files_from_github(path)

if not area_files:
    st.warning("No areas with no entry zones were found.")
    st.stop()
else:
    # Table data
    table_data = []

    for file_name in area_files:
        zones = load_area_file_from_github(path,file_name)
        zone_count = len(zones)
        
        # Add to table
        table_data.append({"Area": file_name.replace("_area.json", ""), "# of Zones": zone_count})

        # Add all zone shapes to global array
        for zone in zones:
            st.session_state.shapes.append(zone)

    # Convert to DataFrame without index
    df = pd.DataFrame(table_data)

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
    
    # Edit and Delete Buttons and Map of selected area
    if not selected.empty:
        selected_file = selected.iloc[0]["Area"] + "_area.json"
        if st.button("Delete Area"):
            if delete_github_file("areas", selected_file):
                st.session_state.confirm_delete = None
                st.rerun()
        # Draw map of selected area
        zones_data = load_area_file_from_github(path, selected_file)
        #st.write(zones_data)
        if not zones_data or len(zones_data) == 0:
            st.write("No zones found in the selected area: " + selected_file)
            st.stop()
        
        st.write("Zones in Selected Area:" + str(len(zones_data)))

