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
                              'plot': root.find('plot').text}
                colorinfos = []
                for colorinfo in root.iter('colorinfo'):
                    colorinfos.append(colorinfo.text)
                movie_dict['colorinfos'] = colorinfos
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
                languages = []
                for language in root.iter('language'):
                    languages.append(language.text)
                movie_dict['languages'] = languages
                soundmixes = []
                for soundmix in root.iter('soundmix'):
                    soundmixes.append(soundmix.text)
                movie_dict['soundmixes'] = soundmixes
                countries = []
                for country in root.iter('country'):
                    countries.append(country.text)
                movie_dict['countries'] = countries
                certificates = []
                for certificate in root.iter('certificate'):
                    certificates.append([certificate.attrib['country'], certificate.text])
                movie_dict['certificates'] = certificates
                releasedates = []
                for releasedate in root.iter('releasedate'):
                    releasedates.append([releasedate.attrib['country'], releasedate.text])
                movie_dict['releasedates'] = releasedates
                runningtimes = []
                for runningtime in root.iter('runningtime'):
                    runningtimes.append([runningtime.attrib['country'], runningtime.text])
                movie_dict['runningtimes'] = runningtimes
                directors = []
                for director in root.iter('director'):
                    directors.append(director.text)
                movie_dict['directors'] = directors
                writers = []
                for writer in root.iter('writer'):
                    writers.append(writer.text)
                movie_dict['writers'] = writers
                composers = []
                for composer in root.iter('composer'):
                    composers.append(composer.text)
                movie_dict['composers'] = composers
                actors = []
                for actor in root.iter('actor'):
                    actors.append(actor.text)
                roles = []
                for role in root.iter('role'):
                    roles.append(role.text)
                cast = {}
                for i in range(0,len(actors)):
                    cast[actors[i]] = roles[i]
                movie_dict['cast'] = cast
                self.__movies[root.find('docid').text] = movie_dict
            else:
                raise Exception(os.path + " is not a file!")

    # Getter for the fed-in movie information
    def get_movie_info(self):
        if self.__movies:
            return self.__movies
        else:
            raise Exception("The dataset is empty or has not been processed!")
