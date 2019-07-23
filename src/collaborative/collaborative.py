import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:
    """A user-user collaborative recommender.
    """
    def __init__(self, neighborhood_size):
        self.utility_mat, self.users, self.brew_beers = None, None, None
        self.neighborhood_size = neighborhood_size
        self.neighborhoods = None
        self.similarity_mat = None

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
        pivot_table = reviews.pivot_table(
            index='brew_beer', columns='author', values='overall')
        self.utility_mat = csr_matrix(pivot_table.values)
        self.users = list(pivot_table.columns)
        self.brew_beers = list(pivot_table.index)
        self.similarity_mat = cosine_similarity(self.utility_mat)

    def _set_neighborhoods(self):
        least_to_most_sim_indexes = np.argsort(self.similarity_mat, 1)
        self.neighborhoods = least_to_most_sim_indexes[
            :, -self.neighborhood_size:]

    def predict(self, brew_beer: str, n: int = 5) -> list:
        """Given a string representing a beer, returns a list of suggested
        beers.

        Parameters
        ----------
        brew_beer: str:
          A string with the brewery and beer

        Returns
        -------
        beers: list:
          A list of beers the user should try.
        """
        # Get the brew_beer's index
        brew_idx = self.brew_beers.index(brew_beer)
        # Gets the columns that have reviews for this beer
        nearby_beers = self.similarity_mat[brew_idx].argsort()[:-6:-1]
        # Predictions go in here
        return [self.brew_beers[idx] for idx in nearby_beers]
