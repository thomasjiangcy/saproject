# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 19:20:51 2018

@author: Rupini Karthik
"""

import os
import pickle
import re
import string

import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from travel_planner.db.connector import Connector
from travel_planner.lda.utils import lda_results_to_csv, retrieve_topic_distributions
from travel_planner.models import Venue

CURRENT_DIR = os.path.dirname(__file__)

proceed = input('Build LDA model to overwrite existing model? [y/n]')
proceed = True if proceed == 'y' else False

if os.path.isfile(os.path.join(CURRENT_DIR, 'lda.model')) and not proceed:
    print('LDA model exists, loading it into memory...')
    with open(os.path.join(CURRENT_DIR, 'lda.pkl'), 'rb') as f:
        ldamodel = pickle.load(f)
else:
    connector = Connector()
    documents = []

    # Fetch venues in a stream
    print('Fetching venue data...')
    connector.cursor.execute('SELECT * FROM venue;')
    for v in connector.cursor:
        venue = Venue(*v)
        print('Fetching all comments for venue: ', venue.name)
        # Fetch all the comments for this venue
        conn = Connector()
        conn.cursor.execute("SELECT content FROM tip WHERE venue_id='%s'" % venue.id)
        comments = [comment[0] for comment in conn.cursor]
        print('Number of comments for venue %s: %s' % (venue.name, str(len(comments))))
        doc = ' '.join([venue.name, venue.description, *comments])
        documents.append(doc)

    print('Setting up stopwords...')
    #Pre-processing steps for LDA 
    stop = set(stopwords.words('english'))
    with open(os.path.join(CURRENT_DIR, 'stopwords'), 'r') as f:
        additional_stopwords = set([x.strip().lower() for x in f.readlines() if x])
    stop.update(additional_stopwords)

    print('Setting up lemmatizer')
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    def clean(doc):
        tokenized = word_tokenize(doc.lower())
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
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        print(normalized)
        return normalized

    print('Clean documents...')
    doc_clean = [clean(doc).split() for doc in documents] 

    print('Create dictionary of corpus...')
    #Creating variable dictionary of courpus, where every unique term is assigned an index
    dictionary = corpora.Dictionary(doc_clean)

    print('Processing document to bag of words...')
    # Converting list of documents (corpus) into Document Term Matrix using dictionary variable
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    print('Training LDA model...')
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=10, id2word=dictionary, passes=50)
    print('LDA model complete.')
    print('Pickling LDA model...')
    # Save model
    with open(os.path.join(CURRENT_DIR, 'lda.pkl'), 'wb') as f:
        pickle.dump(ldamodel, f, protocol=pickle.HIGHEST_PROTOCOL)
    print('Pickling complete')

# Print LDA model results
print(ldamodel.print_topics(num_topics=10, num_words=20))

# Output results into CSV
OUTPUT_PATH = os.path.join(CURRENT_DIR, 'topics.csv')
ALT_PATH = os.path.join(CURRENT_DIR, 'topics_by_line.csv')
lda_results_to_csv(ldamodel, OUTPUT_PATH, ALT_PATH)

# Get topic distributions of each venue
distributions = retrieve_topic_distributions(ldamodel, doc_term_matrix)

with open(os.path.join(CURRENT_DIR, 'distribution.pkl'), 'wb') as f:
    pickle.dump(distributions, f, protocol=pickle.HIGHEST_PROTOCOL)
