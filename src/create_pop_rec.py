from popularity.popularity import PopularityRecommender
import pandas as pd
import pickle
import boto3
from botocore.exceptions import ClientError
import logging


def main():
    pop_rec = PopularityRecommender()

    beer_data = pd.read_csv('data/2-clean/beers_trunc.csv')

    print('Fitting the model')
    pop_rec.fit(beer_data)

    print('Pickling the model')
    with open('models/3-popularity/pop_rec1.pkl', 'wb') as f:
        pickle.dump(pop_rec, f)

    print('Uploading to S3')
    upload_file('models/3-popularity/pop_rec1.pkl', 'brett-craft-beer')

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
