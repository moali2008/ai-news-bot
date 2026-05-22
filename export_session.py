import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH

async def main():
    old_client = TelegramClient("my_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await old_client.connect()

    new_session = StringSession()
    new_session.set_dc(
        old_client.session.dc_id,
        old_client.session.server_address,
        old_client.session.port
    )
    new_session.auth_key = old_client.session.auth_key

    session_str = new_session.save()
    await old_client.disconnect()

    with open("session_string.txt", "w") as f:
        f.write(session_str)

    print("Done! saved to session_string.txt")

asyncio.run(main())
