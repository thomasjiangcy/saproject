# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:26:17 2018

@author: Rupini Karthik
"""

from travel_planner.db.connector import Connector
import gensim
import preprocess2

connector = Connector()
comment = connector.fetch_venues()

# To retrieve and combine venue name, description, and tips from venue and tip table
for i in range(len(comment)):
     tip_content = "SELECT b.content From tip b where b.venue_id ='" +  comment[i][0] +"';"
     name = comment[i][1]
     desc = comment[i][2]
     connector_lda = Connector()
     conn = connector_lda.connection
     with conn:
         with connector_lda.cursor as cursor:
             cursor.execute(tip_content)
             tip_fetch = cursor.fetchall()
             
# To write venue name, description, and tip in a single document
     tf = comment[i][0]+".txt"
     ftips=open(tf,'w',encoding="utf-8")
     ftips.write('%s\t%s\t%s\t' %(name,desc,tip_fetch))
     ftips.close()
     
# Retrieve venue documents from a given folder and perform pre-processing using a user-package    
sg_corpus = preprocess2.load_corpus('E:\SMU MITB\Term 2\Social Analytics\Project_LDA\saproject\LDA docs')
sg_docs = preprocess2.corpus2docs(sg_corpus)

#Creating variable dictionary of courpus, where every unique term is assigned an index
sg_dictionary = gensim.corpora.Dictionary(sg_docs)

#Converting list of documents (corpus) into Document Term Matrix using dictionary variable
sg_vecs = preprocess2.docs2vecs(sg_docs, sg_dictionary)

# Creating the object for LDA model using gensim library
sg_lda = gensim.models.ldamodel.LdaModel(corpus=sg_vecs, id2word=sg_dictionary, num_topics=30)

# Print LDA model results
topics = sg_lda.show_topics(30, 25)
for i in range(0, 30):
    print(topics[i])

# To trace-back venue with topics
fids = sg_corpus.fileids()
index_of_file=fids.index('4b0bd124f964a520e03323e3.txt')
print("file_index:",index_of_file)
vec = sg_vecs[index_of_file]
vec_lda=sg_lda[vec]
print("topic distribution:",vec_lda)