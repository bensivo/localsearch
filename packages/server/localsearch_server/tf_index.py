import os
import json
import numpy as np
from abc import ABC, abstractmethod

class TFIndex(ABC):
    """
    Stores tf_dict for each document
    """

    @abstractmethod
    def insert_document(self, document_id, tf_dict):
        """
        Insert term frequencies for a document
        """
        pass

    @abstractmethod
    def get_tf_dict(self, document_id):
        """
        Insert term frequencies for a document
        """
        pass

class InMemoryTFIndex(TFIndex):
    """
    Implementation of TFIndex using a simple in-memory dict
    """
    def __init__(self):
        self.index = {}
    
    def insert_document(self, document_id, tf_dict):
        self.index[document_id] = tf_dict
    
    def get_tf_dict(self, document_id):
        return self.index[document_id]

# class FileTFIndex(TFIndex):
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

#     def insert_document(self, document_id, tf_dict):
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
    