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


for tip in tips:
    results_dict = polarity_scores(tip.content)
    results_dict['id'] = tip.venue_id
    results_dict['tip_id'] = tip.id
   
    insert_statement = """INSERT INTO sentiment (id, tip_id, compound, positive, neutral, negative) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    connectorChee = Connector()
    conn = connectorChee.connection
    with conn:
        with connectorChee.cursor as cursor:
            cursor.execute(insert_statement, tuple(v for v in results_dict.values()))
