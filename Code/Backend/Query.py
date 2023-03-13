"""
------------------------------------------------------------
Author: Leo LI
Date: 10th Feb 2023
Description: Responsible for retrieve results for different
types of queries
------------------------------------------------------------
"""
import math
import Util


class Query:
    """
    Class handling the query request and providing APIs
    """
    def __init__(self, dataset):
        self.__dataset = dataset.get_data()
        self.__index_general = dataset.get_index()
        self.__index_title = dataset.get_index_title()
        self.__index_keyword = dataset.get_index_keywords()
        self.__index_genre = dataset.get_index_genre()
        self.__index_language = dataset.get_index_language()
        self.__average_number_of_terms = self.__cal_average_number_of_terms()
        self.__number_of_docs = len(self.__dataset.keys())
        self.__stop_words = dataset.get_stop_words()
        self.__number_of_terms_dict = {}
        for docid in self.__dataset:
            self.__number_of_terms_dict[docid] = self.__number_of_terms(docid)

    # providing util method for proper prickling
    def __getstate__(self):
        return {
            "dataset": self.__dataset,
            "index_general": self.__index_general,
            "index_title": self.__index_title,
            "index_keyword": self.__index_keyword,
            "index_genre": self.__index_genre,
            "index_language": self.__index_language,
            "average_number_of_terms": self.__average_number_of_terms,
            "number_of_docs": self.__number_of_docs,
            "stop_words": self.__stop_words,
            "number_of_terms": self.__number_of_terms_dict
        }

    def __setstate__(self, state):
        self.__dataset = state["dataset"]
        self.__index_general = state["index_general"]
        self.__index_title = state["index_title"]
        self.__index_keyword = state["index_keyword"]
        self.__index_genre = state["index_genre"]
        self.__average_number_of_terms = state["average_number_of_terms"]
        self.__number_of_docs = state["number_of_docs"]
        self.__stop_words = state["stop_words"]
        self.__index_language = state["index_language"]
        self.__number_of_terms_dict = state["number_of_terms"]

    def by_title(self, keywords, year1=None, year2=None, not_ranking=False):
        """
        Search by title

        Args:
            keywords: String -> query contents
            year1: Integer -> year filter - published later than...
            year2: Integer -> year filter - published earlier than...
            not_ranking: Bool -> switch for applying BM25 ranking

        Raises:
            Exception: If keywords is empty

        Returns:
            List -> A list of relevant docids
        """
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

    def by_keywords(self, keywords, year1=None, year2=None, not_ranking=False):
        """
        Search by keywords

        Args:
            keywords: String -> query contents
            year1: Integer -> year filter - published later than...
            year2: Integer -> year filter - published earlier than...
            not_ranking: Bool -> switch for applying BM25 ranking

        Returns:
            List -> A list of relevant docids

        Raises:
            Exception: If keywords is empty
        """
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

    def by_genres(self, keywords, year1=None, year2=None, not_ranking=False):
        """
        Search by genre

        Args:
            keywords: String -> query contents
            year1: Integer -> year filter - published later than...
            year2: Integer -> year filter - published earlier than...
            not_ranking: Bool -> switch for applying BM25 ranking

        Returns:
            List -> A list of relevant docids

        Raises:
            Exception: If keywords is empty
        """
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

    def by_language(self, keywords, year1=None, year2=None, not_ranking=False):
        """
        Search by language

        Args:
            keywords: String - query contents
            year1: Integer -> year filter - published later than...
            year2: Integer -> year filter - published earlier than...
            not_ranking: Bool -> switch for applying BM25 ranking

        Returns:
            List -> A list of relevant docids

        Raises:
            Exception: If keywords is empty
        """
        result = []
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                result = self.__plain_search(keywords[0].lower(), "language")
            else:
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "language")
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

    def by_general(self, keywords, year1=None, year2=None, not_ranking=False):
        """
        Perform general queries

        Args:
            keywords: String - query contents
            year1: Integer -> year filter - published later than...
            year2: Integer -> year filter - published earlier than...
            not_ranking: Bool -> switch for applying BM25 ranking

        Returns:
            List -> A list of relevant docids

        Raises:
            Exception: If keywords is empty
        """
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

    def __filter_year(self, year, position, docids):
        """
        Method to filter the result by year

        Args:
            year: Integer -> representing the date
            position: Integer -> Direction of the filter, 1 represent find result later than "year", otherwise earlier
            docids: List -> A list of docids

        Returns:
            List -> A list of docids filtered
        """
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

    def __plain_search(self, word_to_be_queried, attributes=None):
        """
        Method to perform plain single word search

        Args:
            word_to_be_queried: String -> the word to be queried
            attributes: String -> which area to be queried (e.g. "title"), perform a general query if it's None

        Returns:
            List -> A list of relevant docids
        """
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
            if attributes == "language":
                if word_to_be_queried in self.__index_language:
                    for docid, position in self.__index_language[word_to_be_queried][1].items():
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

    def __position_search(self, word_to_be_queried, attribute=None):
        """
        Method to direct perform single word search with docid

        Args:
            word_to_be_queried: String -> the word to be queried
            attribute: String -> which area to be queried (e.g. "title"), perform a general query if it's None

        Returns:
            List -> A list of relevant docids
        """
        result = {}
        print("test: ", word_to_be_queried)
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
        elif attribute == "language":
            search_field = self.__index_language
        if word_to_be_queried in search_field:
            for docid, position in search_field[word_to_be_queried][1].items():
                position_list = [x for x in position if x.isnumeric()]
                if position_list:
                    if docid not in result:
                        result[docid] = position_list
                    else:
                        result[docid] += position_list
        if stemmed in search_field:
            for docid, position in search_field[stemmed][1].items():
                position_list = [x for x in position if x.isnumeric()]
                if position_list:
                    if docid not in result:
                        result[docid] = position_list
                    else:
                        result[docid] += position_list
        if punctuationRemoved1 in search_field:
            for docid, position in search_field[punctuationRemoved1][1].items():
                position_list = [x for x in position if x.isnumeric()]
                if position_list:
                    if docid not in result:
                        result[docid] = position_list
                    else:
                        result[docid] += position_list
        if punctuationRemoved2 in search_field:
            for docid, position in search_field[punctuationRemoved2][1].items():
                position_list = [x for x in position if x.isnumeric()]
                if position_list:
                    if docid not in result:
                        result[docid] = position_list
                    else:
                        result[docid] += position_list
        # remove duplicate
        for key in result:
            new_list = []
            for item in result[key]:
                if item not in new_list:
                    new_list.append(item)
            result[key] = new_list
        return result

    def phrase_search_handler(self, keywords, year1=None, year2=None, not_ranking=False, attribute=None, is_list=False):
        """
        Entry for perform a new query, handling the phrase search

        Args:
            keywords: String -> query contents
            year1: Integer -> Year filter - published later than...
            year2: Integer -> Year filter - published earlier than...
            not_ranking: Bool -> Switch for applying BM25 ranking
            attribute: String -> which area to be queried (e.g. "title"), perform a general query if it's None
            is_list: Bool -> if the keywords is passed in as a list of words, used for recursive call

        Returns:
            List -> A list of relevant docids

        Raises:
            Exception: If keywords is empty
        """
        result = []
        if keywords:
            # remove " in the beginning and the ending
            if not is_list:
                if not Util.is_phrase_search(keywords):
                    if attribute is None:
                        return self.by_general(keywords, year1, year2, not_ranking)
                    elif attribute == "title":
                        return self.by_title(keywords, year1, year2, not_ranking)
                    elif attribute == "keywords":
                        return self.by_keywords(keywords, year1, year2, not_ranking)
                    elif attribute == "genre":
                        return self.by_genres(keywords, year1, year2, not_ranking)
                    elif attribute == "language":
                        return self.by_language(keywords, year1, year2, not_ranking)
                keywords = keywords.split()
                keywords[0] = keywords[0][1:]
                keywords[len(keywords) - 1] = keywords[len(keywords) - 1][:-1]
            for i in range(1, len(keywords)):
                if i == 1:
                    result += self.proximity_search(keywords[i - 1].lower(), keywords[i].lower(), 1, True, attribute,
                                                    False, None, None, True)
                else:
                    new_result = self.proximity_search(keywords[i - 1].lower(), keywords[i].lower(), 1, True, attribute,
                                                       False, None, None, True)
                    result = list(set(result) & set(new_result))
                if not result:
                    break
            print("1st res: ", result)
            if not is_list:
                keywords_plot = Util.remove_stop_words(keywords, self.__stop_words)
                result += self.phrase_search_handler(keywords_plot, year1, year2, not_ranking, attribute, True)
                result = list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
        if year1:
            result = self.__filter_year(year1, 1, result)
        if year2:
            result = self.__filter_year(year2, 2, result)
        if not_ranking:
            return result
        return list(dict.fromkeys(self.bm25_ranking(keywords, result)))

    def proximity_search(self, word1, word2, distance, phrase_search=False, attribute=None,
                         direct_call=False, year1=None, year2=None, not_ranking=False):
        """
        Method to perform proximity search

        Args:
            word1: String -> first word to be queried
            word2: String -> second word to be queried
            distance: Integer -> distance between the two words
            phrase_search: Bool -> is this a phrase search
            attribute: String -> which area to be queried (e.g. "title"), perform a general query if it's None
            direct_call: Bool -> if the method is directly called by the frontend
            year1: Integer -> Year filter - published later than...
            year2: Integer -> Year filter - published earlier than...
            not_ranking: Bool -> Switch for applying BM25 ranking

        Returns:
            List -> A list of relevant docids
        """
        result = []
        if word1 and word2 and distance is not None:
            word1_result = self.__position_search(word1, attribute)
            word2_result = self.__position_search(word2, attribute)
            common_result = set(word1_result.keys()) & set(word2_result.keys())
            # print("gogogo", common_result)
            if common_result:
                for docid in common_result:
                    # print("docid: ", docid)
                    position_1 = word1_result[docid]
                    # print(word1, " : ", position_1)
                    position_2 = word2_result[docid]
                    # print(word2, " : ", position_2)
                    positions = position_1 + position_2
                    # print("Merge: ", positions)
                    if phrase_search:
                        for i in range(len(position_1)):
                            for j in range(len(position_1), len(positions)):
                                # print("position at the doc: ", positions[i], int(positions[j]))
                                if int(positions[i]) - int(positions[j]) == -1 or \
                                        int(positions[i]) - int(positions[j]) == 0:
                                    result.append(docid)
                    else:
                        for i in range(len(position_1)):
                            for j in range(len(position_1), len(positions)):
                                if abs(int(positions[i]) - int(positions[j])) <= distance:
                                    result.append(docid)
                    # print("result: ", result)
        if direct_call:
            if year1:
                result = self.__filter_year(year1, 1, result)
            if year2:
                result = self.__filter_year(year2, 2, result)
            if not_ranking:
                return result
            return self.bm25_ranking([word1, word2], result)
        return result

    def __term_frequency(self, word_to_be_queried, docid):
        """
        Compute the term frequency for a token in a specific document

        Args:
            word_to_be_queried: String -> the token to be proceed
            docid: Integer -> the document id

        Returns:
            Integer -> term frequency
        """
        appearance_in_cast = 0
        appearance_in_title = 0
        appearance_in_spot = 0
        appearance_in_keywords = 0
        if docid in self.__index_general[word_to_be_queried][1]:
            for position in self.__index_general[word_to_be_queried][1][docid]:
                if position.isnumeric():
                    if int(position) < 100:
                        appearance_in_title += 1
                    elif int(position) > 1000000:
                        appearance_in_cast += 1
                    elif int(position) > 500:
                        appearance_in_spot += 1
                elif position == "keyword":
                    appearance_in_keywords += 1
            return (len(self.__index_general[word_to_be_queried][1][docid]) - appearance_in_cast * 0.5 +
                    appearance_in_title * 3.5 + appearance_in_spot * 1.8 + appearance_in_keywords * 2.3)
        else:
            return 0

    def __document_frequency(self, word_to_be_queried):
        """
        Compute the document frequency for a token

        Args:
            word_to_be_queried: String -> the token to be proceed

        Returns:
            Integer -> document freqhency
        """
        return len(self.__index_general[word_to_be_queried][1])

    def __cal_average_number_of_terms(self):
        """
        Calculate the average number of terms included in each document

        Args:
            n/a

        Returns:
            Integer -> the average number of terms included in each document
        """
        number_of_tokens = 0
        for docid, info in self.__dataset.items():
            for attribute, token in info.items():
                if token is not None:
                    number_of_tokens += len(token)
        return number_of_tokens / len(self.__dataset)

    def __number_of_terms(self, docid):
        """
        Compute the number of terms appeared in a specific document

        Args:
            docid: Integer -> the document to be proceeded

        Returns:
            Integer -> number of terms appeared in a specific document
        """
        number_of_tokens = 0
        for attribute, token in self.__dataset[docid].items():
            if token is not None:
                number_of_tokens += len(token)
        return number_of_tokens

    def bm25(self, word_to_be_queried, docid):
        """
        Calculate the BM25 score for a specific term in a specific document

        Args:
            word_to_be_queried: String -> the term to be proceed
            docid: Integer -> the document to be proceeded

        Returns:
            Integer -> BM25 score
        """
        k = 1.5
        if word_to_be_queried not in self.__index_general:
            return 0
        document_frequency = self.__document_frequency(word_to_be_queried)
        term_frequency = self.__term_frequency(word_to_be_queried, docid)
        L_division = self.__number_of_terms_dict[docid] / self.__average_number_of_terms
        log_value = (self.__number_of_docs - document_frequency + 0.5) / \
                    (document_frequency + 0.5)
        w_td = format((term_frequency / (k * L_division + term_frequency + 0.5))
                      * math.log10(log_value), '.4f')
        w_td = float(w_td)
        return w_td

    def bm25_ranking(self, keywords, docid_list, returnScore=False):
        """
        Ranking a list of document by BM25 scoring

        Args:
            keywords: String -> query contents
            docid_list: List -> a list of document id
            returnScore: Bool -> return the scoring rather than sorting the docid_list

        Returns:
            docid_list: List -> a list of document id sorted based on BM25 scheme
            bm25score_list(optional): List -> a list of BM25 scoring, the list will not be ranked if this is returned
        """
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
        """
        Sort a list of document by alphabet order

        Args:
            docid_list: List -> a list of document id

        Returns:
            List -> a list of document id sorted based on alphabet order
        """
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

    # TODO Is the above 3 method really useful?
