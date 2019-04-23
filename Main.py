import pandas as pd
import re
import numpy as np
import random
# pip install nltk
import nltk
#nltk.download('vader_lexicon')

import numpy as np
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import datetime, time
from PorterStemmer import PorterStemmer

from ProductJudge import ProductJudge
from ReviewJudge import ReviewJudge

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('./data/OrinigalReview.csv')
data = data[['name', 'reviews.date','reviews.numHelpful', 'reviews.rating','reviews.text', 'reviews.title', 'reviews.username']]
data['review_id'] = data.index
data.name = data.name.fillna('Unknow Item')

reason1 = input('Product Search? y/n  ')
ProductJudge(reason1, data)

reason2 = input('Reviews Search? y/n  ')
ReviewJudge(reason2, data)

print('\nSearch Finished.')