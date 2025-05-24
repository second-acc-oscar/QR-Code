import qrcode
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# === Configurable variables ===
qr_data = "https://www.instagram.com/cpcfi.unam/"
qr_color = "#8B0000"  # Color for QR modules
center_circle_color = "#8B0000"  # Color for center circle
fade_opacity_outer = 180  # Opacity of the diffused outer circle
fade_opacity_inner = 255  # Opacity of the solid center circle

logo_path = "CPCFI.png"  # Path to the logo image

border_color = "#FFFFFF"  # Color of the outer border
border_radius_factor = 0.5  # 50% radius (0.5 means very rounded)

box_size = 20  # Size of each QR pixel (bigger = higher resolution)
qr_border = 4  # Standard border for QR (quiet zone)

# === Generate QR matrix ===
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=box_size,
    border=qr_border,
)
qr.add_data(qr_data)
qr.make(fit=True)
qr_matrix = np.array(qr.get_matrix())

# Dimensions
qr_pixel_size = qr_matrix.shape[0]  # Total modules (including quiet zone)
canvas_size = (qr_pixel_size + 2) * box_size  # +2 to leave space for border

# === Create base image ===
img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# === Draw blurred circle for fade ===
center = (canvas_size // 2, canvas_size // 2)
fade_radius_outer = box_size * (qr_pixel_size // 2 + 1)
fade = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
fade_draw = ImageDraw.Draw(fade)
fade_draw.ellipse([
    center[0] - fade_radius_outer,
    center[1] - fade_radius_outer,
    center[0] + fade_radius_outer,
    center[1] + fade_radius_outer
], fill=(int(qr_color[1:3], 16), int(qr_color[3:5], 16), int(qr_color[5:], 16), fade_opacity_outer))
blurred_fade = fade.filter(ImageFilter.GaussianBlur(radius=box_size * 2))
img.alpha_composite(blurred_fade)

# === Draw QR code manually ===
for r in range(qr_pixel_size):
    for c in range(qr_pixel_size):
        if qr_matrix[r, c]:
            x0 = (c + 1) * box_size
            y0 = (r + 1) * box_size
            x1 = x0 + box_size
            y1 = y0 + box_size

            # Detect Finder Pattern zones (top-left, top-right, bottom-left)
            in_finder = (
                (r <= 6 and c <= 6) or
                (r <= 6 and c >= qr_pixel_size - 7) or
                (r >= qr_pixel_size - 7 and c <= 6)
            )
            
            if in_finder:
                draw.rounded_rectangle([x0, y0, x1, y1], radius=box_size//2, fill=qr_color)
            else:
                draw.rectangle([x0, y0, x1, y1], fill=qr_color)

# === Draw outer rounded border ===
border_thickness = box_size
outer_radius = (canvas_size - 2 * border_thickness)
border_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
border_draw = ImageDraw.Draw(border_img)
border_draw.rounded_rectangle(
    [border_thickness//2, border_thickness//2, canvas_size-border_thickness//2, canvas_size-border_thickness//2],
    radius=int((outer_radius/2) * border_radius_factor),
    outline=border_color,
    width=border_thickness
)
img.alpha_composite(border_img)

# === Draw solid center circle ===
center_circle_radius = box_size * 7
center_circle = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
center_draw = ImageDraw.Draw(center_circle)
center_draw.ellipse([
    center[0] - center_circle_radius,
    center[1] - center_circle_radius,
    center[0] + center_circle_radius,
    center[1] + center_circle_radius
], fill=(int(center_circle_color[1:3], 16), int(center_circle_color[3:5], 16), int(center_circle_color[5:], 16), fade_opacity_inner))
img.alpha_composite(center_circle)

# === Insert logo ===
logo = Image.open(logo_path).convert("RGBA")
logo_size = int(center_circle_radius * 1.5)
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (center[0] - logo_size//2, center[1] - logo_size//2), logo)

# === Save final image ===
img.save("custom_qr_code.png")
