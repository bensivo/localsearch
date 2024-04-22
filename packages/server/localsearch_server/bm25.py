import numpy as np
import math

class BM25:
    """
    Implementation of the BM25 ranking function.
    """
    def __init__(self, tf_index, tf_inverted_index, document_store, k=1.5, b=0.75):
        self.tf_index = tf_index
        self.tf_inverted_index = tf_inverted_index
        self.document_store = document_store

        self.k = k
        self.b = b

        self.avg_doc_length = 0
        self.idf_index = {}
    
    def preprocess(self):
        """
        Compute precomputed parameters used in querying:
            - average document length
            - term idf (for each term)
        """

        # Compute average document length
        total_doc_len = 0
        doc_ids = self.document_store.list_documents()
        for doc_id in doc_ids:
            tf_dict = self.tf_index.get_tf_dict(doc_id)
            doc_len = np.sum(list(tf_dict.values()))
            total_doc_len += doc_len
        self.avg_doc_length = total_doc_len / len(doc_ids) 
    
        # Compute idf for each term
        terms = self.tf_inverted_index.list_terms()
        for term in terms:
            document_frequency = len(self.tf_inverted_index.get_document_tfs(term))
            self.idf_index[term] = math.log(len(doc_ids) / (document_frequency + 1))
        
    
    def compute_score(self, query_tf_dict, document_tf_dict):
        """
        Compute the BM25 score for a given query and document.
        """

        # Compute the intersection of the query and document terms
        # Only terms that appear in both the query and the document contribute to the score
        query_terms = set(query_tf_dict.keys())
        document_terms = set(document_tf_dict.keys())
        common_terms = query_terms.intersection(document_terms)

        # Compute the BM25 score
        score = 0
        for term in common_terms:
            k = self.k
            b = self.b
            idf = self.idf_index[term]
            tf = document_tf_dict[term]
            qf = query_tf_dict[term]
            doc_len_normalization = (1 - b + b * (len(document_terms) / self.avg_doc_length))
            term_score = idf * (tf * (k+1)) / ((qf * k) / doc_len_normalization)
            score += term_score

        return score