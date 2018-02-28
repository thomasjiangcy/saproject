import requests
import sys

def make_request(req, uri, params, data=None):
    try:
        if data is None:
            res = req(uri, params=params, timeout=10)
        else:
            res = req(uri, data=data, params=params, timeout=10)
        return res
    except:
        print("Something went wrong while making request to ", uri)
        sys.exit(1)


def crawl_comments(TIPS_API, venue, tips_params, Connector):
    res = make_request(requests.get, TIPS_API.format(venue_id=venue), params=tips_params)
    results = res.json()
    total_tips_count = results['response']['tips']['count']

    print('Total tips for %s: %s'% (venue, str(total_tips_count)))

    n = 0
    while n < total_tips_count:
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
            if results['response'].get('tips') is not None:
                if results['response']['tips'].get('items') is not None:
                    for r in results['response']['tips']['items']:
                        tip_dict = {
                            'id': r['id'],
                            'venue_id': venue,
                            'tip': r['text']
                        }

                        # If it doesn't exist, insert
                        try:
                            insert_statement = """INSERT INTO tip (id, venue_id, content) VALUES (%s, %s, %s)"""
                            connector = Connector()
                            conn = connector.connection
                            with conn:
                                with connector.cursor as cursor:
                                    cursor.execute(insert_statement, tuple(v for v in tip_dict.values()))
                                    print('Inserted into table, comment ID: ', r['id'])
                        except:
                            print('Tip ID %s already exists.' % r['id'])
        n += 500
