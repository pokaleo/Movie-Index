import time
import unittest
import RetrieveData
import json
import DataPreprocessing
import Query
import Util
import os,random
import xml.etree.ElementTree as ET
import sys

# movies from web crawler
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

    def test_proximity_search(self):
        start = time.time()
        results = query1.proximity_search("Eren","Titans", distance = 15)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('tt2560140', results[:15])  

if __name__ == '__main__':
    unittest.main()
