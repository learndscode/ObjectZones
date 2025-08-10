import streamlit as st
import pandas as pd

from st_aggrid import AgGrid, GridOptionsBuilder
from utils.storageHandling import get_files_from_github, load_file_from_github, delete_github_file

st.title("Multiple Object Location Info 🏗️")
st.write("**🚧 Under Construction 🚧**")

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



path = "objects"
object_files = get_files_from_github(path)

if not object_files:
    st.warning("No objects were found. Add an object to get started.")
    st.stop()

# Initialize data in session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Object": ["Location A", "Location B"],
        "Latitude": [34.0522, 40.7128],
        "Longitude": [-118.2437, -74.0060],
        "Country": ["USA", "USA"],
        "Closest border": ["Mexico", "Canada"],
        "In no entry zone": [False, True]
    })

def add_blank_row():
    new_row = {
        "Object": "",
        "Latitude": 0.0,
        "Longitude": 0.0,
        "Country": "",
        "Closest border": "",
        "In no entry zone": False
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

def update_columns(df):
    df["Closest border"] = df["Latitude"].apply(lambda x: "Mexico" if x < 36 else "Canada")
    df["In no entry zone"] = df["Latitude"] > 35
    return df

# Buttons for adding and deleting rows in columns
col1, col2 = st.columns(2)
with col1:
    st.button("Add new row", on_click=add_blank_row)
with col2:
    pass  # Delete button below grid

# Update computed columns before showing grid
st.session_state.data = update_columns(st.session_state.data)

# Build grid options with filtering and single row selection (no checkbox)
gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
gb.configure_columns(["Object", "Latitude", "Longitude"], editable=True)
gb.configure_columns(["Country", "Closest border", "In no entry zone"], editable=False)
gb.configure_selection(selection_mode="single", use_checkbox=False)  # No checkboxes here
gb.configure_column("In no entry zone", cellRenderer='agCheckboxCellRenderer')
gb.configure_default_column(filter=True)
grid_options = gb.build()

# Show AgGrid table
grid_response = AgGrid(
    st.session_state.data,
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    update_mode="MODEL_CHANGED",
    fit_columns_on_grid_load=True,
    height=300,
    reload_data=True
)

# Get selected rows for deletion
selected_rows = grid_response["selected_rows"]

selected_list = grid_response.get('selected_rows', [])
selected = pd.DataFrame(selected_list)

# Delete selected row button below grid
if st.button("Delete Selected Row"):
    if not selected.empty:  # Properly check if list is non-empty
        for obj in selected["Object"]:
            st.session_state.data = st.session_state.data[st.session_state.data["Object"] != obj]
        st.success(f"Deleted {len(selected_rows)} row(s)")
        st.session_state.data = st.session_state.data.reset_index(drop=True)
    else:
        st.warning("Please select a row to delete")
