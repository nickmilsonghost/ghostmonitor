from discord_webhook import DiscordWebhook
import os

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1422518082878046291/GyWRtAOuPuuQomaAgAIF72ZQKHDxLLZBgkWxyJdS_Cl9sM86ciA8mxZgjb3YMzmH7sE2"
from datetime import datetime

CHECK_INTERVAL = 60  # seconds

while True:
    try:
        product_count = check_site()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Checked site: {product_count} products listed.")

        if product_count > 0:
            message = f"⚡ {product_count} ghost(s) detected on York Ghost Merchants!"
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
            response = webhook.execute()
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Error: {e}")
    time.sleep(CHECK_INTERVAL)

from datetime import datetime
from flask import Flask
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "👻 Ghost monitor is alive!"

def check_site():
    url = "https://www.yorkghostmerchants.com/apparition"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # look for products (adjust if site changes)
    products = soup.find_all("div", class_="product-grid-item")
    return len(products)

def run_monitor():
    while True:
        try:
            product_count = check_site()
            print(f"Checked site: {product_count} products listed.")
            # TODO: Add Discord/email alert here if product_count > 0
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)  # check every 1 minutes

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host='0.0.0.0', port=8080)
