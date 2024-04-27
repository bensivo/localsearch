import numpy as np
import math

class BM25:
    """
    Implementation of the BM25 ranking function.
    """
    def __init__(self, avdl, idf_dict, k=1.5, b=0.75):
        self.avdl = avdl
        self.idf_dict = idf_dict
        self.k = k
        self.b = b
    
    def compute_score(self, query_tf_dict, document_tf_dict):
        """
        Compute the BM25 score for a given query and document.
        """

        # Compute the intersection of the query and document terms
        # Only terms that appear in both the query and the document contribute to the score
        query_terms = set(query_tf_dict.keys())
        document_terms = set(document_tf_dict.keys())
        common_terms = query_terms.intersection(document_terms)

        document_length = sum(document_tf_dict.values())

        # Compute the BM25 score
        score = 0.0
        for term in common_terms:
            idf = self.idf_dict[term]
            tf = document_tf_dict[term]
            qf = query_tf_dict[term]
            doc_len_normalization = (1 - self.b + self.b * (document_length / self.avdl))
            term_score = idf * (tf * (self.k+1)) / ((qf * self.k) / doc_len_normalization)
            score += term_score

        return score