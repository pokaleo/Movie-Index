"""
------------------------------------------------------------
Author: Leo LI
Date: 9th Feb 2023
Description: Acting as the API to read in and retrieve the
movie info from the dataset by providing the path to the
dataset
------------------------------------------------------------
"""
import os
import xml.etree.ElementTree as ET

# ==============================================================================

"""
Class handling the interaction with the dataset
"""


class MovieInfo:
    # Check if the filepath is empty
    def __init__(self, file_path):
        self.file_path = file_path
        if self.file_path == "":
            raise Exception('The file path entered for the dataset is empty!')
        if not os.path.exists(self.file_path):
            raise Exception("Path of the dataset is invalid!")
        if os.listdir(self.file_path) == 0:
            raise Exception("The given dir for the dataset is empty!")
        self.__movies = {}

    # Read in all files from the given path
    def read_files(self):
        for filename in os.listdir(self.file_path):
            file = os.path.join(self.file_path, filename)
            # checking if it is a file
            if os.path.isfile(file):
                tree = ET.parse(file)
                root = tree.getroot()
                movie_dict = {'title': root.find('title').text,
                              'year': root.find('year').text, 'type': root.find('type').text,
                              'colorinfo': root.find('./colorinfos/colorinfo').text}
                editors = []
                for editor in root.iter('editor'):
                    editors.append(editor.text)
                movie_dict['editors'] = editors
                genres = []
                for genre in root.iter('genre'):
                    genres.append(genre.text)
                movie_dict['genres'] = genres
                keywords = []
                for keyword in root.iter('keyword'):
                    keywords.append(keyword.text)
                movie_dict['keywords'] = keywords
                self.__movies[root.find('docid').text] = movie_dict
            else:
                raise Exception(os.path + " is not a file!")

    # Getter for the fed-in movie information
    def get_movie_info(self):
        if self.__movies:
            return self.__movies
        else:
            raise Exception("The dataset is empty or has not been processed!")
