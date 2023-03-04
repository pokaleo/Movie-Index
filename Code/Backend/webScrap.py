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
        # self.colorinfo = defaultdict(list)
        # self.soundmixes = defaultdict(list)
        # self.directors = defaultdict(list)
        # self.cast = defaultdict(list)

        # TODO
        # self.type = defaultdict(list)
        # self.editors = defaultdict(list)
        # self.keywords = defaultdict(list)
        # self.producers = defaultdict(list)
        # self.writers = defaultdict(list)
        # self.composers = defaultdict(list)


    def certainResponse(self, container, curr_class, curr_str):
        if curr_str == 'runtime':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                return container.p.find(curr_class, class_ = curr_str).text.replace(' min','')
        elif curr_str == 'certificate':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                return container.p.find(curr_class, class_ = curr_str).text
        elif curr_str == 'genre':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                raw_ = container.find(curr_class, class_ = curr_str).text.replace('\n','')
                return re.sub(' +', '', raw_)
        elif curr_str == 'color':
            temp = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-techspec_color'})
            if temp == None:
                return None
            else:
                return temp.a.text
        elif curr_str == 'soundmixes':
            temp = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-techspec_soundmix'})
            if temp == None:
                return None
            else:
                return temp.a.text
        elif curr_str == 'director':
            temp = container.find_all(curr_class, attrs = {'class':'ipc-inline-list__item'})
            if temp == None:
                return None
            else:
                director_ = ''
                for i in temp:
                    if i == temp[-1]:
                        dir_ = i.find('a', attrs={'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                        director_ = director_ + dir_.text
                    else:
                        dir_ = i.find('a', attrs={'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                        director_ = director_ + dir_.text + ', '
                print(director_)

    def getCredit(self, container, curr_class, curr_str):

        if curr_str == 'cast':
            cast_list = ''
            for i in container:
                if i == container[-1]:
                    cast_ = i.find(curr_class, attrs={'data-testid':'title-cast-item__actor'})
                    cast_list = cast_list + cast_.text
                else:
                    cast_ = i.find(curr_class, attrs={'data-testid':'title-cast-item__actor'})
                    cast_list = cast_list + cast_.text + ', '
            # print(cast_list)
            return cast_list
        elif curr_str =='director':
            temp = container.find_all(curr_class, attrs = {'class':'ipc-inline-list__item'})
            if temp == None:
                return None
            else:
                director_ = ''
                for i in temp:
                    if i == temp[-1]:
                        dir_ = i.find('a', attrs={'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                        director_ = director_ + dir_.text
                    else:
                        dir_ = i.find('a', attrs={'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
                        director_ = director_ + dir_.text + ', '
                # print(director_)
                return director_


    def getResponse(self):

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data_div = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})
        print(len(data_div))
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
            data_detail = curr_soup.find('div', attrs = {'data-testid':'title-details-section','class':'sc-f65f65be-0 fVkLRr'})
            curr_info['releasedates'] = data_detail.find('li', class_="ipc-inline-list__item").text
            data_country = data_detail.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-origin'})
            curr_info['countries'] = data_country.a.text
            data_language = data_detail.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-languages'})
            curr_info['language'] = data_language.a.text

            data_tech = curr_soup.find('div', attrs = {'data-testid':'title-techspecs-section','class':'sc-f65f65be-0 fVkLRr'})
            curr_info['colorinfo'] = self.certainResponse(data_tech,'li','color')
            curr_info['soundmixes'] = self.certainResponse(data_tech,'li','soundmixes')

            data_director = curr_soup.find('div', attrs={'class':'ipc-metadata-list-item__content-container'})
            curr_info['directors'] = self.getCredit(data_director,'li','director')

            data_cast = curr_soup.findAll('div', attrs={'data-testid':'title-cast-item','class':'sc-bfec09a1-5 kUzsHJ'})
            curr_info['cast'] = self.getCredit(data_cast,'a','cast')



            print(curr_info)
            self.allInfo[curr_id] = curr_info
            





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
    