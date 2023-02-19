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
