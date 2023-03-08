import argparse
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from xml.dom.minidom import parseString
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

import urllib.parse


class imageRequest:
    def __init__(self,url_baseline,file_path):
        self.url_baseline = url_baseline
        self.file_path = file_path
        self.movieInfo = defaultdict(lambda: defaultdict(str))
        self.images = self.getResponse()

    def get_movie_info(self):
        for filename in os.listdir(self.file_path):
            file = os.path.join(self.file_path, filename)
            # checking if it is a file
            if os.path.isfile(file):
                tree = ET.parse(file)
                root = tree.getroot()
                title = urllib.parse.quote(root.find('title').text)
                id = root.find('docid').text
                movie_dict = {'title': urllib.parse.quote(root.find('title').text)}
                self.movieInfo[id] = movie_dict


    

    def getResponse(self):
        imageInfo = defaultdict(lambda: defaultdict(str))
        for k,v in self.movieInfo.items():
            one_image = defaultdict(str)
            curr_ = self.url_baseline + '/find/?q='+ v['title'] + '&ref_=nv_sr_sm'
            req = requests.get(url= curr_, headers={'User-Agent': 'Mozilla/5.0'}).text
            curr_page = BeautifulSoup(req,'html.parser')
            
            search_access = curr_page.find('div', attrs={'class':'sc-17bafbdb-2 ffAEHI'})
            response_href = search_access.find('li').a['href']
            
            target_url = self.url_baseline + response_href
            target_req = requests.get(url= target_url, headers={'User-Agent': 'Mozilla/5.0'}).text
            target_page = BeautifulSoup(target_req,'html.parser')

            opt_data = target_page.find('div', attrs={'class':"ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"})
            one_image['poster'] = opt_data.img['src']
            imageInfo[k] = one_image
        return imageInfo
    
    def return_image(self,title):
        """
        Return image url by giving the corresponding title

        Args:
            title: String -> a title

        Returns:
            String -> Image url

        """
        encode_title = urllib.parse.quote(title)
        url_baseline = 'https://www.imdb.com'
        curr_url = url_baseline + '/find/?q='+ encode_title + '&ref_=nv_sr_sm'
        req = requests.get(url= curr_url, headers={'User-Agent': 'Mozilla/5.0'}).text
        curr_page = BeautifulSoup(req,'html.parser')
        
        search_access = curr_page.find('div', attrs={'class':'sc-17bafbdb-2 ffAEHI'})
        response_href = search_access.find('li').a['href']
        
        target_url = url_baseline + response_href
        target_req = requests.get(url= target_url, headers={'User-Agent': 'Mozilla/5.0'}).text
        target_page = BeautifulSoup(target_req,'html.parser')

        opt_data = target_page.find('div', attrs={'class':"ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"})
        print(opt_data.img['src'])
        return opt_data.img['src']
    
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_baseline', type=str, help='url baseline')
    parser.add_argument('--file_path', type=str, help='path to movie dataset')
    args = parser.parse_args()
    imageR = imageRequest(args.url_baseline, args.file_path)

    # imageR.get_movie_info()
    # imageR.getResponse()
    imageR.return_image('Aftersun')


# command line: 
# python3 imageRequest.py --url_baseline https://www.imdb.com --file_path Your/Path/To/TestDataset