import logging
import os
from flask import Flask, render_template, request, url_for
from urllib.parse import urlparse
import qrcode
from PIL import Image

# Pastikan folder logs sudah ada
if not os.path.exists("logs"):
    os.makedirs("logs")

# Konfigurasi logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Aplikasi Flask dimulai")

app = Flask(__name__)

def generate_qr_with_logo(url, fill_color="black", back_color="white", logo_path=None):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # Tambahkan logo jika tersedia
    if logo_path:
        logo = Image.open(logo_path)
        logo_size = (qr_img.size[0] // 5, qr_img.size[1] // 5)  # Ukuran logo 1/5 dari QR Code
        logo = logo.resize(logo_size, Image.LANCZOS)
        
        # Posisi tengah
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        
        # Gabungkan QR Code dengan Logo
        qr_img.paste(logo, pos, mask=logo)

    # Simpan hasil
    file_name = f"static/qrcode_with_logo.png"
    qr_img.save(file_name)
    return file_name

@app.route("/", methods=["GET", "POST"])
def home():
    qr_code_url = None

    if request.method == "POST":
        url = request.form["url"]
        fill_color = request.form.get("fill_color", "black")
        back_color = request.form.get("back_color", "white")
        logo = request.files.get("logo")

        # Validasi URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logging.warning(f"Input tidak valid: {url}")
            return "Masukkan URL yang valid!", 400

        try:
            logo_path = None
            if logo:
                logo_path = f"static/{logo.filename}"
                logo.save(logo_path)

            qr_code_url = generate_qr_with_logo(url, fill_color, back_color, logo_path)
            logging.info(f"QR Code dengan logo berhasil dibuat: {qr_code_url}")

        except Exception as e:
            logging.error(f"Terjadi kesalahan saat membuat QR Code: {e}")
            return "Kesalahan internal, coba lagi nanti!", 500

    return render_template("index.html", qr_code_url=qr_code_url)

if __name__ == "__main__":
    logging.info("Aplikasi Flask berjalan")
    app.run(debug=True)