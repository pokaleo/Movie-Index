"""
------------------------------------------------------------
Author: Leo LI
Date: 10th Feb 2023
Description: Responsible for retrieve results for different
types of queries
------------------------------------------------------------
"""


class Query:
    def __init__(self, dataset):
        self.dataset = dataset.get_data()
        self.index_general = dataset.get_index()
        self.index_title = dataset.get_index_title()
        self.average_number_of_terms = self.__cal_average_number_of_terms()

    # Naive implementation of search by title without ranking
    def by_title(self, keywords):
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                return self.__plain_search(keywords[0].lower(), "title")
            else:
                result = []
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "title")
                return list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
            
    # Naive implementation of search by keywords without ranking
    def by_keywords(self, keywords):
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                return self.__plain_search(keywords[0].lower(), "keywords")
            else:
                result = []
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower(), "keywords")
                return list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
    
    # Naive implementation of search for general without ranking
    def by_general(self, keywords):
        if keywords:
            keywords = keywords.split()
            # if search for a single word
            if len(keywords) == 1:
                return self.__plain_search(keywords[0].lower())
            else:
                result = []
                for keyword in keywords:
                    result += self.__plain_search(keyword.lower())
                return list(dict.fromkeys(result))
        else:
            raise Exception("Keywords is empty!")
    
    # Method to perform plain single word search
    def __plain_search(self, word_to_be_queried, attributes=None):
        result = []
        # Detect if the search is specified to an attribute
        if attributes:
            if attributes == "title":
                for doic, info in self.dataset.items():
                    if word_to_be_queried in info['title']:
                        result.append(doic)
            if attributes == "keywords":
                for doic, info in self.dataset.items():
                    if word_to_be_queried in info['keywords']:
                        result.append(doic)
        # Use general research if no attribute input 
        else:
            for doic, info in self.dataset.items():
                for attribute in info.keys():
                    if word_to_be_queried in info[attribute]:
                        result.append(doic)
        return result
    
    # Method to perform single word search with docid and position
    def __position_search(self, word_to_be_queried):
        from nltk.stem.snowball import SnowballStemmer
        word1 = SnowballStemmer(language='english').stem(word_to_be_queried.lower())
        word2 = word_to_be_queried.lower()
        if word1 or word2 in self.index_general.keys():
            if word1 in self.index_general.keys():
                result = self.index_general[word1][1]
            if word2 in self.index_general.keys():
                result= self.index_general[word2][1]
                return result
            else:
                raise Exception("We did not find the result!")
        else: 
            raise Exception("We did not find the result!")
        
    
    # Proximity Search : "#distance word1 word2"
    def proximity_search(self, keywords):
        import re
        if keywords:
            keywords = keywords.split()
            if not re.match(r'#\d*', keywords[0]): 
                return Exception("The format is wrong!")
            else:
                if len(keywords) != 3:
                    return Exception("The format is wrong!")
                else:
                    distance = int(keywords[0].strip("#"))
                    keyword1 = keywords[1]
                    keyword2 = keywords[2]
                    dict1 = self.__position_search(keyword1)
                    dict2 = self.__position_search(keyword2)
                    # if in common document
                    common_doic = list(dict1.keys() & dict2.keys())
                    if common_doic:
                        result = []
                        for doic in common_doic:
                            for position1 in dict1[doic]:
                                if not position1.isdigit():
                                    continue
                                for position2 in dict2[doic]:
                                    if not position2.isdigit():
                                        continue
                                    if abs(int(position1) - int(position2)) <= distance:
                                        result.append(doic)
                        if result:
                            return list(dict.fromkeys(result))
                        else:
                            raise Exception("We did not find the result!")
                    else:
                        raise Exception("We did not find the result!")                
        else:
            raise Exception("Keywords is empty!")
        
    # Phrase Search : "word1 word2"
    def phrase_search(self, keywords):
        if keywords:
            keywords = keywords.split()
            if len(keywords) != 2:
                return Exception("The format is wrong!")
            else:
                keyword1 = keywords[0]
                keyword2 = keywords[1]
                dict1 = self.__position_search(keyword1)
                dict2 = self.__position_search(keyword2)
                # if in common document
                common_doic = list(dict1.keys() & dict2.keys())
                if common_doic:
                    result = []
                    for doic in common_doic:
                         for position1 in dict1[doic]:
                            if not position1.isdigit():
                                continue
                            for position2 in dict2[doic]:
                                if not position2.isdigit():
                                    continue
                                if int(position2) - int(position1) == 1 or int(position2) - int(position1) == 0:
                                    result.append(doic)
                    if result:
                        return list(dict.fromkeys(result))
                    else:
                        raise Exception("We did not find the result!")
                else:
                    raise Exception("We did not find the result!")                
        else:
            raise Exception("Keywords is empty!")
    
    
    def __term_frequency(self, word_to_be_queried, docid):
        # TODO information in cast missing
        if docid in self.index_general[word_to_be_queried][1]:
            return len(self.index_general[word_to_be_queried][1][docid])
        else:
            return 0.1

    def __document_frequency(self, word_to_be_queried):
        return len(self.index_general[word_to_be_queried][1])

    def __cal_average_number_of_terms(self):
        number_of_tokens = 0
        for docid, info in self.dataset.items():
            for attribute, token in info.items():
                number_of_tokens += len(token)
        return number_of_tokens/len(self.dataset)

    def __number_of_terms(self, docid):
        number_of_tokens = 0
        for attribute, token in self.dataset[docid].items():
            number_of_tokens += len(token)
        return number_of_tokens
    
    # Use Okapi BM25 to calculate the Ranking 
    def bm25(self, word_to_be_queried, docid):
        import math
        k = 1.5
        N = len(self.dataset.keys())
        L_division = self.__number_of_terms(docid)\
                    /self.__cal_average_number_of_terms()
        restpart = (N - self.__document_frequency(word_to_be_queried) + 0.5)\
                    /(self.__document_frequency(word_to_be_queried) + 0.5)
        w_td = format(math.log10(restpart) * self.__term_frequency(word_to_be_queried, docid)\
                /((k * L_division) + self.__term_frequency(word_to_be_queried, docid) + 0.5), '.4f')
        w_td = float(w_td)
        return w_td

    def bm25_ranking(self,keywords,docid_list,stemming = False):
        keywords = keywords.lower()
        term_list = keywords.split(' ')
        if not re.match(r'#\d*', term_list[0]):
            keywords = keywords
        else:
            del term_list[0]
        if stemming == True:
            from nltk.stem.snowball import SnowballStemmer
            for term in term_list:
                stemmed_term = SnowballStemmer(language='english').stem(term)
                if stemmed_term not in term_list:
                    term_list.append(stemmed_term)
        bm25score_list = []
        for docid in docid_list:
            sum = 0
            for term in term_list:
                bm25_score = self.bm25(term,docid)
                sum = sum + bm25_score
            bm25score_list.append(sum)
        ordered_list = sorted(docid_list,key = lambda x:bm25score_list[docid_list.index(x)],reverse=True)
        return ordered_list

    def alphabet_ranking(self,docid_list):
        title_list = []
        for docid in docid_list:
            temp_list = self.dataset[docid]['title']
            title = ' '.join(temp_list)
            title_list.append(title)
        print(title_list)
        ordered_list = sorted(docid_list,key = lambda x:title_list[docid_list.index(x)],reverse=False)
        return ordered_list

    #TODO: define a function to decide using which ranking method in several kinds of situation, for example using alphabet_ranking when producting by_title search etc.
