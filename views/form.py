import streamlit as st
from db_logic import insert_submission
from verification import send_sms_code, check_sms_code

# Initialize Session States to track user progress during the app refresh
if 'sms_sent' not in st.session_state:
    st.session_state.sms_sent = False
if 'phone_verified' not in st.session_state:
    st.session_state.phone_verified = False

st.title("Get Your Gadget!")
st.write("Please fill out the details below to get your gadget.")

with st.form("registration_form"):
    st.subheader("Personal Information")
    first_name = st.text_input("First Name *")
    middle_name = st.text_input("Middle Name (Optional)")
    last_name = st.text_input("Last Name *")
    
    st.subheader("Contact Information")
    email = st.text_input("Email Address *")
    
    # Phone Number Input formatting instructions: +1234567890
    # Ask for just the 10 digits
    phone_input = st.text_input("Phone Number *", max_chars=10, placeholder="3055551234")
    
    # Automatically format it for Twilio and the database
    formatted_phone = f"+1{phone_input}" if phone_input else ""
    
    st.write("---")
    st.markdown("📄 [Read our Privacy Policy here](#)") 
    privacy_accepted = st.checkbox("I have read and accept the privacy policy *")
    
    # ---------------------------------------------------------
    # SMS Verification UI Block
    # ---------------------------------------------------------
    st.write("### Phone Verification")
    
    if not st.session_state.phone_verified:
        # Button to trigger the SMS
        send_code_btn = st.form_submit_button("1. Send Verification Code")
        
        if send_code_btn:
            if not phone_input or len(phone_input) != 10 or not phone_input.isdigit():
                st.error("Please enter a valid 10-digit phone number without dashes or spaces.")
            else:
                # Use the formatted_phone variable here!
                result = send_sms_code(formatted_phone)
                if result["success"]:
                    st.session_state.sms_sent = True
                    st.success("Verification code sent! Please check your messages.")
                else:
                    st.error(f"Failed to send code: {result['message']}")
        
        # Input field for the 6-digit OTP
        if st.session_state.sms_sent:
            entered_code = st.text_input("Enter 6-digit code")
            verify_code_btn = st.form_submit_button("2. Verify Code")
            
            if verify_code_btn and entered_code:
                check_result = check_sms_code(formatted_phone, entered_code)
                if check_result["success"]:
                    st.session_state.phone_verified = True
                    st.success("Phone verified successfully!")
                    st.rerun() # Refresh the UI to instantly unlock the final submit button
                else:
                    st.error(check_result["message"])
    else:
        st.success(f"✅ Phone number securely verified.")
    
    # ---------------------------------------------------------
    # Final Submission Block
    # ---------------------------------------------------------
    st.write("---")
    # Disable the final submit button until the phone is verified
    submit_disabled = not st.session_state.phone_verified
    
    submitted = st.form_submit_button("Submit Registration", disabled=submit_disabled, use_container_width=True)
    
    if submitted:
        if not first_name or not last_name or not formatted_phone or not email:
            st.error("Please fill in all required fields (*).")
        elif not privacy_accepted:
            st.error("You must accept the privacy policy to proceed.")
        else:
            db_result = insert_submission(
                first_name=first_name, 
                middle_name=middle_name, 
                last_name=last_name, 
                phone=formatted_phone, 
                email=email, 
                privacy_accepted=privacy_accepted
            )
            
            if db_result["success"]:
                st.success(f"Awesome! Thank you, {first_name}. Your registration is complete!")
            else:
                st.error(db_result["message"])