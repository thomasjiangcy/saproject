import re

def lda_results_to_csv(model, path, alt_path):
    raw_topics = model.print_topics(num_topics=10, num_words=20)
    topic_words = []
    topics = []
    for res in raw_topics:
        index = res[0] + 1
        eqn = res[1]
        # extract words from each part of the equation
        words = re.findall(r'\"[a-zA-Z]+\"', eqn)
        topics.append(str(index))
        topic_words.append([w.strip('"') for w in words])

    with open(alt_path, 'w') as f:
        for i, topic in enumerate(topics):
            f.write(','.join([topic, *topic_words[i]]) + '\n')

    formatted = list(zip(*topic_words))
    with open(path, 'w') as f:
        f.write(','.join(topics) + '\n')
        for row in formatted:
            f.write(','.join(row) + '\n')


def retrieve_topic_distributions(model, doc_term_matrix):
    dist = []
    print('Getting individual topic distributions')
    for matrix in doc_term_matrix:
        distribution = model.get_document_topics(matrix)
        dist.append(distribution)
    return dist
