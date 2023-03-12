import time
import unittest
import RetrieveData
import json
import DataPreprocessing
import Query
import Util
import os,random
import xml.etree.ElementTree as ET
import argparse
import sys

movies = RetrieveData.MovieInfo("../TestDataset")
movies.read_files()
# movies = RetrieveData.MovieInfo("../Code/TestDataset")


processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
processed_data.tokenise()
processed_data.to_lowercase()
processed_data.remove_punctuation()
processed_data.stem_data()
processed_data.remove_stopwords()
processed_data.create_index()
query = Query.Query(processed_data)

def randomPick(data,num):
    rand = random.sample(list(data.items()), k=num)
    res = []
    for f in rand:
        a = random.choice(list(f[1].keys()))
        # print(a)
        # print(f[1].get(a))
        res.append(f[1].get(a))
    return res


class TestSearch(unittest.TestCase):
    def __init__(self, testname,query_params, docid, year1,year2):
        super(TestSearch, self).__init__(testname)
        self.query_params = query_params
        self.docid = docid
        self.year1 = year1
        self.year2 = year2

    def test_general_search(self):
            start = time.time()
            results = query.by_general(query_params, int(year1), int(year2), not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)

    def test_keywords_search(self):
            start = time.time()
            results = query.by_keywords(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_title_search(self):
            start = time.time()
            results = query.by_title(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_language_search(self):
            start = time.time()
            results = query.by_language(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_genres_search(self):
            start = time.time()
            results = query.by_genres(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
if __name__ == '__main__':
    query_params = sys.argv[1]
    docid = sys.argv[2]
    year1 = sys.argv[3]
    year2 = sys.argv[4]

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestSearch)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestSearch(test_name, query_params, docid, year1,year2))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())


# Command line: python3 Testsearch.py 'peace and harmony' 375972 1900 2020



# testsearch = TestSearch()
# print('test: ', testsearch)
# print(testsearch.test_general_search(query_params="peace and harmony",docid="375972",year1=1900, year2=2020, not_ranking=False))    
# print(testsearch.test_title_search("Monsieur Vincent",1900,2020,False)) 
# print(testsearch.test_keywords_search("poverty arrest",1900,2020,False))
# print(testsearch.test_genres_search("Monsieur Vincent",1900,2020,False)) 
# print(testsearch.test_language_search("French",1900,2020,False))

