"""
Helper script to generate a test QR code image for testing the scanner
"""

import qrcode
from PIL import Image

def generate_test_qr(data="Hello, QR Scanner!", filename="test_qr_code.png"):
    """Generate a test QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"Test QR code generated: {filename}")
    print(f"QR Code contains: {data}")
    return filename

if __name__ == "__main__":
    import sys
    data = sys.argv[1] if len(sys.argv) > 1 else "Hello, QR Scanner! This is a test QR code."
    filename = sys.argv[2] if len(sys.argv) > 2 else "test_qr_code.png"
    generate_test_qr(data, filename)

