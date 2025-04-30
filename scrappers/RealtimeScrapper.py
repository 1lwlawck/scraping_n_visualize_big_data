import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
import requests, time, schedule
from datetime import datetime
from utils import get_mongo_connection 
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("CMC_API_KEY")
CMC_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
HEADERS = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
PARAMS = {'start': '1', 'limit': '100', 'convert': 'USD'}

def get_mongo_connection():
    return MongoClient(os.getenv("MONGO_URI"))


def fetch_realtime_data():
    client = get_mongo_connection()
    collection = client['ranking']['crypto']
    timestamp = datetime.utcnow()

    try:
        res = requests.get(CMC_URL, headers=HEADERS, params=PARAMS)
        data = res.json().get("data", [])
        inserted = 0

        for coin in data:
            symbol = coin['symbol']
            entry = {
                'rank': coin['cmc_rank'],
                'name': coin['name'],
                'symbol': symbol,
                'market_cap_usd': coin['quote']['USD']['market_cap'],
                'price_usd': coin['quote']['USD']['price'],
                'last_updated': coin['last_updated'],
                'scraped_at': timestamp
            }

            if not collection.find_one({'symbol': symbol, 'scraped_at': timestamp}):
                collection.insert_one(entry)
                inserted += 1

        print(f"[✓] Realtime: {inserted} records inserted at {timestamp}")
    except Exception as e:
        print(f"[!] Realtime fetch error: {e}")

# Scheduler
schedule.every(6).hours.do(fetch_realtime_data)
print("⏳ Realtime scraper running... Ctrl+C to stop.")
fetch_realtime_data()

while True:
    schedule.run_pending()
    time.sleep(1)
