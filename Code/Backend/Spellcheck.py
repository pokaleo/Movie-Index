import translators as ts
from serpapi import GoogleSearch
from spellchecker import SpellChecker
import deepl


def deepl_trans(text):
    translator = deepl.Translator('f82be482-1b15-f491-da0e-c64e081bd201:fx')
    translated_texts = set([])
    results = translator.translate_text(text, target_lang='EN-GB')
    for result in results:
        translated_texts.add(result.text)
    return list(translated_texts)


def trans_api(string):
    return ts.translate_text(string)


def spellcheck(string):
    params = {
        "q": string,
        "gl": "us",
        "api_key": 'c',
        "num": "1"

    }

    spell_corrected = []
    related_queries = []
    related = []
    search = GoogleSearch(params)
    results = search.get_dict()
    if results:
        search_result = results
    else:
        results =[]
    if "related_searches" in results.keys():
        related = results["related_searches"]
    if 'spelling_fix' in search_result.keys():
        spell_corrected.append(search_result['spelling_fix'])
    if related is not None:
        for query in related:
            related_queries.append(query["query"])
    return spell_corrected, related_queries


def local_spellcheck(string):
    '''
    return a list of string
    '''
    spell = SpellChecker(distance=2)
    es = SpellChecker(language='es')
    fr = SpellChecker(language='fr')
    pt = SpellChecker(language='pt')
    de = SpellChecker(language='de')
    ru = SpellChecker(language='ru')

    words = string.split()
    new_words = []
    res = []
    for checker in [spell, es, fr, pt, de, ru]:
        misspelled = checker.unknown(words)
        for word in words:
            if word in misspelled:
                new_word = checker.correction(word)
                if new_word != None and new_word != word:
                    new_words.append(new_word)
            else:
                new_words.append(word)
        res.append(" ".join(new_words))
        new_words = []
    res = list(set(res))
    return res
