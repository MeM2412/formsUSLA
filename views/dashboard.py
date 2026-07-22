import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from db_logic import get_all_submissions, update_gadget_status
from modules import handle_give_gadget

load_dotenv()

expected_password = os.environ.get("ADMIN_PASSWORD")

# ---------------------------------------------------------
# Authentication (Main Page, No Sidebar)
# ---------------------------------------------------------
# Remember if the user is logged in across page refreshes
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Centered login form
    st.write("### 🔒 Organizer Dashboard")
    st.write("Please enter the admin password to view live registrations.")
    
    with st.form("login_form"):
        password_attempt = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In", use_container_width=True)
        
        if submitted:
            if password_attempt == expected_password:
                st.session_state.authenticated = True
                st.rerun() # Refresh immediately to load the dashboard
            else:
                st.error("Incorrect password. Please try again.")
    
    # Stop the script here so the data below is completely protected
    st.stop() 

# ---------------------------------------------------------
# Dashboard Logic (Only runs if authenticated)
# ---------------------------------------------------------

# Automatically refresh this page every 10 seconds (10000 milliseconds)
st_autorefresh(interval=10000, key="data_refresh")

# Header with a Logout button
col1, col2 = st.columns([8, 2])
col1.title("Admin Dashboard")
if col2.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

# Fetch your data
raw_data = get_all_submissions()

# Safely count the records based on how the database returns them
if isinstance(raw_data, dict) and "data" in raw_data:
    total_users = len(raw_data["data"])
elif isinstance(raw_data, list):
    total_users = len(raw_data)
else:
    total_users = 0

# Use columns to keep the little square compact on the left side
col1, col2, col3 = st.columns([1, 1, 2])
col1.metric("Registered Attendees", total_users)

#-------

# Safely extract the list of records depending on how db_logic.py returns it
if isinstance(raw_data, dict) and "data" in raw_data:
    df = pd.DataFrame(raw_data["data"])
elif isinstance(raw_data, dict):
    # Fallback just in case it's a flat dictionary
    df = pd.DataFrame([raw_data])
else:
    # If it is already a clean list of records
    df = pd.DataFrame(raw_data)

# DF
if not df.empty:
    st.write("---")
    st.write("### Recent Registrations")
    
    # --- Slim Down the Master Table ---
    # The column indices you want to hide (0-indexed, so 0 is the first column)
    indices_to_hide = [0, 2]
    
    # Safety check: Only try to drop indices that actually exist in the table
    valid_indices = [i for i in indices_to_hide if i < len(df.columns)]
    
    # Get the actual names of the columns at those positions
    cols_to_drop = df.columns[valid_indices]
    
    # Drop them to create the clean display table
    display_df = df.drop(columns=cols_to_drop)

    # Rename Columns 
    display_df = display_df.rename(columns={
        0: "#",
        1: "First Name",
        3: "Last Name",
        4: "Phone Number",
        5: "Email Address",
        6: "Date/Time",
        7: "Gadget Given"
    })

    # Display the simplified table without the row index numbersS
    st.dataframe(display_df, hide_index=True, use_container_width=True)

    # Implement the "Give Gadget" Action Button
    with st.popover("🎁 Give Gadget", use_container_width=True):
        st.write("**Attendees waiting for a gadget:**")
        
        # Filter the original df to find people where column 7 (Gadget Given) is not True
        # Dynamically find the ID of the last column (Gadget Given)
        last_col_id = df.columns[-1]
        
        # Filter the original df using that dynamic ID
        pending_users = df[df[last_col_id] != True]
        
        if pending_users.empty:
            st.success("Awesome! Everyone has received their gadget.")
        else:
            # Loop through the pending users to create a list with "Give" buttons
            for index, row in pending_users.iterrows():
                user_id = row[0]
                first_name = row[1]
                last_name = row[3]
                
                col1, col2 = st.columns([7, 3])
                col1.write(f"👤 {first_name} {last_name}")
                
                # 3. Use 'on_click' and 'args' instead of checking if the button was clicked
                col2.button(
                    label="Give", 
                    key=f"give_btn_{user_id}", 
                    type="primary", 
                    use_container_width=True,
                    on_click=handle_give_gadget,  # Point to the function
                    args=(user_id,)               # Hand the function the user_id
                )

    # end of the table
    # The download button always grabs the FULL dataframe (df), not the slimmed down one
    st.write("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full CSV Database",
        data=csv,
        file_name='event_registrations.csv',
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("No registrations yet. Waiting for attendees...")