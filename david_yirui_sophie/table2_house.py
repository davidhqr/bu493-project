# 1 - 15, 15 - 30, 30 - 45, 45 - 60, 60+

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import collections


house_returns = pd.read_csv('house_returns.csv')

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  

house_list = house_returns['representative'].unique()

occurrences = collections.Counter(house_returns['representative'].tolist())
house = pd.DataFrame.from_dict(occurrences, orient='index', columns=['num_trades'])

bins = [0, 20, 40, 60, 80, 100, float('inf')]
binned = pd.cut(house['num_trades'], bins=bins)

ax = binned.value_counts(sort=False).plot.bar(rot=0, color="b", figsize=(8,4))
ax.set_xticklabels([str(c) for c in binned.cat.categories])
plt.title('Number of Trades for House of Representatives in 2020')
plt.xlabel('Number of Trades')
plt.ylabel('Number of Representatives')
plt.savefig('house-trades.png', bbox_inches='tight', pad_inches=0.05)
