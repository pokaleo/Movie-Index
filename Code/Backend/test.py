import json

import RetrieveData
import DataPreprocessing
import Query
import Util

movies = RetrieveData.MovieInfo("../TestDataset")
# movies = RetrieveData.MovieInfo("../Dataset/TestData")
movies.read_files()
movies.get_movie_info()

processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
processed_data.tokenise()
processed_data.to_lowercase()
processed_data.remove_punctuation()
processed_data.stem_data()
processed_data.remove_stopwords()
processed_data.create_index()
query = Query.Query(processed_data)

# print(processed_data.get_index())
# print(processed_data.get_index_title())
# print(json.dumps(movies.get_movie_info(), indent=4))
# print(json.dumps(processed_data.get_data(), indent=4))
# print(query.by_title(processed_data.get_data(), "Vincent"))
# print(query.by_title("vinCeNt #Bfl"))
# print(query.by_general("Lipstick Vincent"))
# print(query.by_genres("comedy"))
# print(query.bm25("vincent","002359"))
# print(query.proximity_search("#15 vishnuvardhan himself"))
# print(query.phrase_search("littlest thing"))
# print(query.proximity_search("#400 work richard"))
# docid_list = query.proximity_search("#400 work richard")
# keywords = "#400 work richard"
# print(query.bm25_ranking(keywords,docid_list,stemming = True))
# print(query.alphabet_ranking(docid_list))
query_tokens = "\"monotonous and passionless marriage\""
query_tokens2 = "\"1st Person Shooter\""
print("test result: ")
print("result: ", query.phrase_search_handler(query_tokens, 1990, 2000, False, None))
print("result2: ", query.phrase_search_handler(query_tokens2, 2000, 2010, True, "title"))
print("result3: ", query.phrase_search_handler("14 ways", None, None, True, "title"))
