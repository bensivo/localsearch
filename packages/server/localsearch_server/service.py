import numpy as np

class LocalsearchService:
    def __init__(self, tokenizer, tf_index, tf_inverted_index, document_store, bm25):
        self.tokenizer = tokenizer
        self.tf_index = tf_index
        self.tf_inverted_index = tf_inverted_index
        self.document_store = document_store
        self.bm25 = bm25


    def insert_document(self, document_id, content):
        """
        Insert a document into the store, and index it for querying
        """
        self.document_store.insert_document(document_id, content)

        tf_dict = self.tokenizer.tokenize(content)

        self.tf_index.insert_tf_dict(document_id, tf_dict)
        self.tf_inverted_index.insert_tf_dict(document_id, tf_dict)

        self.bm25.preprocess()
        

    def get_document(self, document_id):
        """
        tf_vectorRetreive a document from the store
        """
        return self.document_store.get_document(document_id)


    def query(self, query):
        """
        Query all inserted documents based on similarity to the given query text.
        """
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
        
        return document_scores


