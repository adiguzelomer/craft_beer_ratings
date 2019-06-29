import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd


AWS_REGION = 'us-east-2'
DYNAMODB = boto3.resource('dynamodb', region_name=AWS_REGION)
BEER_TABLE = DYNAMODB.Table('beers')
REVIEW_TABLE = DYNAMODB.Table('reviews')
BREWERY_TABLE = DYNAMODB.Table('breweries')

STRING_COLUMNS = [
    'beer', 'beer_url', 'brewery', 'brewery_profile_url', 'note', 'style'
]
NUM_COLUMNS = [
    'abv', 'gots', 'pdev', 'rank', 'rating', 'ratings_count', 'review_count',
    'trade', 'wants'
]
INT_COLUMNS = [
    'gots', 'rank', 'rating', 'ratings_count', 'review_count', 'trade', 'wants'
]
FLOAT_COLUMNS = ['abv', 'pdev', 'rating']

REVIEW_STRING_COLUMNS = ['author', 'beer', 'review_id', 'text']
REVIEW_NUM_COLUMNS = ['feel', 'look', 'overall', 'smell', 'taste']


def main():
    print("Nothing to see here. This file is meant to be imported.")


def get_beer_df():
    '''
    Returns a Pandas DataFrame object consisting of the full beer table.
    '''

    response = BEER_TABLE.scan()
    beer_df = pd.DataFrame(response['Items'])
    last_key = response.get('LastEvaluatedKey', None)
    while last_key is not None:
        response = BEER_TABLE.scan(ExclusiveStartKey=last_key)
        beer_df = pd.concat([beer_df, pd.DataFrame(response['Items'])])
        last_key = response.get('LastEvaluatedKey', None)

    # Not sure that I actually need to do this.
    # The columns seem to be Decimal's at this point.
    beer_df[STRING_COLUMNS] = beer_df[STRING_COLUMNS].astype(str)
    beer_df[NUM_COLUMNS] = beer_df[NUM_COLUMNS].astype(float)
    # beer_df[INT_COLUMNS] = beer_df[INT_COLUMNS].astype(int)
    # beer_df[FLOAT_COLUMNS] = beer_df[FLOAT_COLUMNS].astype(float)

    return beer_df


def get_reviews_df(beers: list, n: int = 20) -> pd.DataFrame:
    '''
    Returns a Pandas DataFrame object consisting of the first n reviews
    for every beer in beer list.
    '''
    reviews_df = pd.DataFrame()

    for beer in beers:
        # Iterate through the list of beers and add those rows to a dataframe.
        for review in range(n):
            response = REVIEW_TABLE.query(
                    KeyConditionExpression=Key('review_id').eq(
                        beers[0] + ' ' + str(review)
                    )
            )
            reviews_df = pd.concat(
                [reviews_df, pd.DataFrame(response['Items'])]
                )

    reviews_df[REVIEW_STRING_COLUMNS] = (
        reviews_df[REVIEW_STRING_COLUMNS].astype(str)
        )
    reviews_df[REVIEW_NUM_COLUMNS] = (
        reviews_df[REVIEW_NUM_COLUMNS].astype(float)
        )
    return reviews_df


def get_all_reviews_df():
    '''
    Returns a Pandas DataFrame object consisting of all reviews.
    '''
    response = REVIEW_TABLE.scan()
    reviews_df = pd.DataFrame(response['Items'])
    last_key = response.get('LastEvaluatedKey', None)
    while last_key is not None:
        response = REVIEW_TABLE.scan(ExclusiveStartKey=last_key)
        reviews_df = pd.concat([reviews_df, pd.DataFrame(response['Items'])])
        last_key = response.get('LastEvaluatedKey', None)

    reviews_df[REVIEW_STRING_COLUMNS] = (
        reviews_df[REVIEW_STRING_COLUMNS].astype(str)
        )
    reviews_df[REVIEW_NUM_COLUMNS] = (
        reviews_df[REVIEW_NUM_COLUMNS].astype(float)
        )
    return reviews_df


if __name__ == "__main__":
    main()
