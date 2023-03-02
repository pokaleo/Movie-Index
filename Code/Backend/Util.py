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


def to_lowercase(terms):
    result = []
    for term in terms:
        result.append(term.lower())
    return result


def remove_punctuation(terms, plot=False):
    result = []
    if plot:
        for term in terms:
            result.append(term.lstrip(punctuation).rstrip(punctuation))
    else:
        for term in terms:
            result.append(term.rstrip(","))
    return result


def stem_data(terms):
    result = []
    for term in terms:
        result.append(SnowballStemmer(language='english').stem(term))
    return result


def remove_stopwords(terms):
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    result = []
    for term in terms:
        if term not in stop_words:
            result.append(SnowballStemmer(language='english').stem(term))
    return result
