#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:22:21 2022

@author: carlmagnusson
"""

import pandas as pd 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Reading Excel-files into dataframe
data = pd.read_excel('articles.xlsx')
sources = pd.read_excel('BlogMe_Sources.xlsx')

#Summary of the data
data.info()
data.describe()

#counting the number of articles per source
#format of groupby: df.groupby(['column_to_group_by'])['column_to_count'].count()

data.groupby(['source_id'])['article_id'].count()

#Number of reactions per publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping column engagement_comment_plugin_count
data = data.drop('engagement_comment_plugin_count', axis=1)

#Function, loop through the dataframe. Check the title if it contains the word "crash" if it does, add a value to a new column 
#Creating a keyword flag
#keyword = 'crash'


#let first create a for-loop to isolate each title row
def keyWordAnalysisFunction(keyword): 
    length = len(data)
    keyword_flag = []
    
    for x in range(0, length): 
        heading = data['title'][x]
        try:
            if keyword in heading: 
                flag = 1
            else: 
                flag = 0
        except: 
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

k = keyWordAnalysisFunction("murder")

#Creating a new column in data
data['keyword_flag'] = pd.Series(k)


#Using VADER as a sentiment analysis tool. 
#SentimentIntensityAnalyzer


# text  = data['title'][16]
# sent = sent_int.polarity_scores(text)

title_pos_sentiment =[]
title_neg_sentiment =[]
title_neu_sentiment =[]
sent_int = SentimentIntensityAnalyzer()
length = len(data)

for x in range(0, length):
    #Utför sentiment analys på texten
    try: 
        # Hämtar datan i title-kolumnen för rad x
        text = data['title'][x]
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except: 
        neg = 0
        pos = 0
        neu = 0
    #Sparar dict-väderna i variabler. 
    title_pos_sentiment.append(pos)
    title_neg_sentiment.append(neg)
    title_neu_sentiment.append(neu)
    

data['title_neg_sentiment'] = pd.Series(title_neg_sentiment)
data['title_pos_sentiment'] = pd.Series(title_pos_sentiment)
data['title_neu_sentiment'] = pd.Series(title_neu_sentiment)

data.to_excel('blogme_clean.xlsx', sheet_name='blogme_data', index =False)
