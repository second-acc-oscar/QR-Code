
import qrcode
from PIL import Image

def generate_qr():
    url = "https://github.com/CPCFI-org"
    output_path = "generated-logos/10g_github_cpcfi.png"
    qr_size = 2000

    # Color del QR (blanco)
    qr_color_hex = "#FFFFFE"

    # 1. Generate QR
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 2. Make QR image
    qr_img = qr.make_image(fill_color=qr_color_hex, back_color="white").convert('RGBA')
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    # 3. Make white background transparent
    datas = qr_img.getdata()
    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))  # transparent
        else:
            new_data.append(item)
    qr_img.putdata(new_data)

    # 4. Save
    qr_img.save(output_path)
    print(f"QR code saved as '{output_path}'.")

if __name__ == "__main__":
    generate_qr()
