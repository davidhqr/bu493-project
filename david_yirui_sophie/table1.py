import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


fig = plt.figure() 
ax = fig.add_subplot(111)
col_labels = ['Unit', 'N', 'Mean', 'SD', 'Min', 'P25', 'Median', 'P75', 'Max']
# row_labels = ['Age', 'Buy or Sell', 'Years in Office', 'Party']
row_labels = ['Age', 'Years in Office', 'Party', 'Buy or Sell', 'Amount', 'Market Cap', 'Market Cap All Trades']
table_vals = []

senate_transactions = pd.read_csv('senate_transactions.csv')
senate_members = pd.read_csv('senate_members.csv')
market_cap = pd.read_csv('MarketCap_Dec31_2020.csv')

senate_transactions = senate_transactions[senate_transactions.apply(lambda x: x['ticker'] != '--', axis=1)]

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  

# print(senate_transactions.describe(include='all'))
# print(senate_transactions.dtypes)

senate_members = senate_members[senate_members.apply(lambda x: x['Party'] == 'Democratic' or x['Party'] == 'Republican', axis=1)]

end_date = datetime.date(2020, 12, 31)

# time_difference = end_date - birth_date
senate_members['Born'] = pd.to_datetime(senate_members['Born'])
senate_members['today'] = '2021-05-31'
senate_members['today'] = pd.to_datetime(senate_members['today'])
senate_members['age'] = np.floor((senate_members['today'] - senate_members['Born']).dt.days / 365.2425)
table_vals.append(['Date'] + np.round(senate_members.describe()['age'].values, decimals=2).tolist())

# years in office
senate_members['Assumed office'] = pd.to_datetime(senate_members['Assumed office'])
senate_members['Years in office'] = np.floor((senate_members['today'] - senate_members['Assumed office']).dt.days / 365.2425)
table_vals.append(['Number'] + np.round(senate_members.describe()['Years in office'].values, decimals=2).tolist())

# party
senate_members['Party'] = senate_members['Party'].map({'Democratic': 1, 'Republican': 0})
table_vals.append(['Democratic: 1,\nRepublican: 0'] + np.round(senate_members.describe()['Party'].values, decimals=2).tolist())

# direction
senate_transactions['direction'] = senate_transactions['type'].map(lambda x: 1 if x == 'Purchase' else 0)
# print(senate_transactions['direction'])
table_vals.append(['Purchase: 1,\nSell: 0'] + np.round(senate_transactions.describe()['direction'].values, decimals=2).tolist())

# amount
senate_transactions = senate_transactions[senate_transactions.apply(lambda x: x['amount'] != 'Unknown', axis=1)]
amount_map = {
    '$15,001 - $50,000': 32500,
    '$1,001 - $15,000': 7500,
    '$50,001 - $100,000': 75000,
    '$500,001 - $1,000,000': 750000,
    '$100,001 - $250,000': 175000,
    '$1,000,001 - $5,000,000': 2500000,
    '$250,001 - $500,000': 375000,
    '$5,000,001 - $25,000,000': 15000000,
    '$25,000,001 - $50,000,000': 37500000,
    'Over $50,000,000': 75000000
}
senate_transactions['amount_val'] = senate_transactions['amount'].map(lambda x: amount_map[x])
table_vals.append(['Dollars'] + np.round(senate_transactions.describe()['amount_val'].values, decimals=2).tolist())

# market cap for unique stocks
senate_tickers = senate_transactions['ticker'].unique()
market_cap['Market Cap'] = np.abs(market_cap['Market Cap'])
market_caps = pd.DataFrame({'ticker': senate_tickers})
market_caps = market_caps.merge(market_cap, left_on='ticker', right_on='ticker')
table_vals.append(['Dollars'] + np.round(market_caps.describe()['Market Cap'].values, decimals=2).tolist())


# market cap for each transaction
market_cap['Market Cap'] = np.abs(market_cap['Market Cap'])
senate_transactions = senate_transactions.merge(market_cap, left_on='ticker', right_on='ticker')
table_vals.append(['Dollars'] + np.round(senate_transactions.describe()['Market Cap'].values, decimals=2).tolist())



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
plt.savefig('senate-table1.png', bbox_inches='tight', pad_inches=0.05)

