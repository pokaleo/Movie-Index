import argparse
import pandas
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


class webScraping:
    def __init__(self, url):
        self.url = url
        self.title = defaultdict(list)
        self.year = defaultdict(list)
        self.type = defaultdict(list)
        self.colorinfo = defaultdict(list)
        self.editors = defaultdict(list)
        self.genres = defaultdict(list)
        self.keywords = defaultdict(list)
        self.language = defaultdict(list)
        self.soundmixes = defaultdict(list)
        self.countries = defaultdict(list)
        self.certificates = defaultdict(list)
        self.releasedates = defaultdict(list)
        self.runningtimes = defaultdict(list)
        self.directors = defaultdict(list)
        self.producers = defaultdict(list)
        self.writers = defaultdict(list)
        self.composers = defaultdict(list)
        self.cast = defaultdict(list)
        self.plot = defaultdict(list)




    def getResponse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data_info = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})
        for i in data_info:
            name = i.h3.a.text
            year_of_release = store.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')       
            runtime = store.p.find('span', class_ = 'runtime').text.replace(' min', '')     
            rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')    
            meta  = store.find('span', class_ = 'metascore').text.replace(' ', '') if store.find('span', class_ = 'metascore') else '^^^^^^'

            #since, gross and votes have same attributes, that's why we had created a common variable and then used indexing
            value = store.find_all('span', attrs = {'name': 'nv'})
            

            # Description of the Movies -- Not explained in the Video, But you will figure it out. 
            plot = store.find_all('p', class_ = 'text-muted')
            description_ = plot[1].text.replace('\n', '') if len(plot) >1 else '*****'

            
            #Cast Details -- Scraping Director name and Stars -- Not explained in Video
            cast = store.find("p", class_ = '')
            cast = cast.text.replace('\n', '').split('|')
            cast = [x.strip() for x in cast]
            cast = [cast[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
            # Director.append(cast[0])
            # Stars.append([x.strip() for x in cast[1].split(",")])
        







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='URL')
    args = parser.parse_args()
    webScrap = webScraping(args.url)

    webScrap.getResponse()
    