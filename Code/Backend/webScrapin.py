"""
------------------------------------------------------------
Author: Yvonne Ding
Date: 7th March 2023
Description: Web-scraping IMDb info and convert to XML format
methods
Usage example:
python3 webScrapin.py --url https://www.imdb.com/search/title/?release_date=2010-01-01,2023-01-01 --url_baseline
https://www.imdb.com
------------------------------------------------------------
"""

import argparse
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import urllib.parse


class WebScraping:
    def __init__(self, url, url_baseline):
        self.url = url
        self.url_baseline = url_baseline
        self.doc_id = []  # link to access the page of video details
        self.allInfo = defaultdict(lambda: defaultdict(str))  # {id1: {title: , year: , type: ,colorinfo: ,}, id2:{...}}

    def certainResponse(self, container, curr_class, curr_str):
        res = []
        if curr_str == 'runtime':
            temp = container.p.find(curr_class, class_=curr_str)
            if temp == None:
                return None
            else:
                test = container.p.find(curr_class, class_=curr_str).text.replace(' min', '')
                if test == None:
                    return None
                else:
                    res.append(test)
                    return res
        elif curr_str == 'certificate':
            data_cer = container.find(curr_class, attrs={'class': 'ipl-zebra-list__item', 'id': 'certifications-list'})
            if data_cer == None:
                return None
            else:
                cert_ = data_cer.find_all('li', attrs={'class': 'ipl-inline-list__item'})
                if cert_ == None:
                    return None
                else:
                    for i in cert_:
                        raw_ = i.a.text.split(':')
                        res.append((raw_[0], raw_[1]))
                    return res
        elif curr_str == 'genre':
            res = []
            temp = container.p.find(curr_class, class_=curr_str)
            if temp == None:
                return None
            else:
                test = container.find(curr_class, class_=curr_str)
                if test == None:
                    return None
                else:
                    raw_ = test.text.replace('\n', '')
                    return re.sub(' +', '', raw_).split(',')
        elif curr_str == 'color':
            res = []
            temp = container.find(curr_class,
                                  attrs={'class': 'ipc-metadata-list__item', 'data-testid': 'title-techspec_color'})
            if temp == None:
                return None
            else:
                res.append(temp.a.text)
                return res
        elif curr_str == 'soundmixes':
            temp = container.find(curr_class,
                                  attrs={'class': 'ipc-metadata-list__item', 'data-testid': 'title-techspec_soundmix'})
            if temp == None:
                return None
            else:
                res.append(temp.a.text)
                return res
        elif curr_str == 'keywords':
            k_list = []
            data_keyword_ = container.findAll(curr_class, attrs={'class': 'soda sodavote'})
            if data_keyword_ == None:
                return None
            else:
                for i in data_keyword_:
                    k_list.append(i['data-item-keyword'])
                return k_list
        elif curr_str == 'country':
            data_country = container.find(curr_class, attrs={'class': 'ipc-metadata-list__item',
                                                             'data-testid': 'title-details-origin'})
            if data_country == None:
                return None
            else:
                res.append(data_country.a.text)
                return res
        elif curr_str == 'releasedate':
            date_list = []
            data_released = container.find(curr_class, attrs={'data-testid': 'sub-section-releases',
                                                              'class': 'sc-f65f65be-0 fVkLRr'})
            if data_released == None:
                return None
            else:
                date_ = data_released.find_all('li', attrs={'data-testid': 'list-item'})
                if date_ == None:
                    return None
                else:
                    for i in date_:
                        date_ = ''.join(i.span.text.split(','))
                        date_list.append((i.a['aria-label'], date_))
                    return date_list
            # res.append(container.find(curr_class, class_="ipc-inline-list__item").text)
            # return res
        elif curr_str == 'language':
            data_language = container.find(curr_class, attrs={'class': 'ipc-metadata-list__item',
                                                              'data-testid': 'title-details-languages'})
            if data_language == None:
                return None
            else:
                res.append(data_language.a.text)
                return res

    def getCrew(self, container, curr_class, curr_id):
        crew_ = container.find(curr_class, attrs={'class': "dataHeaderWithBorder", 'id': curr_id})
        if crew_ == None:
            return None
        else:
            contents = crew_.next_sibling.next_sibling
            all_cast = contents.find_all('tr')
            if all_cast == None:
                return None
            else:
                cr_list = []
                for i in all_cast:
                    if i.find('a') == None:
                        continue
                    else:
                        name_ = i.find('a').text.replace('\n', '')
                        cr_list.append(name_)

                return cr_list

    def geCast(self, container, curr_class):
        cast_list = []
        for i in container:
            act_ = defaultdict(str)
            char_ = defaultdict(str)
            act_test = i.find(curr_class, attrs={'data-testid': 'title-cast-item__actor'})
            if act_test == None:
                act_['actor'] = None
            else:
                act_['actor'] = act_test.text
            # role_ = i.find(curr_class, attrs={'data-testid': 'cast-item-characters-link'})
            role_test = i.find('span', attrs={'class':'sc-bfec09a1-4 llsTve'})
            if role_test == None:
                char_['role'] = None
            else:
                char_['role'] = role_test.text
            cast_list.append((act_, char_))

        return cast_list
    
    def getImage(self,title):
        encode_title = urllib.parse.quote(title)
        curr_url = self.url_baseline + '/find/?q=' + encode_title + '&ref_=nv_sr_sm'
        req = requests.get(url=curr_url, headers={'User-Agent': 'Mozilla/5.0'}).text
        curr_page = BeautifulSoup(req, 'html.parser')

        search_access = curr_page.find('div', attrs={'class': 'sc-17bafbdb-2 ffAEHI'})
        response_href = search_access.find('li').a['href']

        target_url = self.url_baseline + response_href
        target_req = requests.get(url=target_url, headers={'User-Agent': 'Mozilla/5.0'}).text
        target_page = BeautifulSoup(target_req, 'html.parser')

        opt_data = target_page.find('div', attrs={
            'class': "ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"})
        if opt_data == None:
            return None
        else:
            return opt_data.img['src']



    def getResponse(self):

        flag = True
        curr_url = self.url
        count = 0
        while count <1:
            print(count)
            count += 1
            response = requests.get(curr_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            data_div = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
            data_page = soup.find('a', attrs={'class':"lister-page-next next-page"})
            curr_url = self.url_baseline + data_page['href']
            print(curr_url)
            test_count = 0
            for container in data_div:
                test_count += 1
                print('test_count: ',test_count)
                curr_info = defaultdict(str)
                raw_id = container.h3.a['href']
                curr_id = raw_id.split('/')[2]
                self.doc_id.append(curr_id)
                curr_info['docid'] = curr_id
                curr_info['title'] = container.h3.a.text
                print(container.h3.a.text)
                curr_info['image'] = self.getImage(container.h3.a.text)
                curr_info['year'] = container.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(',
                                                                                                                        '').replace(
                    ')', '').split('–')[0]
                curr_info['runningtimes'] = self.certainResponse(container, 'span', 'runtime')
                curr_info['genres'] = self.certainResponse(container, 'span', 'genre')
                all_in_text_muted = container.find_all('p', class_='text-muted')
                curr_info['plot'] = all_in_text_muted[1].text.replace('\n', '') if len(all_in_text_muted) > 1 else '*****'

                # Access to the detail page
                curr_ = self.url_baseline + '/title/' + curr_id + '/'
                req = requests.get(url=curr_, headers={'User-Agent': 'Mozilla/5.0'}).text
                curr_page = BeautifulSoup(req, 'html.parser')
                data_detail = curr_page.find('div', attrs={'data-testid': 'title-details-section',
                                                        'class': 'sc-f65f65be-0 fVkLRr'})

                curr_info['countries'] = self.certainResponse(data_detail, 'li', 'country')
                curr_info['languages'] = self.certainResponse(data_detail, 'li', 'language')

                data_tech = curr_page.find('div', attrs={'data-testid': 'title-techspecs-section',
                                                        'class': 'sc-f65f65be-0 fVkLRr'})
                curr_info['colorinfos'] = self.certainResponse(data_tech, 'li', 'color')
                curr_info['soundmixes'] = self.certainResponse(data_tech, 'li', 'soundmixes')

                data_cast = curr_page.findAll('div',
                                            attrs={'data-testid': 'title-cast-item', 'class': 'sc-bfec09a1-5 kUzsHJ'})
                curr_info['cast'] = self.geCast(data_cast, 'a')

                data_type = curr_page.find('meta', attrs={'property': {'og:type'}})
                if len(data_type['content'])==1:
                    curr_info['type'] = data_type['content']
                else:
                    curr_info['type'] = data_type['content'].split('.')[1]

                releaseInfo_ = self.url_baseline + '/title/' + curr_id + '/releaseinfo/?ref_=tt_dt_rdat'
                req_re = requests.get(url=releaseInfo_, headers={'User-Agent': 'Mozilla/5.0'}).text
                re_soup = BeautifulSoup(req_re, 'html.parser')
                curr_info['releasedates'] = self.certainResponse(re_soup, 'div', 'releasedate')

                certificateInfo_ = self.url_baseline + '/title/' + curr_id + '/parentalguide?ref_=tt_stry_pg'
                req_cer = requests.get(url=certificateInfo_, headers={'User-Agent': 'Mozilla/5.0'}).text
                cer_soup = BeautifulSoup(req_cer, 'html.parser')

                curr_info['certificates'] = self.certainResponse(cer_soup, 'tr', 'certificate')

                keywords_ = self.url_baseline + '/title/' + curr_id + '/keywords?ref_=tt_stry_kw'
                req_k = requests.get(url=keywords_, headers={'User-Agent': 'Mozilla/5.0'}).text
                k_soup = BeautifulSoup(req_k, 'html.parser')

                curr_info['keywords'] = self.certainResponse(k_soup, 'td', 'keywords')

                cast_crew_ = self.url_baseline + '/title/' + curr_id + '/fullcredits/?ref_=tt_cl_sm'
                req_c = requests.get(url=cast_crew_, headers={'User-Agent': 'Mozilla/5.0'}).text
                c_soup = BeautifulSoup(req_c, 'html.parser')

                curr_info['directors'] = self.getCrew(c_soup, 'h4', 'director')
                curr_info['composers'] = self.getCrew(c_soup, 'h4', 'composer')
                curr_info['producers'] = self.getCrew(c_soup, 'h4', 'producer')
                curr_info['writers'] = self.getCrew(c_soup, 'h4', 'writer')
                curr_info['editors'] = self.getCrew(c_soup, 'h4', 'editor')


                # print(curr_info)
                self.allInfo[curr_id] = curr_info


    def dict2XML(self):
        for id, values in self.allInfo.items():
            # Create the root element
            root = ET.Element('doc', {'id': id})

            # Loop over each value in the inner defaultdict
            for key, value in values.items():
                # If the value is a list, loop over it and create a separate XML element for each item
                if isinstance(value, list):
                    sub = ET.SubElement(root, key)
                    if key == 'runningtimes':
                        for item in value:
                            ET.SubElement(sub, key[:-1], {'country': "default"}).text = item
                    elif key == 'certificates':
                        for item in value:
                            ET.SubElement(sub, key[:-1], {'country': item[0]}).text = item[1]
                    elif key == 'releasedates':
                        for item in value:
                            ET.SubElement(sub, key[:-1], {'country': item[0]}).text = item[1]
                    elif key == 'cast':
                        for actor_dict, role_dict in value:
                            credit = ET.SubElement(sub, 'credit')
                            actor = ET.SubElement(credit, 'actor')
                            actor.text = actor_dict['actor']
                            role = ET.SubElement(credit, 'role')
                            role.text = role_dict['role']
                    elif key == 'countries':
                        for item in value:
                            ET.SubElement(sub, 'country').text = item
                    elif key == 'soundmixes':
                        for item in value:
                            ET.SubElement(sub, 'soundmix').text = item
                    else:
                        for item in value:
                            ET.SubElement(sub, key[:-1]).text = item
                else:
                    ET.SubElement(root, key).text = value

            # Create the XML tree and write it to a file with the id as its filename
            tree = ET.ElementTree(root)
            xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t")

            with open(os.path.join('../Dataset/IMDB TestData', id + '.xml'), "w", encoding="utf-8") as f:
                f.write(xmlstr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help='URL')
    parser.add_argument('--url_baseline', type=str, help='detail URL')
    args = parser.parse_args()
    webScrap = WebScraping(args.url, args.url_baseline)

    webScrap.getResponse()
    webScrap.dict2XML()
