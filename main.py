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
        time.sleep(300)  # check every 1 minutes

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host='0.0.0.0', port=8080)
