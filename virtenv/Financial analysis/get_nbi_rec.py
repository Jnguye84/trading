import yfinance as yf

ticker_symbol = '^NBI'

def get_nbi_trend():
    nbi_ticker = yf.Ticker(ticker_symbol)
    fifty_day_avg = nbi_ticker.info["fiftyDayAverage"]
    close = nbi_ticker.info["previousClose"]
    if close > fifty_day_avg:
        return "Trending Up"
    if close < fifty_day_avg:
        return "Trending Down"


print(get_nbi_trend())
