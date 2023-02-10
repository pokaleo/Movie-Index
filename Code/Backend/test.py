import json

import RetrieveData
import DataPreprocessing
import Query

movies = RetrieveData.MovieInfo("../TestDataset")
movies.read_files()
processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
processed_data.tokenise()
processed_data.to_lowercase()
# print(Query.by_title(processed_data.get_data(), "Vincent"))
print(json.dumps(processed_data.get_data(), indent=4))
