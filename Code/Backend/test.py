import json

import RetrieveData
import DataPreprocessing
import Query

movies = RetrieveData.MovieInfo("../TestDataset")
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
#print(json.dumps(movies.get_movie_info(), indent=4))
# print(json.dumps(processed_data.get_data(), indent=4))
# print(Query.by_title(processed_data.get_data(), "Vincent"))
print(query.by_title("vinCeNt #Bfl"))

