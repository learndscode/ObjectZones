import streamlit as st

info_page = st.Page("pages/checkObjectNoEntryZone.py", title="Check Object in No Entry Zone", icon="📍")
info_multiple_page = st.Page("pages/checkMultipleNoEntryZones.py", title="Check Multiple Objects in No Entry Zones", icon="🗺️")
zones_page = st.Page("pages/manageNoEntryZones.py", title="Manage No Entry Zones",  icon="🚫")

pg = st.navigation([info_page, info_multiple_page, zones_page])

st.set_page_config(
    page_title="No Entry Zone Manager",
    page_icon="assets/favicon.ico",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

pg.run()