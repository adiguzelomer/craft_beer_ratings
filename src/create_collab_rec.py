from src.collaborative.collaborative import CollaborativeRecommender
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
