import streamlit as st
import pandas as pd

from utils.storageHandling import get_area_files_from_github, load_area_file_from_github

st.title("Manage No Entry Zones Around the World")

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
    st.session_state.shapes = []

    for file_name in area_files:
        zones = load_area_file_from_github(path,file_name)
        zone_count = len(zones)
        
        # Add to table
        table_data.append({"File Name": file_name.replace("_area.json", ""), "Zone Count": zone_count})

        # Add all zone shapes to global array
        for zone in zones:
            st.session_state.shapes.append(zone)

    # Convert to DataFrame without index
    df = pd.DataFrame(table_data)

    # Reset index so it doesn't show
    st.dataframe(df, hide_index=True)


