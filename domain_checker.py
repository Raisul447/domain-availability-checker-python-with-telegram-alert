# ============================================
# Domain Availability Telegram Alert
# Works perfectly on PythonAnywhere or any server
# Author: Raisul Islam
# Contact: deploy@raisul.dev
# Website: https://raisul.dev
# ============================================

import requests
import time

# ======== CONFIGURATION ========
DOMAINS = ["raisul.dev"]  # <-- Replace with your own domain, also you can add more, e.g. ["test.dev", "test.com"]
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- Replace with your bot token
CHAT_ID = "YOUR_CHAT_ID_HERE"      # <-- Replace with your chat ID
CHECK_INTERVAL = 43200  # Check every 12 hours (43200 seconds)
# ===============================


def send_telegram_message(message):
    """Send a message to your Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload)
        if r.status_code != 200:
            print("⚠️ Telegram API error:", r.text)
    except Exception as e:
        print("⚠️ Telegram connection error:", e)


def check_domain(domain):
    """Check if a domain is available using a public WHOIS API."""
    url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "domains" in data and data["domains"]:
                print(f"❌ {domain} is still registered.")
                return False
            else:
                print(f"✅ {domain} is AVAILABLE!")
                send_telegram_message(f"✅ {domain} is AVAILABLE! Hurry up and register it 🚀")
                return True
        else:
            print(f"⚠️ Server responded with status {response.status_code}")
            return False
    except Exception as e:
        print("⚠️ Error checking domain:", e)
        return False


def main():
    print("🔎 Domain availability checker started...\n")
    while True:
        for domain in DOMAINS:
            check_domain(domain)
            time.sleep(5)  # Wait 5 seconds between domain checks
        print(f"\n⏳ Next check in {CHECK_INTERVAL/3600} hours...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    send_telegram_message("Test message: Telegram bot is working from the script!") # If this message received your bot then Telegram connected (You can remove it)
    main()