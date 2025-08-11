from datetime import datetime
import pyautogui

def take_screenshot():
    # Take screenshot and save as PDF
    screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime("Motor Analyzer %Y%m%d_%H%M%S")
    screenshot.convert('RGB').save(f"Record/Screen record/{timestamp}.pdf", 'PDF')
    return timestamp


# import qrcode
# from PIL import Image

#
# def create_motor_qr_code(material_ref, customer_name, date, time):
#     """Generate QR code with motor reference data"""
#
#     # Format data for QR code
#     qr_data = f"""Material Reference: {material_ref}
# Customer Name: {customer_name}
# Date: {date}
# Time: {time}"""
#
#     # Create QR code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_H,
#         box_size=10,
#         border=4,
#     )
#
#     qr.add_data(qr_data)
#     qr.make(fit=True)
#
#     # Generate image
#     qr_img = qr.make_image(fill_color="black", back_color="white")
#
#     return qr_img
#
#
# # Usage example
# qr_image = create_motor_qr_code("1234567843", "Seriar Motor", "10-08-2025", "23:20:32")
# qr_image.save("motor_qr_code.png")
#
