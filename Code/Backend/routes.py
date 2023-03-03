from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import time

import json
import RetrieveData
import DataPreprocessing
import Query
import Spellcheck
import JSONParser
import Util

movies = RetrieveData.MovieInfo("../Dataset/IMDB Movie Info")
movies.read_files()
moviedict = movies.get_movie_info()
processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
processed_data.tokenise()
processed_data.to_lowercase()
processed_data.remove_punctuation()
processed_data.stem_data()
processed_data.remove_stopwords()
processed_data.create_index()
query = Query.Query(processed_data)

app = Flask(__name__)
CORS(app, supports_credentials=True)
#cors = CORS(app, resources={r"/test": {"origins": "*"}})

@app.route('/')
def foo():
    return 'test!'

@app.route('/test', methods=['GET','POST'])
def testQuery():
    data = request.get_json()
    queryMsg= data.get('query')
    response = {
        'results': 'This is a test result! \n Your input is' + queryMsg,
        'title':[],
    }
    print('data (json): ', data)
    print('query: ', data.get('query'))
    return jsonify(response)

@app.route('/movie/<id>', methods=['GET','POST'])
def getMovie(id):
    print(id)
    response = moviedict[id]
    print(response)
    return jsonify(response)

@app.route('/search', methods=['GET','POST'])
def searchQuery():
    # get request
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args
        #data=json.dumps(data)
    '''
    parse the data
    parsed_args = {'queryMsg':"",
            'by':"", # a str for search category, i.e. title, any, genres, keywords, proximity
            'need_check':False, # for debug only
            'color':"", # a str in ["all", "bw", "color"]
            'from':0, # int or None
            'to':9999, # int or None
            'additionQ':True, # a boolean value to check whether it is advanced search or not
            'andQueries':[],# list of tuples (by, query), i.e. (title, "Vincent")
            'orQueries':[], # list of tuples (by, query), i.e. (title, "Vincent")
            'notQueries':[] # list of tuples (by, query), i.e. (title, "Vincent")
        }
    '''
    parsed_args = JSONParser.dataParse(data, request.method)
    print(parsed_args)

    #print(type(queryMsg))
    queryMsg=parsed_args['queryMsg']
    #function to wrap up
    
    def formatRes(id):
        doc = {
            "id": id,
            "movieName": moviedict[id]['title'],
            "description": moviedict[id]['plot'],
            "director": moviedict[id]['directors'],
            "year": moviedict[id]['year'],
            "country": moviedict[id]['countries'],
            "runtime": moviedict[id]['runningtimes']
        }
        return doc
    
    #Add function for extract results
    st = time.time()
    st_cpu = time.process_time()

    search_method = {
        'title': query.by_title,
        'keywords': query.by_keywords,
        'genres': query.by_genres,
        'proximity': query.proximity_search,
        'any': query.by_general
        }

    if parsed_args['by'] == 'title':
        res = search_method[parsed_args['by']](queryMsg, parsed_args['from'], parsed_args['to'])  
        print("By title",res)
    elif parsed_args['by'] == 'keywords':
        res = query.by_keywords(queryMsg, parsed_args['from'], parsed_args['to'])
        print("By keywords",res)
    elif parsed_args['by'] == 'genres':
        res = query.by_genres(queryMsg, parsed_args['from'], parsed_args['to'])
        print("By genres",res)
    elif parsed_args['by'] == 'proximity':
        res = query.proximity_search(queryMsg)
        print("By proximity",res)
    else:
        res = query.by_general(queryMsg, parsed_args['from'], parsed_args['to'])
        print("By general",res)
    
    if parsed_args['additionQ']:
        if len(parsed_args['andQueries'])>0:
            print("AND",parsed_args['andQueries'])
            for q in parsed_args['andQueries']:
                print(q)
                if q[0] != 'proximity':
                    new_res = search_method[q[0]](q[1], parsed_args['from'], parsed_args['to']) 
                else:
                    new_res = search_method[q[0]](q[1]) 
                new_res = set(new_res)
                res = [value for value in res if value in new_res]
        if len(parsed_args['notQueries'])>0:
            for q in parsed_args['notQueries']:
                if q[0] != 'proximity':
                    new_res = search_method[q[0]](q[1], parsed_args['from'], parsed_args['to']) 
                else:
                    new_res = search_method[q[0]](q[1]) 
                new_res = set(new_res)
                res = [value for value in res if value not in new_res]
        if len(parsed_args['orQueries'])>0:
            for q in parsed_args['orQueries']:
                if q[0] != 'proximity':
                    new_res = search_method[q[0]](q[1], parsed_args['from'], parsed_args['to']) 
                else:
                    new_res = search_method[q[0]](q[1]) 
                res = set(res).union(new_res)
    res = list(res)
    print(res)
    reslist = []
    id_res=[]
    #final_ses = []
    for id in res:
        if parsed_args['color'] == 'bw':
            if 'Black and White' not in moviedict[id]['colorinfos']:
                continue
        elif parsed_args['color'] == 'color':
            if 'Color' not in moviedict[id]['colorinfos']:
                continue
        reslist.append(formatRes(id))
        id_res.append(id)

    ed = time.time()
    ed_cpu = time.process_time()

    response = {
        'results': reslist,
        'ids': id_res,
        'wallT': round((ed-st)*1000, 6),
        'cpuT': round((ed_cpu-st_cpu)*1000, 6),
    }
    
    #print('data: ', data)
    #print()
    #return jsonify({})
    return jsonify(response)

@app.route('/spellcheck', methods=['GET','POST'])
def spell():
    '''
    #query translate and spell check
    '''
    data = request.args
    msg = data.get('input')
    corrected = []
    try:
        correct=Spellcheck.spellcheck(msg)
        if isinstance(correct,str):
            corrected.append(correct)
        print("try",corrected)
    except:
        corrected=Spellcheck.local_spellcheck(msg)
        print("except",corrected)
    print(corrected)
    sentences = corrected
    sentences.append(msg)
    print("test1",sentences)
    sentences = set(sentences)
    print("test2",sentences)
    translist = []

    try:
        translist = Spellcheck.deepl_trans(list(sentences))
    except:
        for sen in sentences:
            trans = Spellcheck.trans_api(sen)
            if isinstance(trans, str):
                translist.append(trans)

    translist = set(translist)
    final_res= translist.union(sentences)    
    final_res.remove(msg)
    response = {
        'corrected': list(final_res),
    }
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8800)