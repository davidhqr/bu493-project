import numpy as np
import pandas as pd

# pd.set_option('display.max_rows', None)  
# pd.set_option('display.max_columns', None)  

senate_transactions_w_returns = pd.read_csv('senate_transactions_w_returns.csv')
senate_members = pd.read_csv('senate_members.csv').set_index('Senator')

index_prices = pd.read_csv('RUSSEL_3000_2020.csv')
index_prices['Date'] = pd.to_datetime(index_prices['Date'])

all_committees = pd.read_csv('Committee.csv', header=None)[0].to_list()

senate_committees = pd.read_csv('senate_committees.csv')
senate_committees['Sen'] = senate_committees['Name']
senate_committees = senate_committees.set_index('Name')
# senate_committees = senate_committees[senate_committees['Committee #'] == 117]

joined = senate_members.join(senate_committees)
joined = joined.groupby(joined.index).agg({
    'Sen': 'first', 
    'Party': 'first', 
    'Born': 'first',
    'Occupation(s)': 'first',
    'Assumed office': 'first',
    'Committee': ';'.join, 
    }).reset_index()

for newcol in ['1d index', '5d index', '1m index']:
    senate_transactions_w_returns[newcol] = np.nan

def get_returns(date, time):
    times = {'1d':1, '5d':5, '1m':22}
    stock_prices = index_prices[(index_prices['Date'] >= pd.to_datetime(date))]
    # print(stock_prices.iloc[times[time], 4], stock_prices.iloc[0, 4])
    try:
        return float(stock_prices.iloc[times[time], 4].replace(',', '')) / float(stock_prices.iloc[0, 4].replace(',', '')) - 1
    except:
        return None

print(senate_transactions_w_returns.apply(lambda row: get_returns(row.transaction_date, '1d'), axis = 1))
senate_transactions_w_returns['1d index'] = senate_transactions_w_returns.apply(lambda row: get_returns(row.transaction_date, '1d'), axis = 1)
senate_transactions_w_returns['5d index'] = senate_transactions_w_returns.apply(lambda row: get_returns(row.transaction_date, '5d'), axis = 1)
senate_transactions_w_returns['1m index'] = senate_transactions_w_returns.apply(lambda row: get_returns(row.transaction_date, '1m'), axis = 1)


for newcol in all_committees:
    senate_transactions_w_returns[newcol] = 0

for index, row in senate_transactions_w_returns.iterrows():
    senator_info = joined.loc[joined['Sen'] == row['senator']]
    if senator_info.empty:
        continue

    committees = senator_info.iloc[0]['Committee'].split(';')
    for committee in committees:
        senate_transactions_w_returns.at[index, committee] = 1
    
print(senate_transactions_w_returns.head(5))
senate_transactions_w_returns.to_csv('temp.csv')
