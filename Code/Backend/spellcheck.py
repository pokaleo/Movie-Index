import nltk
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
import translators as ts
from serpapi import GoogleSearch

nltk.download('words')
from nltk.corpus import words

def local_correct(string):
    correct_words = words.words()

    incorrect_words=['happpy', 'azmaing', 'Deutsch']

    for word in incorrect_words:
        temp = [(jaccard_distance(set(ngrams(word, 2)),
                                  set(ngrams(w, 2))),w)
    for w in correct_words if w[0]==word[0]]
        print(sorted(temp, key = lambda val:val[0])[0][1])

def trans_api(string):
    return ts.translate_text(string)

def spellcheck(string):
    params = {
        "q": string,
        #"hl": "en",
        "gl": "us",
        "api_key": 'c12acfe0db8b5121456501187b15bee5050b365fcec0a75660456e14aad16a5e'
        }

    search = GoogleSearch(params)
    results = search.get_dict()
    results =results["search_information"]
    if 'spelling_fix' in results.keys():
        return results['spelling_fix']
    return string

print(spellcheck('happiey'))