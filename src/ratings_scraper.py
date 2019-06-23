import os
import sys
import time
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
# The home url can be appended with the data as well.
BA_URLS = {
    'top_rated': 'https://www.beeradvocate.com/lists/top/',
    'style': 'https://www.beeradvocate.com/lists/style/<style_id>',
    'location:': 'https://www.beeradvocate.com/lists/<loc>',
    'brewery': 'https://www.beeradvocate.com/beer/profile/<brewery_id>',
    'beer': 'https://www.beeradvocate.com/beer/profile/<brewery_id>/<beer_id>',
    'home': 'https://www.beeradvocate.com'
}
AWS_REGION = 'us-east-2'
DYNAMODB = boto3.resource('dynamodb', region_name=AWS_REGION)
BEER_TABLE = DYNAMODB.Table('beers')
BREWERY_TABLE = DYNAMODB.Table('breweries')

def main():
    arg_parser = argparse.ArgumentParser(
        description='Scrapes Beeradvocate for ratings data.'
    )
    arg_parser.add_argument('--url', help='A particular url to be scraped.')
    arg_parser.add_argument('--styles', help='Will scrape the tops beers'
                                             ' from each style.',
                            action='store_true')
    args = arg_parser.parse_args()
    if args.url is not None:
        print(args.url)

        links = get_beer_profile_links(args.url)

        for link in links:
            beer_data = scrape_beer_profile(link)
            put_beer(beer_data)
            time.sleep(5)

    elif args.styles:
        style_ids = get_style_ids()

        for style, id in style_ids.items():
            print('Now scraping this style: {}'.format(style))
            links = get_beer_profile_links(BA_URLS['style'].replace('<style_id>', id))

            for link in links:
                beer_data = scrape_beer_profile(link)
                put_beer(beer_data)
                time.sleep(5)

            print('Completed scraping this style: {}'.format(style))


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
    links_list = [BA_URLS['home'] + link.get('href') for link in links if regex.search(link.get('href'))]

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
        name = style.text.lower()
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


def scrape_beer_profile(url):
    """
    Given an the url for a beer's profile page, scrapes the data
    and returns it as a dictionary.

    Parameters
    ----------
    url: string:
      The url for the page to be scraped.

    Returns
    -------
    beer_data: dictionary:
      The data scraped from the page. (Does not include reviews.)
    """

    beer_data = {'beer_url': url}

    website = get_url(url)
    if website is None:
        return None

    soup = BeautifulSoup(website.text, 'html5lib')

    title_bar = soup.find(
        lambda tag: tag.name == 'div' and tag.get('class') == ['titleBar']
    )
    beer_data['beer'] = title_bar.find('h1').text.split(' |')[0].lower()

    beer_data.update(get_beer_info(soup))

    score_tag = soup.find(
        lambda tag: tag.name == 'span' and tag.get('class') == ['ba-ravg']
    )
    beer_data['rating'] = decimal.Decimal(score_tag.text)

    beer_data.update(get_beer_stats(soup))

    return beer_data


def get_beer_info(soup):
    '''
    Extracts the information from the beer info box.

    Parameters
    ----------
    soup: bs4.BeautifulSoup
      The page containing the beer information

    Returns
    -------
    beer_info: dictionary
      A dictionary containing the beer information.
    '''
    beer_data = {}

    beer_info = soup.find(
        lambda tag: tag.name == 'div' and tag.get('id') == 'info_box'
    )

    link_tags = beer_info.find_all(
        lambda tag: tag.name == 'a' and tag.has_attr('href')
    )

    brewery_link_regex = re.compile(r'/beer/profile/[\d]*/')

    for tag in link_tags:
        if brewery_link_regex.search(tag.get('href')):
            beer_data['brewery'] = tag.find('b').text.lower()
            beer_data['brewery_profile_url'] = tag.get('href').lower()
        elif tag.get('href').startswith('/beer/styles/'):
            beer_data['style'] = tag.find('b').text.lower()

    found = re.search(r'[\d]*.[\d]*%', beer_info.text)
    if found is not None:
        beer_data['abv'] = decimal.Decimal(
            found.group(0).replace('%', '')
        )

    notes_idx = beer_info.text.find('Description:\n\n') + 14
    beer_data['note'] = beer_info.text[notes_idx:].strip()



    return beer_data


def get_beer_stats(soup):
    '''
    Extracts the information from the beer stats box.

    Parameters
    ----------
    soup: bs4.BeautifulSoup
      The webpage containing the stats box

    Returns
    -------
    beer_stats: dictionary
      A dictionary containing the statistics
    '''
    beer_stats = {}

    stats_tag = soup.find(
        lambda tag: tag.name == 'div' and tag.get('id') == 'item_stats'
    )

    found = re.search(r'#[\d,]*', stats_tag.text)
    if found is not None:
        beer_stats['rank'] = int(
            found.group(0).replace('#', '').replace(',', '')
        )

    beer_stats['reviews'] = int(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-reviews']
        ).text.replace(',', '')
    )

    beer_stats['ratings'] = int(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-ratings']
        ).text.replace(',', '')
    )

    beer_stats['pdev'] = decimal.Decimal(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-pdev']
        ).text.replace('%', '')
    )

    beer_stats['wants'] = int(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-wants']
        ).text.replace(',', '')
    )

    beer_stats['gots'] = int(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-gots']
        ).text.replace(',', '')
    )

    link_tags =  stats_tag.find_all(
            lambda tag: tag.name == 'a'
                and tag.has_attr('href')
                and tag.get('href').endswith('FT')
    )

    # There are two tags that match the above search.
    # The number of trades is found in the second tag.
    beer_stats['trade'] = int(link_tags[1].text.replace(',', ''))

    return beer_stats


def put_beer(beer, print_message=False):
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
    response = BEER_TABLE.put_item(
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
