from flask import Flask
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from datetime import datetime
import requests
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "👻 Ghost monitor is alive!"


# --- Discord webhook URL (replace with yours, or use env variable) ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1422518082878046291/GyWRtAOuPuuQomaAgAIF72ZQKHDxLLZBgkWxyJdS_Cl9sM86ciA8mxZgjb3YMzmH7sE2"


# --- Site check function ---
def check_site():
    url = "https://www.yorkghostmerchants.com/apparition", "www.yorkghostmerchants.com/shop"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", class_="product-grid-item")
    return len(products)


# --- Monitor loop ---
CHECK_INTERVAL = 60  # seconds (1 minutes)

def run_monitor():
    while True:
        try:
            product_count = check_site()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Checked site: {product_count} products listed.")

            if product_count > 0:
                message = f"⚡ {product_count} ghost(s) detected on York Ghost Merchants!"
                webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
                webhook.execute()

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    import threading
    threading.Thread(target=run_monitor).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
