import qrcode
import os
import time
from flask import url_for  # Tambahkan impor url_for

def generate_qr(url, fill_color="blue", back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Pastikan folder static/ ada
    if not os.path.exists("static"):
        os.makedirs("static")

    qr_filename = f"qr_{int(time.time())}.png"  # Nama file unik berdasarkan waktu
    qr_path = os.path.join("static", qr_filename)
    img.save(qr_path)

    return url_for('static', filename=qr_filename)