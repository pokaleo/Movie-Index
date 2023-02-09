import  xml.dom.minidom
import re
import numpy as np
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def get_xml_elements(file_name):
    path_name = "xml-utf8_with_plots_with_url"
    dom = xml.dom.minidom.parse(path_name +"/"+file_name)
    root = dom.documentElement
    dd = root.getElementsByTagName('docid')
    tt = root.getElementsByTagName('title')
    kk = root.getElementsByTagName('keyword')
    pp = root.getElementsByTagName('plot')
    d=dd[0]
    t=tt[0]
    p=pp[0]
    k = ""
    for i in range(len(kk)):
        k_ = kk[i].firstChild.data
        k=k+" "+k_ 
    text_content = t.firstChild.data + k + p.firstChild.data
    return d.firstChild.data, text_content

import os
path = "C:/Users/86180/xml-utf8_with_plots_with_url" 
files= os.listdir(path) 
movie_index = []
movie_content = []
for file in files: 
    movie_index.append(get_xml_elements(file)[0])
    movie_content.append(get_xml_elements(file)[1])

# Tokenisation: delete the punctuation mark, convert character into lowercase and split the sentence 
# Delete stopping words

# Stopping words
with open("C:\\Users\\86180\\Desktop\\Msc\\Text-2\\CW2\\englishST.txt", 'r') as stop_words:
    stop_words = stop_words.read().split()
print(stop_words)
    
movie_content1 =[]
for text in movie_content:
    word_final = []
    text = re.sub(r'[\W\\\\]',' ',text).lower().split()
    for word in text:
        if word not in stop_words:
                word_final.append(ps.stem(word))
    movie_content1.append(word_final)
print(movie_content1)

# Create a list to store the unique term
empty_list = []
for news in movie_content1:
    for word in news:
        empty_list.append(word)
trec_uni = np.unique(empty_list)
trec_uni=trec_uni.tolist()

# Define a function to find the position for the term t in document d
def get_index1(lst=None, item=''):
        return [index+1 for (index,value) in enumerate(lst) if value == item]


# Create a list to store df(t) (number of documents term t appeared in) of each term
list_k =[]
for word in trec_uni:
    k = 0
    for news in movie_content1:
        if word in news:
            k = k+1
    list_k.append(k)

# Save the output as index.txt
path = "C:\\Users\\86180\\Desktop\\index.txt" 
with open(path, 'r+', encoding='UTF-8') as file0:  
    for word in trec_uni:
        count = -1
        # print the term and the df(t) (number of documents term t appeared in) of each term
        print(word+':'+str(list_k[trec_uni.index(word)]), file=file0)
        for news in movie_content1:
            count = count + 1
            if word in news:
                # get the docID for each term
                news_index = str(movie_index[count])
                # get the posID for each term in document[docID]
                pos_index = str(get_index1(news, item=word))
                print("\t"+ news_index+': '+ pos_index.replace('[','').replace(']','').replace(' ', ''), file=file0)
        print("",file=file0)
    print("\n", file=file0)           
file0.close()