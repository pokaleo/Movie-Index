"""
------------------------------------------------------------
Author: Leo LI
Date: 10th Feb 2023
Description: Responsible for retrieve results for different
types of queries
------------------------------------------------------------
"""


# Naive implementation of search by title without ranking
def by_title(dataset, keywords):
    if keywords:
        result = []
        if isinstance(keywords, str):
            print("Searching: " + keywords)
            for doic, info in dataset.items():
                print("current docid: " + doic)
                print("current title: ")
                print(info['title'])
                if keywords in info['title']:
                    result.append(doic)
        return result
    else:
        raise Exception("Keywords is empty!")
