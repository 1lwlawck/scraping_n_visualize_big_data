import pandas as pd
from utils.db import get_mongo_connection

def get_latest_marketcap_data(collection):
    data = list(collection.find({}, {'_id': 0}))
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame()
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    latest = df[df['scraped_at'] == df['scraped_at'].max()]
    return latest.sort_values(by='market_cap_usd', ascending=False)

def get_historical_data(collection, symbol):
    data = list(collection.find({'symbol': symbol}, {'_id': 0}))
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    return df.sort_values('scraped_at')
