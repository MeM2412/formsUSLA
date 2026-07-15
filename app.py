import streamlit as st

# 1. Define the pages and their file paths
form_page = st.Page(
    page="views/form.py", 
    title="Event Registration", 
    default=True # This is what loads at the base URL
)

admin_page = st.Page(
    page="views/dashboard.py", 
    title="Organizer Dashboard", 
    url_path="admin" # This sets the secret URL extension
)

# 2. Configure the navigation router and hide the sidebar
pg = st.navigation(
    pages=[form_page, admin_page], 
    position="hidden" # This completely removes the sidebar menu
)

# 3. Run the application
pg.run()