import os
import sys
if os.path.dirname(__file__) not in sys.path:
    print("Appendeded current path to sys.path")
    sys.path.append(os.path.dirname(__file__))

import argparse
import boto3
import json
import decimal
# import pandas as pd
from bs4 import BeautifulSoup



# The basic URLs that will be scraped.
# Every URL except for top_rated the item enclosed in <>
# must be replaced with an appropriate value.

BA_URLS = {
    'top_rated': 'https://www.beeradvocate.com/lists/top/'
    'style': 'https://www.beeradvocate.com/lists/style/<style_id>'
    'location:': 'https://www.beeradvocate.com/lists/<loc>'
    'brewery': 'https://www.beeradvocate.com/beer/profile/<brewery_id>'
    'beer': 'https://www.beeradvocate.com/beer/profile/<brewery_id>/<beer_id>'
}


def main():
    arg_parser = argparse.ArgumentParser(
        description='Scrapes Beeradvocate for ratings data.'
    )
    arg_parser.parse_args()

    # dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    # table = dynamodb.Table('beer_ratings')
    # print(type(table))
    # beer = {
    #     'beer': 'Sensory Overload',
    #     'brewery': 'Olögy',
    #     'rating': decimal.Decimal('4.9')
    # }

    # put_beer(beer, table, True)

    return 0

def get_style_ids():


def put_beer(beer, table, print_message=False):
    """
    Loads the beer to the DynanoDB table.

    Parameters
    ----------
    beer: dictionary
      The object to be loaded to DynamoDB
    table: boto3.resources.factory.dynamodb.Table
      The table to which the beer will be inserted
    print_message: bool: default=False
      Whether to print the response message.
    """
    response = table.put_item(
        Item=beer
    )

    if print_message:
        print('PutItem succeeded:"')
        print(json.dumps(response, indent=4, cls=DecimalEncoder))


# The following class is taken from the AWS Tutorial found at:
# https://docs.aws.amazon.com/amazondynamodb/
# latest/developerguide/GettingStarted.Python.03.html
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


if __name__ == "__main__":
    main()
