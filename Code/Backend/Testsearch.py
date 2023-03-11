import time
import unittest
import RetrieveData
import json
import DataPreprocessing
import Query
import Util
import os,random
import xml.etree.ElementTree as ET

# movies = RetrieveData.MovieInfo("../TestDataset")
movies = RetrieveData.MovieInfo("../Code/TestDataset")


processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
processed_data.tokenise()
processed_data.to_lowercase()
processed_data.remove_punctuation()
processed_data.stem_data()
processed_data.remove_stopwords()
processed_data.create_index()
query = Query.Query(processed_data)


class TestSearch(unittest.TestCase):

    def test_general_search(self, query_params, docid, year1=None, year2=None, not_ranking=False):
            start = time.time()
            results = query.by_general(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)

    def test_keywords_search(self, query_params, docid, year1=None, year2=None, not_ranking=False):
            start = time.time()
            results = query.by_general(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_title_search(self, query_params, docid, year1=None, year2=None, not_ranking=False):
            start = time.time()
            results = query.by_general(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_language_search(self, query_params, docid, year1=None, year2=None, not_ranking=False):
            start = time.time()
            results = query.by_general(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
    def test_genres_search(self, query_params, docid, year1=None, year2=None, not_ranking=False):
            start = time.time()
            results = query.by_general(query_params, year1=None, year2=None, not_ranking=False)
            end = time.time()
            print("Basic {:.4f} s".format(end-start), results)
            self.assertIn(docid, results)
        
if __name__ == '__main__':
    unittest.main()
    
testsearch = TestSearch()
print(testsearch.test_general_search("peace and harmony","375972",1900, 2020, False))    
#print(testsearch.test_title_search("Monsieur Vincent",1900,2020,False)) 
#print(testsearch.test_keywords_search("poverty arrest",1900,2020,False))
#print(testsearch.test_genres_search("Monsieur Vincent",1900,2020,False)) 
#print(testsearch.test_language_search("French",1900,2020,False))

