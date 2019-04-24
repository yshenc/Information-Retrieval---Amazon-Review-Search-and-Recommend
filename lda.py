import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
%matplotlib inline
import string
import nltk
import re
import heapq
from nltk import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.decomposition import LatentDirichletAllocation

path = '/Users/hush/Downloads/consumer-reviews-of-amazon-products/1429_1.csv'
pd.set_option('display.max_colwidth', 0)

def getData(path):
    reviews = pd.read_csv(path,low_memory=False)
    reviews.columns = ['id', 'name', 'asins', 'brand', 'categories', 'keys', 'manufacturer','date', 'dateAdded',
                       'dateSeen', 'didPurchase', 'doRecommend', 'rid','numHelpful', 'rating', 'sourceURLs',
                       'text', 'title', 'userCity','userProvince', 'username']
    rating_perprodcut = reviews['name'].value_counts()
    product_dic = {}
    for name in rating_perprodcut.keys():
        if rating_perprodcut[name] >= 200:
            product_dic[name] = reviews[reviews['name'] == name]
            product_dic[name] = product_dic[name].reset_index(drop=True)
    return product_dic

def getDataFrameforLDA(product_dic):
    dic = {}
    for key,reviews in product_dic.items():
        data = pd.concat([reviews['name'],reviews['text']+" "+ reviews['title'],reviews['rating'],
                          reviews['doRecommend'],reviews['username']],axis=1)
        data.columns=['name','text','rating','recommend','username']
        data = data.dropna(axis=0,subset = ['text'])
        dic[key] = data
    return dic

stop_words = nltk.corpus.stopwords.words('english')
ps = PorterStemmer()

def textPrecessing(sent): 
    temp1 ="".join(x for x in sent if x not in string.punctuation)
    temp2 = re.split('\W+',temp1.lower())
    temp3 = [ps.stem(x) for x in temp2 if x not in stop_words]
    return temp3

def textPrecessing_new(text):
    #Lowercase
    text = text.strip().lower()
    #Remove special punctuation
    for c in string.punctuation:
        text = text.replace(c, ' ')
    #Participle
    wordLst = nltk.word_tokenize(text)
    #Remove stop words
    filtered = [w for w in wordLst if w not in stopwords.words('english')]
    #Keep only nouns or specific POS   
    refiltered =nltk.pos_tag(filtered)
    filtered = [w for w, pos in refiltered if pos.startswith('NN')]
    #Stemming
    ps = PorterStemmer()
    filtered = [ps.stem(w) for w in filtered]
    return filtered

def getTextMatrix(dic_lda):
    textmatrix_dic = {}
    vectext = CountVectorizer(analyzer=textPrecessing_new)
    for key,data in dic_lda.items():
        textfeatures = vectext.fit_transform(data['text'])
        textmatrix = pd.DataFrame(textfeatures.toarray(),columns=vectext.vocabulary_)
        # textmatrix_dic is the TfidfVec of text of different product
        textmatrix_dic[key] = textmatrix
        print("Stemmed - " + str(len(vectext.get_feature_names())))
    return textmatrix_dic

def getNumofTopics(textmatrix):
    r, l = textmatrix.shape
    if l > 3000:
        return 20
    elif 1700 < l <= 3000:
        return 15
    else:
        return 10

def getModel(textmatrix_dic):
    text_model = {}
    for key,textmatrix in textmatrix_dic.items():
        lda = LatentDirichletAllocation(n_components=getNumofTopics(textmatrix),
                                        doc_topic_prior=2,
                                        topic_word_prior=2,
                                        max_iter=10,
                                        learning_method='batch')
        lda.fit(textmatrix)
        text_model[key] = (lda, textmatrix)
    return text_model

def getFinalMatrix(path):
    product_dic = getData(path)
    dic = getDataFrameforLDA(product_dic)
    textmatrix_dic = getTextMatrix(dic)
    text_model = getModel(textmatrix_dic)
    return text_model

def getTopicofInput(product_name, inputwordstr, text_model, krelated=5):
    model, textmatrix = text_model[product_name]
    inputword = textPrecessing_new(inputwordstr)[0]
    if inputword not in textmatrix.columns:
        return 'no results found'
    idx = textmatrix.columns.get_loc(inputword)
    # Variational parameters for topic word distribution
    topic_word_arr = model.components_
    # Index of topic
    topic = np.argmax(topic_word_arr[:,idx])
    temp = topic_word_arr[topic]
    wordlistidx = list(map(list(temp).index, heapq.nlargest(krelated, temp)))
    # The krelated names in that topic
    names = [textmatrix.iloc[:,i].name for i in wordlistidx]
    return names

text_model = getFinalMatrix(path)
product_name = input('Product name: ')
inputwordstr = input('Search review word: ')
names = getTopicofInput(product_name, inputwordstr, text_model)
print('related words: ',names)