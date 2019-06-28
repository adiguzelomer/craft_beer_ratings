import boto3
import pandas as pd


AWS_REGION = 'us-east-2'
DYNAMODB = boto3.resource('dynamodb', region_name=AWS_REGION)
BEER_TABLE = DYNAMODB.Table('beers')
REVIEW_TABLE = DYNAMODB.Table('reviews')
BREWERY_TABLE = DYNAMODB.Table('breweries')

STRING_COLUMNS = ['beer', 'beer_url', 'brewery', 'brewery_profile_url', 'note', 'style']
NUM_COLUMNS = ['abv', 'gots', 'pdev', 'rank', 'rating', 'ratings_count', 'review_count', 'trade', 'wants']
INT_COLUMNS = ['gots', 'rank', 'rating', 'ratings_count', 'review_count', 'trade', 'wants']
FLOAT_COLUMNS = ['abv', 'pdev', 'rating']

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

    # Not sure that I actually need to do this. The columns seem to be Decimal's at this point.
    beer_df[STRING_COLUMNS] = beer_df[STRING_COLUMNS].astype(str)
    beer_df[NUM_COLUMNS] = beer_df[NUM_COLUMNS].astype(float)
    # beer_df[INT_COLUMNS] = beer_df[INT_COLUMNS].astype(int)
    # beer_df[FLOAT_COLUMNS] = beer_df[FLOAT_COLUMNS].astype(float)
    return beer_df

def get_reviews_df(beers: list, n: int=20) -> pd.DataFrame:
    '''
    Returns a Pandas DataFrame object consisting of the first n reviews for every beer
    in beer list.
    '''
    # Iterate through the list of beers and add those rows to a dataframe.
    reviews_df = pd.DataFrame()
    for beer in beers:
        response = REVIEW_TABLE.query(
                #INPUT QUERY HERE
        )
        
        reviews_df = pd.concat([reviews_df, pd.DataFrame(response['Items'])])
        
    return reviews_df
    
    
    
    return pd.DataFrame()

if __name__ == "__main__":
    main()
