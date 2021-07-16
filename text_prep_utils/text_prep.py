#Load the libraries
import numpy as np
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
import spacy
import re, string, unicodedata
from tqdm import tqdm 
from spacy.lang.en.stop_words import STOP_WORDS
import os

class Text_processing_pipeline():

    try:
        nlp = spacy.load('en_core_web_trf') # spacy model
    except:
        raise ValueError('spaCy en_core_web_trf model not found.')

    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load('en_core_web_trf') # spacy model
        self.tokens = None
        self.rm_tokens = None
        self.rm_text = None

    # Removing the html strips
    def strip_html(self):
        soup = BeautifulSoup(self.text, "html.parser")
        self.text = soup.get_text().lower()
        return self

    def text_preprocessor(self, remove_stopwords=True):
        """
        - Lowercase the sentence
        - Change 'm to 'am'
        - Change "'t" to "not"
        - Remove "@name"
        - Isolate and remove punctuations except "?"
        - Remove other special characters
        - Remove stop words
        - Remove trailing whitespace
        - Remove emojis
        """
        s = self.text

        emoji_clean= re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)

        # Change 'm to 'am'
        s = re.sub(r"\'m", "am", s)
        # Change 't to 'not'
        s = re.sub(r"\'t", " not", s)
        # Remove @name
        s = re.sub(r'(@.*?)[\s]', ' ', s)
        # Isolate and remove punctuations except '?'
        s = re.sub(r'([\'\"\.\(\)\!\?\\\/\,])', r' \1 ', s)
        s = re.sub(r'[^\w\s\?]', ' ', s)
        # Removing the square brackets
        s = re.sub('\[[^]]*\]', '', s)
        # Remove some special characters
        s = re.sub(r'([\;\:\|•«\n])', ' ', s)
        s = re.sub(r'[^a-zA-z0-9\s]','',s)
        # Remove trailing whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        # Remove emojis
        s = emoji_clean.sub(r'',s)

        self.tokens = [str(t) for t in self.nlp(s)]

        if remove_stopwords:
            self.rm_tokens = [w for w in self.tokens if w not in STOP_WORDS]
            self.rm_text = " ".join([t for t in self.rm_tokens])
        else:
            pass

        return self
        
    # Stemming the text
    def simple_stemmer(self):
        ps = nltk.porter.PorterStemmer()
        self.text= ' '.join([ps.stem(word) for word in self.text.split()])
        return self

    @staticmethod
    def lemmatize(text, nlp):
        return (" ".join([w.lemma_ for w in nlp(text)]))

    def main_pipeline(self):
        return self.lemmatize(self.strip_html().text_preprocessor().get_rm_text(), self.nlp)

    def get_text(self):
        return self.text

    def get_tokens(self):
        return self.tokens

    def get_rm_text(self):
        return self.rm_text

    def __repr__(self):
        return f"text_processing_pipeline([text = '{self.text}'])"