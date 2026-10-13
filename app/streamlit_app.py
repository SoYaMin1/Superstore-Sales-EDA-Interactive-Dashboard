import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Superstore Dashboard", layout="wide")
st.title("📊 Superstore Sales Dashboard")

@st.cache_data
def load():
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = load()

# --- Сайдбар фильтров ---
st.sidebar.header("Фильтры")
years = st.sidebar.multiselect("Год", sorted(df["Order Year"].unique()),
                               default=sorted(df["Order Year"].unique()))
regions = st.sidebar.multiselect("Регион", sorted(df["Region"].unique()),
                                 default=sorted(df["Region"].unique()))
cats = st.sidebar.multiselect("Категория", sorted(df["Category"].unique()),
                              default=sorted(df["Category"].unique()))

mask = df["Order Year"].isin(years) & df["Region"].isin(regions) & df["Category"].isin(cats)
d = df[mask]

# --- KPI ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Sales",     f"${d['Sales'].sum():,.0f}")
c2.metric("📈 Profit",    f"${d['Profit'].sum():,.0f}")
c3.metric("🧾 Orders",    d["Order ID"].nunique())
c4.metric("📊 Avg Margin",f"{(d['Profit'].sum()/d['Sales'].sum())*100:.1f}%")

# --- Графики ---
col1, col2 = st.columns(2)

with col1:
    ts = d.groupby("Order Month")["Sales"].sum().reset_index()
    st.plotly_chart(px.line(ts, x="Order Month", y="Sales",
                            title="Sales by Month"), use_container_width=True)

with col2:
    reg = d.groupby("Region")["Profit"].sum().reset_index()
    st.plotly_chart(px.bar(reg, x="Region", y="Profit",
                           title="Profit by Region",
                           color="Profit", color_continuous_scale="RdYlGn"),
                    use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(px.treemap(d, path=["Category","Sub-Category"],
                               values="Sales",
                               title="Sales Treemap"),
                    use_container_width=True)
with col4:
    st.plotly_chart(px.scatter(d, x="Discount", y="Profit",
                               color="Category", opacity=0.5,
                               title="Discount vs Profit"),
                    use_container_width=True)

st.subheader("📋 Данные")
st.dataframe(d.head(200))