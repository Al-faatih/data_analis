import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Data Analysis Dashboard")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "data", "E-commerce-public-dataset", "E-Commerce Public Dataset"))

    orders = pd.read_csv(os.path.join(DATA_DIR, "orders_dataset.csv"))
    order_items = pd.read_csv(os.path.join(DATA_DIR, "order_items_dataset.csv"))
    products = pd.read_csv(os.path.join(DATA_DIR, "products_dataset.csv"))
    category = pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv"))

    # merge dataset
    df = orders.merge(order_items, on="order_id")
    df = df.merge(products, on="product_id")
    df = df.merge(category, on="product_category_name", how="left")

    # cleaning
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    df = df.dropna(subset=['order_purchase_timestamp', 'price', 'product_category_name_english'])

    # convert datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # feature engineering
    df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    return df

df = load_data()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("Filter Data")

category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=df['product_category_name_english'].unique(),
    default=df['product_category_name_english'].unique()
)

df_filtered = df[df['product_category_name_english'].isin(category)]

# ===============================
# METRIC
# ===============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", f"${df_filtered['price'].sum():,.2f}")
col3.metric("Total Products", df_filtered['product_id'].nunique())

# ===============================
# TOP CATEGORY
# ===============================
st.subheader("🏆 Top 10 Kategori Produk")

category_sales = (
    df_filtered.groupby('product_category_name_english')['price']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
category_sales.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# ===============================
# TREND BULANAN
# ===============================
st.subheader("📈 Tren Order Bulanan")

monthly_orders = (
    df_filtered.groupby('month')['order_id']
    .nunique()
)

fig2, ax2 = plt.subplots()
monthly_orders.plot(ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# ===============================
# INSIGHT
# ===============================
st.subheader("💡 Insight")

st.write("""
- Penjualan didominasi oleh beberapa kategori utama  
- Terjadi peningkatan order pada akhir tahun  
- Terdapat fluktuasi order bulanan  
""")

# ===============================
# RECOMMENDATION
# ===============================
st.subheader("🚀 Recommendations")

st.write("""
1. Fokus pada kategori dengan penjualan tinggi  
2. Optimalkan kategori dengan performa rendah  
3. Maksimalkan campaign pada akhir tahun  
4. Buat strategi promo di bulan sepi  
""")