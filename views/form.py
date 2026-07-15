import streamlit as st
from db_logic import insert_submission

# Configure the page for a clean, mobile-friendly look
st.set_page_config(page_title="Event Registration", page_icon="📝", layout="centered")

st.title("Event Registration")
st.write("Please fill out the details below to register for the event.")

# Create the form container
with st.form("registration_form"):
    st.subheader("Personal Information")
    first_name = st.text_input("First Name *")
    middle_name = st.text_input("Middle Name (Optional)")
    last_name = st.text_input("Last Name *")
    
    st.subheader("Contact Information")
    phone = st.text_input("Phone Number *")
    email = st.text_input("Email Address *")
    
    st.write("---")
    # Placeholder link for the actual PDF
    st.markdown("📄 [Read our Privacy Policy here](#)") 
    privacy_accepted = st.checkbox("I have read and accept the privacy policy *")
    
    # Submit button
    submitted = st.form_submit_button("Submit Registration", use_container_width=True)
    
    if submitted:
        # 1. Check for missing mandatory fields
        if not first_name or not last_name or not phone or not email:
            st.error("Please fill in all required fields (*).")
        # 2. Check for privacy policy acceptance
        elif not privacy_accepted:
            st.error("You must accept the privacy policy to proceed.")
        # 3. Attempt database insertion
        else:
            result = insert_submission(
                first_name=first_name, 
                middle_name=middle_name, 
                last_name=last_name, 
                phone=phone, 
                email=email, 
                privacy_accepted=privacy_accepted
            )
            
            if result["success"]:
                # Personalized greeting upon successful submission
                st.success(f"Awesome! Thank you, {first_name}. Your registration is complete!")
            else:
                st.error(result["message"])