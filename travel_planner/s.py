from nltk.sentiment.vader import SentimentIntensityAnalyzer

from travel_planner.db.connector import Connector

connector = Connector()
senti_score = SentimentIntensityAnalyzer()

results = []

# Loop through all the tips
for tip in connector.fetch_tips():
    # When we call polarity_score on the content, we get a dictionary
    results_dict = senti_score.polarity_score(tip.content)
    # We can add two more keys to the dictionary like so
    results_dict['id'] = tip.venue_id
    results_dict['tip_id'] = tip.id

    # We don't actually need to do this but for the sake of demonstration
    results.append(results_dict)
