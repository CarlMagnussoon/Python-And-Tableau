#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:24:42 2022

@author: carlmagnusson
"""

import pandas as pd

#file_name = pd.read_csv('file.csv') format for importing csv-files using panda

# read_csv, expects ',' as a separator. 
# However, transaction.csv has ; as a separator
# To get around it, send i sep = ';' as a parameter for the read_csv function.
# every row in transaction.csv, represents a salestransaction.
data = pd.read_csv('transaction.csv', sep = ';') 

# Summary of the data
data.info()

# Playing around with variables
#var = 'Hello World'                             #String
#var = 9                                         #Int
#var = 2.5                                       #Float
#var = ['apple','pear', 'banana']                #List
#var = ('apple','pear', 'banana')                #Tuple, like List can't change the values 
#var = range(10)                                 #Number range 0-10
#var = {'name': 'Carl', 'Location': 'Sweden'}    #Dict, similar to JSON. Key-value pairs
#var = {'apple', 'pear', 'banana'}               #Set, like List but you can't change values
#var = True                                      #Boolean, either true = 1 or False = 0


# Want to apply the above to the column values in data
# CostPerTransaction Column Calculation 
# CostPerTransaction = CostPerItem = NumberOfItemsPurchased

# How to single out a column: variable = dataframe['column_name']
# This creates a series variable. 
# So we do that for CostPerItem and NumberOfItemsPurchased, when multiplying these, we get a third series variable. 
CostPerItem = data['CostPerItem']
NumberOfItemsPurchased = data['NumberOfItemsPurchased']
CostPertransaction = CostPerItem * NumberOfItemsPurchased

# To insert this into the dataframe we do the following: 
data['CostPerTransaction'] = CostPertransaction

# Do the same for SellingPricePerTransaction
SellingPricePerItem = data['SellingPricePerItem']
SellingPricePerTransaction = SellingPricePerItem * NumberOfItemsPurchased
data['SellingPricePerTransaction'] = SellingPricePerTransaction

# ProfitPerTransaction = Sales - Costs
data['ProfitPerTransaction'] = data['SellingPricePerTransaction'] - data['CostPerTransaction']

#Markup = Profit/Costs
data['Markup'] = data['ProfitPerTransaction']/data['CostPerTransaction']

# Rounded to 2 decimals
data['Markup'] = round(data['Markup'], 2)

# Create one column Date instead of year, month and day 

#Checking data types of columns
#print(data['Day'].dtype)

# Changing columns data type
day = data['Day'].astype(str)
month = data['Month'].astype(str)
year = data['Year'].astype(str)

data['date'] = day +'-'+month+'-'+year

# Using iloc to view specific columns/rows. iloc is a part of the pandas library
# Pulls out the row corresponding to the index inside the square brackets
data.iloc[0] # First row
data.iloc[0:3] # First four rows
data.iloc[-5:] # Last 5 rows

data.head(5) # First 5 rows, not using pandas. 

data.iloc[:,2] # All rows but only third column
data.iloc[4,2] # Fifth row and third column


#   Separating strings. Separate the ClientKeyWords into 3 separe columns. 
# Use split accordingly: new_var = column.str.split('sep', expand = True)

split_col = data['ClientKeywords'].str.split(', ', expand = True)

# Creating new columns in data from the split_cols retrieved from the ClientKeyWords column in data
data['ClientAge'] = split_col[0]
data['ClientType'] = split_col[1]
data['LengthOfContract'] = split_col[2]

# Removing characters using replace function.
data['ClientAge'] = data['ClientAge'].str.replace('[', '')
data['LengthOfContract'] = data['LengthOfContract'].str.replace(']', '')

# Using lower-function to change item column to lowercase
data['ItemDescription'] = data['ItemDescription'].str.lower()

# Joining seasonal data (another data set) to our main dataframe
# Start by reading the file.
seasons = pd.read_csv('value_inc_seasons.csv', ';')

# Now we're going to join the seasons on the months in the data dataframe. 
# Merging files: merge_df = pd.merge(df_old, df_new, on = 'key')
# This seems to rearrange the rows
data = pd.merge(data, seasons, on = 'Month')

# Dropping unused columns, such as day, month, year and clientkeywords
# df = df.drop['columnname', axis = 1]

data = data.drop('ClientKeywords', axis = 1)
data = data.drop('Day', axis = 1)

# You can drop multiple columns at once. See below
data = data.drop(['Month', 'Year'], axis = 1)

# Exporting the dataframe as a csv-file
# index = False means we'll not export the index in the dataframe.
data.to_csv('ValueInc_Cleaned.csv', index = False)


