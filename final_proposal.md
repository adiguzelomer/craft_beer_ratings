# A Craft Beer Recommendation System

## Objectives

With so many beers available in the market, it is extremely difficult for a
customer to review all of his or her options before making a purchase. I'd
like to help solve this problem by creating a system that can use data about
the users preferences and the characteristics of beers they enjoy to make
recommendations about what beers they will prefer.

## Existing Solutions

The idea of soliciting recommendations is hardly new. There are sites like
[BeerAdvocate](http://www.beeradvocate.com) which allow users to rate and
review beers. These are then made available to other users. The site also
curates top-rated lists for each style of beer. This is essentially a
popularity/content hybrid recommender. However, we can hopefully do better than
this approach through machine learning.

Here are a couple examples of what has been done before:
1. [BeerRecommender](http://http://www.recommend.beer/)
2. [Ninkasi Beer Recommender](http://ninkasibeer.herokuapp.com/)

### BeerRecommender

There are two types of machine learning here. First, this application
uses a Random Forest to predict whether a beer is an ale or a lager based on
reviews. Second, this application attempts to infer with which topic (taste, look,
smell, or feel) a review is most associated. A user is then asked to input
three beers they prefer and the recommender selects beers that are similar to
be recommended.

### Ninkasi Beer Recommender

This application actually houses to recommendation systems: a content-based
recommender, and a collaborative-filtering recommender.

In the content-based recommender, Term Frequency-Inverse Document Frequency
(TF-IDF) is calculated and used to calculate the cosine similarity. These
values are used to make recommendations to the user given a beer that the user
enjoys. They say that they have uses Latent Semantic Analysis, which implies
that they use Singular Value Decomposition (SVD) at some point in the analysis.

In the collaborative-filtering recommendation system, a user is asked to rate
as many beers as they would like. As they note, rating information tends to be
quite sparse. So, to deal with this problem they use SVD++ (a modified version
of FunkSVD which takes into account biases for both users and items) and a
Restricted Boltzmann Machine (RBM), a type of neural network which also
accounts for user and item bias. Each of these techniques generates a user-item
matrix which is then combined to produce the final user-item matrix.

For more information, see the groups blog
[here](
https://nycdatascience.com/blog/student-works/ninkasi-beer-recommender-system/
).

## Differences from the Existing Solutions

## Presentation

## The Data

## Challenges

## First Steps

## References:
1. http://www.recommend.beer/
2. https://nycdatascience.com/blog/student-works/ninkasi-beer-recommender-system/
3. http://ninkasibeer.herokuapp.com/
