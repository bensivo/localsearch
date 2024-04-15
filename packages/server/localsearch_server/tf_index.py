import os
import json
from abc import ABC, abstractmethod

class TFIndex(ABC):
    """
    An inverted index for term frequencies in each document.

    Maps from each term, to the number of occurences of that term in each document
    """
    @abstractmethod
    def save_term_frequency(self, term, document_id, term_frequency):
        """
        Save the term frequency for a term in a document
        """
        pass

    @abstractmethod
    def get_term_frequency(self, term, document_id):
        """
        Get the number of times a term appears in a document
        """
        pass

    @abstractmethod
    def get_terms(self):
        """
        Return a list of all terms in the index
        """
        pass
        
    @abstractmethod
    def get_term_vector(self, document_id):
        """
        Returns a vector of term frequencies for a document, terms are returned in the same order as get_terms()
        """
        pass

class FileTFIndex(TFIndex):
    """
    Implements TFIndex using a single file on the local filesystem

    Saves term frequencies in a JSON file
        {
            "term": {
                "document_id": term_frequency,
                "document_id": term_frequency,
                ...
            },
        }
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.index = {}

    def init(self):
        if not os.path.exists(os.path.dirname(self.filepath)):
            os.makedirs(os.path.dirname(self.filepath))

        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.index = json.load(file)
        else:
            with open(self.filepath, 'w') as file:
                json.dump({}, file)

    def save_term_frequency(self, term, document_id, term_frequency):
        if term not in self.index:
            self.index[term] = {}

        self.index[term][document_id] = term_frequency

        with open(self.filepath, 'w') as file:
            json.dump(self.index, file, indent=2)

    def get_term_frequency(self, term, document_id):
        if term not in self.index:
            return 0

        if document_id not in self.index[term]:
            return 0

        return self.index[term][document_id]
    
    def get_terms(self):
        terms = list(self.index.keys())
        terms.sort()
        return terms
    
    def get_term_vector(self, document_id):
        terms = self.get_terms()
        term_vector = [self.get_term_frequency(term, document_id) for term in terms]
        return term_vector
