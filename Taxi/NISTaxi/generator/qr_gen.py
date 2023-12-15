import qrcode
from io import BytesIO

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "http://127.0.0.1:8000/"

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("example_qrcode.png")

buffer = BytesIO()
img.save(buffer, format="PNG")
qr_bytes = buffer.getvalue()

"""
conn = sqlite3.connect('your_database.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS QRImages (ImageData BLOB)")

cursor.execute("INSERT INTO QRImages (ImageData) VALUES (?)", (sqlite3.Binary(image_bytes),))

conn.commit()
conn.close()
"""