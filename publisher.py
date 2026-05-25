import os

LOGOS_DIR = os.path.join(os.path.dirname(__file__), "logos")

COMPANY_MAP = {
    "openai": ["openai", "chatgpt", "gpt-4", "gpt-5", "o3", "o4", "sora", "dall-e"],
    "anthropic": ["anthropic", "claude"],
    "google": ["google", "gemini", "deepmind", "notebooklm", "veo"],
    "meta": ["meta", "llama"],
    "xai": ["grok", "xai"],
    "mistral": ["mistral"],
}

def get_logo_path(title, description=""):
    text = (title + " " + description).lower()
    for company, keywords in COMPANY_MAP.items():
        if any(kw in text for kw in keywords):
            path = os.path.join(LOGOS_DIR, f"{company}.png")
            if os.path.exists(path):
                return path
    return os.path.join(LOGOS_DIR, "default.png")

def save_instagram_post(text, index):
    filename = f"instagram_post_{index}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved IG post: {filename}")
