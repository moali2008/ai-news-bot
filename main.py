"""
بوت أخبار الذكاء الاصطناعي اليومي
ينشر كل يوم الساعة 9 مساءً بتوقيت الرياض
"""
import schedule
import time
from datetime import datetime
from news_fetcher import fetch_ai_news
from content_writer import write_telegram_post, write_instagram_post
from publisher import post_to_telegram, save_instagram_post
from config import POST_HOUR, POST_MINUTE

def daily_job():
    print(f"\n🚀 بدء جلب أخبار AI — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    articles = fetch_ai_news()
    if not articles:
        print("⚠️ لا توجد أخبار اليوم")
        return

    print(f"📰 وجدت {len(articles)} خبر")

    for i, article in enumerate(articles, 1):
        print(f"\n📌 خبر {i}: {article['title'][:60]}...")

        # كتابة وننشر على تيليكرام
        tg_post = write_telegram_post(article)
        post_to_telegram(tg_post)

        # كتابة وحفظ كابشن انستا
        ig_post = write_instagram_post(article)
        save_instagram_post(ig_post, i)

        # انتظار 3 دقائق بين كل بوست (يحسّن الخوارزمية)
        if i < len(articles):
            print("⏳ انتظار 3 دقائق للبوست التالي...")
            time.sleep(180)

    print(f"\n✅ اكتمل النشر اليومي — {len(articles)} بوست")

# جدولة النشر الساعة 9 مساءً
schedule.every().day.at(f"{POST_HOUR:02d}:{POST_MINUTE:02d}").do(daily_job)

print(f"🤖 البوت شغّال — ينشر الساعة {POST_HOUR}:{POST_MINUTE:02d} مساءً يومياً")
print("اضغط Ctrl+C لإيقافه\n")

# تشغيل فوري لاختبار (علّق هذا السطر بعد التأكد)
# daily_job()

while True:
    schedule.run_pending()
    time.sleep(60)
