# pip install qrcode[pil] pillow

import os
import qrcode
from PIL import Image, ImageDraw, ImageOps

tasks = [
    {
        "website_url": "https://scholar.google.com/citations?user=llTqHTUAAAAJ&hl=en",
        "logo_path": "resource/scholar.png",
        "output_path": "qr/scholar.png",
    },
    {
        "website_url": "https://pypi.org/user/rui1002",
        "logo_path": "resource/pypi.png",
        "output_path": "qr/pypi.png",
    },
    {
        "website_url": "https://github.com/rui-luo1002",
        "logo_path": "resource/github.png",
        "output_path": "qr/github.png",
    },
]

for item in tasks:
    website_url = item["website_url"]
    logo_path = item["logo_path"]
    output_path = item["output_path"]

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create QR code (high error correction for center logo)
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=32,
        border=2
    )
    qr.add_data(website_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_w, qr_h = qr_img.size

    # Logo background (white rounded rectangle)
    bg_size = qr_w // 4
    radius = bg_size // 5
    padding = bg_size // 8

    badge = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    draw.rounded_rectangle(
        [(0, 0), (bg_size - 1, bg_size - 1)],
        radius=radius,
        fill=(255, 255, 255, 255)
    )

    # ----- Resize logo to fit the rectangle's inner area -----
    logo = Image.open(logo_path).convert("RGBA")
    inner_w = bg_size - 2 * padding
    inner_h = bg_size - 2 * padding

    # Keeps aspect ratio; fits entirely inside (inner_w, inner_h)
    logo_fit = ImageOps.contain(logo, (inner_w, inner_h), Image.LANCZOS)

    # Center the resized logo in the inner area
    lx = padding + (inner_w - logo_fit.width) // 2
    ly = padding + (inner_h - logo_fit.height) // 2
    badge.paste(logo_fit, (lx, ly), logo_fit)
    # ---------------------------------------------------------

    # Paste badge at QR center
    x = (qr_w - bg_size) // 2
    y = (qr_h - bg_size) // 2
    qr_img.paste(badge, (x, y), badge)

    # Save
    qr_img.convert("RGB").save(output_path)
    print(f"Saved: {output_path}")
