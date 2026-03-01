from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import math
from datetime import datetime

# YouTube thumbnail dimensions
WIDTH = 1280
HEIGHT = 720


def get_font(size, bold=False):
    font_paths_bold = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    font_paths_regular = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    paths = font_paths_bold if bold else font_paths_regular
    for fp in paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_glow_text(img, pos, text, font, fill, glow_color, glow_radius=8):
    """Draw text with a soft glow effect behind it."""
    x, y = pos
    # Create a temporary image for the glow
    glow_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    # Draw glow text multiple times with offsets
    for dx in range(-glow_radius, glow_radius + 1, 2):
        for dy in range(-glow_radius, glow_radius + 1, 2):
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= glow_radius:
                alpha = int((1 - dist / glow_radius) * 60)
                glow_draw.text((x + dx, y + dy), text, font=font,
                               fill=(*glow_color, alpha))
    # Composite glow
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, glow_img)
    # Draw main text on top
    temp_draw = ImageDraw.Draw(img_rgba)
    # Shadow
    temp_draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0, 180))
    # Main text
    temp_draw.text((x, y), text, font=font, fill=fill)
    return img_rgba.convert('RGB')


if __name__ == '__main__':
    # Load the background image (dot-pattern face - futuristic AI vibe)
    bg_path = os.path.join(os.path.dirname(__file__), "images", "pexels-aleksandar-pasaric-3355925.jpg")
    bg = Image.open(bg_path).convert("RGB")

    # Resize the face image to fit the right portion, slightly larger for impact
    face_h = int(HEIGHT * 1.1)
    face_ratio = face_h / bg.height
    face_w = int(bg.width * face_ratio)
    bg = bg.resize((face_w, face_h), Image.LANCZOS)

    # Create a dark base canvas with deep blue-black tone
    img = Image.new('RGB', (WIDTH, HEIGHT), (8, 10, 18))

    # Place the face on the right side, slightly up for a dramatic crop
    face_x = WIDTH - face_w + 60
    face_y = -30
    img.paste(bg, (face_x, face_y))

    # Boost contrast on the face for more punch
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.95)

    # Add a cyan/electric blue tint to the dots for a tech feel
    img = img.convert('RGBA')
    blue_tint = Image.new('RGBA', (WIDTH, HEIGHT), (40, 180, 255, 25))
    img = Image.alpha_composite(img, blue_tint)

    # Strong left-to-right gradient for clean text area
    left_fade = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    left_draw = ImageDraw.Draw(left_fade)
    fade_end = int(WIDTH * 0.55)
    for x in range(fade_end):
        alpha = int((1 - x / fade_end) ** 0.5 * 245)
        left_draw.line([(x, 0), (x, HEIGHT)], fill=(8, 10, 18, alpha))
    img = Image.alpha_composite(img, left_fade)

    # Bottom vignette
    bottom_fade = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    bottom_draw = ImageDraw.Draw(bottom_fade)
    for y in range(int(HEIGHT * 0.6), HEIGHT):
        progress = (y - HEIGHT * 0.6) / (HEIGHT * 0.4)
        alpha = int(progress ** 2 * 140)
        bottom_draw.line([(0, y), (WIDTH, y)], fill=(8, 10, 18, alpha))
    img = Image.alpha_composite(img, bottom_fade)

    # Top vignette (subtle)
    top_fade = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    top_draw = ImageDraw.Draw(top_fade)
    for y in range(int(HEIGHT * 0.25)):
        progress = 1 - y / (HEIGHT * 0.25)
        alpha = int(progress ** 2 * 80)
        top_draw.line([(0, y), (WIDTH, y)], fill=(8, 10, 18, alpha))
    img = Image.alpha_composite(img, top_fade)

    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ---- ACCENT ELEMENTS ----

    # Draw a vertical accent bar on the left edge
    draw.rectangle([0, 0, 6, HEIGHT], fill=(40, 180, 255))

    # Draw a thin horizontal accent line
    line_y = 155
    draw.line([(50, line_y), (320, line_y)], fill=(40, 180, 255), width=3)

    # ---- TEXT LAYOUT ----
    text_x = 50
    cyan = (40, 180, 255)       # electric blue accent
    amber = (255, 190, 80)      # warm amber
    white = (255, 255, 255)
    light_gray = (200, 205, 215)

    # Top label
    font_label = get_font(22, bold=True)
    draw.text((text_x + 2, 125), "THE COMPLETE GUIDE", font=font_label, fill=cyan)

    # Main title - "CLAUDE" with glow
    font_huge = get_font(130, bold=True)
    img = draw_glow_text(img, (text_x - 5, 170), "CLAUDE", font_huge, white, (40, 180, 255), glow_radius=10)
    draw = ImageDraw.Draw(img)

    # Main title - "CODE" with amber glow
    img = draw_glow_text(img, (text_x - 5, 300), "CODE", font_huge, amber, (255, 160, 40), glow_radius=10)
    draw = ImageDraw.Draw(img)

    # Subtitle with slight spacing feel
    font_sub = get_font(34, bold=False)
    draw.text((text_x + 3, 455), "Explained for", font=font_sub, fill=light_gray)
    font_sub_bold = get_font(34, bold=True)
    # Measure "Explained for " width to place "Everyone" in accent
    ef_bbox = draw.textbbox((0, 0), "Explained for ", font=font_sub)
    ef_w = ef_bbox[2] - ef_bbox[0]
    draw.text((text_x + 3 + ef_w, 455), "Everyone", font=font_sub_bold, fill=white)

    # Pill badge
    font_tag = get_font(20, bold=True)
    tagline = "NO CODING EXPERIENCE NEEDED"
    bbox = draw.textbbox((0, 0), tagline, font=font_tag)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    pill_x = text_x
    pill_y = 520
    px, py = 22, 12
    # Pill shadow
    draw.rounded_rectangle(
        [pill_x + 2, pill_y + 2, pill_x + tw + px * 2 + 2, pill_y + th + py * 2 + 2],
        radius=25, fill=(0, 0, 0, 80)
    )
    # Pill with gradient feel (solid cyan)
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + tw + px * 2, pill_y + th + py * 2],
        radius=25, fill=cyan
    )
    draw.text((pill_x + px, pill_y + py), tagline, font=font_tag, fill=(8, 10, 18))

    # Save
    base_dir = os.path.join(os.path.dirname(__file__), "generated-images")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "thumbnail.png")
    img.save(output_path, "PNG")
    print(f"Thumbnail saved to: {output_path}")
