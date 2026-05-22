from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

CARD_PROMPT = """أنت كاتب محتوى عربي متخصص في أخبار ChatGPT وClaude وGemini.

الخبر:
العنوان: {title}
التفاصيل: {description}

أعطني مخرجين فقط بهذا الشكل بالضبط:

العنوان: [عنوان عربي جذاب ومختصر، 8 كلمات كحد أقصى]
التفاصيل: [شرح بسيط وممتع في 3-4 جمل قصيرة، بأسلوب شبابي]"""

TELEGRAM_PROMPT = """أنت كاتب محتوى متخصص في أخبار ChatGPT وClaude وGemini لجمهور عربي خليجي.

الخبر:
العنوان: {title}
التفاصيل: {description}
المصدر: {source}

اكتب كابشن مرافق للصورة على تيليكرام بالعربي:
- سطر أول: عنوان جذاب مع إيموجي
- 3 نقاط رئيسية مع إيموجي
- جملة تحفز على التفاعل

الطول: 80-120 كلمة"""

INSTAGRAM_PROMPT = """أنت كاتب محتوى محترف للانستا يفهم الخوارزميات.

الخبر:
العنوان: {title}
التفاصيل: {description}

اكتب كابشن انستا بالعربي:
- السطر الأول: جملة صادمة أو سؤال يوقف التمرير تماماً
- 3 نقاط مختصرة وممتعة مع إيموجي
- CTA قوي في النهاية (شارك، احفظ، علّق)
- 10 هاشتاقات مناسبة (عربي وإنجليزي)

الطول: 100-180 كلمة + الهاشتاقات"""

def write_card_content(article):
    """يكتب عنوان وتفاصيل للكارد الإخباري"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": CARD_PROMPT.format(
            title=article["title"],
            description=article.get("description", "")
        )}],
        max_tokens=300
    )
    text = response.choices[0].message.content
    title, body = "", ""
    for line in text.splitlines():
        if line.startswith("العنوان:"):
            title = line.replace("العنوان:", "").strip()
        elif line.startswith("التفاصيل:"):
            body = line.replace("التفاصيل:", "").strip()
    return title or article["title"], body

def write_telegram_post(article):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": TELEGRAM_PROMPT.format(
            title=article["title"],
            description=article.get("description", ""),
            source=article.get("source", "")
        )}],
        max_tokens=600
    )
    return response.choices[0].message.content

def write_instagram_post(article):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": INSTAGRAM_PROMPT.format(
            title=article["title"],
            description=article.get("description", "")
        )}],
        max_tokens=500
    )
    return response.choices[0].message.content
