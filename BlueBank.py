#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:08:30 2022

@author: carlmagnusson
"""

import pandas as pd
import json as json
import numpy as np
import matplotlib.pyplot as plt

# Does this work? Yes. 
#data = pd.read_json('loan_data_json.json')

# Method 1 to read json data in python
#json_file = open('loan_data_json.json')
#data = json.load(json_file)

# Method 2 to read json data in python 
with open('loan_data_json.json') as json_file: 
    data = json.load(json_file)

# transforming data into a dataframe
loandata = pd.DataFrame(data)

# List unique values in a dataframe
loandata.info()

loandata['purpose'].unique()

#Describing the data
# .describe returns a dataframe containing: count, mean, std, min, 25%, 50%, 75% percentiles and max value.
loandata.describe()

# You can get this information on specific columns as well. 
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#Converting log.annual.inc to the actual annual income in dollars.
# This is done using the exp function in the numpy library. 
#income = np.exp(loandata['log.annual.inc'])
loandata['annualincome']  = np.exp(loandata['log.annual.inc'])

length = len(loandata)
ficocat = []

for x in range(0,length): 
    fico = loandata['fico'][x]
    try:
        if fico >= 300 and fico < 400:
            ficocategory = 'Very poor'
        elif fico >= 400 and fico < 600:
            ficocategory = 'Poor'
        elif fico >= 600 and fico < 660:
            ficocategory = 'Fair'
        elif fico >= 660 and fico < 700:
            ficocategory = 'Good'
        elif fico >= 700:
            ficocategory = 'Excellent'
        else:
            ficocategory = 'Unknown'
    except:
        ficocategory = 'Error - Unknown'
    ficocat.append(ficocategory)

ficocat = pd.Series(ficocat)

loandata['fico.category'] = ficocat

# df.log as conditional statements
# df.loc[df[columnname] condition, newcolumnname] = 'value if condition is met

#for interest rates, a new column is wanted. If rate>0.12 then high, else low

loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

# number of loans/rows by fico.category
catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar(color = 'green', width = 0.1)
plt.show()


purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color = 'red', width = 0.2)
plt.show()


#Scatter plots
ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint,ypoint, color = '#fcba03')
plt.show()


#writing to csv
loandata.to_csv('loandata_cleaned.csv', index = True)

