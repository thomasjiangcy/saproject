# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 19:20:51 2018

@author: Rupini Karthik
"""

from travel_planner.db.connector import Connector
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from functools import reduce
import operator
import string
import gensim
from gensim import corpora

connector = Connector()
comment = connector.fetch_venues_lda()

#Convert venue details with comments from tuple to list
comment = [list(i) for i in comment]
#Convert list of list to single list
comment = reduce(operator.concat, comment)

#Pre-processing steps for LDA 
stop = set(stopwords.words('english'))
stop.update(('none','singapore','None','one','Singapore','1st','damn','shit','since','v6','da','leh','la','meh','pte','ltd','blk','many','mr','here','wah','enough','u','5','I','n','go'))

exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in comment] 

#Creating variable dictionary of courpus, where every unique term is assigned an index
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary variable
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=50)

# Print LDA model results
print(ldamodel.print_topics(num_topics=5, num_words=20))