import qrcode
from PIL import Image, ImageDraw, ImageChops

def generate_qr_with_logo():
    """
    Generate a QR code with transparent background, solid-colored code,
    and a solid background circle under the logo, without any glow effect.
    """

    # === CONFIGURABLE PARAMETERS ===
    url = "https://drive.google.com/file/d/1Itn_7qkVnencTfClkkSJJa_zo8A-htO0/view?usp=sharing"
    logo_path = "ic.png"
    output_path = "generated-logos/temario_react.png"
    qr_size = 2000
    logo_scale = 0.2  # relative to QR size

    # Colors
    qr_color_hex = "#00a9b400"      # Color for the QR code
    circle_color_hex = "#000193ff"  # Color for the background circle behind the logo

    # Opacities
    circle_opacity = 255  # Opacity of the background circle (0-255)

    # Step 1: Generate the QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Step 2: Create QR image
    qr_img = qr.make_image(fill_color=qr_color_hex, back_color="white").convert('RGBA')
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    """
    # Step 3: Make white background fully transparent
    datas = qr_img.getdata()
    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)https://canva.link/l6vdxpqvgdno28u
    qr_img.putdata(new_data)
    """

    # Step 4: Load and resize the logo
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = int(qr_size * logo_scale)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    """
    # Step 5: Create solid colored circle behind logo
    circle_color_rgb = tuple(int(circle_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    logo_solid_bg = Image.new('RGBA', logo.size, (0, 0, 0, 0))
    draw_solid = ImageDraw.Draw(logo_solid_bg)
    draw_solid.ellipse(
        (0, 0, logo.size[0], logo.size[1]),
        fill=circle_color_rgb + (circle_opacity,)
    )

    # Step 6: Create circular cropped logo
    logo_mask = Image.new('L', logo.size, 0)
    draw_logo = ImageDraw.Draw(logo_mask)
    draw_logo.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)

    # Step 7: Combine solid color background and logo
    logo_with_bg = Image.alpha_composite(logo_solid_bg, logo)
    """

    # Step 8: Paste the logo
    pos_logo = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)

    # --- NEW LINES: Erase the bits behind the logo ---
    # Define the box area where the logo will go (left, top, right, bottom)
    clear_box = (pos_logo[0], pos_logo[1], pos_logo[0] + logo_size, pos_logo[1] + logo_size)
    
    # Overwrite that exact area with fully transparent pixels (0 opacity)
    qr_img.paste((255, 255, 255, 0), clear_box)
    # -------------------------------------------------

    qr_img.paste(logo, pos_logo, mask=logo)    # Step 9: Save output
    qr_img.save(output_path)
    print(f"Circular QR code with logo saved as '{output_path}'")

if __name__ == "__main__":
    generate_qr_with_logo()
