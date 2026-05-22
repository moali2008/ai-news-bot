import feedparser
from datetime import datetime, timezone

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://www.wired.com/feed/category/artificial-intelligence/latest/rss",
    "https://openai.com/news/rss/",
    "https://www.anthropic.com/rss.xml",
]

# أخبار هذه الشركات فقط تُنشر
PRIORITY_KEYWORDS = [
    "chatgpt", "openai", "gpt-4", "gpt-5", "o3", "o4", "sora", "dall-e",
    "claude", "anthropic",
    "gemini", "google ai", "google deepmind", "notebooklm", "veo",
    "grok", "llama", "meta ai", "mistral", "copilot"
]

def fetch_ai_news():
    """جلب أحدث أخبار الذكاء الاصطناعي من RSS"""
    articles = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:2]:  # أحدث خبرين من كل مصدر
                articles.append({
                    "title":       entry.get("title", ""),
                    "description": entry.get("summary", entry.get("description", ""))[:500],
                    "link":        entry.get("link", ""),
                    "source":      feed.feed.get("title", ""),
                })
        except Exception as e:
            print(f"⚠️ خطأ في {feed_url}: {e}")

    # فلترة: أخبار ChatGPT/Claude/Gemini فقط
    seen = set()
    unique = []
    for a in articles:
        title_lower = a["title"].lower()
        desc_lower  = a.get("description", "").lower()
        is_relevant = any(kw in title_lower or kw in desc_lower for kw in PRIORITY_KEYWORDS)
        if is_relevant and a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)

    print(f"📰 جُلب {len(unique)} خبر مناسب")
    return unique[:5]
