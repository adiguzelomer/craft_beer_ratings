import os
import sys
import datetime as dt
import argparse
import boto3
import json
import decimal
import re
# import pandas as pd
import requests
from bs4 import BeautifulSoup

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

# The basic URLs that will be scraped.
# Every URL except for top_rated the item enclosed in <>
# must be replaced with an appropriate value.

BA_URLS = {
    'top_rated': 'https://www.beeradvocate.com/lists/top/',
    'style': 'https://www.beeradvocate.com/lists/style/<style_id>',
    'location:': 'https://www.beeradvocate.com/lists/<loc>',
    'brewery': 'https://www.beeradvocate.com/beer/profile/<brewery_id>',
    'beer': 'https://www.beeradvocate.com/beer/profile/<brewery_id>/<beer_id>'
    'home': 'https://www.beeradvocate.com'
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

def get_beer_profile_links(url):
    """
    Given a url, returns a list of all the beer
    profile urls found on that page.

    Parameters
    ----------
    url: string:
      An url with a table of beer profile links

    Returns
    -------
    profile_urls: list of strings
      A list of all the profile links found on that page.
    """

    ratings_page = get_url(url)
    if ratings_page is None:
        return None

    soup = BeautifulSoup(ratings_page.text, 'html5lib')

    table = soup.find(name='table')

    links = table.find_all(
        lambda tag: tag.has_attr('href'))

    regex = re.compile(r'/beer/profile/[\d]*/[\d]*/')
    links_list = [link.get('href') for link in links if regex.search(link.get('href'))]

    return links_list


def get_style_ids():
    """
    Scrapes the style ids from the top_rated page.

    Parameters
    ----------
    None

    Returns
    -------
    style_ids: dictionary:
      The keys are the names of the style the value is the ids.
      For example, 'american_ipa': '116'
    """

    top_rated = get_url(BA_URLS['top_rated'])
    if top_rated is None:
        return None

    top_rated_soup = BeautifulSoup(top_rated.text, 'html5lib')
    style_list = top_rated_soup.find(
        lambda tag: tag.name == 'form' and tag.get('name') == 'styles')

    style_ids = {}
    for style in style_list.find_all(
        lambda tag: tag.name == 'option' and not tag.has_attr('disabled')
    ):
        if style.get('value') == '':
            continue
        name = style.text.lower().replace(' ', '_')
        style_ids[name] = style.get('value')

    return style_ids


def get_url(url):
    """
    Wrapper for requests.get that includes status and error messages.

    Parameters
    ----------
    url: string:
      The url of the website to be retrieved.

    Returns
    -------
    website: requests.models.Response
      The website that was retrieved.
    None:
      Returns None if the website was not retrieved.
    """

    try:
        website = requests.get(url)
    except Exception as e:
        print(
            'Failed to retrieve {}\nError message: {}'.format(
                url, e),
            file=sys.stderr,
            flush=True
        )
        return None

    if website.status_code == 200:
        print(
            'Retrieved {} at {}'.format(
                url, dt.datetime.now())
        )
    else:
        print(
            'Attempted to retreive {} at {}\nStatus Code: {}'.format(
                url, dt.datetime.now(), website.status_code),
            file=sys.stderr,
            flush=True
        )
        return None

    return website


def put_beer(beer, table, print_message=False):
    """
    Loads the beer to the DynamoDB table.

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
