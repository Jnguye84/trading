import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Alpha Vantage API key and ticker symbol
api_key = 'NUITBAL6RYNHAL6G'
ticker_symbol = 'PCRX'

def get_income_data(ticker):
    base_url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}'
    response = requests.get(base_url)
    data = response.json()

    if 'quarterlyReports' in data:
        income_df = pd.DataFrame(data['quarterlyReports'])
        income_df['date'] = pd.to_datetime(income_df['fiscalDateEnding'])
        income_df.set_index('date', inplace=True)
        income_df.sort_index(inplace=True)
        
        # Convert 'totalRevenue' column to numeric (if it contains strings)
        income_df['totalRevenue'] = pd.to_numeric(income_df['totalRevenue'], errors='coerce')
        
        return income_df
    else:
        return pd.DataFrame()

data = get_income_data(ticker_symbol)

# Create a column for 'totalRevenue' in millions
data['totalRevenue_millions'] = data['totalRevenue'] / 1000000

plt.figure(figsize=(10, 6))

# Scatter plot with markers
plt.scatter(data.index, data['totalRevenue_millions'], label='revenue', marker='o')

# Connect points with dotted lines
plt.plot(data.index, data['totalRevenue_millions'], linestyle='dotted', color='black')

plt.title(f'Revenue Over Time for {ticker_symbol}')
plt.xlabel('Date')
plt.ylabel('Total Revenue (Millions)')
plt.legend()
plt.grid(True)

# Formatting y-axis ticks to display in millions
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}M'))

plt.show()
