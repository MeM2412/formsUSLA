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
    with st.expander("📄 Tap to preview Privacy Policy"):
        st.markdown(
"""<div style='font-size: 13px; color: #666666; text-align: justify; line-height: 1.5;'>
<b>DATA PRIVACY POLICY NOTICE</b><br>
<i>Effective Date: July 22, 2026</i><br><br>

By accessing, browsing, or submitting information through our forms, you acknowledge and agree to the following terms regarding the collection, use, and processing of your personal information.<br><br>

<b>1. Information We Collect</b><br>
We collect the personal information you explicitly provide in this form (such as your name, contact details, and any submitted message or responses), as well as standard technical data (such as IP address and browser type) necessary for site security and functionality.<br><br>

<b>2. How We Use Your Data</b><br>
Your information is used strictly to process your requests, communicate with you regarding your submission, provide requested services, and improve our overall operations and user experience.<br><br>

<b>3. Data Sharing & Protection</b><br>
We do not sell, rent, or trade your personal data to third parties. We may share your data with trusted service providers solely for the purpose of operating our website and conducting our business, subject to strict confidentiality agreements. We implement industry-standard technical and organizational measures to ensure your data remains secure against unauthorized access.<br><br>

<b>4. Retention of Information</b><br>
We retain your personal information only for as long as necessary to fulfill the specific purposes for which it was collected, or as required by applicable legal, regulatory, or accounting obligations.<br><br>

<b>5. Your Rights</b><br>
Depending on your jurisdiction, you have the right to request access to, correction of, or deletion of your personal data. You may also withdraw your consent at any time. To exercise these rights, please contact our support team using the information provided below.<br><br>

</div>""", 
            unsafe_allow_html=True
        )

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