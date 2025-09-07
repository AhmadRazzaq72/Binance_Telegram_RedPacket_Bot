
------------------------------------------------------------
🎟 Coupon Auto-Redeemer Bot
------------------------------------------------------------

A Python automation tool that applies coupon codes on Binance (or similar platforms) from Telegram using Selenium WebDriver.

It includes:
- Smart Queue system (no overlapping execution).
- Automatic retries on network or click failures.
- Graceful handling of WinError 121 (semaphore timeout).
- Reload + retry on intercepted button clicks.

------------------------------------------------------------
Features
------------------------------------------------------------
- Smart Queue: Coupons are processed one-by-one, failed codes are re-queued automatically.
- Retry Mechanism: Network errors, intercepted clicks, or timeouts are retried before skipping.
- Non-Overlapping Clicks: Uses Selenium waits to ensure buttons are clickable before clicking.
- Error Handling: Detects issues like "element click intercepted" and "WinError 121".

------------------------------------------------------------
Requirements
------------------------------------------------------------
- Python 3.9 or higher
- Google Chrome (latest version)
- ChromeDriver (matching your Chrome version)
- Python dependency: selenium

Install with:
pip install selenium

------------------------------------------------------------
Setup
------------------------------------------------------------
1. Clone or download the project.
2. Place your chromedriver.exe in the project root or add it to PATH.
3. Edit the coupons list in main.py, for example:

   coupons = ["BWJK6BTS", "ABC123", "XYZ999"]

4. Run the bot with:
   python coupon_bot.py

------------------------------------------------------------
Project Structure
------------------------------------------------------------
coupon-bot/
  coupon_bot.py           -> Core script with smart queue
  README.txt        -> Documentation

------------------------------------------------------------
Smart Queue Logic
------------------------------------------------------------
1. Load all coupons into a queue.
2. Try applying the coupon.
   - If success, remove from queue.
   - If error, re-queue and retry later.
3. Prevents duplicate clicks and overlapping Selenium commands.

------------------------------------------------------------
Troubleshooting
------------------------------------------------------------
- WinError 121: Semaphore timeout → Network/server delay. Handled with retry, but check internet stability.
- Element click intercepted: Popup/overlay blocking button. Script reloads page and retries.
- ChromeDriver mismatch: Download correct version from https://chromedriver.chromium.org/downloads

------------------------------------------------------------

