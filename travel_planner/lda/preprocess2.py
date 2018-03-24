import nltk
import re
import gensim

stop_list = nltk.corpus.stopwords.words('english')
# The following list is to further remove some frequent words in SGNews.
stop_list += ['would', 'said', 'say', 'year', 'day', 'also', 'first', 'last', 'one', 'two', 'people', 'told', 'new', 'could', 'singapore', 'three', 'may', 'like', 'world', 'really', 'try', 'get', 'place','since','none','singapore','None','one','Singapore','1st','damn','shit','since','v6','da','leh','la','meh','pte','ltd','blk','many','mr','here','wah','enough','u','5','I','n','go']


def load_corpus(dir):
    # dir is a directory with plain text files to load.
    corpus = nltk.corpus.PlaintextCorpusReader(dir, '.+\.txt')
    return corpus

def corpus2docs(corpus):
    # corpus is a object returned by load_corpus that represents a corpus.
    fids = corpus.fileids()
    docs1 = []
    for fid in fids:
        doc_raw = corpus.raw(fid)
        doc = nltk.word_tokenize(doc_raw)
        docs1.append(doc)
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
    return docs4

def docs2vecs(docs, dictionary):
    # docs is a list of documents returned by corpus2docs.
    # dictionary is a gensim.corpora.Dictionary object.
    vecs1 = [dictionary.doc2bow(doc) for doc in docs]
    return vecs1

    