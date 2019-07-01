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
import pickle
import boto3
from botocore.exceptions import ClientError
import logging
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
        '--n_beers', default=None, type=int, help='The number of beers to sample.'
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
        '--max_df', default=.95, type=float,
        help='The maximum document frequency.'
    )
    arg_parser.add_argument(
        '--max_features', default=5000, type=int,
        help='The maximum number of features to consider.'
    )
    arg_parser.add_argument(
        '--n_topics', default=15, type=int,
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

    # Create NMF
    nmf_model = NMF(n_components=args.n_topics)
    W = nmf_model.fit_transform(tf_idf)

    # Pickle the results
    with open('pickles/W.pkl', 'wb') as p:
        pickle.dump(W, p)

    with open('pickles/NMF.pkl', 'wb') as p:
        pickle.dump(nmf_model, p)

    with open('pickles/TF-IDF-Vectorizer.pkl', 'wb') as p:
        pickle.dump(tf_idf_vectorizer, p)

    with open('pickles/TF-IDF.pkl', 'wb') as p:
        pickle.dump(tf_idf, p)

    upload_file('pickles/W.pkl', 'brett-craft-beer')
    upload_file('pickles/NMF.pkl', 'brett-craft-beer')
    upload_file('pickles/TF-IDF-Vectorizer.pkl', 'brett-craft-beer')
    upload_file('pickles/TF-IDF.pkl', 'brett-craft-beer')

    return 0

# Copied from boto3 tutorials
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    main()
