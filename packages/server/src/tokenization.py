import os
import logging
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string

class Tokenizer():
    def init(self):
        nltk.download('popular', download_dir='./data/nltk')


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
        tf = dict(freq_dist)
        return tf
