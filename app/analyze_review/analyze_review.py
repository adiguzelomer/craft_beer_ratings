import sys
sys.path.append('/Users/brettcastellanos/galvanize/craft_beer_ratings/src')
import re
import pickle
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
# import src.popularity
# import src.collab


def main():
    print('Nothing to see here. Import me instead.')
    return 0

class ReviewProcessor:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
        self.punctuation = '.!,;:\'"\(\)\[\]\n/'
        self.rgx = re.compile('[{}]'.format(self.punctuation))
        self.reviews_df = pd.read_csv('data/1-clean/clean_reviews.csv')

        with open('models/1-nmf/TF-IDF-Vectorizer.pkl','rb') as p:
            self.tfidf_vectorizer = pickle.load(p)

        self.stemmer = LancasterStemmer()

        with open('models/1-nmf/NMF.pkl','rb') as p:
            self.NMF = pickle.load(p)

        with open('models/1-nmf/W.pkl','rb') as p:
            self.W = pickle.load(p)

        with open('models/2-collab/collab_rec.pkl', 'rb') as p:
            self.collab = pickle.load(p)

        with open('models/3-popularity/pop_rec.pkl', 'rb') as p:
            self.popularity = pickle.load(p)

        return None

    def predict(self, input_review: str = 'I like beer.'):
        """Given text about beer, returns a set of recommendations.
        """

        clean_review = self.clean_review(input_review)
        tf_idf_vec = self.get_tfidf_vector(clean_review)
        topic_vec = self.get_topic_vector(tf_idf_vec)[0]
        # print(topic_vec)
        reviews_1 = self.get_topic_reviews(np.argmax(topic_vec))
        reviews_2 = self.get_topic_reviews(np.argsort(topic_vec)[-2])
        reviews_3 = self.get_topic_reviews(np.argsort(topic_vec)[-3])

        assert type(reviews_1) == pd.DataFrame
        assert type(reviews_2) == pd.DataFrame
        assert type(reviews_3) == pd.DataFrame

        top_10_reviews = pd.concat(
            (reviews_1.iloc[:4, :], reviews_2.iloc[:3, :], reviews_3.iloc[:3, :]),
            axis=0
        )
        # print(top_9_reviews)
        brew_beers = []
        for brew_beer in top_10_reviews['brew_beer']:
            brew_beers.extend(self.collab.predict(brew_beer)[0:2])
        brew_beers = set(brew_beers)
        # You now have a list of beers close to the beers in the topic.
        # You can recommend a subset of these beers.

        return brew_beers








    def get_topic_reviews(self, topic_idx):
        """Given a topic idx, returns the top ten reviews associated with that
        topic.
        """
        top_reviews_idx = np.argsort(self.W[:, topic_idx])[-1:-11:-1]
        return self.reviews_df.iloc[top_reviews_idx]

    def get_topic_vector(self, tf_idf_vector):
        """Given a tf_idf_vector, return the topic vector.
        """
        topic_vector = tf_idf_vector.dot(self.NMF.components_.T)
        return topic_vector

    def get_tfidf_vector(self, review):
        """Given a review string, returns the TF-IDF Vector for that review.
        """
        return self.tfidf_vectorizer.transform([review])

    def clean_review(self, review):
        """Given a review, return a review ready to be vectorized.
        """
        clean_review = self.remove_punctuation(review)
        clean_review = self.remove_stopwords(clean_review)
        split_words = clean_review.split()
        stemmed_review = ' '.join(
            [self.stemmer.stem(word) for word in split_words]
        )
        return stemmed_review

    def remove_punctuation(self, review):
        """Given a review, return the review without punctuation.
        """
        return self.rgx.sub(' ', review.lower())

    def remove_stopwords(self, review):
        """Given a review, return the review minus stopwords.
        """
        split_words = review.split()

        return ' '.join(
            [word for word in split_words if word not in self.stopwords]
            )
