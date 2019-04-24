# Information Retrieval --- Amazon Review Access and Recommendation

## Project Description

Team members: Guancheng Yao, Bowen Tang, Yuchen Shen

The project is foucus on "Amazon Review Access and Recommendation", which is the final project for class CS525/DS595: Information Retrieval & Social Web at Worcestor Polytechnic Institute (WPI).

Our dataset is gathered from Kaggle (https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products) which provided by Amazon. Anyone can gather it from the link or you can unzip the Review data.zip in our repository.
The original dataset contains a list of over 34,000 reviews and 49 different products of Amazon products like the Kindle, Fire TV, etc. it also contains information about product rating, number of lighten and other useful features.

Our project is going to retrieve reviews for certain product based on given terms, and different from most of other review search services, we will also recommend some other reviews that consumer's may interested in. It will save consumer’s time in extracting the comments they are looking for. We combined several methods together, to rank the reviews and recommend most possible ones. Methods we are using is learned from the IR and ML class.

Since we want our retrieved reviews different from recommended reviews, we drop all products that have less than 200 reviews or without product name. Also, in order to make the result easier to understand, we did some small changes to the products name. Finally, the processed dataset contains 27198 Reviews and 12 products, and keep features : Product name, rating, rating date, numHelpful, review text, title and username.

The function of our Review Access and Recommendation system can be seperated into parts.

  1. Apply Boolean Search on products to retrieve product names containing requried words
  
  2. Apply Boolean Search on reviews to retrieve reviews containing search words
  
  3. Apply Ranking method on retrieved reviews to give top score 5
  
  4. Apply Latent Dirichlet Allocation (LDA) method to cluster all words into topics, return words in the same topics with search words 
  
  5. Apply Boolean Search and ranking methods on reviews to retrieve reviews containing words returned from part 4.
  
Following the steps above, the system can retrieve required products, reviews and recommended reviews.

## System Set Up

### System
See requirement.txt for python library requirement.

In 'dict' folder, we already provide inverted index dictionary for product and review.

For product and review search, just simply run 'Main.py' in terminal.
The program will ask your purpose, such as 'Product Search? y/n'. Just answer questions as the description appearing.
Then type in terms you want for products as 'Search Product: ' appear, then products will be returned.

Similarly, review search will follow the same way.
Then products and reviews will be retrieved.

For review recommendation, run 'lda.py' in terminal.
Then type in the saerch term, the program will return words in the same topic. Finally, use 'Main.py' again to retrieve recommended reviews.

### Website Demo

We create a static HTML website demo for our project. For the purpose of the demonstration, this website shows one case of how you can use this search engine to get the review you care about.
There are 12 products listed on the home page, and by selecting each one of them you will be directed to the search page. In the search page, by typing the review you are looking for and then the search engine finds the related reviews for you. At the bottom of the review page, we provide recommended reviews that belong to the same topic you are searching for.

How to use:
In 'Website Demo' folder, 'index.html' is the start file.
Because this is a static html, you can import it to any IDE you prefer to use, or just double-click the 'index.html' directly. It will show the page in your browser.

# Reference

The website templete: https://html5up.net/
