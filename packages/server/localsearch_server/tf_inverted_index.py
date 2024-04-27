import os
import json
import numpy as np
from abc import ABC, abstractmethod

class TFInvertedIndex(ABC):
    """
    Inverted index of document term frequencies. 
    
    Contains 2 separate data-structures:
        - document_frequencies: Maps from a term, to the number of docs that contain that term
        - postings: Maps from a term, to a list of (document_id, term_frequency) tuples

    Reading: https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-an-inverted-index-1.html
    """

    @abstractmethod
    def insert_document(self, document_id, tf_dict):
        """
        Insert term frequencies for a document
        """
        pass

    @abstractmethod
    def get_terms(self):
        """
        Return all terms
        """
        pass

    @abstractmethod
    def get_document_frequency(self, term):
        """
        Returns documents containing this term, and the frequency of the term in each document
        """
        pass

    @abstractmethod
    def get_postings(self, term):
        """
        Returns documents containing this term, and the frequency of the term in each document
        """
        pass


class InMemoryTFInvertedIndex(TFInvertedIndex):
    """
    Implementation of TFInvertedIndex using in-memory data structures
    """
    def __init__(self):
        self.document_frequencies = {}
        self.postings = {}

    def insert_document(self, document_id, tf_dict):
        for term in tf_dict:
            if term not in self.document_frequencies:
                self.document_frequencies[term] = 0
            self.document_frequencies[term] += 1

            if term not in self.postings:
                self.postings[term] = []
            self.postings[term].append((document_id, tf_dict[term]))

    def get_terms(self):
        return list(self.document_frequencies.keys())
    
    def get_document_frequency(self, term):
        return self.document_frequencies[term]
    
    def get_postings(self, term):
        return self.postings[term]

# class FileTFIndex(TFInvertedIndex):
#     """
#     Implements TFIndex using a single file on the local filesystem

#     Saves term frequencies in a JSON file
#         {
#             "term": {
#                 "document_id": term_frequency,
#                 "document_id": term_frequency,
#                 ...
#             },
#         }
#     """

#     def __init__(self, filepath):
#         self.filepath = filepath
#         self.index = {}

#     def init(self):
#         if not os.path.exists(os.path.dirname(self.filepath)):
#             os.makedirs(os.path.dirname(self.filepath))

#         if os.path.exists(self.filepath):
#             with open(self.filepath, 'r') as file:
#                 self.index = json.load(file)
#         else:
#             with open(self.filepath, 'w') as file:
#                 json.dump({}, file)

#     def insert_document_document(self, document_id, tf_dict):
#         for term, term_frequency in tf_dict.items():
#             if term not in self.index:
#                 self.index[term] = {}

#             self.index[term][document_id] = term_frequency

#             with open(self.filepath, 'w') as file:
#                 json.dump(self.index, file, indent=2)
    
#     def get_tf_dict(self, document_id):
#         terms = self.get_terms()
#         tf_dict = {}
#         for term in terms:
#             tf_dict[term] = self.get_term_frequency(term, document_id)
#         return tf_dict


#     def get_term_documents(self, term):
#         if term not in self.index:
#             return []

#         return self.index[term].keys()

#     def get_term_frequency(self, term, document_id):
#         if term not in self.index:
#             return 0

#         if document_id not in self.index[term]:
#             return 0

#         return self.index[term][document_id]
    
#     def get_terms(self):
#         terms = list(self.index.keys())
#         terms.sort()
#         return terms
    