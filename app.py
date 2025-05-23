
# S&P500 + 양자컴퓨터 관련 종목 매수 신호 웹앱 (내부자 매수 강조 버전)

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

st.set_page_config(page_title="S&P500 & 양자컴퓨터 매수 신호", layout="centered")
st.title("🧠 오늘의 매수 신호 종목: S&P500 + 양자컴퓨터 관련")

tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'UNH', 'JNJ',
    'JPM', 'XOM', 'V', 'PG', 'MA', 'CVX', 'LLY', 'HD', 'MRK', 'ABBV', 'PEP', 'KO',
    'AVGO', 'COST', 'BAC', 'WMT', 'DIS', 'MCD', 'TMO', 'CSCO', 'PFE', 'ADBE',
    'CRM', 'ABT', 'NKE', 'ACN', 'INTC', 'TXN', 'NEE', 'DHR', 'QCOM', 'LIN', 'UPS',
    'HON', 'UNP', 'AMD', 'LOW', 'PM', 'SBUX', 'ORCL', 'INTU', 'AMGN', 'RTX',
    'ISRG', 'BLK', 'GILD', 'AMAT', 'CAT', 'MDT', 'BA', 'NOW', 'LRCX', 'ADI', 'ZTS',
    'MO', 'TGT', 'CI', 'GE', 'MMC', 'SPGI', 'ELV', 'SYK', 'DE', 'ETN', 'TJX',
    'CL', 'SCHW', 'PGR', 'ADP', 'APD', 'REGN', 'EW', 'BDX', 'FDX', 'AON', 'FISV',
    'C', 'MS', 'PLD', 'ICE', 'CB', 'ECL', 'CTSH', 'AIG', 'HCA', 'MAR', 'ROP', 'PSA',
    'IBM', 'GOOG', 'IONQ', 'QSI', 'RGTI', 'AMZN', 'MSFT'
]

insider_favored = ['MU', 'NVDA', 'META', 'PLTR', 'TSLA', 'AMZN', 'CRM']

end_date = datetime.today()
start_date = end_date - timedelta(days=180)

def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

signals = []

with st.spinner("📊 전체 종목 분석 중입니다..."):
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty or len(data) < 60:
                continue

            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['RSI'] = compute_rsi(data)
            data['Daily Return'] = data['Close'].pct_change()
            data['Volatility'] = data['Daily Return'].rolling(window=20).std()

            recent = data.iloc[-1]
            sma_target = recent['SMA20'] * 1.07
            upside_potential = (sma_target - recent['Close']) / recent['Close']

            if ticker in insider_favored:
                if (
                    0.06 <= upside_potential <= 0.12 and
                    recent['RSI'] < 80 and
                    recent['Volatility'] < 0.07
                ):
                    signals.append({
                        '티커': ticker + ' ⭐',
                        '현재가': round(recent['Close'], 2),
                        '목표가 (+7%)': round(sma_target, 2),
                        '예상 수익률': f"{round(upside_potential * 100, 2)}%",
                        'RSI': round(recent['RSI'], 2),
                        '변동성': round(recent['Volatility'], 4)
                    })
            else:
                if (
                    0.07 <= upside_potential <= 0.10 and
                    recent['RSI'] < 78 and
                    recent['Volatility'] < 0.06
                ):
                    signals.append({
                        '티커': ticker,
                        '현재가': round(recent['Close'], 2),
                        '목표가 (+7%)': round(sma_target, 2),
                        '예상 수익률': f"{round(upside_potential * 100, 2)}%",
                        'RSI': round(recent['RSI'], 2),
                        '변동성': round(recent['Volatility'], 4)
                    })
        except:
            continue

if signals:
    st.success(f"✅ 총 {len(signals)}개 종목이 조건을 만족했습니다.")
    df = pd.DataFrame(signals)
    st.dataframe(df)
else:
    st.warning("🔍 현재 조건을 만족하는 종목이 없습니다. 내일 다시 확인해보세요.")
