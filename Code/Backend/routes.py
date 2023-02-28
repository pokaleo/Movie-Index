from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import json
import RetrieveData
import DataPreprocessing
import Query
import Spellcheck
import JSONParser

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
    '''
    parse the data
    parsed_args = {'queryMsg':"",
            'by':"", # a str for search category, i.e. title, any, genres, keywords
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
    '''
    #query translate and spell check
    '''
    corrected = ''
    #print(type(queryMsg))
    print(parsed_args['need_check'])
    if parsed_args['need_check']:
        corrected=Spellcheck.spellcheck(parsed_args['queryMsg'])
        if corrected == parsed_args['queryMsg']:
            corrected = ""
        print(parsed_args['need_check'])
    queryMsg=Spellcheck.trans_api(parsed_args['queryMsg'])
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
    
    if parsed_args['by'] == 'title':
        res = query.by_title(queryMsg)
        print("By title",res)
    elif parsed_args['by'] == 'keywords':
        res = query.by_keywords(queryMsg)
        print("By keywords",res)
    else:
        res = query.by_title(queryMsg)
        print("By general",res)

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
    print()
    #return jsonify({})
    return jsonify(response)


app.run(debug=True,host='0.0.0.0',port=8800)