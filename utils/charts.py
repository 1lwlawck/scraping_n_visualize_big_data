import plotly.express as px
import pandas as pd

def bar_chart_marketcap(df):
    return px.bar(df, x='symbol', y='market_cap_usd', color='symbol',
                  hover_data=['name', 'price_usd'], title='Top 10 Market Cap (USD)',
                  labels={'market_cap_usd': 'Market Cap (USD)'})


def line_chart_price(df, title):
    return px.line(df, x='scraped_at', y='price_usd', title=title,
                   labels={'scraped_at': 'Tanggal', 'price_usd': 'Harga (USD)'})

def line_chart_compare(df_compare):
    df_compare['price_normalized'] = df_compare.groupby('symbol')['price_usd'].transform(lambda x: (x / x.iloc[0]) * 100)
    return px.line(df_compare, x='scraped_at', y='price_normalized', color='symbol',
                   title='Perbandingan Kinerja (% dari Harga Awal)',
                   labels={'scraped_at': 'Tanggal', 'price_normalized': 'Persentase'})

