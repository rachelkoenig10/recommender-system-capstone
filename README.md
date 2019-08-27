# Recommender System Capstone

_Author: Rachel Koenig_

-------
### Table of Contents
[Web Scraping Notebook](2_amazon-scrape.ipynb)  
[Data Cleaning & Concatonating Scrapes](3_EDA-and-concatonate-scrapes.ipynb)  
[Text Data & Merging Reviews with Product Scrapes](4_NLP-merge-reviews-product-scrape.ipynb)   
[Feature Engineering](5_feature-engineering.ipynb)  
[Recommender Model](6_content-based-recommender.ipynb)

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

The final [content-based recommender](6_content-based-recommender.ipynb) returns pairwise distance scores of 0.025 to 0.055. Often times recommender systems' successes are measured by revenue or click-through-rate (CTR).  However, these can be deceiving or inaccurate. According to an article on [Quora](https://www.quora.com/How-do-you-measure-and-evaluate-the-quality-of-recommendation-engines), if a recommended item does not bring in more revenue, it is hard to know if that was purely because the customer did not like the recommendation or just because they did't like the price.  CTR is also hard to measure because customers could just be clicking because the recommendation is flashy and attention grabbing but then not actually purchasing still. Since we do not know "correct" answer to compare this model's results to until an item is actually purchased, another way to check success is by human evaluation, i.e. randomly selecting different products, checking that top 10 pairwise distance scores are close to zero and checking that the recommended products make sense. Of the large handful I looked at, I can say that this recommender meets both criteria.  Therefore, I think if my model was implemented on an eCommerce site, it would help consumers navigate the complex world of online shopping!  



## Data Collection
[Web Scraping Notebook](2_amazon-scrape.ipynb)  
You may need to pip install selenium to run this notebook.   

