# Recommender System Capstone

_Author: Rachel Koenig_

-------

## Executive Summary

**Problem Statement**

The world of retail is changing at a rapid pace.  Many brick and mortar locations are closing and being replaced by online stores.  However, while the breadth of assortment that comes with shopping online is something that drives customers to a website, a lot of eCommerce platforms fail to sell through a high percent of their merchandise.  This is often due to a poor user browsing experience. Customers can spend hours scrolling through hundreds, sometimes thousands of items of merchandise never finding an item they want to buy.  

This goal of this project is to create both content-based and collaborative user- and item-based recommender systems, that will help solve this problem. Customers should be provided suggestions based on their likes and needs in order to create a better shopping environment that boosts sales and increases their time spent on a website.

These recommenders will be built with the intent of generalizing well to online retailers besides Amazon who are in need of such resources by using features like color, brand and product category.   

**Metrics** 
This is unsupervised learning because there is no target variable. I'll use cosine similarity, aiming for a score of 1 and pairwise distance, aiming for a score of 0, as metrics to check similarity between items and users.

**Key Takeaways**
Raw text data is a wild beast.  The majority of time on this project was spent cleaning the scraped text from the Amazon, specifically trying to pull keywords from the name and descriptions columns to use as features.  As you will learn below, I ended up only using the CountVectorizer process on the `name` column and not using features from the `description` or `details` columns at all because the dataset was so large to being with. I started with the more is more approach, but scaling back and only using the more important features returned better pairwise distance scores. With more time I would continue to use both feature extraction and feature elimination to find....

**Results**  
The [item-based recommender](1_item-based-recommender.ipynb) was kind of my baseline.  Without any NLP or feature engineering, I used the products(items) as rows, reviewers(users) as columns and ratings out of 5-stars as the values.  Pairwise distance scores were landing between 0.5 and 0.85 which were much closer to 1 than I wanted so the goal was to get below 0.5 on future iterations. 

The final [content-based recommender](6_content-based-recommender.ipynb) returns scores of __ . Since this there is not correct answer to compare to for this modoel, the only way to check success is by randomly selecting different products, checking that top 10 pairwise distance scores are close to zero and checking that the recommended products make sense. Of the large handful I looked at, I can say that this recommender meets both criteria.  However, it is not perfect and still needs some further exploration of the features before it could be implemented on an ecommerce site. 



## Data Collection
[Web Scraping Notebook](2_amazon-scrape.ipynb)  
You may need to pip install selenium to run this notebook.   

I was lucky enough to find and download an amazing dataset of 278,677 Amazon reviews and ratings of Clothing, Shoes, and Jewelry [here](http://jmcauley.ucsd.edu/data/amazon/index.html), but while it was robust in rows, it was actually lacking in product details including product name, color, and description. 

Using Selenium Webdriver, I scraped the 23,033 unique Amazon product IDs in the dataset in search of the product names and features. Since the reviews were from 1996 to 2014 however, many of the items are no longer available on Amazon or have html and/or javascript tags that are difficult to determine. After numerous rescrapes and multiple modifications to tag requests, I decided to drop any rows that were still "unknown", leaving me with 15655 usable products' info.

Amazon reviews data dictionary
**Column**|**Type**|**Description**
:-----:|:-----:|:-----:
reviewerID|object|unique reviewer identification number
asin|object|unique product identification number
reviewText|object|written customer review
overall|float|numerical rating 1-5 out of 5 stars
summary|object|short recap of review
review date|datetime|date of review   

Dropped columns from amazon reviews
**Column**|**Type**|**Description**|**Reason for drop**
:-----:|:-----:|:-----:|:-----:
reviewerName|object|customer name|too many different formats and not enough unique values, some first name only, some full names, some nicknames
helpful|object|a list of two numbers, one for how many times review was helpful and the other for how many times it was not|68% of the rows had no helpful votes at all which made the whole column pretty useless
unixReviewTime|int|time of review in universal time zone|error converting to datetime format
reviewTime|object|date of review |replaced with date in correct datetime format
 
Additional columns from scrape   
**Column**|**Type**|**Description**
:-----:|:-----:|:-----:
category|object|the departments and subdepartments list from the top right of an Amazon product page
color|object|supposed to be available colors of the products, scaper occasionally picked up size from this tag too
description|object|the product description from the Amazon product page 
details|object|additional details provided from a different hidden portion of the Amazon product page
name|object|the product header - included brand, type/short description of product
size|object|product size, occasionally picked up color for this tag though


## EDA & Missing Data 

Wrote a function to:  
Remove html and strip off brackets and 'Color:' from color column  
Replace escape characters and white space in Category column  
Split Category column on the '›' symbol, up to 6 times and return them in a new df where each split is a new column   
Rename each category split column and add it onto the original df  

    **New Category Name**|**Category Column**
:-----:|:-----:
department|0th
demographic|1st
division|2nd
category|3rd
subcategory|4th
type|5th
detail type|6th
Remove special characters from the description column  
Remove html and strip off brackets from details column  
Remove html and cut off 'Size:' from the size column   

Turned these columns in to dummies: departments, demographic, details, category, division, subcategory

At one point in this process I had 19766 rows of scraped data.  However upon further analysis, I discovered duplicates which cut the rows down to 16816.  Then I noticed that there were still 7% unknown `department` rows and 11% of `department` rows with a 0s  which meant that none of the subdepartments would have values either.  I made the decision to remove these as well because they would create similarities between unnrelated products and hurt my model, leaving me with 13732 unique rows.  

After I merge the reviews and product info DataFrames, I check for nulls and see I have almost 39% missing.  These are the rows of products which I was not able to scrape.  This type of data is called missing at random and I have to drop it because it doesn't exist and I have no access to accurate information to fill it in.   

During the EDA process I also determined the `size` scrape came out way too messy.  Majority of cells were empty/missing and there was no way to parse it to pull consistently pull out the size.   

At this point, I also realized that dummying out the departement columns led to 117 duplicate column names in my 940 columns. I wanted to merge the duplicates together and keep the max value per row, rather than adding them up so that no cells would be different than 1s or 0s. After dropping the duplicates I am left with 168995 rows and 823 columns.  


## Feature Engineering 


## Modeling 

My first recommender attempt was with 811 category columns and a column for the average rating out of 5 stars. Some of the products did return relevant results with "good" scores close to 0, in the 0.2 range.  Many products, however were returning recommendations with identical pairwise distance scores very close to 0, right around or under 0.1, and for products unrelated to the search.  

To fix this I needed to add more features. I had the product names in a column so I used CountVectorizer to split up the words individually and by 2- and 3-gram phrases.  I set the binary parameter to true so that each word and phrase became a feature/column and each row/product got a 1 in the column if it contained that word or phrase in the name and a 0 if it did not.  
Other parameters included max_df of 2 which says that the word or phrase must appear in at least two documents and stop words were set to a list of colors I created from my colors dataset. There was no limit set to max features so I ended up with about 23000 columns. I was able to eliminate almost 200 by taking out any columns with integer only names.  
I joined the new features onto the categories column and ran the recommender again. 

Scores did get a little better 

To futher iterate, I joined on my colors onto the features and categories df.  


Changing max features to 10,000, greatly imporved my score and item relavancy 



citations:
WWW / SIGIR papers http://jmcauley.ucsd.edu/data/amazon/index.html,
R. He, J. McAuley. Modeling the visual evolution of fashion trends with one-class collaborative filtering. WWW, 2016
J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based recommendations on styles and substitutes. SIGIR, 2015
1

dataworld = https://data.world/dilumr/color-names/workspace/file?filename=wikipedia_color_names.csv

