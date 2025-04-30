from pycoingecko import CoinGeckoAPI
from utils.db import get_mongo_connection
from datetime import datetime
import time

cg = CoinGeckoAPI()

def fetch_historical_data():
    client = get_mongo_connection()
    collection = client['ranking']['history']

    coins = cg.get_coins_markets(vs_currency='usd', per_page=100, page=1)
    coin_map = {c['symbol'].upper(): c['id'] for c in coins}

    from_time = int(datetime(2020, 1, 1).timestamp())
    to_time = int(time.time())

    for symbol, gecko_id in coin_map.items():
        print(f"🔄 {symbol} ({gecko_id})")
        try:
            data = cg.get_coin_market_chart_range_by_id(
                id=gecko_id,
                vs_currency='usd',
                from_timestamp=from_time,
                to_timestamp=to_time
            )
            prices = data.get('prices', [])
            inserted = 0

            for p in prices:
                ts = datetime.fromtimestamp(p[0]/1000)
                price = p[1]
                entry = {'symbol': symbol, 'scraped_at': ts, 'price_usd': price}

                if not collection.find_one({'symbol': symbol, 'scraped_at': ts}):
                    collection.insert_one(entry)
                    inserted += 1
            print(f"   [✓] {inserted} data disimpan.")
        except Exception as e:
            print(f"   [!] Error {symbol}: {e}")

if __name__ == "__main__":
    fetch_historical_data()
