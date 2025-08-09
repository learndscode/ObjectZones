import streamlit as st
import emoji

info_page = st.Page("pages/showBorderProximity.py", title="Show Object Location Info", icon="📍")
zones_page = st.Page("pages/manageNoEntryZones.py", title="Manage No Entry Zones",  icon="🚫")
add_zone = st.Page("pages/addNoEntryZone.py", title="Create/Update No Entry Zones",  icon="➕")

pg = st.navigation([info_page, zones_page, add_zone])

st.set_page_config(
    page_title="Border Proximity",
    page_icon="assets/favicon.ico",  # Optional: You can also set a page icon (favicon)
    layout="wide", # Optional: Set the layout (e.g., "wide" or "centered")
    initial_sidebar_state="auto" # Optional: Control the initial state of the sidebar
)

pg.run()