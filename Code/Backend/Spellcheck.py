import translators as ts
from serpapi import GoogleSearch
from spellchecker import SpellChecker


def trans_api(string):
    return ts.translate_text(string)

def spellcheck(string):
    params = {
        "q": string,
        "gl": "us",
        "api_key": 'c12acfe0db8b5121456501187b15bee5050b365fcec0a75660456e14aad16a5e'
        }

    search = GoogleSearch(params)
    results = search.get_dict()
    results =results["search_information"]
    if 'spelling_fix' in results.keys():
        return results['spelling_fix']
    return string

def local_spellcheck(string):
    spell = SpellChecker(distance=2)
    words = string.split()
    misspelled = spell.unknown(words)
    new_words = []

    for word in words:
        if word in misspelled:
            new_word=spell.correction(word)
            if new_word != None:
                new_words.append(new_word)
        else:
            new_word.append(word)
    return " ".join(new_words)

