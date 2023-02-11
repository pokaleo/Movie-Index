"""
------------------------------------------------------------
Author: Leo LI, Baoyan Deng, Zhijun Zeng
Date: 9th Feb 2023
Description: Acting as the API to preprocess the read-in
data before performing queries
------------------------------------------------------------
"""
import json
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation

# ==============================================================================

"""
Class handling the preprocessing for the read-in data
"""


class PreProcessing:
    def __init__(self, dataset):
        # Check if the dataset is empty
        if dataset:
            self.__dataset = dataset
        else:
            raise Exception("The provided dataset to be processed is empty!")

    # Method which perform tokenisation
    def tokenise(self):
        for docid, info in self.__dataset.items():
            self.__dataset[docid]['title'] = self.__dataset[docid]['title'].split()
            self.__dataset[docid]['plot'] = self.__dataset[docid]['plot'].split()
            editors = []
            for editor in self.__dataset[docid]['editors']:
                editors.append(editor.split())
            self.__dataset[docid]['editors'] = editors
            # TODO decide if need to tokenise releasedates
            directors = []
            for director in self.__dataset[docid]['directors']:
                editors.append(director.split())
            self.__dataset[docid]['directors'] = directors
            writers = []
            for writer in self.__dataset[docid]['writers']:
                writers.append(writer.split())
            self.__dataset[docid]['writers'] = writers
            composers = []
            for composer in self.__dataset[docid]['composers']:
                composers.append(composer.split())
            self.__dataset[docid]['composers'] = composers

    # Method which cast all tokens to lower case
    def to_lowercase(self):
        for docid, info in self.__dataset.items():
            info['title'] = [token.lower() for token in info['title']]
            info['plot'] = [token.lower() for token in info['plot']]
            info['colorinfos'] = [token.lower() for token in info['colorinfos']]
            info['genres'] = [token.lower() for token in info['genres']]
            info['keywords'] = [token.lower() for token in info['keywords']]
            info['languages'] = [token.lower() for token in info['languages']]
            info['soundmixes'] = [token.lower() for token in info['soundmixes']]
            info['countries'] = [token.lower() for token in info['countries']]
            for i in range(len(info['editors'])):
                info['editors'][i] = [token.lower() for token in info['editors'][i]]
            for i in range(len(info['certificates'])):
                info['certificates'][i] = [token.lower() for token in info['certificates'][i]]
            for i in range(len(info['releasedates'])):
                info['releasedates'][i] = [token.lower() for token in info['releasedates'][i]]
            for i in range(len(info['directors'])):
                info['directors'][i] = [token.lower() for token in info['directors'][i]]
            for i in range(len(info['writers'])):
                info['writers'][i] = [token.lower() for token in info['writers'][i]]
            for i in range(len(info['composers'])):
                info['composers'][i] = [token.lower() for token in info['composers'][i]]
            for i in range(len(info['runningtimes'])):
                info['runningtimes'][i] = [token.lower() for token in info['runningtimes'][i]]

    # Method which removes leading and trailing punctuations and individual punctuations
    def remove_punctuation(self):
        for docid, info in self.__dataset.items():
            temp_list = []
            for token in (info['plot']):
                if token not in punctuation:
                    temp_list.append(token.lstrip(punctuation).rstrip(punctuation))
                info['plot'] = temp_list
            for token in (info['writers']):
                token[0] = token[0].rstrip(",")
            for token in (info['composers']):
                token[0] = token[0].rstrip(",")

    # Method which removes stop words from the spot attribute
    # def remove_stopwords(self):
    #     nltk.download("stopwords")
    #     stop_words = set(stopwords.words("english"))

    def stem_data(self):
        stemmer = SnowballStemmer("english")

    # Getter for the processed data
    def get_data(self):
        if self.__dataset:
            return self.__dataset
        else:
            raise Exception("The dataset is empty or has not been processed!")
