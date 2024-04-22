import math
import numpy as np
import os
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string

documents = {}  # Raw documents

tf_index = {}  # Maps from doc_id to tf_dict
tf_inverted_index = {}  # Maps from each term to doc_ids and tfs

avg_doc_length = 0
idf_index = {}  # Maps from term to idf


def tokenize(text):
    text = text.lower() # Make everything lowercase, to prevent duplicates that only differ in casing 

    stop = set(stopwords.words('english') + list(string.punctuation)) # Set of english stop words and punctuation marks

    tokens = [i for i in nltk.word_tokenize(text) if i not in stop] # Perform tokenization, removing stop words

    freq_dist = FreqDist(tokens)
    tf_dict = dict(freq_dist)
    return tf_dict


def insert_document(doc_id, content):
    # Save raw document
    documents[doc_id] = content

    # Tokenize
    tf_dict = tokenize(content)

    # Insert tf_dict in index
    tf_index[doc_id] = tf_dict

    # Update tf_dict records into inverted index
    for term in tf_dict:
        if term not in tf_inverted_index:
            tf_inverted_index[term] = {}
        tf_inverted_index[term][doc_id] = tf_dict[term]
    
    preprocess()

def preprocess():
    global avg_doc_length

    # Pre-compute some BM25 parameters, like average document length and idf for each term
    total_doc_len = 0
    for doc_id in documents:
        tf_dict = tf_index[doc_id]
        doc_len = np.sum(np.array(list(tf_dict.values())))
        total_doc_len += doc_len

    avg_doc_length = total_doc_len / len(documents) 

    # Compute idf for each term
    for term in tf_inverted_index:
        doc_frequency = len(tf_inverted_index[term])
        idf_index[term] = math.log(len(documents) / (doc_frequency + 1))

def compute_score(query_tf_dict, doc_tf_dict):
    # Compute the intersection of the query and document terms
    # Only terms that appear in both the query and the document contribute to the score
    query_terms = set(query_tf_dict.keys())
    document_terms = set(doc_tf_dict.keys())
    common_terms = query_terms.intersection(document_terms)


    doc_len = np.sum(np.array(list(doc_tf_dict.values())))

    # Compute the BM25 score
    score = 0
    for term in common_terms:
        k = 1.5
        b = 0.75
        idf = idf_index[term]
        tf = doc_tf_dict[term]
        qf = query_tf_dict[term]
        doc_len_normalization = (1 - b + b * (doc_len / avg_doc_length))
        term_score = idf * (tf * (k+1)) / ((qf * k) / doc_len_normalization)
        score += term_score

    return score

def query(query_str):
    query_tf_dict = tokenize(query_str)

    document_scores = []

    for doc_id in documents:
        doc_tf_dict = tf_index[doc_id]
        score = compute_score(query_tf_dict, doc_tf_dict)
        document_scores.append({
            'document_id': doc_id,
            'score': score,
        })

    document_scores.sort(key=lambda x: x['score'], reverse=True)
    return document_scores


def main():
    nltk.download('popular')
    nltk.download('stopwords')

    # Insert N documents
    insert_document(1, "Hello world. It's a great day")
    insert_document(2, "Goodbye, cruel world")
    insert_document(3, "It's a great day")
    insert_document(4, "Lets not go to the beach today")
    insert_document(5, "Looking like rain today")
    insert_document(6, "Goodbye yall, I'll see you tomorrow.")

    # preprocess()

    print('documents', documents)
    print('tf_index', tf_index)
    print('tf_inverted_index', tf_inverted_index)
    print('avg_doc_length', avg_doc_length)
    print('idf_index', idf_index)


    print('great day', query("great day"))
    print('tomorrow', query("tomorrow"))
    print('world', query("world"))

if __name__ == "__main__":
    main()


# Pre-compute some BM25 parameters, like average document length and idf for each term

# Query for a given query string