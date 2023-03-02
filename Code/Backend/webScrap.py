import argparse
import pandas
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from urllib.request import Request, urlopen


class webScraping:
    def __init__(self, url,url_baseline):
        self.url = url
        self.url_baseline = url_baseline
        self.doc_id = [] # link to access the page of video details
        self.allInfo = defaultdict(lambda: defaultdict(str)) # {id1: {title: , year: , type: ,colorinfo: ,}, id2:{...}}
        
        # DONE
        # self.title = defaultdict(list)
        # self.year = defaultdict(list) 
        # self.runningtimes = defaultdict(list) 
        # self.certificates = defaultdict(list) 
        # self.genres = defaultdict(list) 
        # self.plot = defaultdict(list) 
        # self.releasedates = defaultdict(list)
        # self.countries = defaultdict(list) 
        # self.language = defaultdict(list)       

        # TODO
        # self.type = defaultdict(list)
        # self.colorinfo = defaultdict(list)
        # self.editors = defaultdict(list)
        # self.keywords = defaultdict(list)
        # self.soundmixes = defaultdict(list)
        # self.directors = defaultdict(list)
        # self.producers = defaultdict(list)
        # self.writers = defaultdict(list)
        # self.composers = defaultdict(list)
        # self.cast = defaultdict(list)

    def certainResponse(self, container, curr_class, curr_str):
        temp = container.p.find(curr_class, class_ = curr_str)
        res = None
        if temp == None:
            return res
        else:
            if curr_str == 'runtime':
                return container.p.find(curr_class, class_ = curr_str).text.replace(' min','')
            elif curr_str == 'certificate':
                return container.p.find(curr_class, class_ = curr_str).text
            elif curr_str == 'genre':
                raw_ = container.find('span', class_ = 'genre').text.replace('\n','')
                return re.sub(' +', '', raw_)

 

    def getResponse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data_div = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})
        # print(data_div[0].find_all('p', class_ = 'text-muted'))
        for container in data_div:
            curr_info = defaultdict(str)
            raw_id = container.h3.a['href']
            curr_id = raw_id.split('/')[2]
            self.doc_id.append(curr_id)
            curr_info['title'] = container.h3.a.text
            curr_info['year'] = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
            curr_info['runningtimes'] = self.certainResponse(container,'span','runtime')
            curr_info['certificates'] = self.certainResponse(container,'span','certificate')
            curr_info['genres'] = self.certainResponse(container,'span','genre')
            all_in_text_muted = container.find_all('p', class_ = 'text-muted')
            curr_info['plot'] = all_in_text_muted[1].text.replace('\n', '') if len(all_in_text_muted) >1 else '*****'
            
            # Access to the detail page
            curr_ = self.url_baseline + '/title/'+curr_id+'/'   
            req = requests.get(url= curr_, headers={'User-Agent': 'Mozilla/5.0'}).text
            curr_soup = BeautifulSoup(req,'html.parser')
            data_div = curr_soup.find('div', attrs = {'data-testid':'title-details-section','class':'sc-f65f65be-0 fVkLRr'})
            curr_info['releasedates'] = data_div.find('li', class_="ipc-inline-list__item").text
            data_country = data_div.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-origin'})
            curr_info['countries'] = data_country.a.text
            data_language = data_div.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-languages'})
            curr_info['language'] = data_language.a.text
            self.allInfo[curr_id] = curr_info

            # rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')    
            # meta  = store.find('span', class_ = 'metascore').text.replace(' ', '') if store.find('span', class_ = 'metascore') else '^^^^^^'

            # #since, gross and votes have same attributes, that's why we had created a common variable and then used indexing
            # value = store.find_all('span', attrs = {'name': 'nv'})


            # print(self.allInfo)
            # #Cast Details -- Scraping Director name and Stars -- Not explained in Video
            # cast = store.find("p", class_ = '')
            # cast = cast.text.replace('\n', '').split('|')
            # cast = [x.strip() for x in cast]
            # cast = [cast[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
            # Director.append(cast[0])
            # Stars.append([x.strip() for x in cast[1].split(",")])
        

            print(curr_info)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='URL')
    parser.add_argument('--url_baseline', type=str, help= 'detail URL' )
    args = parser.parse_args()
    webScrap = webScraping(args.url, args.url_baseline)

    webScrap.getResponse()
    # webScrap.getDetailResponse()


# command line: 
# python3 webScrap.py --url https://www.imdb.com/search/title/\?release_date\=2010-01-01,2023-01-01 --url_baseline https://www.imdb.com 
    