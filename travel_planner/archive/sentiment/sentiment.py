#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:08:14 2018

@author: cheehonchin
"""

import os
import random
import sys

import requests

from travel_planner.db.connector import Connector
from travel_planner.crawler.utils import make_request, crawl_comments, parse_request_error

connectorChee = Connector()
conn = connectorChee.connection
# Get a list of existing venue ids from the DB first so we won't add duplicates
tips = connectorChee.fetch_tips()
existing_tip_ids= connectorChee.fetch_tip_ids()

x=[]
for i in range(len(tips)):
    x.append(tips[i].id)
    
a=[]
for i in range(len(tips)):
    a.append(tips[i].content)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
senti_score = SentimentIntensityAnalyzer()

b=[]
for i in range(len(a)):
    b.append(senti_score.polarity_scores(a[i])["compound"])
    
c=[]
for i in range(len(a)):
    c.append(senti_score.polarity_scores(a[i])["pos"])

d=[]
for i in range(len(a)):
    d.append(senti_score.polarity_scores(a[i])["neu"])

e=[]
for i in range(len(a)):
    e.append(senti_score.polarity_scores(a[i])["neg"])
y=[]
for i in range(len(a)):
    y.append(i+1)

sentiment_dic={'id':y, 'tip_id':x, 'compound':b, 'positive':c, 'neutral':d, 'negative':e}

sentiment_list=[]
for i in range(len(y)):
    sen_dic={}
    sen_dic={'id':y[i],'tip_id':x[i],'compound':b[i],'positive':c[i],'neutral':d[i],'negative':e[i]}
    sentiment_list.append(sen_dic)   
    
# Double crawl tips
# This is mainly a workaround for an initial mistake in crawling tips
#_DOUBLE_CRAWL_TIPS = '<boolean>'
#DOUBLE_CRAWL_TIPS = _DOUBLE_CRAWL_TIPS == 'True'

insert_statement = """INSERT INTO sentiment (id, tip_id, compound, positive, neutral, negative) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
connectorChee = Connector()
conn = connectorChee.connection
with conn:
    with connectorChee.cursor as cursor:
        cursor.execute(insert_statement, tuple(v for v in sentiment_list.values()))
                        
