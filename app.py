Python
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="MSIN Broker Summary Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. Basis Data Kumulatif (Hasil Ekstraksi 33 Screenshot MSIN)
@st.cache_data
def load_data():
    # Data Buyer
    buyers_data = {
        'Broker': ['EP', 'XL', 'ZP', 'AK', 'YP'],
        'Kategori': ['Domestik', 'Domestik', 'Asing', 'Asing', 'Domestik'],
        'Volume': [1139300, 309200, 291600, 224200, 175700],
        'Value': [74500000000, 25600000000, 18100000000, 16300000000, 14300000000],
        'Avg_Price': [654, 828, 621, 727, 814]
    }
    
    # Data Seller
    sellers_data = {
        'Broker': ['CC', 'RX', 'YP', 'BK', 'PD'],
        'Kategori': ['Institusi', 'Asing', 'Domestik', 'Asing', 'Domestik'],
        'Volume': [1488200, 761000, 148600, 81300, 68300],
        'Value': [98200000000, 33400000000, 11800000000, 6800000000, 4500000000],
        'Avg_Price': [660, 439, 794, 836, 659]
    }
    
    return pd.DataFrame(buyers_data), pd.DataFrame(sellers_data)

df_buyers, df_sellers = load_data()

# Fungsi untuk memberikan emoji warna berdasarkan Kategori Broker
def get_color_emoji(kategori):
    if kategori == 'Asing':
        return '🔴 Asing'
    elif kategori == 'Institusi':
        return '🟢 Institusi'
    else:
        return '🟣 Domestik'

df_buyers['Tipe Broker'] = df_buyers['Kategori'].apply(get_color_emoji)
df_sellers['Tipe Broker'] = df_sellers['Kategori'].apply(get_color_emoji)

# 3. INTERFACE DASHBOARD
st.title("📊 Dashboard Interaktif Broker Summary: MSIN")
st.markdown("---")

# TAMPILAN INDIKATOR UTAMA (METRICS CARD)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Volume Transaksi Periodik", value="15.42M Lot")
with col2:
    st.metric(label="Harga Terakhir (Last Price)", value="570", delta="+24.45% (ARA)")
with col3:
    st.metric(label="Status Money Flow", value="Big Accumulation")

st.markdown("---")

# TAMPILAN TABEL INTERAKTIF (TOP 5 BUYER & SELLER)
st.subheader("📋 Analisis Detail Top 5 Broker")
tab1, tab2 = st.tabs(["🛒 Top 5 Buyer (Akumulasi)", "📉 Top 5 Seller (Distribus)"])

with tab1:
    st.dataframe(
        df_buyers[['Broker', 'Tipe Broker', 'Volume', 'Value', 'Avg_Price']].style.format({
            'Volume': '{:,.0f} Lot',
            'Value': 'Rp {:,.0f}',
            'Avg_Price': '{:,.0f}'
        }), use_container_width=True
    )

with tab2:
    st.dataframe(
        df_sellers[['Broker', 'Tipe Broker', 'Volume', 'Value', 'Avg_Price']].style.format({
            'Volume': '{:,.0f} Lot',
            'Value': 'Rp {:,.0f}',
            'Avg_Price': '{:,.0f}'
        }), use_container_width=True
    )

st.markdown("---")

# VISUALISASI GRAFIK INTERAKTIF (PLOTLY CHARTS)
st.subheader("📈 Visualisasi Kekuatan Pasar (Net Value)")
col_chart1, col_chart2 = st.columns(2)

# Map warna untuk konsistensi grafik
color_map = {'Domestik': '#8A2BE2', 'Asing': '#FF4136', 'Institusi': '#2ECC40'}

with col_chart1:
    st.write("**Top 5 Buyer - Kekuatan Beli (Rp)**")
    fig_buy = px.bar(
        df_buyers, x='Broker', y='Value', color='Kategori',
        color_discrete_map=color_map,
        text_auto='.2s', labels={'Value': 'Nilai Transaksi (Rp)'}
    )
    st.plotly_chart(fig_buy, use_container_width=True)

with col_chart2:
    st.write("**Top 5 Seller - Kekuatan Jual (Rp)**")
    fig_sell = px.bar(
        df_sellers, x='Broker', y='Value', color='Kategori',
        color_discrete_map=color_map,
        text_auto='.2s', labels={'Value': 'Nilai Transaksi (Rp)'}
    )
    st.plotly_chart(fig_sell, use_container_width=True)

st.markdown("---")

# PANEL FILTRASI TAMBAHAN (MEMBUATNYA BENAR-BENAR INTERAKTIF)
st.sidebar.header("⚙️ Kontrol & Filter")
pilihan_broker = st.sidebar.multiselect(
    "Pilih Broker Tertentu untuk Riset:",
    options=list(df_buyers['Broker'].unique()) + list(df_sellers['Broker'].unique())
)

if pilihan_broker:
    st.sidebar.write("Anda memilih untuk memantau:", pilihan_broker)
    # Filter dinamis bisa dikembangkan di sini untuk riset berikutnya
