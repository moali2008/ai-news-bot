from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display
import textwrap
import os
import re

# ألوان الشركات
COMPANY_COLORS = {
    "openai":    {"bg": (0, 0, 0),       "accent": (16, 163, 127), "name": "OpenAI"},
    "chatgpt":   {"bg": (0, 0, 0),       "accent": (16, 163, 127), "name": "ChatGPT"},
    "anthropic": {"bg": (10, 10, 20),    "accent": (204, 120, 60), "name": "Anthropic"},
    "claude":    {"bg": (10, 10, 20),    "accent": (204, 120, 60), "name": "Claude"},
    "google":    {"bg": (5, 15, 35),     "accent": (66, 133, 244), "name": "Google AI"},
    "gemini":    {"bg": (5, 15, 35),     "accent": (66, 133, 244), "name": "Gemini"},
    "deepmind":  {"bg": (5, 15, 35),     "accent": (66, 133, 244), "name": "DeepMind"},
    "grok":      {"bg": (10, 5, 20),     "accent": (120, 80, 200), "name": "xAI"},
    "meta":      {"bg": (5, 10, 30),     "accent": (24, 119, 242), "name": "Meta AI"},
    "llama":     {"bg": (5, 10, 30),     "accent": (24, 119, 242), "name": "Meta AI"},
    "mistral":   {"bg": (15, 10, 5),     "accent": (255, 140, 0),  "name": "Mistral"},
    "default":   {"bg": (10, 10, 25),    "accent": (100, 100, 220), "name": "AI"},
}

def get_font_path():
    candidates = [
        "C:\\Windows\\Fonts\\arial.ttf",       # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

FONT_PATH = get_font_path()

def detect_company(title, description=""):
    text = (title + " " + description).lower()
    for key in COMPANY_COLORS:
        if key != "default" and key in text:
            return COMPANY_COLORS[key]
    return COMPANY_COLORS["default"]

def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def wrap_arabic(text, max_chars=22):
    words = text.split()
    lines, line = [], []
    count = 0
    for word in words:
        count += len(word) + 1
        if count > max_chars:
            lines.append(" ".join(line))
            line = [word]
            count = len(word)
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return lines

def make_gradient(size, color_top, color_bottom):
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    w, h = size
    for y in range(h):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / h)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / h)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def create_news_card(title_ar, body_ar, company_info, filename="card.png"):
    W, H = 1080, 1080
    bg_color = company_info["bg"]
    accent   = company_info["accent"]
    company  = company_info["name"]

    # خلفية متدرجة
    bg_dark = tuple(max(0, c - 15) for c in bg_color)
    img = make_gradient((W, H), bg_color, bg_dark)
    draw = ImageDraw.Draw(img)

    # شريط علوي ملون
    draw.rectangle([(0, 0), (W, 12)], fill=accent)

    # نقاط زخرفية
    for x in range(0, W, 60):
        for y in range(40, H - 80, 60):
            draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=(*accent, 15))

    # اسم الشركة
    try:
        font_company = ImageFont.truetype(FONT_PATH, 36)
        font_title   = ImageFont.truetype(FONT_PATH, 62)
        font_body    = ImageFont.truetype(FONT_PATH, 38)
        font_channel = ImageFont.truetype(FONT_PATH, 32)
        font_tag     = ImageFont.truetype(FONT_PATH, 28)
    except:
        font_company = font_title = font_body = font_channel = font_tag = ImageFont.load_default()

    # شريط اسم الشركة
    draw.rectangle([(60, 60), (60 + len(company) * 22 + 30, 110)], fill=accent)
    draw.text((75, 65), company, font=font_company, fill=(255, 255, 255))

    # عنوان الخبر (عربي)
    title_lines = wrap_arabic(title_ar, max_chars=18)
    y_title = 160
    for line in title_lines[:3]:
        shaped = reshape_arabic(line)
        bbox = draw.textbbox((0, 0), shaped, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y_title), shaped, font=font_title, fill=(255, 255, 255))
        y_title += 80

    # خط فاصل
    draw.rectangle([(80, y_title + 20), (W - 80, y_title + 24)], fill=accent)

    # نص التفاصيل
    body_lines = wrap_arabic(body_ar, max_chars=28)
    y_body = y_title + 60
    for line in body_lines[:7]:
        shaped = reshape_arabic(line)
        bbox = draw.textbbox((0, 0), shaped, font=font_body)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y_body), shaped, font=font_body, fill=(200, 200, 200))
        y_body += 56

    # شريط سفلي
    draw.rectangle([(0, H - 80), (W, H)], fill=tuple(min(255, c + 20) for c in bg_color))
    draw.rectangle([(0, H - 80), (W, H - 78)], fill=accent)

    channel_text = "@ainews_arabic"
    bbox = draw.textbbox((0, 0), channel_text, font=font_channel)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 55), channel_text, font=font_channel, fill=accent)

    output_path = os.path.join(os.path.dirname(__file__), filename)
    img.save(output_path, quality=95)
    return output_path
