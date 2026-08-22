import qrcode
from PIL import Image

def generate_qr():
    url = "https://puzzel.org/es/crossword/play?p=-OsRCuYidpYJzk8VPpTC"
    output_path = "generated-logos/crossword-bd.png"
    qr_size = 2000

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    qr_img.save(output_path)
    print(f"QR code saved as '{output_path}'.")

if __name__ == "__main__":
    generate_qr()
