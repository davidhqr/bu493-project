import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


fig = plt.figure() 
ax = fig.add_subplot(111)
col_labels = ['Unit', 'N', 'Mean', 'SD', 'Min', 'P25', 'Median', 'P75', 'Max', "Prop of 1's"]
# row_labels = ['Age', 'Buy or Sell', 'Years in Office', 'Party']
row_labels = ['Age', 'Years in Office', 'Party', 'proportion buys', 'Buy or Sell', 'Amount', 'Market Cap', 'Market Cap All Trades', 'Reps that trade age', 'Reps that trade years in office']
table_vals = []

house_transactions = pd.read_csv('house_returns.csv')
house_members = pd.read_csv('house_members.csv')
house_returns = pd.read_csv('house_returns.csv')
market_cap = pd.read_csv('MarketCap_Dec31_2020.csv')

house_transactions = house_transactions[house_transactions.apply(lambda x: x['ticker'] != '--', axis=1)]
house_transactions = house_transactions[house_transactions.apply(lambda x: x['type'] != 'Purchase', axis=1)]

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  

house_members['name'] = house_members['name'].str.split(' ').str[0] + house_members['name'].str.split(' ').str[-1]
house_transactions['representative'] = house_transactions['representative'].str.split(' ').str[1] + house_transactions['representative'].str.split(' ').str[-1]

house_members = house_members[house_members.apply(lambda x: x['Party'] == 'Democratic' or x['Party'] == 'Republican', axis=1)]
house_transactions = house_transactions[house_transactions.apply(lambda x: x['Party'] == 'Democratic' or x['Party'] == 'Republican', axis=1)]

end_date = datetime.date(2020, 12, 31)

#age
# time_difference = end_date - birth_date
house_members['Born'] = pd.to_datetime(house_members['Born'])
house_members['today'] = '2021-05-31'
house_members['today'] = pd.to_datetime(house_members['today'])
house_members['age'] = np.floor((house_members['today'] - house_members['Born']).dt.days / 365.2425)

house_returns['born'] = pd.to_datetime(house_returns['born'])
house_returns['today'] = '2021-05-31'
house_returns['today'] = pd.to_datetime(house_returns['today'])
house_returns['age'] = np.floor((house_returns['today'] - house_returns['born']).dt.days / 365.2425)

table_vals.append(['Years'] + np.round(house_members.describe()['age'].values, decimals=2).tolist() + [None])

# years in office
house_members['Assumed office'] = pd.to_datetime(house_members['Assumed office'])
house_members['Years in office'] = 2020 - house_members['Assumed office'].dt.year

house_returns['assumed_office'] = pd.to_datetime(house_returns['assumed_office'])
house_returns['Years in office'] = 2020 - house_returns['assumed_office'].dt.year

table_vals.append(['Years'] + np.round(house_members.describe()['Years in office'].values, decimals=2).tolist() + [None])

# party
house_members['Party'] = house_members['Party'].map({'Democratic': 1, 'Republican': 0})
table_vals.append(['Democratic: 1,\nRepublican: 0'] + np.round(house_members.describe()['Party'].values, decimals=2).tolist() + [None])

# house_transactions = house_transactions.merge(house_members, left_on='representative', right_on='name')
# print('Proportion democratic trades:', np.sum(house_transactions['Party']) / len(house_transactions['Party']))

house_transactions['Party'] = house_transactions['Party'].map({'Democratic': 1, 'Republican': 0})
proportion_democratic = np.sum(house_transactions['Party']) / len(house_transactions['Party'])
table_vals.append(['Proportion Democratic'] + [None] * 8 + [proportion_democratic])
print('Proportion democratic trades:', proportion_democratic)

# direction
house_transactions['direction'] = house_transactions['type'].map(lambda x: 1 if x == 'purchase' else 0)
print('Proportion of buys:', np.sum(house_transactions['direction']) / len(house_transactions['direction']))

# amount
house_transactions = house_transactions[house_transactions.apply(lambda x: x['amount'] != 'Unknown', axis=1)]
amount_map = {
    '$1,001 -': 500,
    '$15,001 - $50,000': 32500,
    '$1,001 - $15,000': 7500,
    '$50,001 - $100,000': 75000,
    '$500,001 - $1,000,000': 750000,
    '$100,001 - $250,000': 175000,
    '$1,000,001 - $5,000,000': 2500000,
    '$250,001 - $500,000': 375000,
    '$5,000,001 - $25,000,000': 15000000,
    '$25,000,001 - $50,000,000': 37500000,
    '$50,000,000 +': 75000000
}
house_transactions['amount_val'] = house_transactions['amount'].map(lambda x: amount_map[x])

# market cap for unique stocks
house_tickers = house_transactions['ticker'].unique()
market_cap['Market Cap'] = np.abs(market_cap['Market Cap'])
market_caps = pd.DataFrame({'ticker': house_tickers})
market_caps = market_caps.merge(market_cap, left_on='ticker', right_on='ticker')

# market cap for each transaction
market_cap['Market Cap'] = np.abs(market_cap['Market Cap'])
house_transactions = house_transactions.merge(market_cap, left_on='ticker', right_on='ticker')

# representatives that trade
reps_that_trade = house_returns.groupby('representative').first()

# add data to table
table_vals.append(['Buy: 1,\nSell: 0'] + np.round(house_transactions.describe()['direction'].values, decimals=2).tolist() + [None])
table_vals.append(['Dollars'] + np.round(house_transactions.describe()['amount_val'].values, decimals=2).tolist() + [None])
table_vals.append(['Thousand Dollars'] + np.round(market_caps.describe()['Market Cap'].values, decimals=2).tolist() + [None])
table_vals.append(['Thousand Dollars'] + np.round(house_transactions.describe()['Market Cap'].values, decimals=2).tolist() + [None])
table_vals.append(['Years'] + np.round(reps_that_trade.describe()['age'].values, decimals=2).tolist() + [None])
table_vals.append(['Years'] + np.round(reps_that_trade.describe()['Years in office'].values, decimals=2).tolist() + [None])

# Draw table
the_table = plt.table(cellText=table_vals,
                      colWidths=[0.15] * len(col_labels),
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(24)
the_table.scale(4, 6)

# Removing ticks and spines enables you to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('house-table1-sales.pdf', bbox_inches='tight', pad_inches=0.05)

