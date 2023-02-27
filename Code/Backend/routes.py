from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import json
import RetrieveData
import DataPreprocessing
import Query
import Spellcheck

movies = RetrieveData.MovieInfo("../TestDataset")
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
    queryMsg= data.get('query')
    search_type = data.get('type')
    need_check = bool(data.get('need_check'))
    before= data.get('before')
    if before != "" and before != None:
       before = int(before)
    else:
       before = None
    after= data.get('after')
    if after != "" and after != None:
       after = int(after)
    else:
       after = None
    color=data.get('color')
    not_query = data.get('not_include')
    print(not_query)
    '''
    query translate and spell check
    '''
    corrected = ''
    #print(type(queryMsg))
    print(need_check)
    if need_check:
        corrected=Spellcheck.spellcheck(queryMsg)
        if corrected == queryMsg:
            corrected = ""
        print(need_check)
    queryMsg=Spellcheck.trans_api(queryMsg)
    '''
    function to wrap up
    '''
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
    '''
    Add function for extract results
    '''
    if search_type == 'title':
        res = query.by_title(queryMsg)
        print("By title",res)
    elif search_type == 'keywords':
        res = query.by_keywords(queryMsg)
    else:
        res = query.by_general(queryMsg)

    #print(res)
    reslist = []
    for id in res:
        reslist.append(formatRes(id))

    response = {
        'results': reslist,
        'ids': res,
        'corrected': corrected
    }
    #print('data: ', data)
    print(reslist)
    return jsonify(response)

app.run(debug=True,host='0.0.0.0',port=8800)