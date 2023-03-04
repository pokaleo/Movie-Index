"""
------------------------------------------------------------
Author: Leo LI
Date: 28th Feb 2023
Description: Utility functions providing useful static
methods
------------------------------------------------------------
"""
from string import punctuation

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def to_lowercase(term):
    return term.lower()


def remove_punctuation(term, plot=False):
    if plot:
        return term.lstrip(punctuation).rstrip(punctuation)
    else:
        return term.rstrip(",")
    return result


def stem_data(term):
    return SnowballStemmer(language='english').stem(term)


def is_phrase_search(query):
    if query.startswith("\"") and query.endswith("\"") and len(query.split())>1:
        return True
    else:
        return False


def remove_stop_words(query, stop_words):
    temp_list = []
    for token in query:
        if token not in stop_words:
            temp_list.append(token.lstrip(punctuation).rstrip(punctuation))
    return temp_list
