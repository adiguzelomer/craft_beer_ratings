import pandas as pd
import itertools

class PopularityRecommender:
    """Gives recommendations based on the beer group/style and the mean rating
    of the beers.
    """
    def __init__(self):
        self.beer_data = None
        self.style_groups = {
            'bocks': ['german bock', 'german doppelbock ', 'german eisbock',
                    'german maibock', 'german weizenbock'],
            'brown ales': ['american brown ale', 'english brown ale',
                        'english dark mild ale', 'german altbier'],
            'dark ales': ['american black ale', 'belgian dark ale', 'belgian dubbel',
                    'german roggenbier', 'scottish ale', 'winter warmer'],
            'dark lagers': ['american amber / red lager', 'european dark lager',
                    'german märzen / oktoberfest', 'german rauchbier',
                    'german schwarzbier', 'munich dunkel lager',
                    'vienna lager'],
            'hybrid beers': ['american cream ale', 'bière de champagne / bière brut',
                     'braggot', 'california common / steam beer'],
            'india pale ales': ['american brut ipa', 'american imperial ipa',
                        'american ipa', 'belgian ipa',
                        'english india pale ale (ipa)',
                        'new england ipa'],
            'pale ales': ['american amber / red ale', 'american blonde ale',
                  'american pale ale (apa)', 'belgian blonde ale',
                  'belgian pale ale', 'belgian saison', 'english bitter',
                  'english extra special / strong bitter (esb)',
                  'english pale ale', 'english pale mild ale',
                  'french bière de garde', 'german kölsch', 'irish red ale'],
            'pilseners and pale lagers': [
                'american adjunct lager', 'american imperial pilsner',
                'american lager', 'american light lager', 'american malt liquor',
                'bohemian pilsener', 'european export / dortmunder',
                'european pale lager', 'european strong lager', 'german helles',
                'german kellerbier / zwickelbier', 'german pilsner'
                ],
            'porters': ['american imperial porter', 'american porter', 'baltic porter',
                'english porter', 'robust porter', 'smoke porter'],
            'speciality beers': ['chile beer', 'finnish sahti', 'fruit and field beer',
                         'herb and spice beer', 'japanese happoshu',
                         'japanese rice lager', 'low alcohol beer',
                         'pumpkin beer', 'russian kvass', 'rye beer',
                         'scottish gruit / ancient herbed ale', 'smoke beer'],
            'stouts': ['american imperial stout ', 'american stout',
               'english oatmeal stout', 'english stout',
               'english sweet / milk stout', 'foreign / export stout',
               'irish dry stout', 'russian imperial stout'],
            'strong ales': ['american barleywine', 'american imperial red ale',
                    'american strong ale', 'american wheatwine ale',
                    'belgian quadrupel (quad)', 'belgian strong dark ale',
                    'belgian strong pale ale', 'belgian tripel',
                    'british barleywine', 'english old ale',
                    'english strong ale', 'scotch ale / wee heavy'],
            'wheat beers': ['american dark wheat ale', 'american pale wheat ale',
                    'belgian witbier', 'berliner weisse',
                    'german dunkelweizen', 'german hefeweizen',
                    'german kristalweizen'],
            'wild/sour beers': ['american brett', 'american wild ale', 'belgian faro',
                        'belgian fruit lambic', 'belgian gueuze',
                        'belgian lambic', 'flanders oud bruin',
                        'flanders red ale', 'leipzig gose' ]
        }
        return None

    def fit(self, beer_data: pd.DataFrame)->None:
        """Given a DataFrame with at beers name, brewery, style, and average
        rating, returns nothing.

        Parameters
        ----------
        beer_data: pd.DataFrame:
          A dataframe with the columns: beer, brewery, style, mean rating

        Returns
        -------
        None
        """
        columns = ['beer', 'brewery', 'style', 'rating']
        self.beer_data = beer_data[columns]
        return None

    def styles(self)->list:
        """Returns the styles this object can predict on.

        Parameters
        ----------
        None

        Returns
        -------
        styles: list
          A list of styles that can be used to make predictions
        """
        return list(itertools.chain.from_iterable(self.style_groups.values()))

    def groups(self):
        """Returns the styles this object can predict on.

        Parameters
        ----------
        None

        Returns
        -------
        styles: list
          A list of styles that can be used to make predictions
        """
        return list(self.style_groups.keys())

    def predict_style(self, style: str):
        pass

    def predict_group(self, group: str):
        pass
