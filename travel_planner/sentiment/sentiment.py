from nltk.sentiment.vader import SentimentIntensityAnalyzer

from travel_planner.db.connector import Connector

connector = Connector()
senti_score = SentimentIntensityAnalyzer()

print('Running through all tips...')

# Loop through all the tips
for tip in connector.fetch_tips():
    print('Calculating polarity scores for Tip {}...'.format(tip.id))
    # When we call polarity_score on the content, we get a dictionary
    results_dict = senti_score.polarity_scores(tip.content)
    # We can add two more keys to the dictionary like so
    results_dict['id'] = tip.venue_id
    results_dict['tip_id'] = tip.id
    print('Results for Tip {}'.format(tip.id))
    print('Compound: {}\tPositive: {}\tNeutral: {}\tNegative: {}\t'.format(
        results_dict['compound'],
        results_dict['pos'],
        results_dict['neu'],
        results_dict['neg'],
    ))
    print('Inserting results into DB...')
    insert_statement = """INSERT INTO sentiment (id, tip_id, compound, positive, neutral, negative) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    connector = Connector()
    conn = connector.connection
    try:
        with conn:
            with connector.cursor as cursor:
                cursor.execute(insert_statement, tuple(v for v in results_dict.values()))
                print('Successfully inserted Tip {} into DB'.format(tip.id))
    except Exception as err:
        print('Something went wrong with inserting into DB: {}'.format(err))
