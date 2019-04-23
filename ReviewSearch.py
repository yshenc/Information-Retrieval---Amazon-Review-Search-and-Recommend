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


class Index_Review(object):
    def __init__(self):
        self._inverted_index = {}
        
        self._documents = []
        self.products = {}
        
    def index_dir(self, data, exist):
        num_files_indexed = 0
        for files in data['review_id']: 
            all_tokens = []
            self._documents.append(files) 
            if exist == False: 
                prod = data[data['review_id']==files]['name'].values[0]
                try:
                    self.products[prod]+=[files]
                except:
                    self.products[prod]=[files]
                  
                text = data[data['review_id']==files]['reviews.text'].values[0]
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
        try:
            tokens = list(set(re.split('[^a-zA-Z0-9]',text.lower())))
        except:
            pass
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
    
    def boolean_search(self, product, text):
        results = []
        words = text.split(' ')
        if len(words) == 1:
            processed_word = self.stemming(self.tokenize(text))[0]
            if processed_word in self._inverted_index.keys():
                for l in self._inverted_index[processed_word]:
                    results.append(self._documents[l])
                
        product_re = self.products[product]
        results = set(results) & set(product_re)
        return results

    def sentiment(self, data):
        analyzer = SentimentIntensityAnalyzer()
        review = data['reviews.text']
        scores = np.zeros(len(review))
        
        for i, t in enumerate(review):
            # Extract the text portion of the tweet
            reviews = t
            # Measure the polarity of the tweet
            polarity = analyzer.polarity_scores(reviews)

            # Store the normalized, weighted composite score
            scores[i] = polarity['compound']
            data['review_sentiment'] = abs(scores)
            
        return data

    def view_rank(self, data_target):
        scale_col = ['reviews.numHelpful','reviews_rating','reviews.days','review_sentiment','title_boolen']
        pre_data = data_target[scale_col].apply(lambda x: x/max(x))
        imp_help = 0.4
        imp_rating = 0.15
        imp_time = 0.05
        imp_sentiment = 0.25
        imp_title = 0.15

        data_target['final_score'] = pre_data['reviews.numHelpful']*imp_help+pre_data['reviews_rating']*imp_rating + pre_data['reviews.days']*imp_time+pre_data['review_sentiment']*imp_sentiment+pre_data['title_boolen']*imp_title
        return data_target.sort_values('final_score', ascending= False)

    def Review_Search(self, data, product, term):
        results = self.boolean_search(product, term)
        #print("searching:," ,term ,"-- results:", str(results))
        if len(results) > 0:
            data_target = data.iloc[list(results)]
            data_target = self.sentiment(data_target)
            data_target['title_boolen'] = data_target['reviews.title'].str.lower().str.contains(term.lower()).astype(int)
            data_target['reviews.date'] = pd.to_datetime(data['reviews.date'])
            now = datetime.datetime.now()
            data_target['reviews.days'] = (data_target['reviews.date'] - now).apply(lambda x: getattr(x, 'days'))
            data_target['reviews_rating'] = abs(data_target['reviews.rating']-3)

            result = self.view_rank(data_target)
            result.reset_index(inplace = True)
            output = result.loc[0:4,['reviews.title','reviews.text','final_score','reviews.username','reviews.numHelpful','reviews.rating']]
            return output
        else:
            print('Find no related reviews.')