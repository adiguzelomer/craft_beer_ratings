

class CollaborativeRecommender:
    """A user-user collaborative recommender.
    """
    def __init__(self):
        self.utility_mat, self.users, self.beers = None, None, None

    def fit(self, reviews: pd.DataFrame) -> None:
        """Fits to the reviews provided.

        Parameters
        ----------
        reviews: pd.DataFrame
          Contains the users, beers, ratings, brewery

        Returns
        -------
        None
        """
        pass

    def predict(self, user_vector: np.array) -> list:
        """Given a vector representing a user, returns a list of suggested
        beers.

        Parameters
        ----------
        user_vector: np.array:
          A vector of beer ratings

        Returns
        -------
        beers: list:
          A list of beers the user should try.
        """
        pass
