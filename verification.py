import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Fetch credentials from the .env file
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
verify_sid = os.environ.get("TWILIO_VERIFY_SERVICE_SID")

# Initialize the Twilio client
client = Client(account_sid, auth_token)

def send_sms_code(phone_number):
    """Sends a 6-digit OTP to the provided phone number."""
    try:
        verification = client.verify.v2.services(verify_sid).verifications.create(
            to=phone_number, channel="sms"
        )
        return {"success": True, "status": verification.status}
    except Exception as e:
        return {"success": False, "message": str(e)}

def check_sms_code(phone_number, code):
    """Verifies the code inputted by the user."""
    try:
        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=phone_number, code=code
        )
        if verification_check.status == "approved":
            return {"success": True}
        else:
            return {"success": False, "message": "Invalid code. Please try again."}
    except Exception as e:
        return {"success": False, "message": str(e)}