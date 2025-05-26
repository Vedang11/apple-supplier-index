{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import yfinance as yf\
import streamlit as st\
from datetime import datetime, timedelta\
import plotly.express as px\
\
st.set_page_config(page_title="Apple Supplier Index", layout="wide")\
st.title("\uc0\u55357 \u56520  Apple Supplier Index Tracker")\
\
@st.cache_data\
def load_data():\
    df = pd.read_csv("apple_supplier_index_constituents.csv")\
    df = df.dropna(subset=["Ticker"])\
    return df\
\
df_const = load_data()\
\
st.sidebar.header("\uc0\u55358 \u56809  Constituents")\
st.sidebar.dataframe(df_const[["Company", "Ticker"]])\
\
period = st.sidebar.selectbox("History", ["1y", "2y", "5y"], index=0)\
days_back = \{"1y": 365, "2y": 730, "5y": 1825\}[period]\
start_date = datetime.today() - timedelta(days=days_back)\
\
@st.cache_data\
def download_prices(tickers, start):\
    return yf.download(tickers, start=start.strftime("%Y-%m-%d"))["Adj Close"]\
\
prices = download_prices(df_const["Ticker"].tolist(), start_date)\
\
weights = df_const.set_index("Ticker")["Weight"]\
weights = weights / weights.sum()\
returns = prices.pct_change().fillna(0)\
index = (returns * weights).sum(axis=1).add(1).cumprod()\
index = index / index.iloc[0] * 100\
\
fig = px.line(index, title="Custom Apple Supplier Index (base = 100)",\
              labels=\{"value": "Index Level", "index": "Date"\})\
st.plotly_chart(fig, use_container_width=True)\
\
with st.expander("\uc0\u55357 \u56522  Raw Price Data"):\
    st.dataframe(prices.tail(10))\
}