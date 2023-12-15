from PIL import Image
from io import BytesIO
from qr_utils import *

qr_bytes = generate_qr_code_bytes()

for str in decode_qr_bytes(qr_bytes):
    print(str)

"""
@app.route('/')
def index():
    image_bytes = b''  # Replace with coded data
    
    qr_img = Image.open(BytesIO(image_bytes))

    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template('index.html', img_str=img_str)
"""