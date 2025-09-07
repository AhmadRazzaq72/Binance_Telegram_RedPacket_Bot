import os
import re
import time
import random
from dotenv import load_dotenv
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import asyncio
import socks


# Load env
load_dotenv()

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
PHONE = os.getenv("TG_PHONE")
CHANNEL = os.getenv("TG_CHANNEL")

COUPON_REGEX = re.compile(r"\b[A-Z0-9]{8}\b")  # 8-char code

# Logging
def log_result(code, status):
    with open("redeem_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {code} | {status}\n")

# Setup Selenium
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://www.binance.com/en/my/wallet/account/payment/cryptobox")

print("👉 Please log into Binance manually in this browser (captcha/2FA).")
input("✅ Press Enter after you are fully logged in and coupon page is visible...")

# Queue for incoming codes
pending_codes = []

def human_delay():
    time.sleep(random.uniform(1, 3))

def close_modal():
    """Try to close modal if visible"""
    try:
        close_icon = driver.find_element(By.CSS_SELECTOR, "svg.bn-svg")
        close_icon.click()
        human_delay()
    except NoSuchElementException:
        pass

def redeem_coupon(code, retry=False):
    try:
        print(f"🎟 Trying code: {code}")

        # Input field
        input_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter red packet code']")
        input_box.clear()
        human_delay()
        input_box.send_keys(code)

        # Claim button
        claim_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Claim')]")
        claim_btn.click()
        human_delay()

        time.sleep(2)  # wait for modal

        # Try Open button
        try:
            open_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Open')]")
            open_btn.click()
            human_delay()
            print(f"✅ Code {code} opened successfully")
            log_result(code, "Opened Successfully")
        except NoSuchElementException:
            print(f"⚠️ No Open button → already claimed for {code}")
            log_result(code, "Already Claimed / Invalid")

        # Close modal
        close_modal()

    except Exception as e:
        print(f"❌ Error with code {code}: {e}")

        if not retry:  # retry once
            print(f"🔄 Retrying code {code}...")
            human_delay()
            redeem_coupon(code, retry=True)
        else:
            try:
                # reload page on unexpected error
                print("♻️ Reloading coupon page...")
                driver.get("https://www.binance.com/en/my/wallet/account/payment/cryptobox")
                human_delay()
            except WebDriverException as we:
                print("⚠️ Critical WebDriver error:", we)

            log_result(code, f"Failed after retry: {e}")
            close_modal()

proxy = (socks.SOCKS5, "142.171.138.233", 8989, True)

# Telegram client
client = TelegramClient("session", API_ID, API_HASH,  proxy=proxy)

@client.on(events.NewMessage(chats=CHANNEL))
async def handler(event):
    text = event.raw_text.strip()
    match = COUPON_REGEX.search(text)
    if match:
        code = match.group(0)
        print(f"📩 Received code from Telegram: {code}")
        pending_codes.append(code)

async def worker():
    """Continuously process codes from queue"""
    while True:
        if pending_codes:
            code = pending_codes.pop(0)
            redeem_coupon(code)
        await asyncio.sleep(2)

print("🤖 Bot is running… waiting for coupon codes from Telegram")

with client:
    client.loop.create_task(worker())
    client.run_until_disconnected()
