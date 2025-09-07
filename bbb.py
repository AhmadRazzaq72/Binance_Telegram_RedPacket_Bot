import asyncio
from telethon import TelegramClient
import socks
import os

api_id = 1111111  # your API ID
api_hash = ""  # your API hash

# SOCKS5 proxy (with rdns=True)
proxy = (socks.SOCKS5, "142.171.138.233", 8989, True)

client = TelegramClient("tg_session2", api_id, api_hash, proxy=proxy)

async def main():
    print("Attempting connection via proxy...")
    await client.connect()

    if not await client.is_user_authorized():
        print("🔑 Not authorized. You will get a login code on Telegram.")
        await client.start()  # will ask for phone/code
    else:
        print("✅ Already authorized!")

    me = await client.get_me()
    print(f"🎉 Logged in as {me.first_name} (@{me.username})")

    await client.disconnect()

if __name__ == "__main__":
    # remove stale session if needed
    if os.path.exists("tg_session.session"):
        os.remove("tg_session.session")

    asyncio.run(main())
