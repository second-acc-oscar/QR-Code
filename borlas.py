import qrcode
from PIL import Image, ImageDraw, ImageFilter

# =================== CONFIGURACIÓN ===================

# URL que se quiere codificar
url = "https://www.instagram.com/cpcfi.unam/"

# Parámetros de tamaño
qr_size = 1000           # Tamaño en píxeles del QR
logo_size_ratio = 0.2    # Proporción del tamaño del logo respecto al QR

# Colores
qr_color_hex = "#8B0000"       # Color del QR (rojo oscuro)
glow_color_hex = "#8B0000"     # Color del aro difuminado
circle_color_hex = "#8B0000"   # Color del círculo de fondo del logo

# Opacidades
glow_opacity = 100             # Opacidad del difuminado (0-255)
circle_opacity = 255           # Opacidad del círculo de fondo (0-255)

# Imagen del logo (debe estar en el mismo directorio o dar ruta completa)
logo_path = "CPCFI.png"

# =================== CREACIÓN DEL QR ===================

# 1. Generar QR básico
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr.add_data(url)
qr.make(fit=True)

matrix = qr.get_matrix()
matrix_size = len(matrix)

# 2. Crear imagen base transparente
qr_img = Image.new('RGBA', (qr_size, qr_size), (255, 255, 255, 0))
draw = ImageDraw.Draw(qr_img)

# 3. Dibujar los módulos redondeados
module_size = qr_size // matrix_size
padding = (qr_size - (module_size * matrix_size)) // 2  # Centrado

for y in range(matrix_size):
    for x in range(matrix_size):
        if matrix[y][x]:  # Si es un módulo "activo"
            top_left = (padding + x * module_size, padding + y * module_size)
            bottom_right = (padding + (x + 1) * module_size, padding + (y + 1) * module_size)

            # Dibujar rectángulo redondeado
            draw.rounded_rectangle(
                [top_left, bottom_right],
                radius=module_size * 0.3,  # 30% de redondeo, puedes ajustar
                fill=qr_color_hex
            )

# =================== ARO DIFUMINADO ===================

# Crear imagen para el glow
glow_img = Image.new('RGBA', qr_img.size, (255, 255, 255, 0))
glow_draw = ImageDraw.Draw(glow_img)

# Dibujar el mismo QR en otro canvas para el efecto
for y in range(matrix_size):
    for x in range(matrix_size):
        if matrix[y][x]:
            top_left = (padding + x * module_size, padding + y * module_size)
            bottom_right = (padding + (x + 1) * module_size, padding + (y + 1) * module_size)
            glow_draw.rounded_rectangle(
                [top_left, bottom_right],
                radius=module_size * 0.3,
                fill=glow_color_hex + f"{glow_opacity:02x}"
            )

# Aplicar desenfoque
blurred_glow = glow_img.filter(ImageFilter.GaussianBlur(10))

# Combinar el glow difuminado y el QR principal
final_img = Image.alpha_composite(blurred_glow, qr_img)

# =================== LOGO CON CÍRCULO ===================

# Abrir logo
logo = Image.open(logo_path).convert("RGBA")

# Redimensionar logo
logo_size = int(qr_size * logo_size_ratio)
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Crear círculo de fondo
circle_size = logo_size * 6 // 5  # Un poco más grande que el logo
circle = Image.new('RGBA', (circle_size, circle_size), (255, 255, 255, 0))
circle_draw = ImageDraw.Draw(circle)

# Dibujar el círculo de fondo
circle_draw.ellipse(
    (0, 0, circle_size, circle_size),
    fill=circle_color_hex + f"{circle_opacity:02x}"
)

# Combinar el logo encima del círculo
circle.paste(logo, ((circle_size - logo_size) // 2, (circle_size - logo_size) // 2), logo)

# Posicionar el círculo con logo en el centro del QR
final_img.paste(circle, (
    (qr_size - circle_size) // 2,
    (qr_size - circle_size) // 2
), circle)

# =================== GUARDAR RESULTADO ===================

final_img.save('generated-logo/custom_qr.png')
print("QR personalizado generado exitosamente como 'custom_qr.png'.")
