import db_access.db_access as db
import pandas as pd
import os
import sys

def main():

    cur_dir_path = os.path.dirname(os.path.abspath(__file__))
    print(cur_dir_path)
    filename = os.path.join(cur_dir_path, os.path.pardir, 'data/beers.csv')
    print(filename)
    reviews_df = db.get_beer_df()
    reviews_df.to_csv(filename, index=False)

    return 0


if __name__ == "__main__":
    main()
