# 1 - 15, 15 - 30, 30 - 45, 45 - 60, 60+

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import collections


senate_returns = pd.read_csv('senate_returns.csv')

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  

senator_list = senate_returns['senator'].unique()
# print(len(senator_list))

occurrences = collections.Counter(senate_returns['senator'].tolist())
# senator_list['num_trades'] = len(senate_returns[senate_returns['senator'] == senator_list['senator']])
# print(occurrences)

# bins = [0, 1, 5, 10, 25, 50, 100]
# print(pd.cut(senate_returns['senator'], bins=bins).value_counts())

fig = plt.figure() 
ax = fig.add_subplot(111)
col_labels = ['Senator', 'Number of Trades']
table_vals = list(occurrences.items())

# Draw table
the_table = plt.table(cellText=table_vals,
                      colWidths=[0.25] * len(col_labels),
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
plt.savefig('senator-trades.png', bbox_inches='tight', pad_inches=0.05)
