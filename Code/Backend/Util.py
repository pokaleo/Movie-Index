"""
------------------------------------------------------------
Author: Leo LI, Yvonne Ding
Date: 28th Feb 2023
Description: Utility functions providing useful static
methods
------------------------------------------------------------
"""
from string import punctuation
from nltk.stem.snowball import SnowballStemmer
import urllib.parse
import requests
from bs4 import BeautifulSoup


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

def return_image(title):
    """
    Return image url by giving the corresponding title

    Args:
        title: String -> a title

    Returns:
        String -> Image url

    """
    encode_title = urllib.parse.quote(title)
    url_baseline = 'https://www.imdb.com'
    curr_url = url_baseline + '/find/?q='+ encode_title + '&ref_=nv_sr_sm'
    req = requests.get(url= curr_url, headers={'User-Agent': 'Mozilla/5.0'}).text
    curr_page = BeautifulSoup(req,'html.parser')
    
    search_access = curr_page.find('div', attrs={'class':'sc-17bafbdb-2 ffAEHI'})
    response_href = search_access.find('li').a['href']
    
    target_url = url_baseline + response_href
    target_req = requests.get(url= target_url, headers={'User-Agent': 'Mozilla/5.0'}).text
    target_page = BeautifulSoup(target_req,'html.parser')

    opt_data = target_page.find('div', attrs={'class':"ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"})
    return opt_data.img['src']
    
