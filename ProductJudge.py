import pandas as pd
import re
import numpy as np
import random
import numpy as np
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import datetime, time

from ProductSearch import Index_Product


def ProductJudge(reason1, data):
	if reason1 == 'y':

		all_product = data['name'].unique()
		index_product = Index_Product()
		try:
		    filep = open('./dict/ProductDict.txt', 'r') 
		    jsp = filep.read()
		    pdic = json.loads(jsp)   
		    index_product._inverted_index = pdic
		    print("Already Indexed")
		    num_products = index_product.index_dir(data, True)
		    print("indexed %d products" % num_products)
		    filep.close() 
		except:
		    print("starting indexer")
		    num_products = index_product.index_dir(data, False)
		    print("indexed %d products" % num_products)
		    
		    pdic = index_product._inverted_index
		    jsp = json.dumps(pdic)   
		    filep = open('./dict/ProductDict.txt', 'w')  
		    filep.write(jsp)  
		    filep.close()    

		term = input('Search Product: ')
		results = index_product.boolean_search(term)
		print("searching:," ,term ,"-- results: \n ", all_product[list(results)])

	else:
		pass