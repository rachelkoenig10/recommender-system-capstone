# Recommender System Capstone
-------
_Author: Rachel Koenig_

## Problem Statement


The world of retail is changing rapidly.  Many brick and mortar locations are closing and being replaced by online stores.  However, while the breadth of assortment is something that drives customers to a website, a lot of eCommerce platforms fail to sell through a high percent of their merchandise.  This is often due to a poor user browsing experience. Customers can spend hours scrolling through hundreds, sometimes thousands of items of merchandise and never finding an item they want to buy.  

This goal of this project is to create both content-based and collaborative user- and item-based recommender systems, that will help solve this problem. Customers should be provided suggestions based on their likes and needs in order to create a better shopping environment that boosts sales and increases their time spent on a website.

These recommenders will be built with the intent of generalizing well to online retailers besides Amazon who are in need of such resources. Since this is unsupervised learning, there is no target variable. I'll use cosine similarity, aiming for a score of 1 or pairwise distance, aiming for a score of 0, as metrics to check similarity between items and users.

## Data Collection

I was lucky enough to find and download an amazing dataset of 278,677 Amazon reviews and ratings of Clothing, Shoes, and Jewelry from http://jmcauley.ucsd.edu/data/amazon/index.html, but while it was robust in rows it was actually lacking in product details including product name, color, and description. 

Using Selenium Webdriver, I scraped the 23,033 unique Amazon product IDs in the dataset in search of the product names and featuress. Since the reviews were from 1996 to 2014, however, many of the items are no longer available on Amazon or have html and/or javascript that is difficult to determine. After numerous rescrapes and multiple modifications to tag requests, I decided to drop the "unknown" rows leaving me with 15655 usable products' info.

Amazon reviews data dictionary
|Column|Type|Description|
|---|---|---|---|
|reviewerID|object|unique reviewer identification number | 
|asin|object|unique product identification number| 
|reviewText|object|written customer review|
|overall|float|numerical rating 1-5 out of 5 stars|
|summary|object|short recap of written review|
|review_date|datetime64|date of review|

Dropped columns from amazon reviews
|Column|Type|Description|Reason for drop|
|---|---|---|---|---|
|reviewerName|object|customer name|too many different formats and not enough unique values, some first name only, some full names, some nicknames| 
|helpful|object| a list of two numbers, one for how many times review was helpful and the other for how many times it was not|68% of the rows had no helpful votes at all which made the whole column pretty useless| 
|unixReviewTime|int|time of review in universal|error converting to datetime format|   
|reviewTime|object|date of review|replace with date in correct datetime format| 

 

## EDA & Missing Data 

Wrote a function to:
Remove html and strip off brackets and 'Color:' from color column
Replace escape characters and white space in Category column
Split Category column on the '›' symbol, up to 6 times and return them in a new df where each split is a new column 
Rename each category split column and add it onto the original df
    df['department'] = category[0]
    df['demographic'] = category[1]
    df['division'] = category[2]
    df['category'] = category[3]
    df['subcategory'] = category[4]
    df['type'] = category[5]
    df['detail_type'] = category[6]
Remove special characters from the description column
Remove html and strip off brackets from details column
Remove html and cut off 'Size:' from the size column 

Turned these columns in to dummies: departments, demographic, details, category, division, subcategory

After I merge the reviews and product info dfs, I check for nulls and see I have almost 32% missing.  This type of data is Missing At Random and I have to drop it because it doesn't exist.

citations:
WWW / SIGIR papers http://jmcauley.ucsd.edu/data/amazon/index.html,
R. He, J. McAuley. Modeling the visual evolution of fashion trends with one-class collaborative filtering. WWW, 2016
J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based recommendations on styles and substitutes. SIGIR, 2015
1


