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

# movies from web crawler
# movies = RetrieveData.MovieInfo("../TestDataset")
movies1 = RetrieveData.MovieInfo("../Dataset/IMDB TestData/")
movies1.read_files()
processed_data1 = DataPreprocessing.PreProcessing(movies1.get_movie_info())
processed_data1.tokenise()
processed_data1.to_lowercase()
processed_data1.remove_punctuation()
processed_data1.stem_data()
processed_data1.remove_stopwords()
processed_data1.create_index()
query1 = Query.Query(processed_data1)

# movies from original dataset
movies2 = RetrieveData.MovieInfo("../TestDataset/")
movies2.read_files()
processed_data2 = DataPreprocessing.PreProcessing(movies2.get_movie_info())
processed_data2.tokenise()
processed_data2.to_lowercase()
processed_data2.remove_punctuation()
processed_data2.stem_data()
processed_data2.remove_stopwords()
processed_data2.create_index()
query2 = Query.Query(processed_data2)


class TestSearch(unittest.TestCase):
    def test_general_search(self):
        start = time.time()
        results = query1.by_general("fairy rekindle")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn("tt0489974", results[:15])

    def test_keywords_search(self):
        start = time.time()
        results = query1.by_keywords("necromancy racist police")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15])
        
    def test_title_search(self):
        start = time.time()
        results = query1.by_title("Carnival Row")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15])
        
    def test_language_search(self):
        start = time.time()
        results = query1.by_language("English")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15])
        
    def test_genres_search(self):
        start = time.time()
        results = query1.by_genres("Fantasy Drama")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15])

    def test_phrase_search(self):
        start = time.time()
        results = query1.phrase_search_handler("monster Unimaginable")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15]) 

    def test_phrase_search_keys(self):
        start = time.time()
        results = query1.phrase_search_handler("mythical creature", attribute="keywords")
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt0489974', results[:15]) 

    def test_proximity_search(self):
        start = time.time()
        results = query1.proximity_search("Eren","Titans", distance = 15)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt2560140', results[:15])  

# Below are the tests with year filter

    def test_general_search_year(self):
        start = time.time()
        results = query2.by_general("charitable work", year1 = 1946, year2 = 1948)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn("000007", results[:15]) # Monsieur Vincent should not be among musical movies
        self.assertEqual("375972", results[0]) # Monsieur Vincent should be the top result

if __name__ == '__main__':
    unittest.main()

testsearch = TestSearch()
