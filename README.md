# recommender-system-capstone
### _Author: Rachel Koenig_

## Problem Statement


The world of retail is changing rapidly.  Many brick and mortar locations are closing and being replaced by online stores.  However, while the breath of assortment is something that drives customers to a website, a lot of eCommerce platforms fail to sell through a high percent of their merchandise.  This is often due to poor user browsing experience. Customers can spend hours scrolling through hundreds, sometimes thousands of items of merchandise and never finding an item they like.  

This goal of this project is to create collaborative recommender systems, both user and item based, that will help solve this problem. Customers should be provided suggestions based on their likes and needs in order to create a better shopping environment that boosts sales and increases their time spent on a website.

Using data from http://jmcauley.ucsd.edu/data/amazon/index.html, 278,677 reviews of Clothing, Shoes, and Jewelry from Amazon, I will build a recommender with the goal of generalizing well to other online retailers who are in need of such resources. Since this is unsupervised learning, there is no target variable. I'll use cosine similarity, aiming for a score of 1 or pairwise distance, aiming for a score of 0, as metrics to check similarity between items and users.

I would like to scrape the product features, image and product name from amazon as well, but since the reviews are from 1996 to 2014, many of the items are no longer available on Amazon or have html and/or javascript that is difficult to loop through.  If that fails, I will try to use NLP to examine the reviews themselves to find predictive words that identify the item.  
I plan to do this with Selenium but haven't gotten it to work yet. 

Alternatively, maybe I could use NLP to find most popular items.

Maybe a flask app to out put suggested items when a user inputs an item #? 



## EDA
Data is provided with the below columns.
'reviewerID' : unique reviewer identification number    
'asin' : unique product identification number   
'reviewerName': customer name   
'helpful': a list of two numbers, one for how many times review was helpful and the other for how many times it was not.  
'reviewText' : written review   
'overall' : numerical rating 1-5 out of 5 stars.  
'summary': second part written review
'unixReviewTime': time of review  
'reviewTime': date of review 
