import time
import unittest
import RetrieveData
import DataPreprocessing
import Query
# movies from original dataset
movies2 = RetrieveData.MovieInfo("../Dataset/IMDB Movie Info")
movies2.read_files()
processed_data2 = DataPreprocessing.PreProcessing(movies2.get_movie_info())
processed_data2.tokenise()
processed_data2.to_lowercase()
processed_data2.remove_punctuation()
processed_data2.stem_data()
processed_data2.remove_stopwords()
processed_data2.create_index()
query2 = Query.Query(processed_data2)

class TestSearch_year(unittest.TestCase):

    def test_general_search_year(self):
        start = time.time()
        results = query2.by_general("nineteen-knot stirring", year1 = 1900, year2 = 1902)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn("000167", results[:15]) # 'Columbia' and 'Shamrock II' Finishing Second Race
        self.assertNotIn("000208", results[0]) # 'Columbia' and 'Shamrock II' Finishing Second Race should in this result
    
    def test_keywords_search_year(self):
        start = time.time()
        results = query2.by_keywords("selfishness prank", year1 = 2000, year2 = 2005)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('000030', results[:15])
        
    def test_title_search_year(self):
        start = time.time()
        results = query2.by_title("Qian zuo guai", year1 = 1977, year2 = 1982)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertEqual('450459', results[0])
        
    def test_language_search_year(self):
        start = time.time()
        results = query2.by_language("Mandarin", year1 = 1976, year2 = 1978)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('450602', results)
        
    def test_genres_search_year(self):
        start = time.time()
        results = query2.by_genres("Animation Music", year1 = 1948, year2 = 1951)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('593372', results)

    def test_phrase_search_year(self):
        start = time.time()
        results = query2.phrase_search_handler("University Rhodes", year1 = 1997, year2 = 2000)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('593603', results[:15]) 

    def test_proximity_search_year(self):
        start = time.time()
        results = query2.proximity_search("climaxes","Mandela", distance = 15, year1 = 2008, year2 = 2012)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn('231891', results[:15])  

if __name__ == '__main__':
    unittest.main()
    
# TO DO: test color, AND OR NOT in Web
