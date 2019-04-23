import pandas as pd
import re
import numpy as np
import random
import numpy as np
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler
import datetime, time

from ReviewSearch import Index_Review

def ReviewJudge(reason2, data):
	if reason2 == 'y':

		index_review = Index_Review()

		try:
		    filer = open('./dict/ReviewDict.txt', 'r')
		    filerp = open('./dict/ReviewProdDict.txt', 'r') 
		    jsr = filer.read()
		    jsrp = filerp.read()
		    rdic = json.loads(jsr)  
		    rpdic =  json.loads(jsrp)  
		    index_review._inverted_index = rdic
		    index_review.products = rpdic
		    print("\nAlready Indexed")
		    num_products = index_review.index_dir(data, True)
		    print("\nindexed %d products" % num_products)
		    filer.close() 
		    filerp.close()
		except:
		    print("\nstarting indexer")
		    num_products = index_review.index_dir(data, False)
		    print("\nindexed %d products" % num_products)
		    rdic = index_review._inverted_index
		    rpdic = index_review.products
		    jsr = json.dumps(rdic)   
		    jsrp = json.dumps(rpdic)   
		    filer = open('./dict/ReviewDict.txt', 'w')  
		    filerp = open('./dict/ReviewProdDict.txt', 'w') 
		    filer.write(jsr)  
		    filerp.write(jsrp) 
		    filer.close()    
		    filerp.close()
		i=0
		while i <= 3:
			prod = input('\nWhich Product: ')
			if prod not in index_review.products:
				print('\nPlease try another product.')
				i += 1
			else:
				print('\nProduct Found.')
				break
		if i == 4:
			print('\nNo product, too much try.')
		else:
			term = input('\nReview Search: ')
			output_reviews = index_review.Review_Search(data, prod,term)
			i = 1
			try:
				for r in range(len(output_reviews)):
					print('\nTitle is: ', output_reviews['reviews.title'][r])
					print('\nReview',i, 'is: \n',output_reviews['reviews.text'][r])
					print('\nScore is: ', output_reviews['final_score'][r])
					print('\nUser is: ', output_reviews['reviews.username'][r])
					print('\nRating is', output_reviews['reviews.rating'][r],	',\tHelpful is: ',output_reviews['reviews.numHelpful'][r])
					print('------------- ')
					i += 1
			except:
				pass
	else:
		print('\nSearch Finished.')