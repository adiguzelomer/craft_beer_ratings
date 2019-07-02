import pandas as pd
import numpy as np

import nlp as nlp

def main():
    beer_df, reviews_df = nlp.load_data('data/beers.csv', 'data/reviews.csv', 50)

    print(beer_df.head())
    return 0


if __name__ == "__main__":
    main()
