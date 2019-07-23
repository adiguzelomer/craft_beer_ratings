from collaborative.collaborative import CollaborativeRecommender
import argparse
import pickle
import boto3
from botocore.exceptions import ClientError
import logging
import numpy as np
import pandas as pd


def main():
    """Creates and pickles a CollaborativeRecommender.
    """
    arg_parser = argparse.ArgumentParser(
        description='Creates and pickles a CollaborativeRecommender.'
    )

    arg_parser.add_argument(
        '--reviews_csv', default='data/1-cleaned/cleaned_reviews.csv',
        help='The location of the reviews csv.'
    )
    args = arg_parser.parse_args()
    print('Loading the data')
    reviews = pd.read_csv('data/1-clean/clean_reviews.csv',
                          usecols=['brew_beer', 'beer', 'overall', 'author'])

    print('Fitting the Model')
    rec = CollaborativeRecommender(50)
    rec.fit(reviews)

    print('Pickling the model')
    with open('models/2-collaborative-item-item/collab_rec.pkl', 'wb') as f:
        pickle.dump(rec, f)

    print('Uploading to S3')
    upload_file('models/2-collaborative-item-item/collab_rec.pkl', 'brett-craft-beer')

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
