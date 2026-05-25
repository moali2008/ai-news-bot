"""يصنع شعارات الشركات كصور جاهزة للنشر"""
from PIL import Image, ImageDraw, ImageFont
import os

LOGOS_DIR = os.path.join(os.path.dirname(__file__), "logos")
os.makedirs(LOGOS_DIR, exist_ok=True)

COMPANIES = {
    "openai":    {"bg": (0, 0, 0),        "text": "OpenAI",    "color": (255, 255, 255)},
    "anthropic": {"bg": (30, 20, 10),     "text": "Anthropic", "color": (204, 120, 60)},
    "google":    {"bg": (255, 255, 255),  "text": "Gemini",    "color": (66, 133, 244)},
    "meta":      {"bg": (255, 255, 255),  "text": "Meta AI",   "color": (24, 119, 242)},
    "xai":       {"bg": (0, 0, 0),        "text": "Grok / xAI","color": (255, 255, 255)},
    "mistral":   {"bg": (15, 10, 5),      "text": "Mistral AI","color": (255, 140, 0)},
    "default":   {"bg": (15, 15, 30),     "text": "AI News",   "color": (150, 150, 255)},
}

FONT_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"

W, H = 1080, 400

def make_logo(name, info):
    img  = Image.new("RGB", (W, H), info["bg"])
    draw = ImageDraw.Draw(img)

    # خط ملون في الأسفل
    draw.rectangle([(0, H-8), (W, H)], fill=info["color"])

    # نص اسم الشركة في المنتصف
    try:
        font = ImageFont.truetype(FONT_PATH, 120)
    except:
        font = ImageFont.load_default()

    text = info["text"]
    bbox = draw.textbbox((0, 0), text, font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]
    draw.text(((W-tw)//2, (H-th)//2 - 20), text, font=font, fill=info["color"])

    path = os.path.join(LOGOS_DIR, f"{name}.png")
    img.save(path)
    print(f"OK: {path}")

for name, info in COMPANIES.items():
    make_logo(name, info)

print("Done! All logos created.")
