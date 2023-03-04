"""
------------------------------------------------------------
Author: Leo LI, Baoyan Deng, Zhijun Zeng
Date: 9th Feb 2023
Description: Acting as the API to preprocess the read-in
data before performing queries
------------------------------------------------------------
"""
import copy
import json
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation

import Util

# ==============================================================================

"""
Class handling the preprocessing for the read-in data
"""


class PreProcessing:
    def __init__(self, dataset):
        # Check if the dataset is empty
        self.__index = {}
        self.__index_title = {}
        self.__index_keywords = {}
        self.__index_genre = {}
        if dataset:
            self.__dataset = copy.deepcopy(dataset)
        else:
            raise Exception("The provided dataset to be processed is empty!")
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))

    # Method which perform tokenisation
    def tokenise(self):
        for docid, info in self.__dataset.items():
            self.__dataset[docid]['title'] = self.__dataset[docid]['title'].split()
            self.__dataset[docid]['plot'] = self.__dataset[docid]['plot'].split()
            editors = []
            for editor in self.__dataset[docid]['editors']:
                editors.append(editor.split())
            self.__dataset[docid]['editors'] = editors
            directors = []
            for director in self.__dataset[docid]['directors']:
                directors.append(director.split())
            self.__dataset[docid]['directors'] = directors
            writers = []
            for writer in self.__dataset[docid]['writers']:
                writers.append(writer.split())
            self.__dataset[docid]['writers'] = writers
            composers = []
            for composer in self.__dataset[docid]['composers']:
                composers.append(composer.split())
            self.__dataset[docid]['composers'] = composers
            actors = []
            roles = []
            for actor in self.__dataset[docid]['cast'].keys():
                actors.append(actor)
                roles.append(self.__dataset[docid]['cast'][actor])
            for i in range(0, len(actors)):
                actors[i] = actors[i].split()
                if roles[i] is not None:
                    roles[i] = roles[i].split()
            self.__dataset[docid]['actors'] = actors
            self.__dataset[docid]['roles'] = roles

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
            for i in range(len(info['directors'])):
                info['directors'][i] = [token.lower() for token in info['directors'][i]]
            for i in range(len(info['writers'])):
                info['writers'][i] = [token.lower() for token in info['writers'][i]]
            for i in range(len(info['producers'])):
                info['producers'][i] = [token.lower() for token in info['producers'][i]]
            for i in range(len(info['composers'])):
                info['composers'][i] = [token.lower() for token in info['composers'][i]]
            for i in range(len(info['actors'])):
                info['actors'][i] = [token.lower() for token in info['actors'][i]]
            if info['roles'] is not None:
                for i in range(len(info['roles'])):
                    if info['roles'][i] is not None:
                        info['roles'][i] = [token.lower() for token in info['roles'][i]]

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
            for token in (info['editors']):
                token[0] = token[0].rstrip(",")
            for token in (info['producers']):
                token[0] = token[0].rstrip(",")
            for token in (info['composers']):
                token[0] = token[0].rstrip(",")
            for token in (info['actors']):
                token[0] = token[0].rstrip(",")
            if info['roles'] is not None:
                for token in (info['roles']):
                    if token is not None:
                        token[0] = token[0].rstrip(",")

    # Perform Snowball stemming to plot info
    def stem_data(self):
        for docid, info in self.__dataset.items():
            temp_list = []
            for token in (info['plot']):
                temp_list.append(SnowballStemmer(language='english').stem(token))
                info['plot'] = temp_list

    # Method which removes stop words from the spot attribute
    def remove_stopwords(self):
        for docid, info in self.__dataset.items():
            temp_list = []
            for token in (info['plot']):
                if token not in self.stop_words:
                    temp_list.append(token.lstrip(punctuation).rstrip(punctuation))
                info['plot'] = temp_list

    # Method which create the inverted positional index
    def create_index(self):
        for docid, info in self.__dataset.items():
            for i in range(len(info["title"])):
                token = info["title"][i]
                stemmed_token = Util.stem_data(token)
                if token not in self.__index:
                    self.__index[token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append(str(i))
                    else:
                        self.__index[token][1][docid] = [str(i)]
                        self.__index[token][0] += 1
                if token not in self.__index_title:
                    self.__index_title[token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index_title[token][1]:
                        self.__index_title[token][1][docid].append(str(i))
                    else:
                        self.__index_title[token][1][docid] = [str(i)]
                        self.__index_title[token][0] += 1
                if stemmed_token not in self.__index:
                    self.__index[stemmed_token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index[stemmed_token][1]:
                        self.__index[stemmed_token][1][docid].append(str(i))
                    else:
                        self.__index[stemmed_token][1][docid] = [str(i)]
                        self.__index[stemmed_token][0] += 1
                if stemmed_token not in self.__index_title:
                    self.__index_title[stemmed_token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index_title[stemmed_token][1]:
                        self.__index_title[stemmed_token][1][docid].append(str(i))
                    else:
                        self.__index_title[stemmed_token][1][docid] = [str(i)]
                        self.__index_title[stemmed_token][0] += 1
            token = info["year"]
            if token not in self.__index:
                self.__index[token] = [1, {docid: ["year"]}]
            else:
                if docid in self.__index[token][1]:
                    self.__index[token][1][docid].append("year")
                else:
                    self.__index[token][1][docid] = ["year"]
                    self.__index[token][0] += 1
            token = info["type"]
            if token not in self.__index:
                self.__index[token] = [1, {docid: ["type"]}]
            else:
                if docid in self.__index[token][1]:
                    self.__index[token][1][docid].append("type")
                else:
                    self.__index[token][1][docid] = ["type"]
                    self.__index[token][0] += 1
            # TODO detect the keywords "black and white" / when perform query
            for i in range(len(info["colorinfos"])):
                token = info["colorinfos"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["colorinfo"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("colorinfo")
                    else:
                        self.__index[token][1][docid] = ["colorinfo"]
                        self.__index[token][0] += 1
            for i in range(len(info["genres"])):
                token = info["genres"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["genre"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("genre")
                    else:
                        self.__index[token][1][docid] = ["genre"]
                        self.__index[token][0] += 1
                if token not in self.__index_genre:
                    self.__index_genre[token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index_genre[token][1]:
                        self.__index_genre[token][1][docid].append(str(i))
                    else:
                        self.__index_genre[token][1][docid] = [str(i)]
                        self.__index_genre[token][0] += 1
            for i in range(len(info["keywords"])):
                token = info["keywords"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["keyword"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("keyword")
                    else:
                        self.__index[token][1][docid] = ["keyword"]
                        self.__index[token][0] += 1
                if token not in self.__index_keywords:
                    self.__index_keywords[token] = [1, {docid: [str(i)]}]
                else:
                    if docid in self.__index_keywords[token][1]:
                        self.__index_keywords[token][1][docid].append(str(i))
                    else:
                        self.__index_keywords[token][1][docid] = [str(i)]
                        self.__index_keywords[token][0] += 1
            for i in range(len(info["languages"])):
                token = info["languages"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["language"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("language")
                    else:
                        self.__index[token][1][docid] = ["language"]
                        self.__index[token][0] += 1
            for i in range(len(info["soundmixes"])):
                token = info["soundmixes"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["soundmix"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("soundmix")
                    else:
                        self.__index[token][1][docid] = ["soundmix"]
                        self.__index[token][0] += 1
            for i in range(len(info["countries"])):
                token = info["countries"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: ["country"]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append("country")
                    else:
                        self.__index[token][1][docid] = ["country"]
                        self.__index[token][0] += 1
            for i in range(len(info["certificates"])):
                for token in info["certificates"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: ["certificate"]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append("certificate")
                        else:
                            self.__index[token][1][docid] = ["certificate"]
                            self.__index[token][0] += 1
            # TODO separate composers name in position -- currently David Johnson and Jake Wright is in the following
            # format: david 1, johnson 2, jake 3...
            position = len(info["title"]) + 100
            for i in range(len(info["composers"])):
                position += 15
                for token in info["composers"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: [str(position)]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append(str(position))
                        else:
                            self.__index[token][1][docid] = [str(position)]
                            self.__index[token][0] += 1
            position += 100
            for i in range(len(info["editors"])):
                position += 15
                for token in info["editors"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: [str(position)]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append(str(position))
                        else:
                            self.__index[token][1][docid] = [str(position)]
                            self.__index[token][0] += 1
            position += 100
            for i in range(len(info["directors"])):
                position += 15
                for token in info["directors"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: [str(position)]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append(str(position))
                        else:
                            self.__index[token][1][docid] = [str(position)]
                            self.__index[token][0] += 1
            position += 100
            for i in range(len(info["writers"])):
                position += 15
                for token in info["writers"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: [str(position)]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append(str(position))
                        else:
                            self.__index[token][1][docid] = [str(position)]
                            self.__index[token][0] += 1
            position += 100
            for i in range(len(info["plot"])):
                token = info["plot"][i]
                if token not in self.__index:
                    self.__index[token] = [1, {docid: [str(position + i)]}]
                else:
                    if docid in self.__index[token][1]:
                        self.__index[token][1][docid].append(str(position + i))
                    else:
                        self.__index[token][1][docid] = [str(position + i)]
                        self.__index[token][0] += 1
            position += 1000000
            temp_position = position
            for i in range(len(info["actors"])):
                position += 15
                for token in info["actors"][i]:
                    if token not in self.__index:
                        self.__index[token] = [1, {docid: [str(position)]}]
                    else:
                        if docid in self.__index[token][1]:
                            self.__index[token][1][docid].append(str(position))
                        else:
                            self.__index[token][1][docid] = [str(position)]
                            self.__index[token][0] += 1
            position = temp_position + 2
            for i in range(len(info["roles"])):
                position += 15
                if info["roles"][i] is not None:
                    for token in info["roles"][i]:
                        if token is not None and token not in self.__index:
                            self.__index[token] = [1, {docid: [str(position)]}]
                        else:
                            if docid in self.__index[token][1]:
                                self.__index[token][1][docid].append(str(position))
                            else:
                                self.__index[token][1][docid] = [str(position)]
                                self.__index[token][0] += 1

    # Getter for the processed data
    def get_data(self):
        if self.__dataset:
            return self.__dataset
        else:
            raise Exception("The dataset is empty or has not been processed!")

    # Getters for the indices
    def get_index(self):
        if self.__index:
            return self.__index
        else:
            raise Exception("The index is empty!")

    def get_index_title(self):
        if self.__index_title:
            return self.__index_title
        else:
            raise Exception("The index is empty!")

    def get_index_keywords(self):
        if self.__index_keywords:
            return self.__index_keywords
        else:
            raise Exception("The index is empty!")

    def get_index_genre(self):
        if self.__index_genre:
            return self.__index_genre
        else:
            raise Exception("The index is empty!")

    def get_stop_words(self):
        if self.stop_words:
            return self.stop_words
        else:
            raise Exception("No stopwords list found!")
