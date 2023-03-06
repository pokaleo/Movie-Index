import argparse
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from dict2xml import dict2xml
import os


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
        # self.keywords = defaultdict(list)
        # self.type = defaultdict(list)
        # self.writers = defaultdict(list)
        # self.composers = defaultdict(list)
        # self.editors = defaultdict(list)
        # self.producers = defaultdict(list)
        # self.cast = defaultdict(list)

        # TODO
        # Cast Image




    def certainResponse(self, container, curr_class, curr_str):
        res = defaultdict(str)
        if curr_str == 'runtime':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                res['runningtime'] = container.p.find(curr_class, class_ = curr_str).text.replace(' min','')
                return res
        elif curr_str == 'certificate':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                res['certificate'] = container.p.find(curr_class, class_ = curr_str).text
                return res
        elif curr_str == 'genre':
            temp = container.p.find(curr_class, class_ = curr_str)
            if temp == None:
                return None
            else:
                raw_ = container.find(curr_class, class_ = curr_str).text.replace('\n','')
                res['genre'] = re.sub(' +', '', raw_).split(',')
                return res
        elif curr_str == 'color':
            temp = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-techspec_color'})
            if temp == None:
                return None
            else:
                res['colorinfo'] = temp.a.text
                return res
        elif curr_str == 'soundmixes':
            temp = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-techspec_soundmix'})
            if temp == None:
                return None
            else:
                res['soundmixe'] = temp.a.text
                return res
        elif curr_str == 'keywords':
            k_list = []
            data_keyword_ = container.findAll(curr_class, attrs={'class':'soda sodavote'})
            for i in data_keyword_:
                k_list.append(i['data-item-keyword'])
            res['keyword'] = k_list
            return res
        elif curr_str == 'country':
            data_country = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-origin'})
            res[curr_str] = data_country.a.text
            return res
        elif curr_str == 'releasedate':
            res[curr_str] = container.find(curr_class, class_="ipc-inline-list__item").text
            return res
        elif curr_str == 'language':
            data_language = container.find(curr_class, attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-languages'})
            res['language'] = data_language.a.text
            return res


    def getCrew(self,container,curr_class,curr_id):
        res = defaultdict(list)
        crew_ = container.find(curr_class,attrs={'class':"dataHeaderWithBorder",'id':curr_id})
        if crew_ == None:
            return None
        else:
            contents = crew_.next_sibling.next_sibling
            all_cast = contents.find_all('tr')
            cr_list = []
            for i in all_cast:
                if i.find('a') == None:
                    continue
                else:
                    name_ = i.find('a').text.replace('\n','')
                    cr_list.append(name_)

            res[curr_id] = cr_list
            return res
    

    def geCast(self,container,curr_class):
        res_cast = defaultdict(dict)
        cast_list = []
        for i in container:
            act_ = defaultdict(str)
            char_ = defaultdict(str)
            act_['actor'] = i.find(curr_class, attrs={'data-testid':'title-cast-item__actor'}).text
            char_['role'] = i.find(curr_class,attrs={'data-testid':'cast-item-characters-link'}).span.text
            cast_list.append((act_, char_))
        res_cast['credit'] = cast_list
        return res_cast
    

    def getResponse(self):

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data_div = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})
        count = 0

        # TEST CASE
        # container = data_div[0]
        # curr_info = defaultdict(str)
        # raw_id = container.h3.a['href']
        # curr_id = raw_id.split('/')[2]
        # self.doc_id.append(curr_id)
        # curr_info['docid'] = curr_id
        # curr_info['title'] = container.h3.a.text
        # curr_info['year'] = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')

        # all_in_text_muted = container.find_all('p', class_ = 'text-muted')
        # curr_info['plot'] = all_in_text_muted[1].text.replace('\n', '') if len(all_in_text_muted) >1 else '*****'
        
        # curr_info['runningtimes'] = self.certainResponse(container,'span','runtime')
        # curr_info['certificates'] = self.certainResponse(container,'span','certificate')
        # curr_info['genres'] = self.certainResponse(container,'span','genre')

        # # Access to the detail page
        # curr_ = self.url_baseline + '/title/'+curr_id+'/'   
        # req = requests.get(url= curr_, headers={'User-Agent': 'Mozilla/5.0'}).text
        # curr_page = BeautifulSoup(req,'html.parser')
        # data_detail = curr_page.find('div', attrs = {'data-testid':'title-details-section','class':'sc-f65f65be-0 fVkLRr'})
        # curr_info['releasedates'] = self.certainResponse(data_detail,'li', 'releasedate')
        # curr_info['countries'] = self.certainResponse(data_detail,'li', 'country')
        # curr_info['languages'] = self.certainResponse(data_detail,'li', 'language')

        # data_tech = curr_page.find('div', attrs = {'data-testid':'title-techspecs-section','class':'sc-f65f65be-0 fVkLRr'})
        # curr_info['colorinfos'] = self.certainResponse(data_tech,'li','color')
        # curr_info['soundmixes'] = self.certainResponse(data_tech,'li','soundmixes')

        # data_cast = curr_page.findAll('div', attrs={'data-testid':'title-cast-item','class':'sc-bfec09a1-5 kUzsHJ'})
        # curr_info['cast'] = self.geCast(data_cast,'a')
        
        # data_type = curr_page.find('meta',attrs={'property':{'og:type'}})
        # curr_info['type'] = data_type['content'].split('.')[1]


        # keywords_ = self.url_baseline + '/title/'+curr_id+'/keywords?ref_=tt_stry_kw'
        # req_k = requests.get(url= keywords_, headers={'User-Agent': 'Mozilla/5.0'}).text
        # k_soup = BeautifulSoup(req_k,'html.parser')

        # curr_info['keywords'] = self.certainResponse(k_soup,'td','keywords')

        # cast_crew_ = self.url_baseline + '/title/'+curr_id+'/fullcredits/?ref_=tt_cl_sm'
        # req_c = requests.get(url= cast_crew_, headers={'User-Agent': 'Mozilla/5.0'}).text
        # c_soup = BeautifulSoup(req_c,'html.parser')

        # curr_info['directors'] = self.getCrew(c_soup,'h4','director') 
        # curr_info['composers'] = self.getCrew(c_soup,'h4','composer')
        # curr_info['producers'] = self.getCrew(c_soup,'h4','producer')
        # curr_info['writers'] = self.getCrew(c_soup,'h4','writer')
        # curr_info['editors'] = self.getCrew(c_soup,'h4','editor')

        # return curr_info


        # ACTUAL CODE

        for container in data_div:
            print(count)
            count +=1
            curr_info = defaultdict(str)
            raw_id = container.h3.a['href']
            curr_id = raw_id.split('/')[2]
            self.doc_id.append(curr_id)
            curr_info['docid'] = curr_id
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
            curr_page = BeautifulSoup(req,'html.parser')
            data_detail = curr_page.find('div', attrs = {'data-testid':'title-details-section','class':'sc-f65f65be-0 fVkLRr'})
            curr_info['releasedates'] = data_detail.find('li', class_="ipc-inline-list__item").text
            data_country = data_detail.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-origin'})
            curr_info['countries'] = data_country.a.text
            data_language = data_detail.find('li', attrs = {'class':'ipc-metadata-list__item','data-testid':'title-details-languages'})
            curr_info['language'] = data_language.a.text

            data_tech = curr_page.find('div', attrs = {'data-testid':'title-techspecs-section','class':'sc-f65f65be-0 fVkLRr'})
            curr_info['colorinfo'] = self.certainResponse(data_tech,'li','color')
            curr_info['soundmixes'] = self.certainResponse(data_tech,'li','soundmixes')

            data_cast = curr_page.findAll('div', attrs={'data-testid':'title-cast-item','class':'sc-bfec09a1-5 kUzsHJ'})
            curr_info['cast'] = self.geCast(data_cast,'a')
            
            data_type = curr_page.find('meta',attrs={'property':{'og:type'}})
            curr_info['type'] = data_type['content'].split('.')[1]


            keywords_ = self.url_baseline + '/title/'+curr_id+'/keywords?ref_=tt_stry_kw'
            req_k = requests.get(url= keywords_, headers={'User-Agent': 'Mozilla/5.0'}).text
            k_soup = BeautifulSoup(req_k,'html.parser')

            curr_info['keywords'] = self.certainResponse(k_soup,'td','keywords')

            cast_crew_ = self.url_baseline + '/title/'+curr_id+'/fullcredits/?ref_=tt_cl_sm'
            req_c = requests.get(url= cast_crew_, headers={'User-Agent': 'Mozilla/5.0'}).text
            c_soup = BeautifulSoup(req_c,'html.parser')

            curr_info['director'] = self.getCrew(c_soup,'h4','director') 
            curr_info['composer'] = self.getCrew(c_soup,'h4','composer')
            curr_info['producer'] = self.getCrew(c_soup,'h4','producer')
            curr_info['writer'] = self.getCrew(c_soup,'h4','writer')
            curr_info['editor'] = self.getCrew(c_soup,'h4','editor')     
            

            print(curr_info)
            self.allInfo[curr_id] = curr_info

    def toXML(self):
        for k, v in self.allInfo.items():
            id = k
            file_name = id + '.xml'
            res_xml= dict2xml(v, 'doc')
            m_encoding = 'utf-8'

            with open(os.path.join('../Dataset/IMDB TestData',file_name), 'w') as xfile:
                xfile.write('<?xml version="1.0" encoding=\"{}\"?>\n'.format(m_encoding))
                xfile.write(res_xml)
                xfile.close()

            





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='URL')
    parser.add_argument('--url_baseline', type=str, help= 'detail URL' )
    args = parser.parse_args()
    webScrap = webScraping(args.url, args.url_baseline)

    a = webScrap.getResponse()
    webScrap.toXML()


# command line: 
# python3 webScrap.py --url https://www.imdb.com/search/title/\?release_date\=2010-01-01,2023-01-01 --url_baseline https://www.imdb.com 
    