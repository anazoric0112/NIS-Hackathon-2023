import qrcode
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image

# Returns bytes that represent QR code image
# data : User card identification in string format
def generate_qr_code_bytes(data : str = "http://127.0.0.1:8000/"):

    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)

    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_bytes = buffer.getvalue()

    return qr_bytes


# Returns QR code image
# data : Bytes representing QR code
def decode_qr_bytes(data):
    qr_img = Image.open(BytesIO(data))
    data_decoded = decode(qr_img)

    if data_decoded:
        data_str = []
        for obj in data_decoded:
            data_str.append(obj.data.decode('utf-8'))

        return data_str
    else:
        raise ValueError("Error: No QR code detected or unable to decode.")