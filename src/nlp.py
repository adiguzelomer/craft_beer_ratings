import nltk
from nltk.tokenize import SpaceTokenizer
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer

import pandas as pd
import numpy as np
import re

from ast import literal_eval

def main():
    print('Nothing to see here. Import this file instead.')
    return 0

def clean_documents(documents: np.array) -> np.array:
    """Given an np.array of documents, returns a np.array of documents
    that have had stopwords removed and passed through the Lancaster
    Stemmer.
    """
    new_docs = [remove_bad_text(document) for document in documents]
    return new_docs

def get_brew_beer_col(reviews_df: pd.DataFrame) -> pd.DataFrame:
    """Returns the updated dataframe.
    """
    reviews_df['brew_beer'], reviews_df['review_num'] = zip(
        *reviews_df['review_id'].apply(get_review_number)
        )

    return reviews_df

def get_review_number(review_id: str) -> tuple:
    """Returns the review number from the review id.
    """
    match = re.match('(.*?)([0-9]+)$', review_id)
    return match.group(1).strip(), int(match.group(2))

def remove_bad_text(text: str) -> str:
    """Given a review string, removes most of the bad text found
    at the beginning and end of the raw text.
    """
    # 4.4/5\xa0\xa0rDev +0.2%look: 4 | smell: 4.5 | taste: 4.5 | feel: 3.75 | overall: 4.5
    # \xa03,032 charactersTHANAT0PSIS, Aug 28, 2016

    cut_text = text # .replace('\n', ' ')
    # Strip front to 'overall: X.X'
    # print("NEW DOCUMENT")
    # print(repr(cut_text))
    result = re.search('(?<=overall:\s\d)((.|\n)*)', cut_text)
    if result is not None:
        cut_text = result.group(0)
    else:
        result = re.search('(?<=%)((.|\n)*)', cut_text)
        cut_text = result.group(0)

    # Strip back after '\xa
    # Use repr to find escape characters
    xa_idx = repr(cut_text).find('\\xa')
    cut_text = literal_eval(repr(cut_text)[:xa_idx] + repr(cut_text)[-1])
    if cut_text.startswith('.25') or cut_text.startswith('.75'):
        cut_text = cut_text[3:]
    elif cut_text.startswith('.'):
        cut_text = cut_text[2:]

    return cut_text


def strip_punc(documents: list, punc = '.!,;:\'"\(\)\[\]\n/') -> list:
    '''Given documents, return the documents with punctuation removed.
    '''
    rgx = re.compile('[{}]'.format(punc))
    documents = [rgx.sub(' ', document.lower()) for document in documents]

    return documents

def stem_and_rem_stopwords(documents:list, additional_stopwords: list = []):
    """Returns a list of documents that have been stemmed and
    had stopwords removed.
    """
    s_words = set(stopwords.words('english') + additional_stopwords)
    stemmer = LancasterStemmer()

    processed_documents =[]
    for document in documents:
        tokens = document.split()
        processed_documents.append(
            ' '.join([token for token in tokens if token not in s_words])
            )

    return processed_documents
