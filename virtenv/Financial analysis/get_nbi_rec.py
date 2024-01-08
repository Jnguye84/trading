import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker_symbol = '^NBI'

def get_nbi_prices():
    nbi_ticker = yf.Ticker(ticker_symbol)
    hist = nbi_ticker.history(period="3mo")  # Fetch historical data for 3 months
    return hist

nbi_prices = get_nbi_prices()

# Plotting Close prices over time
plt.figure(figsize=(10, 6))
plt.plot(nbi_prices.index, nbi_prices['Close'], label='Close Price')
plt.title('Close Prices Over Time for ^NBI')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.grid(True)
plt.show()
