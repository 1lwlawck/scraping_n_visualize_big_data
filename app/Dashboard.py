import streamlit as st
import pandas as pd
from utils.db import get_collections
from utils.data_loader import get_latest_marketcap_data, get_historical_data
from utils.charts import bar_chart_marketcap, line_chart_price, line_chart_compare

# ------------------------ SETUP ------------------------
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="🪙",
    layout="wide"
)
st.title("📊 Crypto Market Dashboard")

realtime_collection, history_collection = get_collections()
df_latest = get_latest_marketcap_data(realtime_collection)
top10 = df_latest.head(10).copy()
available_symbols = history_collection.distinct('symbol')

# ------------------------ TABS ------------------------
tab1, tab2, tab3= st.tabs(["📈 Market Cap", "📉 Harga Historis", "📊 Perbandingan Aset"])

# ------------------------ TAB 1: Market Cap ------------------------
with tab1:
        st.subheader("📊 Grafik Market Cap Top 10")
        st.plotly_chart(bar_chart_marketcap(top10), use_container_width=True)

# ------------------------ TAB 2: Harga Historis ------------------------
with tab2:
    st.subheader("📈 Grafik Harga Historis")
    selected_symbol = st.selectbox("Pilih aset:", sorted(available_symbols), key="symbol_historis")
    hist_df = get_historical_data(history_collection, selected_symbol)

    if not hist_df.empty:
        st.plotly_chart(line_chart_price(hist_df, f"Harga Historis {selected_symbol} (USD)"), use_container_width=True)
    else:
        st.warning("Data historis belum cukup untuk ditampilkan.")

# ------------------------ TAB 3: Perbandingan ------------------------
with tab3:
    st.subheader("📉 Perbandingan Kinerja Beberapa Aset")
    selected_compare = st.multiselect("Pilih aset:", sorted(available_symbols), default=["BTC", "ETH"])

    if selected_compare:
        df_compare = pd.DataFrame()
        for sym in selected_compare:
            temp = get_historical_data(history_collection, sym)
            if not temp.empty:
                temp['symbol'] = sym
                df_compare = pd.concat([df_compare, temp], ignore_index=True)

        if not df_compare.empty:
            st.plotly_chart(line_chart_compare(df_compare), use_container_width=True)
        else:
            st.warning("Data tidak ditemukan untuk aset yang dipilih.")


