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

"""
Case casting

Args:
    term: String -> string to be proceed

Returns:
    String -> Original string in lowercase
"""


def to_lowercase(term):
    return term.lower()


"""
Punctuations removal

Args:
    term: String -> string to be proceed
    plot: Bool -> if the string is in the field of plots

Returns:
    String -> Original string with leading and trailing punctuations removed
"""


def remove_punctuation(term, plot=False):
    if plot:
        return term.lstrip(punctuation).rstrip(punctuation)
    else:
        return term.rstrip(",")
    return result


"""
Stemming

Args:
    term: String -> String to be proceed

Returns:
    String -> Original string stemmed with SnowballStemmer
"""


def stem_data(term):
    return SnowballStemmer(language='english').stem(term)


"""
Check if the query is phrase search

Args:
    query: String -> Query String

Returns:
    Bool -> True if it's phrase search, vice versa
"""


def is_phrase_search(query):
    if query.startswith("\"") and query.endswith("\"") and len(query.split()) > 1:
        return True
    else:
        return False


"""
Remove stopwords for a list of query words

Args:
    query: List -> a list of query words
    stop_words: List -> a list of stop words

Returns:
    List -> A list of query words with stop words removed
"""


def remove_stop_words(query, stop_words):
    temp_list = []
    for token in query:
        if token not in stop_words:
            temp_list.append(token.lstrip(punctuation).rstrip(punctuation))
    return temp_list
