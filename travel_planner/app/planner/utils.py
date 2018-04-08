"""
Helper functions for travel planner
"""

import pickle
import os
import re
import string
from math import radians, cos, sin, asin, sqrt

from django.conf import settings

import gensim
import networkx as nx
import nltk
import numpy as np
import psycopg2
from gensim.matutils import cossim
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from .connector import Connector


# Helper classes copied from models
class Tip:

    def __init__(self, id, venue_id, content):
        self.id = id
        self.venue_id = venue_id
        self.content = content
    
    def __str__(self):
        return self.id


class Venue:

    def __init__(self, id, name, description, rating, lat, long, thumbnail):
        self.id = id
        self.name = name
        self.description = description
        self.rating = rating
        self.lat = lat
        self.long = long
        self.thumbnail = thumbnail
    
    def __str__(self):
        return self.name



def haversine(lng1, lat1, lng2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula 
    dlon = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def tokenize_and_clean(sentence):
    """Word tokenizer"""
    sentence = sentence.lower()

    try:
        stop = set(stopwords.words('english'))
    except:
        nltk.download('stopwords')
        stop = set(stopwords.words('english'))

    with open(os.path.join(settings.BASE_DIR, 'lda/stopwords'), 'r') as f:
        additional_stopwords = set([x.strip().lower() for x in f.readlines() if x])
    stop.update(additional_stopwords)

    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    try:
        tokenized = word_tokenize(sentence)
    except:
        nltk.download('punkt')
        tokenized = word_tokenize(sentence)

    emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
    no_emoji = [emoji_pattern.sub(r'', text) for text in tokenized]  # Remove emojis
    only_letters = [re.findall(r'\w+', l)[0] for l in no_emoji if re.findall(r'\w+', l)]
    stop_free = " ".join([i for i in only_letters if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    try:
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    except:
        nltk.download('wordnet')
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def get_topic_dist(tokenized):
    with open(os.path.join(settings.BASE_DIR, 'lda/lda.pkl'), 'rb') as f:
        lda_model = pickle.load(f)
    with open(os.path.join(settings.BASE_DIR, 'lda/dictionary.pkl'), 'rb') as f:
        dictionary = pickle.load(f)
        doc_bow = dictionary.doc2bow(tokenized.split())

    vec = lda_model[doc_bow]
    avail_topics = [x[0] for x in vec]
    to_be_added = [x for x in list(range(10)) if x not in avail_topics]
    for i in to_be_added:
        vec.append((i, 0.0))
    return sorted(vec, key=lambda x: x[0])


def get_cosine_sim(query, distributions):
    """
    Calculates cosine similarity between query and
    each of the distributions
    """
    similarities = []
    for k, dist in distributions.items():
        sim = cossim(query, dist)
        similarities.append((k, sim))
    return similarities

def get_similar_docs(query, distributions, k):
    """
    Get k most similar documents
    """
    similarities = get_cosine_sim(query, distributions)
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return similarities[:k]


def filter_venues(prefence_topic_dist, num_hours):
    # Load all topic distributions
    with open(os.path.join(settings.BASE_DIR, 'lda/distribution_dict.pkl'), 'rb') as f:
        distributions = pickle.load(f)
    # Get top N venues where N = num_hours
    most_similar_ids = get_similar_docs(prefence_topic_dist, distributions, num_hours)
    # Return list of venue IDs
    return most_similar_ids


def sort_by_sentiment(venues, start_node, with_start=False):
    # Retrieve all venue sentiments by venue id:
    # We can do so by retrieving all sentiments for the tips belong to each venue
    # and then aggregating the results and taking the average compounded sentiment
    # for each venue
    venue_avg_sent = []
    for venue in venues:
        if with_start or venue[0] != start_node.id:
            connector = Connector()
            query_stmt = """
            SELECT v.id, AVG(s.compound) as sent
                FROM sentiment s, tip t, venue v
                WHERE
                    s.tip_id=t.id AND
                    t.venue_id=v.id AND
                    v.id='%s'
                GROUP BY v.id
            """
            connector.cursor.execute(query_stmt % venue[0])
            r = connector.cursor.fetchall()
            if r:
                venue_avg_sent.append(*r)

    # Some venues don't have sentiment attached, we'll assign 0 to them
    existing_ids = [x[0] for x in venue_avg_sent]
    for venue in venues:
        if venue[0] not in existing_ids and (venue[0] != start_node.id or with_start):
            venue_avg_sent.append((venue[0], 0.0))

    # Sort the venues in descending order of average sentiment
    venue_avg_sent = sorted(venue_avg_sent, key=lambda x: x[1], reverse=True)
    # Fetch venues
    venues = []
    for venue in venue_avg_sent:
        connector = Connector()
        connector.cursor.execute("SELECT * FROM venue WHERE id='%s'" % venue[0])
        r = connector.cursor.fetchall()[0]
        v = Venue(*r)
        venues.append(v)
    # Return Venue objects
    return venues

def retrieve_start_node(venue_sent, lat, lng):
    venues = []
    for venue in venue_sent:
        connector = Connector()
        connector.cursor.execute("SELECT * FROM venue WHERE id='%s'" % venue[0])
        r = connector.cursor.fetchall()[0]
        v = Venue(*r)
        venues.append(v)

    distances = []
    for venue in venues:
        dist = haversine(lng, lat, venue.long, venue.lat)
        distances.append((venue.id, dist))
    sorted(distances, key=lambda x: x[1])
    start_node_id = distances[0][0]
    for venue in venues:
        if venue.id == start_node_id:
            start_node = venue
            break
    return start_node

def get_path(venues, start_node):
    current = start_node
    def walk(current, path=[], added_ids=[]):
        distances = []

        if current.id not in added_ids:
            path.append(current)
            added_ids.append(current.id)

        for venue in venues:
            if venue.id != current.id and venue.id not in added_ids:
                distance = haversine(current.long, current.lat, venue.long, venue.lat)
                distances.append((venue.id, venue.name, distance))

        distances = sorted(distances, key=lambda x: x[2])
        if distances:
            current_id = distances[0][0]  # next node
            for v in venues:
                if v.id == current_id:
                    current = v
                    break
        else:
            return path

        return walk(current, path, added_ids)
    
    path = walk(current)

    return path


def get_distance_dict(sorted_venues, starting_point):
    distances = {}
    for venue in sorted_venues:
        dists = {}
        for v in sorted_venues:
            if venue.id != v.id:
                dist = haversine(v.long, v.lat, venue.long, venue.lat)
                dists[v.id] = dist
            else:
                dists[v.id] = 0
        distances[venue.id] = dists
    return distances


def get_location_topic(venue_id):
    with open(os.path.join(settings.BASE_DIR, 'lda/distribution_dict.pkl'), 'rb') as f:
        distributions = pickle.load(f)
    raw_distribution = distributions[venue_id]
    distribution = {}
    for dist in raw_distribution:
        distribution[dist[0]] = dist[1]
    return distribution
