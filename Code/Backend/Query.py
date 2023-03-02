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
from nltk.stem.snowball import SnowballStemmer
import Util


class Query:
    def __init__(self, dataset):
        self.dataset = dataset.get_data()
        self.index_general = dataset.get_index()
        self.index_title = dataset.get_index_title()
        self.index_keyword = dataset.get_index_keywords()
        self.index_genre = dataset.get_index_genre()
        self.average_number_of_terms = self.__cal_average_number_of_terms()
        self.number_of_docs = len(self.dataset.keys())

    # Naive implementation of search by title without ranking
    def by_title(self, keywords, year1=None, year2=None):
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
        return self.bm25_ranking(keywords, result)

    # Naive implementation of search by keywords without ranking
    def by_keywords(self, keywords, year1=None, year2=None):
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
        return self.bm25_ranking(keywords, result)

    # Naive implementation of search by genre without ranking
    def by_genres(self, keywords, year1=None, year2=None):
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
        return self.bm25_ranking(keywords, result)

        # Naive implementation of search for general without ranking

    def by_general(self, keywords, year1=None, year2=None):
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
        return self.bm25_ranking(keywords, result)

    # Method to filter the result by year
    def __filter_year(self, year, position, docids):
        result = []
        if position == 1:
            for docid in docids:
                if int(self.dataset[docid]["year"]) > year:
                    result.append(docid)
        else:
            for docid in docids:
                if int(self.dataset[docid]["year"]) < year:
                    result.append(docid)
        return result

    # Method to perform plain single word search
    def __plain_search(self, word_to_be_queried, attributes=None):
        result = []
        # Detect if the search is specified to an attribute
        if attributes:
            if attributes == "title":
                if word_to_be_queried in self.index_title:
                    for docid, position in self.index_title[word_to_be_queried][1].items():
                        result.append(docid)
            if attributes == "keywords":
                if word_to_be_queried in self.index_keyword:
                    for docid, position in self.index_keyword[word_to_be_queried][1].items():
                        result.append(docid)
            if attributes == "genre":
                if word_to_be_queried in self.index_genre:
                    for docid, position in self.index_genre[word_to_be_queried][1].items():
                        result.append(docid)
        # Use general research if no attribute input 
        else:
            if word_to_be_queried in self.index_general:
                for docid, position in self.index_general[word_to_be_queried][1].items():
                    result.append(docid)
            stemmed = Util.stem_data(word_to_be_queried)
            punctuationRemoved1 = Util.remove_punctuation(word_to_be_queried, True)
            punctuationRemoved2 = Util.remove_punctuation(word_to_be_queried)
            if stemmed in self.index_general:
                for docid, position in self.index_general[stemmed][1].items():
                    result.append(docid)
            if punctuationRemoved1 in self.index_general:
                for docid, position in self.index_general[punctuationRemoved1][1].items():
                    result.append(docid)
            if punctuationRemoved2 in self.index_general:
                for docid, position in self.index_general[punctuationRemoved2][1].items():
                    result.append(docid)
        return list(dict.fromkeys(result))

    # Method to perform single word search with docid and position
    def __position_search(self, word_to_be_queried):
        word1 = SnowballStemmer(language='english').stem(word_to_be_queried.lower())
        word2 = word_to_be_queried.lower()
        if word1 or word2 in self.index_general.keys():
            if word1 in self.index_general.keys():
                result = self.index_general[word1][1]
            if word2 in self.index_general.keys():
                result = self.index_general[word2][1]
                return result
            else:
                raise Exception("We did not find the result!")
        else:
            raise Exception("We did not find the result!")

    # Proximity Search : "#distance word1 word2"
    def proximity_search(self, keywords):
        if keywords:
            keywords = keywords.split()
            if not re.match(r'#\d*', keywords[0]):
                return Exception("The format is wrong!")
            else:
                if len(keywords) != 3:
                    return Exception("The format is wrong!")
                else:
                    distance = int(keywords[0].strip("#"))
                    keyword1 = keywords[1]
                    keyword2 = keywords[2]
                    dict1 = self.__position_search(keyword1)
                    dict2 = self.__position_search(keyword2)
                    # if in common document
                    common_doic = list(dict1.keys() & dict2.keys())
                    if common_doic:
                        result = []
                        for docid in common_doic:
                            for position1 in dict1[docid]:
                                if not position1.isdigit():
                                    continue
                                for position2 in dict2[docid]:
                                    if not position2.isdigit():
                                        continue
                                    if abs(int(position1) - int(position2)) < distance:
                                        result.append(docid)
                        if result:
                            return list(dict.fromkeys(result))
                        else:
                            raise Exception("We did not find the result!")
                    else:
                        raise Exception("We did not find the result!")
        else:
            raise Exception("Keywords is empty!")

    # Phrase Search : "word1 word2"
    def phrase_search(self, keywords):
        if keywords:
            keywords = keywords.split()
            if len(keywords) != 2:
                return Exception("The format is wrong!")
            else:
                keyword1 = keywords[0]
                keyword2 = keywords[1]
                dict1 = self.__position_search(keyword1)
                dict2 = self.__position_search(keyword2)
                # if in common document
                common_doic = list(dict1.keys() & dict2.keys())
                if common_doic:
                    result = []
                    for doic in common_doic:
                        for position1 in dict1[doic]:
                            if not position1.isdigit():
                                continue
                            for position2 in dict2[doic]:
                                if not position2.isdigit():
                                    continue
                                distance = abs(int(position2) - int(position1))
                                if distance < 2:
                                    result.append(doic)
                    if result:
                        return list(dict.fromkeys(result))
                    else:
                        raise Exception("We did not find the result!")
                else:
                    raise Exception("We did not find the result!")
        else:
            raise Exception("Keywords is empty!")

    # TODO add attribute when calculating related tf,df etc in bm25
    def __term_frequency(self, word_to_be_queried, docid):
        # TODO information in cast missing
        if docid in self.index_general[word_to_be_queried][1]:
            return len(self.index_general[word_to_be_queried][1][docid])
        else:
            return 0.1

    def __document_frequency(self, word_to_be_queried):
        return len(self.index_general[word_to_be_queried][1])

    def __cal_average_number_of_terms(self):
        number_of_tokens = 0
        for docid, info in self.dataset.items():
            for attribute, token in info.items():
                if token is not None:
                    number_of_tokens += len(token)
        return number_of_tokens / len(self.dataset)

    def __number_of_terms(self, docid):
        number_of_tokens = 0
        for attribute, token in self.dataset[docid].items():
            if token is not None:
                number_of_tokens += len(token)
        return number_of_tokens

    # Calculate bm25 score for a single term
    def bm25(self, word_to_be_queried, docid):
        k = 1.5
        document_frequency = self.__document_frequency(word_to_be_queried)
        term_frequency = self.__term_frequency(word_to_be_queried, docid)
        L_division = self.__number_of_terms(docid) / self.average_number_of_terms
        log_value = (self.number_of_docs - document_frequency + 0.5) / \
                    (document_frequency + 0.5)
        w_td = format((term_frequency / (k * L_division + term_frequency + 0.5))
                      * math.log10(log_value), '.4f')
        w_td = float(w_td)
        return w_td

    def bm25_ranking(self, keywords, docid_list):
        term_list = keywords
        bm25score_list = []
        for docid in docid_list:
            sum_of_bm25 = 0
            for term in term_list:
                sum_of_bm25 += self.bm25(Util.to_lowercase(term), docid)
                sum_of_bm25 += self.bm25(Util.stem_data(term), docid)
            bm25score_list.append(sum_of_bm25)
        return [x for _, x in sorted(zip(bm25score_list, docid_list), reverse=True)]

    def alphabet_ranking(self, docid_list):
        title_list = []
        for docid in docid_list:
            temp_list = self.dataset[docid]['title']
            title = ' '.join(temp_list)
            title_list.append(title)
        print(title_list)
        ordered_list = sorted(docid_list, key=lambda x: title_list[docid_list.index(x)], reverse=False)
        return ordered_list

    def year_ranking(self, docid_list):
        year_list = []
        for docid in docid_list:
            year_list.append(int(self.dataset[docid]['year']))
        return [x for _, x in sorted(zip(year_list, docid_list))]

    def year_ranking_reverse(self, docid_list):
        year_list = []
        for docid in docid_list:
            year_list.append(int(self.dataset[docid]['year']))
        return [x for _, x in sorted(zip(year_list, docid_list), reverse=True)]

    # TODO: define a function to decide using which ranking method in several kinds of situation, for example using alphabet_ranking when producting by_title search etc.
