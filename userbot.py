import asyncio
import json
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

from news_fetcher import fetch_ai_news
from content_writer import write_telegram_post, write_instagram_post
from publisher import get_logo_path, save_instagram_post

TELEGRAM_API_ID   = int(os.environ.get("TELEGRAM_API_ID",   "34470238"))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH",     "d4e87d995c9e0083a9ad280e0f289621")
TELEGRAM_SESSION  = os.environ.get("TELEGRAM_SESSION",      "")
TELEGRAM_CHANNEL  = os.environ.get("TELEGRAM_CHANNEL",      "@ainews_arabic")

session = StringSession(TELEGRAM_SESSION) if TELEGRAM_SESSION else "my_session"
client  = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)

SEEN_FILE      = os.path.join(os.path.dirname(__file__), "seen_articles.json")
CHECK_INTERVAL = 15 * 60

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen)[-500:], f, ensure_ascii=False)

async def post_article(article):
    try:
        caption   = write_telegram_post(article)
        logo_path = get_logo_path(article["title"], article.get("description", ""))

        await client.send_file(TELEGRAM_CHANNEL, logo_path, caption=caption)

        ig_post = write_instagram_post(article)
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        save_instagram_post(ig_post, ts)

        print(f"[OK] {article['title'][:50]}")
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"[ERR] {e}")

async def get_code():
    print("Enter Telegram OTP:")
    return input().strip()

async def monitor_loop():
    seen = load_seen()
    print("Monitoring AI news every 15 min...")

    while True:
        try:
            print(f"[{datetime.now().strftime('%H:%M')}] Checking...")
            articles    = fetch_ai_news()
            new_articles = [a for a in articles if a["title"] not in seen]

            if new_articles:
                print(f"Found {len(new_articles)} new articles!")
                for article in new_articles:
                    await post_article(article)
                    seen.add(article["title"])
                    await asyncio.sleep(30)
                save_seen(seen)
            else:
                print("No new articles.")
        except Exception as e:
            print(f"[ERR] {e}")

        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("Session invalid or missing!")
        return
    print("Connected successfully.")
    await monitor_loop()

if __name__ == "__main__":
    asyncio.run(main())
