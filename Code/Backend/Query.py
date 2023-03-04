"""
------------------------------------------------------------
Author: Leo LI
Date: 10th Feb 2023
Description: Responsible for retrieve results for different
types of queries
------------------------------------------------------------
"""
import re
import math

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import Util


class Query:
    def __init__(self, dataset):
        self.__dataset = dataset.get_data()
        self.__index_general = dataset.get_index()
        self.__index_title = dataset.get_index_title()
        self.__index_keyword = dataset.get_index_keywords()
        self.__index_genre = dataset.get_index_genre()
        self.__average_number_of_terms = self.__cal_average_number_of_terms()
        self.__number_of_docs = len(self.__dataset.keys())
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))

    # providing util method for proper prickling
    def __getstate__(self):
        return {
            "dataset": self.__dataset,
            "index_general": self.__index_general,
            "index_title": self.__index_title,
            "index_keyword": self.__index_keyword,
            "index_genre": self.__index_genre,
            "average_number_of_terms": self.__average_number_of_terms,
            "number_of_docs": self.__number_of_docs,
        }

    def __setstate__(self, state):
        self.__dataset = state["dataset"]
        self.__index_general = state["index_general"]
        self.__index_title = state["index_title"]
        self.__index_keyword = state["index_keyword"]
        self.__index_genre = state["index_genre"]
        self.__average_number_of_terms = state["average_number_of_terms"]
        self.__number_of_docs = state["number_of_docs"]

    # Naive implementation of search by title without ranking
    def by_title(self, keywords, year1=None, year2=None, not_ranking=False):
        result = []
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                result = self.__plain_search(keywords[0].lower(), "title")
            else:
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "title")
                result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return self.bm25_ranking(keywords, result)

    # Naive implementation of search by keywords without ranking
    def by_keywords(self, keywords, year1=None, year2=None, not_ranking=False):
        result = []
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                result = self.__plain_search(keywords[0].lower(), "keywords")
            else:
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "keywords")
                result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return self.bm25_ranking(keywords, result)

    # Naive implementation of search by genre without ranking
    def by_genres(self, keywords, year1=None, year2=None, not_ranking=False):
        result = []
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                result = self.__plain_search(keywords[0].lower(), "genre")
            else:
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "genre")
                result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return self.bm25_ranking(keywords, result)

        # Naive implementation of search for general without ranking

    def by_general(self, keywords, year1=None, year2=None, not_ranking=False):
        result = []
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                result = self.__plain_search(keywords[0].lower())
            else:
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower())
                result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return self.bm25_ranking(keywords, result)

    # Method to filter the result by year
    def __filter_year(self, year, position, docids):
        result = []
        if position == 1:
            for docid in docids:
                if int(self.__dataset[docid]["year"]) > year:
                    result.append(docid)
        else:
            for docid in docids:
                if int(self.__dataset[docid]["year"]) < year:
                    result.append(docid)
        return result

    # Method to perform plain single word search
    def __plain_search(self, word_to_be_queried, attributes=None):
        result = []
        # Detect if the search is specified to an attribute
        if attributes:
            if attributes == "title":
                if word_to_be_queried in self.__index_title:
                    for docid, position in self.__index_title[word_to_be_queried][1].items():
                        result.append(docid)
            if attributes == "keywords":
                if word_to_be_queried in self.__index_keyword:
                    for docid, position in self.__index_keyword[word_to_be_queried][1].items():
                        result.append(docid)
            if attributes == "genre":
                if word_to_be_queried in self.__index_genre:
                    for docid, position in self.__index_genre[word_to_be_queried][1].items():
                        result.append(docid)
        # Use general research if no attribute input 
        else:
            if word_to_be_queried in self.__index_general:
                for docid, position in self.__index_general[word_to_be_queried][1].items():
                    result.append(docid)
            stemmed = Util.stem_data(word_to_be_queried)
            punctuationRemoved1 = Util.remove_punctuation(word_to_be_queried, True)
            punctuationRemoved2 = Util.remove_punctuation(word_to_be_queried)
            if stemmed in self.__index_general:
                for docid, position in self.__index_general[stemmed][1].items():
                    result.append(docid)
            if punctuationRemoved1 in self.__index_general:
                for docid, position in self.__index_general[punctuationRemoved1][1].items():
                    result.append(docid)
            if punctuationRemoved2 in self.__index_general:
                for docid, position in self.__index_general[punctuationRemoved2][1].items():
                    result.append(docid)
        return list(dict.fromkeys(result))

    # Method to perform single word search with docid and position
    def __position_search(self, word_to_be_queried, attribute=None):
        result = {}
        stemmed = Util.stem_data(word_to_be_queried)
        punctuationRemoved1 = Util.remove_punctuation(word_to_be_queried, True)
        punctuationRemoved2 = Util.remove_punctuation(word_to_be_queried)
        if attribute is None:
            search_field = self.__index_general
        elif attribute == "title":
            search_field = self.__index_title
        elif attribute == "keywords":
            search_field = self.__index_keyword
        elif attribute == "genre":
            search_field = self.__index_genre
        if word_to_be_queried in search_field:
            for docid, position in search_field[word_to_be_queried][1].items():
                if docid not in result:
                    result[docid] = position
                else:
                    result[docid] += position
        if stemmed in search_field:
            for docid, position in search_field[stemmed][1].items():
                if docid not in result:
                    result[docid] = position
                else:
                    result[docid] += position
        if punctuationRemoved1 in search_field:
            for docid, position in search_field[punctuationRemoved1][1].items():
                if docid not in result:
                    result[docid] = position
                else:
                    result[docid] += position
        if punctuationRemoved2 in search_field:
            for docid, position in search_field[punctuationRemoved2][1].items():
                if docid not in result:
                    result[docid] = position
                else:
                    result[docid] += position
        # remove duplicate
        for key in result:
            new_list = []
            for item in result[key]:
                if item not in new_list:
                    new_list.append(item)
            result[key] = new_list
        return result

    def phrase_search_handler(self, keywords, year1=None, year2=None, not_ranking=False, attribute=None, is_list=False):
        result = []
        if keywords:
            # remove " in the beginning and the ending
            if not is_list:
                keywords = keywords.split()
                keywords[0] = keywords[0][1:]
                keywords[len(keywords)-1] = keywords[len(keywords)-1][:-1]
            for i in range(1, len(keywords)):
                if i == 1:
                    result += self.proximity_search(keywords[i-1].lower(), keywords[i].lower(), 1, True, attribute)
                else:
                    result = list(set(result) &
                                  set(self.proximity_search(keywords[i-1].lower(),
                                                            keywords[i].lower(), 1, True, attribute)))
            result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if not result and not attribute:
            return self.phrase_search_handler(Util.remove_stop_words(keywords, self.stop_words),
                                              year1, year2, not_ranking, attribute, True)
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return self.bm25_ranking(keywords, result)

    # Proximity Search : "#distance word1 word2"
    def proximity_search(self, word1, word2, distance, phrase_search=False, attribute=None):
        result = []
        if word1 and word2 and distance is not None:
            word1_result = self.__position_search(word1, attribute)
            word2_result = self.__position_search(word2, attribute)
            common_result = set(word1_result.keys()) & set(word2_result.keys())
            if common_result:
                for docid in common_result:
                    for position1 in word1_result[docid]:
                        if not position1.isnumeric():
                            continue
                        for position2 in word2_result[docid]:
                            if not position2.isnumeric():
                                continue
                            if phrase_search:
                                if int(position2) - int(position1) == 1:
                                    result.append(docid)
                            else:
                                if abs(int(position1) - int(position2)) <= distance:
                                    result.append(docid)
        return result

    # TODO add attribute when calculating related tf,df etc in bm25
    def __term_frequency(self, word_to_be_queried, docid):
        # TODO information in cast missing
        if docid in self.__index_general[word_to_be_queried][1]:
            return len(self.__index_general[word_to_be_queried][1][docid])
        else:
            return 0.1

    def __document_frequency(self, word_to_be_queried):
        return len(self.__index_general[word_to_be_queried][1])

    def __cal_average_number_of_terms(self):
        number_of_tokens = 0
        for docid, info in self.__dataset.items():
            for attribute, token in info.items():
                if token is not None:
                    number_of_tokens += len(token)
        return number_of_tokens / len(self.__dataset)

    def __number_of_terms(self, docid):
        number_of_tokens = 0
        for attribute, token in self.__dataset[docid].items():
            if token is not None:
                number_of_tokens += len(token)
        return number_of_tokens

    # Calculate bm25 score for a single term
    def bm25(self, word_to_be_queried, docid):
        k = 1.5
        if word_to_be_queried not in self.__index_general:
            return 0
        document_frequency = self.__document_frequency(word_to_be_queried)
        term_frequency = self.__term_frequency(word_to_be_queried, docid)
        L_division = self.__number_of_terms(docid) / self.__average_number_of_terms
        log_value = (self.__number_of_docs - document_frequency + 0.5) / \
                    (document_frequency + 0.5)
        w_td = format((term_frequency / (k * L_division + term_frequency + 0.5))
                      * math.log10(log_value), '.4f')
        w_td = float(w_td)
        return w_td

    def bm25_ranking(self, keywords, docid_list, returnScore=False):
        term_list = keywords
        bm25score_list = []
        for docid in docid_list:
            sum_of_bm25 = 0
            for term in term_list:
                sum_of_bm25 += self.bm25(Util.to_lowercase(term), docid)
                sum_of_bm25 += self.bm25(Util.stem_data(term), docid)
            bm25score_list.append(sum_of_bm25)
        if returnScore:
            return docid_list, bm25score_list
        return [x for _, x in sorted(zip(bm25score_list, docid_list), reverse=True)]

    def alphabet_ranking(self, docid_list):
        title_list = []
        for docid in docid_list:
            temp_list = self.__dataset[docid]['title']
            title = ' '.join(temp_list)
            title_list.append(title)
        ordered_list = sorted(docid_list, key=lambda x: title_list[docid_list.index(x)], reverse=False)
        return ordered_list

    def year_ranking(self, docid_list):
        year_list = []
        for docid in docid_list:
            year_list.append(int(self.__dataset[docid]['year']))
        return [x for _, x in sorted(zip(year_list, docid_list))]

    def year_ranking_reverse(self, docid_list):
        year_list = []
        for docid in docid_list:
            year_list.append(int(self.__dataset[docid]['year']))
        return [x for _, x in sorted(zip(year_list, docid_list), reverse=True)]

    # TODO: define a function to decide using which ranking method in several kinds of situation, for example using alphabet_ranking when producting by_title search etc.
