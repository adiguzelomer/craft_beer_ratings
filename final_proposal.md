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

## An Ensemble Approach

Each of the recommender system's above has strengths and utilizes a subset of
the available data to make its recommendations. I plan to improve upon these
systems by creating an ensemble of recommenders and using their individual
recommendations as the inputs for a final recommendation system.

I intend to have three recommenders in the ensemble.
1. A popularity/content-based recommender
2. A content-based recommender
3. A collaborative recommender

## Presentation

I will deploy the recommender through a Flask application where users can input
either some text about beers they enjoy or rate a few beers in order to receive
recommendations.

## The Data

The data comprises, approximately, 700,000 reviews by 40,000 users about 9,000
beers (at this time). I intend to continue scraping data in order to increase
the variety of beers available on which to train the recommenders. The
recommender can only recommend a beer that it has seen before, so the more
data, the better.

This data is currently housed on Amazon Web Services (AWS) in a DynamoDB NoSQL
database.

## Challenges

### Measuring the Results

My recommender systems are based primarily on topic modelling techniques, which
fall squarely in the realm of unsupervised learning. As such, quantifying the
results of the model is difficult.

### Diversity (Serendipity)

Recommender systems often struggle to give recommendations that are diverse.
For example, if a user loves Pale Ales, a model can recommend other Pale Ales
but may struggle to identify new experiences (perhaps, a nice Stout) that the
user would enjoy.

### Tuning

With three models as inputs to a fourth model, there are quite a few hyper
parameters to tune. This is not a trivial task and can have quite an impact on
the models performance.

## First Steps

Given that I currently have a minimally viable content-based recommender, and
Flask application. I need to start by getting the other to recommendation
systems in place. Once those are in place, those models will need to be trained
and then the ensemble model must be built.

## References:

1. http://www.recommend.beer/
2. https://nycdatascience.com/blog/student-works/ninkasi-beer-recommender-system/
3. http://ninkasibeer.herokuapp.com/
