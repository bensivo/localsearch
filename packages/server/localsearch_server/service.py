import math

import numpy as np

from localsearch_server.bm25 import BM25

class LocalsearchService:
    """
    Main application logic for the Localsearch application
    """
    def __init__(self, tokenizer, tf_index, tf_inverted_index, document_store):
        self.tokenizer = tokenizer
        self.tf_index = tf_index
        self.tf_inverted_index = tf_inverted_index
        self.document_store = document_store
        self.bm25 = None


    def insert_document(self, document_id, content):
        """
        Insert a document into the store, and index it for querying
        """
        self.document_store.insert_document(document_id, content)


    def get_document(self, document_id):
        """
        Retreive a document from the store
        """
        return self.document_store.get_document(document_id)
    
    def index(self):
        """
        Performs pre-processing on all docs that have been inserted into the document store, and initializes the BM25 ranker
        """
        total_document_length = 0

        # Tokenize all docs, insert them into indexes
        document_ids = self.document_store.list_documents()
        for document_id in self.document_store.list_documents():
            content = self.document_store.get_document(document_id)
            tf_dict = self.tokenizer.tokenize(content)
            self.tf_index.insert_document(document_id, tf_dict)
            self.tf_inverted_index.insert_document(document_id, tf_dict)

            total_document_length += sum(tf_dict.values())

        # Average document length calculation
        number_of_documents = len(document_ids)
        average_document_length = total_document_length / number_of_documents
    
        # IDF calculation for each term
        idf_dict = {}
        terms = self.tf_inverted_index.get_terms()
        for term in terms:
            document_frequency = self.tf_inverted_index.get_document_frequency(term)
            idf_dict[term] = math.log(number_of_documents / (document_frequency + 1))
        
        self.bm25 = BM25(
            avdl = average_document_length, 
            idf_dict = idf_dict,
            k=1.5,
            b=0.75
        )

    def query(self, query):
        """
        Query all inserted documents based on similarity to the given query text.
        """

        if self.bm25 is None:
            raise Exception("Index not initialized. Please call index() first.")

        document_scores = []
        query_tf_dict = self.tokenizer.tokenize(query)

        document_ids = self.document_store.list_documents()
        for document_id in document_ids:
            doc_tf_dict = self.tf_index.get_tf_dict(document_id)
            document_scores.append({
                'document_id': document_id,
                'score': self.bm25.compute_score(query_tf_dict, doc_tf_dict),
            })
        
        document_scores.sort(key=lambda x: x['score'], reverse=True)
        return document_scores[:10]


