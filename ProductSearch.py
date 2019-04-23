import pandas as pd
import re
import numpy as np
import random
# pip install nltk
import nltk
#nltk.download('vader_lexicon')

import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import datetime, time
from PorterStemmer import PorterStemmer

class Index_Product(object):
    def __init__(self):
        self._inverted_index = {}

        self._documents = []
        self.products = []

    def index_dir(self, data, exist):
        num_files_indexed = 0
        all_product = data['name'].unique()
        for files in range(len(all_product)): 
            all_tokens = []
            self._documents.append(files) 
            text = all_product[files]
            self.products.append(text)
            if exist == False:
                all_tokens = all_tokens + self.stemming(self.tokenize(text))
                #print('1')
                all_tokens = list(set(all_tokens))
                for word in all_tokens:
                    try:
                        self._inverted_index[word]+=[num_files_indexed]
                    except:
                        self._inverted_index[word]=[num_files_indexed]
                num_files_indexed += 1
            else:
                num_files_indexed += 1
                pass
        return num_files_indexed

    def tokenize(self, text):
        tokens = []
        tokens = list(set(re.split('[^a-zA-Z0-9]',text.lower())))
        try:
            tokens.remove('')
        except:
            pass
        return tokens

    def stemming(self, tokens):
        stemmed_tokens = []
        stem_func = PorterStemmer()
        for c in tokens:
            if c.isalpha():
                stemmed_tokens.append(stem_func.stem(c, 0,len(c)-1))
            else:
                stemmed_tokens.append(c)
        return stemmed_tokens
    
    def boolean_search(self, text):
        results = {}
        words = text.split(' ')
        for w in words:
            processed_word = self.stemming(self.tokenize(w))[0]
            if processed_word in self._inverted_index.keys():
                for l in self._inverted_index[processed_word]:
                    try:
                        results[w] += [self._documents[l]]
                    except:
                        results[w] = [self._documents[l]]
        try:
            final = set(results[list(results.keys())[0]])
            for w in words:
                processed_word = self.stemming(self.tokenize(w))[0]
                if processed_word in self._inverted_index.keys():
                    final = set(results[w]) & final
            non = set()
            if len(final) == 0:
                for w in words:
                    processed_word = self.stemming(self.tokenize(w))[0]
                    if processed_word in self._inverted_index.keys():
                        non = set(results[w]) | non
                return non
            else:
                return final
        except:
            print('Find no related products')
            return set([random.randint(0,len(self.products)-1) for i in range(10)])