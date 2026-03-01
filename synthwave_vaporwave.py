from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import math
import random
from datetime import datetime

# YouTube thumbnail dimensions
WIDTH = 1280
HEIGHT = 720

# ---- VAPORWAVE COLOR PALETTE ----
PASTEL_PINK = (255, 130, 200)
SOFT_TEAL = (100, 220, 210)
LAVENDER = (200, 130, 255)
SOFT_MAGENTA = (220, 80, 200)
PEACH = (255, 184, 153)
DEEP_NAVY = (8, 5, 22)
DARK_BG = (8, 5, 22)

# ---- CONFIGURABLE TEXT ----
BAND_NAME = "KLEINER'82"
TRACK_TITLE = "NEON SHADOWS"
SUBTITLE = "VAPORWAVE"


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


def draw_neon_text(img, pos, text, font, color, glow_radius=12, glow_intensity=80):
    x, y = pos
    glow = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Outer glow layers
    for dx in range(-glow_radius, glow_radius + 1, 2):
        for dy in range(-glow_radius, glow_radius + 1, 2):
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= glow_radius:
                alpha = int((1 - dist / glow_radius) ** 1.5 * glow_intensity)
                glow_draw.text((x + dx, y + dy), text, font=font,
                               fill=(*color, alpha))

    # Composite glow
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, glow)

    # Bright white core text with slight color tint
    core_draw = ImageDraw.Draw(img_rgba)
    bright = tuple(min(255, c + 180) for c in color)
    core_draw.text((x, y), text, font=font, fill=bright)
    # Pure white highlight pass
    core_draw.text((x, y), text, font=font, fill=(255, 255, 255, 220))

    return img_rgba.convert('RGB')


def chromatic_aberration(img, offset=3):
    r, g, b = img.split()
    from PIL import ImageChops
    r = ImageChops.offset(r, -offset, 0)
    b = ImageChops.offset(b, offset, 0)
    return Image.merge('RGB', (r, g, b))


