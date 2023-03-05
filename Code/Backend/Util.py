"""
------------------------------------------------------------
Author: Leo LI
Date: 28th Feb 2023
Description: Utility functions providing useful static
methods
------------------------------------------------------------
"""
from string import punctuation
from nltk.stem.snowball import SnowballStemmer


def to_lowercase(term):
    """
    Case casting

    Args:
        term: String -> string to be proceed

    Returns:
        String -> Original string in lowercase
    """
    return term.lower()


def remove_punctuation(term, plot=False):
    """
    Punctuations removal

    Args:
        term: String -> string to be proceed
        plot: Bool -> if the string is in the field of plots

    Returns:
        String -> Original string with leading and trailing punctuations removed
    """
    if plot:
        return term.lstrip(punctuation).rstrip(punctuation)
    else:
        return term.rstrip(",")


def stem_data(term):
    """
    Stemming

    Args:
        term: String -> String to be proceed

    Returns:
        String -> Original string stemmed with SnowballStemmer
    """
    return SnowballStemmer(language='english').stem(term)


def is_phrase_search(query):
    """
    Check if the query is phrase search

    Args:
        query: String -> Query String

    Returns:
        Bool -> True if it's phrase search, vice versa
    """
    if query.startswith("\"") and query.endswith("\"") and len(query.split()) > 1:
        return True
    else:
        return False


def remove_stop_words(query, stop_words):
    """
    Remove stopwords for a list of query words

    Args:
        query: List -> a list of query words
        stop_words: List -> a list of stop words

    Returns:
        List -> A list of query words with stop words removed
    """
    temp_list = []
    for token in query:
        if token not in stop_words:
            temp_list.append(token.lstrip(punctuation).rstrip(punctuation))
    return temp_list
