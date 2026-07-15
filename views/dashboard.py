import streamlit as st
import pandas as pd
import os
from db_logic import get_all_submissions
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Organizer Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------
# Authentication Routing
# ---------------------------------------------------------
expected_password = os.environ.get("ADMIN_PASSWORD")

# Create a password input field
password_attempt = st.sidebar.text_input("Admin Password", type="password")

if password_attempt != expected_password:
    st.warning("🔒 Please enter the correct password in the sidebar to access the dashboard.")
    st.stop() # This prevents the rest of the page from loading

# ---------------------------------------------------------
# Dashboard Logic (Only runs if password is correct)
# ---------------------------------------------------------
st.title("Admin: Event Registration Dashboard")
st.write("Monitor incoming event registrations in real-time.")

# Fetch the data
result = get_all_submissions()

if result["success"]:
    data = result["data"]
    columns = result["columns"]
    
    if len(data) > 0:
        # Convert the raw database rows into a Pandas DataFrame for easy viewing
        df = pd.DataFrame(data, columns=columns)
        
        # Display high-level metrics
        st.metric(label="Total Registrations", value=len(df))
        
        st.write("### Live Data")
        # Display the interactive table
        st.dataframe(df, use_container_width=True)
        
        # Convert the dataframe to a CSV format for the export button
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        st.write("---")
        st.write("### Export Data")
        # Streamlit's built-in download button for easy Excel/Sheets integration
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv_data,
            file_name="event_registrations.csv",
            mime="text/csv"
        )
        
    else:
        st.info("No registrations have been submitted yet.")
        
else:
    st.error(f"Database Error: {result['message']}")