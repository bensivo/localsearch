import os
import logging
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
from abc import ABC, abstractmethod

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str):
        """
        Tokenize a piece of text, returning a dictionary mapping tokens to token frequencies.
        """
        pass

class NaiveTokenizer(Tokenizer):
    def tokenize(self, text: str):
        """
        Naive tokenization of the given text file.
        Makes all tokens lowercase, and performs no stop-word removal.

        Args:
            text (str): Text content to tokenize
        Returns:
            dict, mapping tokens to token frequencies
        """
        # Make everything lowercase, to prevent duplicates that only differ in casing 
        text = text.lower()
        tokens = text.split()
        freq_dist = FreqDist(tokens)
        tf_dict = dict(freq_dist)
        return tf_dict


class NltkTokenizer(Tokenizer):
    def init(self):
        nltk.download('popular')
        nltk.download('stopwords')


    def tokenize(self, text: str):
        """
        Use NLTK to tokenize the given text file.
        Makes all tokens lowercase, and performs basic stop-word removal.

        Args:
            text (str): Text content to tokenize
        Returns:
            dict, mapping tokens to token frequencies
        """
        # Make everything lowercase, to prevent duplicates that only differ in casing 
        text = text.lower()

        # Set of english stop words and punctuation marks
        stop = set(stopwords.words('english') + list(string.punctuation))

        # Perform tokenization, removing stop words
        tokens = [i for i in nltk.word_tokenize(text) if i not in stop]

        freq_dist = FreqDist(tokens)
        tf_dict = dict(freq_dist)
        return tf_dict
