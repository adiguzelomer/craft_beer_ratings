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

import numpy as np
import pandas as pd

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
        '--n_beers', default=None, help='The number of beers to sample.'
    )
    arg_parser.add_argument(
        '--beers_csv', default=os.environ['BEERS_CSV'],
        help='The location of the beers csv.'
    )
    arg_parser.add_argument(
        '--reviews_csv', default=os.environ['REVIEWS_CSV'],
        help='The location of the reviews csv.'
    )
    args = arg_parser.parse_args()

    beers_df, reviews_df = load_data(args.beers_csv, args.reviews_csv, args.n_beers)

    return 0

def load_data(beers_fpath, reviews_fpath, n_beers: int = None) -> tuple:
    """Loads the beer and review dataframes.
    """
    # Load the beer and reviews dataframes
    beers_df = pd.read_csv(beers_fpath)

    if n_beers is not None:
        beers_sample = beers_df.sample(n_beers)
    else:
        beers_sample = beers_df

    # Add the review_id column, and the brew_beer column
    beers_sample = nlp.add_review_id_col(beers_sample)
    reviews_df = pd.read_csv(reviews_fpath)
    reviews_df = nlp.get_brew_beer_col(reviews_df)

    if n_beers is not None:
        reviews_sample = nlp.get_reviews_sample(
            reviews_df,
            list(beers_sample['review_id'])
        )
    else:
        reviews_sample = reviews_df

    return beers_sample, reviews_sample

if __name__ == "__main__":
    main()
