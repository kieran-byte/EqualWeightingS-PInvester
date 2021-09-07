import math
import pandas as pd
import requests
from secrets import IEX_CLOUD_API_TOKEN


def chunks(lst, n):
    # Creates successive n size chunks from a list
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# gets the portfolio size off the user
portfolio_size = input("Enter the value of your portfolio:")
try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \n Try again:")
    portfolio_size = input("Enter the value of your portfolio:")


# setting up the column names of the excel spreadsheet
my_columns = ['Ticker', 'Price', 'Market Capitalization', 'Number Of Shares to Buy']
final_dataframe = pd.DataFrame(columns=my_columns)


# reads in all the stock symbols from the csv file
stocks = pd.read_csv('sp_500_stocks.csv')


# separates the stocks into chunks for the batch api calls
symbol_groups = list(chunks(stocks['Ticker'], 100))  # each chunk is of length 100
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    # print(symbol_strings[i])


final_dataframe = pd.DataFrame(columns=my_columns)

# iterates through all the chunks executing batch api calls
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series([symbol,
                       data[symbol]['quote']['latestPrice'],
                       data[symbol]['quote']['marketCap'],
                       'N/A'],
                      index=my_columns),
            ignore_index=True)

position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])-1):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])


writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
final_dataframe.to_excel(writer, sheet_name='Recommended Trades', index=False)


writer.save()
