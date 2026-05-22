import asyncio
from telethon import TelegramClient
from news_fetcher import fetch_ai_news
from content_writer import write_card_content, write_telegram_post, write_instagram_post
from card_generator import create_news_card, detect_company
from publisher import save_instagram_post
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHANNEL

client = TelegramClient("my_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def main():
    await client.start(phone="+9647763692061", password="yaali208")
    print("✅ متصل")

    articles = fetch_ai_news()
    if not articles:
        print("❌ ما في أخبار مناسبة")
        return

    article = articles[0]
    print(f"📰 الخبر: {article['title'][:60]}")

    print("✍️ يكتب محتوى الكارد...")
    title_ar, body_ar = write_card_content(article)
    print(f"   العنوان: {title_ar}")

    print("🎨 يصمم الكارد...")
    company_info = detect_company(article["title"], article.get("description", ""))
    card_path = create_news_card(title_ar, body_ar, company_info, "test_card.png")
    print(f"   حُفظ: {card_path}")

    print("✍️ يكتب الكابشن...")
    caption = write_telegram_post(article)

    print("📤 ينشر الصورة على تيليكرام...")
    await client.send_file(TELEGRAM_CHANNEL, card_path, caption=caption)

    ig_post = write_instagram_post(article)
    save_instagram_post(ig_post, 1)

    print("\n✅ نجح الاختبار! شوف قناتك على تيليكرام")
    await client.disconnect()

asyncio.run(main())
