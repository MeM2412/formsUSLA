import qrcode

def create_event_qr(url, filename="event_qr.png"):
    """
    Generates a QR code for the provided URL and saves it as a PNG image.
    """
    # Configure the QR code's visual properties
    qr = qrcode.QRCode(
        version=1, # Controls the size of the QR Code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction so it works even if slightly damaged/covered
        box_size=10, # Size of each 'pixel' in the QR code
        border=4, # Thickness of the white border around the QR code
    )
    
    # Add the URL data
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate the image with a black design on a white background
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to your project folder
    img.save(filename)
    print(f"✅ Success! QR code saved as '{filename}'.")
    print(f"When scanned, it will direct users to: {url}")

if __name__ == "__main__":
    # For now, we will use your local Streamlit URL. 
    # Once you deploy the app to the internet, you will replace this with your public link!
    local_app_url = "http://localhost:8501" 
    
    create_event_qr(url=local_app_url)