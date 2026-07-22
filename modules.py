import streamlit as st
from db_logic import update_gadget_status

def handle_give_gadget(uid):
    """Callback function to save status and clear stale data."""
    # Convert the Numpy ID to a standard Python integer
    clean_id = int(uid)
    
    # Run the database update and capture whether it succeeded
    success = update_gadget_status(clean_id, True)
    
    if success:
        # Show a green pop-up on the phone
        st.toast("✅ Gadget successfully logged!")
        
        # Force Streamlit to forget the old table so it pulls fresh data
        st.cache_data.clear() 
    else:
        # Show a red pop-up if the database rejected it
        st.error("❌ Database failed to update. Check your deployment logs.")