I was lucky enough to find and download an amazing dataset of 278,677 Amazon reviews and ratings of Clothing, Shoes, and Jewelry [here](http://jmcauley.ucsd.edu/data/amazon/index.html), but while it was robust in rows, it was actually lacking in product details including product name, color, and description. 

Using Selenium Webdriver, I scraped the 23,033 unique Amazon product IDs in the dataset in search of the product names and features. Since the reviews were from 1996 to 2014 however, many of the items are no longer available on Amazon or have html and/or javascript tags that are difficult to determine. After numerous rescrapes and multiple modifications to tag requests, I decided to drop any rows that were still "unknown", leaving me with 15655 usable products' info.

Amazon reviews data dictionary 


| Column     | Type   | Description |     
|------------|--------|------------------------------------|  
| reviewerID | object | unique reviewer identification num |  
| asin       | object | unique product identification num  |    
| reviewText | object | written customer review            |  
| overall    | float  | numerical rating 1-5 out of 5 stars|  
| summary    | object | short recap of review              |  
|review date | datetime | date of review                   |  


Dropped columns from amazon reviews    


|Column       |Type  |Description  |Reason for drop|  
|-------------|------|-------------|-----|
reviewerName  |object|customer name|too many different formats and not enough unique values, some first name only, some full names, some nicknames  
helpful       |object|a list of two numbers, one for how many times review was helpful and the other for how many times it was not| 68% of the rows had no helpful votes at all which made the whole column pretty useless  
unixReviewTime|int   |time of review in universal time zone|error converting to datetime format  
reviewTime    |object|date of review |replaced with date in correct datetime format  
 
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
[Data Cleaning & Concatonating Scrapes](3_EDA-and-concatonate-scrapes.ipynb)  
[Text Data & Merging Reviews with Product Scrapes](4_NLP-merge-reviews-product-scrape.ipynb)   

Wrote a function to:  
Remove html and strip off brackets and 'Color:' from color column  
Replace escape characters and white space in Category column  
Split Category column on the '›' symbol, up to 6 times and return them in a new df where each split is a new column   
Rename each category split column and add it onto the original df  


   |New Category Name|Category Column|
   |-----------------|---------------|
   |department       |0th            |
   |demographic      |1st            |
   |division         |2nd            |
   |category         |3rd            |
   |subcategory      |4th            |
   |type             |5th            |
   |detail type      |6th            |
 
 Remove special characters from the description column  
 
 Remove html and strip off brackets from details column  
 
 Remove html and cut off 'Size:' from the size column   

Turned these columns in to dummies: departments, demographic, details, category, division, subcategory

At one point in this process I had 19766 rows of scraped data.  However upon further analysis, I discovered duplicates which cut the rows down to 16816.  Then I noticed that there were still 7% unknown `department` rows and 11% of `department` rows with a 0s  which meant that none of the subdepartments would have values either.  I made the decision to remove these as well because they would create similarities between unnrelated products and hurt my model, leaving me with 13732 unique rows.  

After I merge the reviews and product info DataFrames, I check for nulls and see I have almost 39% missing.  These are the rows of products which I was not able to scrape.  This type of data is called missing at random and I have to drop it because it doesn't exist and I have no access to accurate information to fill it in.   

At this point, I also realized that dummying out the departement columns led to 117 duplicate column names in my 940 columns. I wanted to merge the duplicates together and keep the max value per row, rather than adding them up so that no cells would be different than 1s or 0s. After dropping the duplicates I am left with 168995 rows and 823 columns.  


## Feature Engineering   
[Feature Engineering](5_feature-engineering.ipynb)  

Started out by checking for nulls and filling them in with the string 'none' because I did not want to lose any more data.  
Created a Users DataFrame by dropping columns except for reviewerID, asin, overall, color, name and department for clustering types of users.    
Used groupby function to find:   
sum up all categories that a user has purchased to see what types of items they're purchasing
count up how many asins are related to each user to see their total number of reviews   
average the number of stars each user rates to fing out if they are a tough critic or easily satisfied  
Then added up any non-numeric columns (`name`, `color`, `asin`) to create a list of words to dummy/CountVectorize  
Set reviewerID as index.  

So I could drop duplicate rows and work with a smaller DataFrame, I grouped all rows with text like `summary` and `reviewtext` together based on asin #s. To get the text ready to be used as content/features in the content-based recommender, I made a new columns called `all_text` for all the text columns like `all_reviews`, `one_sum`, and `description` to be combined into one.  I decided not to use `details` right away because it was messy and most cells were missing.  I did not get rid of it though, incase I might end up needing it later.  
I did determine though, that the `size` scrape came out way too messy and would probably not ever be useful in the future.  Majority of cells were empty/missing and there was no way to parse it to consistently pull out the size. 

Using the groupby function I found the average rating per product and created a new column containing that value called `overall_mean`.   
  
Next I dropped all the columns except `name`, `asin`, `overall_mean` and all the dummied department columns to create a category only DataFrame and saved it as a csv to use for the model.   

Working with only the text columns now I narrowed in on the `name` and `color` columns to clean up and use in the model.  I made the desicion to start with those and add or eliminate more features later as needed.  Using NLTK, I tokenized, removed stopwords, and lemmatized.  

For the colors, I created a new column called `colors_only` using a list of colors from a dataset found on dataworld [here](https://data.world/dilumr/color-names/workspace/file?filename=wikipedia_color_names.csv) to pull out any words that are actual colors from the `name` and `color` columns for both the product DataFrame and the Users DataFrame and eliminate the noise.  

Lastly, I turned every color into its own binary column for a 1 if a product is that color or if a user purchased an item that color and a 0 if not. Unfortunately this method of extracting color names from a string is not fool-proof. It does over catch words and phrases that just have that word in them. For example, Learn French Rosetta Stone, returns both French Rose and Rose as colors. For the purposes of this project though, I decided to still use it because it it catches those "colors" in one product it'll catch them in another and most likely that means those products have the same words in the title and are therefore probably similar.  

## Modeling 
[Recommender Model](6_content-based-recommender.ipynb)
My first recommender attempt was with 811 category columns and a column for the average rating out of 5 stars. Some of the products did return relevant results with "good" scores close to 0, in the 0.2 range.  Many products, however, were returning recommendations with identical pairwise distance scores very close to 0, right around or under 0.1, and for products unrelated to the search.  

Taking a closer look, I find that a lot of items have the exact same departments/categories in common.  To fix this I needed to add more features. I had the product names in a column so I used CountVectorizer to split up the words individually and by 2- and 3-gram phrases.  I set the binary parameter to true so that each word and phrase became a feature/column and each row/product got a 1 in the column if it contained that word or phrase in the name and a 0 if it did not instead of counting up the total times that word or phrase appeared in the document.  

Other parameters included max_df of 2 which says that the word or phrase must appear at least two times in document to count and stop words were set to a list of colors I created from my colors dataset. There was no limit set to max features so I ended up with about 23000 columns. I was able to eliminate almost 200 by taking out any columns with integer-only names.  
I joined the new features onto the categories column and ran the recommender again. 

Scores did get a little better, but not great. 

To futher iterate, I joined on my color features onto CountVectorized-names and categories.  This actually made the scores a little worse which led me to believe now I have _too many_ features.  

I went back to CountVectorizer at this point and kept everything the same except max features changed to 10,000.  I also removed all the color features and the scores and item relavancy greatly improved. My go-to product of comparison is a child's Buzz Lightyear costume and all of the recommendations were also child's costumes with pairwise scores of about 0.09 to 0.11.  

After this I tried adding the color features back on and the scores decreased slightly again.  

Just out of curiousity, I also tried just using categories and colors as features but the model completely bombed.  

My final interation of the model was to use TfIdfVectorizer on the tokenized name column.  First I only set the parameters of stopwords = list of colors, n-grams=1, 2 and 3 and binary=True. This gave me over 100,000 columns so I went back and chage max features to 10,000 and min_df =2.  The scores improved immensely and products seemed very similar.  The only problem was that the value counts for each feature were not coming out binary.  Then I learned that TfIdf, according to the sklearn documentation, binary means all non-zero term counts are set to 1, but does not mean outputs will have only 0/1 values, only that the tf term in tf-idf is binary. It suggests settig the idf and norm to False to get 0/1 outputs.  So I set both use_idf and smooth_idf to False and norm to None.  My results were then identical to the best scores I got with CountVectorizer. Finally I changed norm to L2 to normalize the date in case of overfitting and the scores came back to the 0.025 to 0.035 range for Buzz Lightyear.  

I think both the CountVectorizer and TfIdf processes probably need some more digging to confirm if they are accurate and/or overfit.  However, from the current standing, they look satisfactory. 

## Future Iterations  
I will continue to work on this project and as I do I would like to dive deeper into user/reviewer clustering.  Finding similarities between users' purchases would be useful for a collaborative user-based recommneder. 

Check for overfitting with TfIdf.  

Expand dataset and scrape additional items from Amazon.  

Launch a "human evaluation A/B test" to get other real opinions (besides my own) on the relevance of of the recommendations.  

Try to evaluate using training and testing data.

[Presentation slides](https://docs.google.com/presentation/d/1C-emUHLX-wpJ4-EEIQcAcrnzNi5Rmj_LtY_hMxRMDHE/edit?usp=sharing)

citations:
WWW / SIGIR papers http://jmcauley.ucsd.edu/data/amazon/index.html,
R. He, J. McAuley. Modeling the visual evolution of fashion trends with one-class collaborative filtering. WWW, 2016
J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based recommendations on styles and substitutes. SIGIR, 2015
1

dataworld = https://data.world/dilumr/color-names/workspace/file?filename=wikipedia_color_names.csv

Quora - https://www.quora.com/How-do-you-measure-and-evaluate-the-quality-of-recommendation-engines

