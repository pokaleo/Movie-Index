import translators as ts
from serpapi import GoogleSearch


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

#print(spellcheck('happiey'))
