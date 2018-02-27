import os
import random
import sys

import requests

from travel_planner.db.connector import Connector
from travel_planner.crawler.utils import make_request


# Secrets
FS_ID = os.getenv('FS_ID')
FS_KEY = os.getenv('FS_KEY')

if FS_ID is None or FS_KEY is None:
    raise ValueError('Please set environment variables: FS_ID, FS_KEY')

# Some useful constants
EXPLORE_API = 'https://api.foursquare.com/v2/venues/explore'
VENUES_API = 'https://api.foursquare.com/v2/venues/{venue_id}'
TIPS_API = 'https://api.foursquare.com/v2/venues/{venue_id}/tips'

connector = Connector()
conn = connector.connection
# Get a list of existing venue ids from the DB first so we won't add duplicates
existing_venue_ids = connector.fetch_venue_ids()

# Get list of venues via Explore API (max 50 results each time)
# Params
# ------
# lat, lng = 1.290270, 103.851959
# radius = 27,000m (Singapore is 50km East-West and 27km North-South)
print('Fetching up to 50 venues in Singapore...')

explore_params = dict(
    client_id=FS_ID,
    client_secret=FS_KEY,
    v=20180227,
    ll='1.290270, 103.851959',
    radius=27000,
    limit=50
)
res = make_request(requests.get, EXPLORE_API, explore_params)
if res.status_code != 200:
    # If response status code was anything other than
    # 200 OK, e.g. if it was 429 Too Many Requests
    # then we want to display the message and exit gracefully
    print(res.text)
    sys.exit(1)
results = res.json()
total_num = results['response']['totalResults']

print('Total venues retrieved: ', total_num)

print('Going through %d venues...' % total_num)

i = 0
venue_ids = set()

# Retrieve more venue ids
while i < total_num:
    if i > 0:
        print('Current offset for venue results: ', i)
        explore_params['offset'] = i
        res = make_request(requests.get, EXPLORE_API, explore_params)
        if res.status_code != 200:
            # If response status code was anything other than
            # 200 OK, e.g. if it was 429 Too Many Requests
            # then we want to display the message and exit gracefully
            print(res.text)
            sys.exit(1)
        results = res.json()
        if results.get('response') is not None:
            if results['response'].get('groups') is not None:
                for r in results['response']['groups'][0]['items']:
                    if r['venue']['id'] not in venue_ids:
                        venue_ids.add(r['venue']['id'])  # Only add unique venue_ids
    i += 50

# For each venue id, if it is not in existing_venue_ids,
# then retrieve the venue's details and add to DB
venue_params = dict(
    client_id=FS_ID,
    client_secret=FS_KEY,
    v=20180227
)

successfully_added = set()

print('Collecting details for each venue...')
for vid in venue_ids:
    if vid not in existing_venue_ids:
        print('Retrieving details for ', vid)
        res = make_request(requests.get, VENUES_API.format(venue_id=vid), venue_params)
        if res.status_code != 200:
            # If response status code was anything other than
            # 200 OK, e.g. if it was 429 Too Many Requests
            # then we want to display the message and exit gracefully
            print(res.text)
            sys.exit(1)
        results = res.json()
        if results.get('response') is not None:
            if results['response'].get('venue') is not None:
                # Handle potentially empty fields
                description = 'None'
                if results['response']['venue'].get('page') is not None:
                    if results['response']['venue']['page'].get('pageInfo') is not None:
                        if results['response']['venue']['page']['pageInfo'].get('description') is not None:
                            description = results['response']['venue']['page']['pageInfo']['description']
                
                thumbnail = 'None'
                if results['response']['venue']['photos'].get('groups') is not None:
                    photos = results['response']['venue']['photos']['groups'][0]['items']
                    # Get a random photo
                    index = random.randint(0, (len(photos) -1))
                    photo_prefix = photos[index]['prefix']
                    if photo_prefix.endswith('/'):
                        photo_prefix = photo_prefix[:-1]
                    photo_suffix = photos[index]['suffix']
                    photo_url = photo_prefix + photo_suffix

                venue_dict = {
                    'id': results['response']['venue']['id'],
                    'name': results['response']['venue']['name'],
                    'description': description,
                    'rating': results['response']['venue']['rating'],
                    'lat': results['response']['venue']['location']['lat'],
                    'long': results['response']['venue']['location']['lng'],
                    'thumbnail': photo_url
                }

                # Insert row into table
                insert_statement = """INSERT INTO venue (id, name, description, rating, lat, long, thumbnail) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
                connector = Connector()
                conn = connector.connection
                with conn:
                    with connector.cursor as cursor:
                        cursor.execute(insert_statement, tuple(v for v in venue_dict.values()))
                        print('Inserted into table, venue ID: ', vid)
                        if vid not in successfully_added:
                            successfully_added.add(vid)
    else:
        print('Venue already in database: ', vid)

# Now we want to retrieve tips for each venue that was successfully added
tips_params = dict(
    client_id=FS_ID,
    client_secret=FS_KEY,
    v=20180227,
    limit=500
)

successfully_added_tips = set()

for venue in successfully_added:
    res = make_request(requests.get, TIPS_API.format(venue_id=venue), params=tips_params)
    results = res.json()
    total_tips_count = results['response']['tips']['count']

    n = 0
    while n < total_tips_count:
        if n > 0:
            print('Current offset for tips results: ', n)
            tips_params['offset'] = n
            res = make_request(requests.get, TIPS_API.format(venue_id=venue), tips_params)
            if res.status_code != 200:
                # If response status code was anything other than
                # 200 OK, e.g. if it was 429 Too Many Requests
                # then we want to display the message and exit gracefully
                print(res.text)
                sys.exit(1)
            results = res.json()
            if results.get('response') is not None:
                if results['response'].get('items') is not None:
                    for r in results['response']['items']:
                        tip_dict = {
                            'id': r['id'],
                            'venue_id': venue,
                            'tip': r['text']
                        }
                        insert_statement = """INSERT INTO tip (id, venue_id, tip) VALUES (%s, %s, %s)"""
                        connector = Connector()
                        conn = connector.connection
                        with conn:
                            with connector.cursor as cursor:
                                cursor.execute(insert_statement, tuple(v for v in tip_dict.values()))
                                print('Inserted into table, comment ID: ', r['id'])
                                if r['id'] not in successfully_added_tips:
                                    successfully_added_tips.add(r['id'])
        i += 500

print('Crawl complete.')
print('Total venues crawled: ', len(successfully_added))
print('Total tips crawled: ', len(successfully_added_tips))