if __name__ == '__main__':
    # ---- BACKGROUND: VAPORWAVE SKY GRADIENT ----
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Sky gradient: deep navy -> purple -> soft pink
    horizon_y = int(HEIGHT * 0.48)
    for y in range(horizon_y):
        progress = y / horizon_y
        if progress < 0.4:
            # Deep navy to purple
            t = progress / 0.4
            r = int(8 + t * 80)
            g = int(5 + t * 10)
            b = int(22 + t * 80)
        elif progress < 0.7:
            # Purple to soft magenta
            t = (progress - 0.4) / 0.3
            r = int(88 + t * 150)
            g = int(15 + t * 30)
            b = int(102 - t * 20)
        else:
            # Soft magenta to pastel pink at horizon
            t = (progress - 0.7) / 0.3
            r = int(238 + t * 17)
            g = int(45 + t * 100)
            b = int(82 + t * 60)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # ---- RETRO SUN ----
    sun_cx = WIDTH // 2
    sun_cy = horizon_y - 10
    sun_radius = 120

    # Sun glow (outer bloom — lavender/pink)
    sun_glow = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    sg_draw = ImageDraw.Draw(sun_glow)
    for r_offset in range(80, 0, -1):
        alpha = int((1 - r_offset / 80) * 40)
        expand = sun_radius + r_offset
        sg_draw.ellipse(
            [sun_cx - expand, sun_cy - expand, sun_cx + expand, sun_cy + expand],
            fill=(200, 130, 255, alpha)
        )
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, sun_glow)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Sun body: peach top -> lavender bottom
    for dy in range(-sun_radius, sun_radius + 1):
        t = (dy + sun_radius) / (2 * sun_radius)
        sr = int(255 - t * 55)
        sg = int(184 - t * 54)
        sb = int(153 + t * 102)
        chord_half = math.sqrt(max(0, sun_radius ** 2 - dy ** 2))
        y_pos = sun_cy + dy
        if 0 <= y_pos < HEIGHT:
            draw.line(
                [(sun_cx - chord_half, y_pos), (sun_cx + chord_half, y_pos)],
                fill=(sr, sg, sb)
            )

    # Sun horizontal stripe cutouts (retro VHS line effect)
    stripe_gap = 8
    stripe_width = 4
    for i in range(6):
        sy = sun_cy + 15 + i * (stripe_gap + stripe_width + i * 2)
        if sy < sun_cy + sun_radius:
            chord_half = math.sqrt(max(0, sun_radius ** 2 - (sy - sun_cy) ** 2))
            for sw in range(stripe_width + i):
                if 0 <= sy + sw < HEIGHT:
                    draw.line(
                        [(sun_cx - chord_half, sy + sw), (sun_cx + chord_half, sy + sw)],
                        fill=(0, 0, 0)
                    )

    # ---- MOUNTAIN SILHOUETTES ----
    mtn_points_back = [(0, horizon_y)]
    peaks_back = [
        (0, horizon_y - 80), (80, horizon_y - 130), (180, horizon_y - 95),
        (280, horizon_y - 170), (380, horizon_y - 120), (460, horizon_y - 190),
        (560, horizon_y - 140), (640, horizon_y - 200), (720, horizon_y - 155),
        (820, horizon_y - 180), (920, horizon_y - 130), (1000, horizon_y - 160),
        (1080, horizon_y - 110), (1160, horizon_y - 145), (1280, horizon_y - 90),
    ]
    mtn_points_back.extend(peaks_back)
    mtn_points_back.append((WIDTH, horizon_y))
    draw.polygon(mtn_points_back, fill=(20, 8, 40))

    mtn_points_front = [(0, horizon_y)]
    peaks_front = [
        (0, horizon_y - 40), (100, horizon_y - 90), (200, horizon_y - 55),
        (320, horizon_y - 110), (420, horizon_y - 70), (520, horizon_y - 95),
        (620, horizon_y - 60), (700, horizon_y - 100), (800, horizon_y - 75),
        (900, horizon_y - 105), (1000, horizon_y - 65), (1100, horizon_y - 85),
        (1200, horizon_y - 50), (1280, horizon_y - 70),
    ]
    mtn_points_front.extend(peaks_front)
    mtn_points_front.append((WIDTH, horizon_y))
    draw.polygon(mtn_points_front, fill=(28, 12, 55))

    # Mountain edge glow (soft pink highlight)
    mtn_glow = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    mg_draw = ImageDraw.Draw(mtn_glow)
    for i in range(len(peaks_front) - 1):
        x1, y1 = peaks_front[i]
        x2, y2 = peaks_front[i + 1]
        mg_draw.line([(x1, y1), (x2, y2)], fill=(*PASTEL_PINK, 40), width=2)
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, mtn_glow)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ---- PERSPECTIVE GRID (below horizon) ----
    grid_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)

    vanishing_x = WIDTH // 2
    vanishing_y = horizon_y

    # Horizontal grid lines
    num_h_lines = 20
    for i in range(1, num_h_lines + 1):
        t = i / num_h_lines
        y = vanishing_y + int((HEIGHT - vanishing_y) * (t ** 1.8))
        alpha = int(40 + t * 160)
        width = 1 if t < 0.4 else 2
        grid_draw.line([(0, y), (WIDTH, y)], fill=(*LAVENDER, alpha), width=width)

    # Vertical grid lines converging to vanishing point
    num_v_lines = 24
    spread = WIDTH * 1.8
    for i in range(num_v_lines + 1):
        bottom_x = int(-spread / 2 + i * (spread / num_v_lines)) + WIDTH // 2
        alpha = 120
        edge_dist = abs(bottom_x - WIDTH // 2) / (WIDTH // 2)
        if edge_dist > 0.6:
            alpha = int(120 * (1 - (edge_dist - 0.6) / 0.4))
        alpha = max(0, min(255, alpha))
        grid_draw.line(
            [(vanishing_x, vanishing_y), (bottom_x, HEIGHT)],
            fill=(*LAVENDER, alpha), width=1
        )

    # ---- GROUND COLOR (dark navy under grid) ----
    ground = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(ground)
    for y in range(horizon_y, HEIGHT):
        progress = (y - horizon_y) / (HEIGHT - horizon_y)
        alpha = int(progress * 180)
        g_draw.line([(0, y), (WIDTH, y)], fill=(8, 5, 22, alpha))

    # Composite: base → ground → grid
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, ground)
    img = Image.alpha_composite(img, grid_img)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ---- MAIN TEXT: BAND NAME ----
    font_band = get_font(110, bold=True)
    bbox = draw.textbbox((0, 0), BAND_NAME, font=font_band)
    band_w = bbox[2] - bbox[0]
    band_x = (WIDTH - band_w) // 2
    band_y = 160

    img = draw_neon_text(img, (band_x, band_y), BAND_NAME, font_band,
                         PASTEL_PINK, glow_radius=16, glow_intensity=90)
    draw = ImageDraw.Draw(img)

    # ---- TRACK TITLE ----
    font_track = get_font(72, bold=True)
    bbox_t = draw.textbbox((0, 0), TRACK_TITLE, font=font_track)
    track_w = bbox_t[2] - bbox_t[0]
    track_x = (WIDTH - track_w) // 2
    track_y = 310

    img = draw_neon_text(img, (track_x, track_y), TRACK_TITLE, font_track,
                         SOFT_TEAL, glow_radius=12, glow_intensity=70)
    draw = ImageDraw.Draw(img)

    # ---- SUBTITLE LABEL ----
    font_sub = get_font(24, bold=True)
    bbox_s = draw.textbbox((0, 0), SUBTITLE, font=font_sub)
    sub_w = bbox_s[2] - bbox_s[0]
    sub_x = (WIDTH - sub_w) // 2
    sub_y = 130

    line_pad = 20
    line_len = 80

    sub_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    sub_draw = ImageDraw.Draw(sub_img)
    sub_draw.text((sub_x, sub_y), SUBTITLE, font=font_sub, fill=(*PEACH, 230))
    # Left line
    sub_draw.line(
        [(sub_x - line_pad - line_len, sub_y + 12), (sub_x - line_pad, sub_y + 12)],
        fill=(*SOFT_MAGENTA, 150), width=2
    )
    # Right line
    sub_draw.line(
        [(sub_x + sub_w + line_pad, sub_y + 12), (sub_x + sub_w + line_pad + line_len, sub_y + 12)],
        fill=(*SOFT_MAGENTA, 150), width=2
    )
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, sub_img)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ---- SCANLINE OVERLAY ----
    scan = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan)
    for y in range(0, HEIGHT, 3):
        scan_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, 30))
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, scan)
    img = img.convert('RGB')

    # ---- VHS NOISE / GRAIN ----
    random.seed(42)
    noise = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    noise_draw = ImageDraw.Draw(noise)
    for _ in range(3000):
        nx = random.randint(0, WIDTH - 1)
        ny = random.randint(0, HEIGHT - 1)
        na = random.randint(8, 30)
        noise_draw.point((nx, ny), fill=(255, 255, 255, na))
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, noise)
    img = img.convert('RGB')

    # ---- CHROMATIC ABERRATION (subtle) ----
    img = chromatic_aberration(img, offset=2)

    # ---- EDGE VIGNETTE ----
    vignette = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for y in range(100):
        alpha = int((1 - y / 100) ** 2 * 120)
        v_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    for y in range(HEIGHT - 80, HEIGHT):
        alpha = int(((y - (HEIGHT - 80)) / 80) ** 2 * 150)
        v_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    for x in range(120):
        alpha = int((1 - x / 120) ** 2 * 100)
        v_draw.line([(x, 0), (x, HEIGHT)], fill=(0, 0, 0, alpha))
    for x in range(WIDTH - 120, WIDTH):
        alpha = int(((x - (WIDTH - 120)) / 120) ** 2 * 100)
        v_draw.line([(x, 0), (x, HEIGHT)], fill=(0, 0, 0, alpha))

    img = img.convert('RGBA')
    img = Image.alpha_composite(img, vignette)
    img = img.convert('RGB')

    # ---- SAVE ----
    base_dir = os.path.join(os.path.dirname(__file__), "generated-images")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "vaporwave_thumbnail.png")
    img.save(output_path, "PNG")
    print(f"Vaporwave thumbnail saved to: {output_path}")
