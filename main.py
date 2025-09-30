from flask import Flask
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from datetime import datetime
import requests
import os
import time
import threading

# --- Flask app (for Render to keep alive) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "👻 Ghost monitor is alive!"


# --- Discord webhook (replace with your URL) ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1422567143756660889/SLjdoBkIG-Si0NTy69VNl0EgULOYZbNlhBJxIHfs6QZl4zesa3HSm-tSOodae2H_KI_h"

# --- Pages to monitor ---
URLS = [
    "https://www.yorkghostmerchants.com/apparition",
    "https://www.yorkghostmerchants.com/shop"
]

# --- Check interval (seconds) ---
CHECK_INTERVAL = 60  # 60 = 1 minutes


# --- Site check function ---
def check_sites():
    results = []
    total_products = 0

    for url in URLS:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("div", class_="product-grid-item")
            count = len(products)
            total_products += count
            results.append((url, count))
        except Exception as e:
            results.append((url, f"Error: {e}"))

    return total_products, results


# --- Monitor loop ---
def run_monitor():
    while True:
        try:
            total_products, results = check_sites()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Print logs for each URL
            for url, count in results:
                print(f"[{timestamp}] {url} → {count} products listed.")

            # Send Discord alert if any products found
            if total_products > 0:
                message = "⚡ Ghosts detected!\n"
                for url, count in results:
                    message += f"{url} → {count} product(s)\n"

                webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
                webhook.execute()

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Error: {e}")

        time.sleep(CHECK_INTERVAL)


# --- Run everything ---
if __name__ == "__main__":
    threading.Thread(target=run_monitor).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

