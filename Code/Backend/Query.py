"""
------------------------------------------------------------
Author: Leo LI
Date: 10th Feb 2023
Description: Responsible for retrieve results for different
types of queries
------------------------------------------------------------
"""


class Query:
    def __init__(self, dataset):
        self.dataset = dataset.get_data()
        self.index_general = dataset.get_index()
        self.index_title = dataset.get_index_title()
        self.average_number_of_terms = self.__cal_average_number_of_terms()

    # Naive implementation of search by title without ranking
    def by_title(self, keywords):
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                return self.__plain_search(keywords[0].lower(), "title")
            else:
                result = []
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "title")
                return result
        else:
            raise Exception("Keywords is empty!")
            
    # Naive implementation of search by keywords without ranking
    def by_keywords(self, keywords):
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                return self.__plain_search(keywords[0].lower(), "keywords")
            else:
                result = []
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "keywords")
                return result
        else:
            raise Exception("Keywords is empty!")

    # Method to perform plain single word search
    def __plain_search(self, word_to_be_queried, attributes):
        result = []
        # Detect if the search is specified to an attribute
        if attributes:
            if attributes == "title":
                for doic, info in self.dataset.items():
                    if word_to_be_queried in info['title']:
                        result.append(doic)
        else:
            pass
        return result

    def __term_frequency(self, word_to_be_queried, docid):
        # TODO information in cast missing
        return len(self.index_general[word_to_be_queried][1][docid])

    def __document_frequency(self, word_to_be_queried):
        return len(self.index_general[word_to_be_queried][1])

    def __cal_average_number_of_terms(self):
        number_of_tokens = 0
        for docid, info in self.dataset.items():
            for attribute, token in info.items():
                number_of_tokens += len(token)
        return number_of_tokens/len(self.dataset)

    def __number_of_terms(self, docid):
        number_of_tokens = 0
        for attribute, token in self.dataset[docid].items():
            number_of_tokens += len(token)
        return number_of_tokens
