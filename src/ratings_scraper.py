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
REVIEW_TABLE = DYNAMODB.Table('reviews')
BREWERY_TABLE = DYNAMODB.Table('breweries')
STYLE_SKIP_LIST = set([
    'german bock', 'german doppelbock', 'german eisbock', 'german maibock', 'german weizenbock',
    'american brown ale', 'english brown ale', 'english dark mild ale', 'german altbier', 'american black ale',
    'belgian dark ale', 'belgian dubbel', 'german roggenbier', 'scottish ale', 'winter warmer', 'american amber / red lager',
    'european dark lager', 'german märzen / oktoberfest', 'german rauchbier', 'german schwarzbier', 'munich dunkel lager',
    'vienna lager', 'american cream ale', 'bière de champagne / bière brut', 'braggot', 'california common / steam beer',
    'american brut ipa', 'american imperial ipa', 'american ipa', 'belgian ipa', 'english india pale ale (ipa)', 'new england ipa',
    'american amber / red ale', 'american blonde ale', 'american pale ale (apa)', 'belgian blonde ale ', 'belgian pale ale',
    'belgian saison', 'english bitter', 'english extra special / strong bitter (esb)', 'english pale ale', 'english pale mild ale',
    'french bière de garde', 'german kölsch', 'irish red ale', 'american adjunct lager', 'american imperial pilsner', 'american lager',
    'american light lager', 'american malt liquor', 'bohemian pilsener', 'european export / dortmunder', 'european pale lager',
    'european strong lager', 'german helles', 'german kellerbier / zwickelbier', 'german pilsner', 'american imperial porter',
    'american porter', 'baltic porter'
    ]
)


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
            beer_data, beer_reviews = scrape_beer_profile(link)
            put_beer(beer_data, beer_reviews)
            time.sleep(5)

    elif args.styles:
        style_ids = get_style_ids()

        for style, id in style_ids.items():
            if style not in STYLE_SKIP_LIST:
                print('Now scraping this style: {}'.format(style))
                links = get_beer_profile_links(BA_URLS['style'].replace('<style_id>', id))

                for link in links:
                    beer_data, beer_reviews= scrape_beer_profile(link)
                    put_beer(beer_data, beer_reviews )
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

    time.sleep(2)
    beer_reviews = get_all_beer_reviews(url, beer_data['review_count'])

    return beer_data, beer_reviews


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

    beer_stats['review_count'] = int(
        stats_tag.find(
            lambda tag: tag.name == 'span' and tag.get('class') == ['ba-reviews']
        ).text.replace(',', '')
    )

    beer_stats['ratings_count'] = int(
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


def put_beer(beer, reviews, print_message=False):
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

    for idx, review in enumerate(reviews):
        review['review_id'] = ' '.join([beer['brewery'], beer['beer'], str(idx)])
        review['beer'] = beer['beer']
        REVIEW_TABLE.put_item(Item=review)

    if print_message:
        print('PutItem succeeded:"')
        print(json.dumps(response, indent=4, cls=DecimalEncoder))


def get_all_beer_reviews(url, num_reviews):
    '''

    '''
    r_list = []
    scraped_reviews = 0

    cur_reviews = get_beer_reviews(url)
    r_list.extend(cur_reviews)
    scraped_reviews = len(cur_reviews)

    while len(cur_reviews) > 0:
        new_url = url + '?view=beer&sort=&start=' + (str(scraped_reviews))
        time.sleep(2)
        cur_reviews = get_beer_reviews(new_url)
        r_list.extend(cur_reviews)
        scraped_reviews += len(cur_reviews)

    return r_list


def get_beer_reviews(url):
    '''
    Returns a dictionary of all the reviews for the beer found at the url.

    Parameters
    ----------
    url: string:
     The url containing reviews

    Returns
    -------
    reviews: dictionary:
     The reviews
    '''
    beer_reviews = []

    website = get_url(url)
    if website is None:
        return None

    soup = BeautifulSoup(website.text, 'html5lib')

    review_container = soup.find('div', {'id': 'rating_fullview'})
    reviews = review_container.find_all('div', {'id': 'rating_fullview_container'})
    r_list = []

    for review in reviews:
        r_dict = {}
        # get author
        user_tag = review.find('a', {'class': 'username'})
        r_dict['author'] = user_tag['href']

        # get ratings
        #r_dict['overall'] = Decimal(review.find('span', {'class': 'BAscore_norm'}).text)
        rating_string = review.find('span', {'class': 'muted'}).text
        if ' | ' in rating_string:
            r_dict.update(parse_rating_string(rating_string))

        r_dict['text'] = review.text

        # add r_dict to the list of reviews
        r_list.append(r_dict)


    return r_list


def parse_rating_string(rating_string='look: 5 | smell: 5 | taste: 5 | feel: 5 | overall: 5'):
    '''
    Parses a rating string, returning a dictionary.

    Parameters
    ----------
    rating_string: string:
     The string to be parsed.

    Returns
    -------
    ratings_dict: dict:
     A dictionary with key category and value rating.
    '''

    split_strings = rating_string.split(' | ')
    r_dict = {}
    for category in split_strings:
        cat, rating = category.split(':')
        cat = cat.replace(':', '').strip()
        rating = decimal.Decimal(rating.strip())
        r_dict[cat] = rating
    return r_dict


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
