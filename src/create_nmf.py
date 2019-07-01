import sys
import os
import dotenv
# Probably more overhead than it's worth, but this ensures that our environment
# variables are set to the proper paths.
cwd = os.getcwd()
new_cwd = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
os.chdir(new_cwd)
dotenv.load_dotenv()
os.chdir(cwd)
del cwd, new_cwd

import argparse

import numpy as np
import pandas as pd

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)))))
import nlp

def main():
    """Creates and pickles an NMF model and the associated W matrix.
    """
    arg_parser = argparse.ArgumentParser(
        description='Creates and pickles an NMF model '
                    'and the associated W matrix.'
    )
    arg_parser.add_argument(
        '--n_beers', default=None, help='The number of beers to sample.'
    )
    arg_parser.add_argument(
        '--beers_csv', default=os.environ['BEERS_CSV'],
        help='The location of the beers csv.'
    )
    arg_parser.add_argument(
        '--reviews_csv', default=os.environ['REVIEWS_CSV'],
        help='The location of the reviews csv.'
    )
    arg_parser.add_argument(
        '--max_df', default=.95,
        help='The maximum document frequency.'
    )
    arg_parser.add_argument(
        '--max_features', default=5000
        help='The maximum number of features to consider.'
    )
    arg_parser.add_argument(
        '--n_topics', default=15,
        help='The maximum number of topics to assess.'
    )
    args = arg_parser.parse_args()

    beers_df, reviews_df = nlp.load_data(args.beers_csv, args.reviews_csv, args.n_beers)
    reviews = nlp.clean_documents(reviews_df['text'].values)

    # Create TF-IDF matrix
    tf_idf_vectorizer = TfidfVectorizer(
        max_df=args.max_df, max_features=args.max_features
        )
    tf_idf = tf_idf_vectorizer.fit_transform(reviews)

    return 0



if __name__ == "__main__":
    main()
