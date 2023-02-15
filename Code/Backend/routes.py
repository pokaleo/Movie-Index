from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import json
import RetrieveData
import DataPreprocessing

movies = RetrieveData.MovieInfo("../TestDataset")
movies.read_files()
moviedict = movies.get_movie_info()

app = Flask(__name__)
CORS(app, supports_credentials=True)
#cors = CORS(app, resources={r"/test": {"origins": "*"}})

@app.route('/')
def foo():
    return 'test!'

@app.route('/test', methods=['GET','POST'])
def testQuery():
    data = request.get_json()
    query= data.get('query')
    response = {
        'results': 'This is a test result! \n Your input is' + query,
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



app.run(host='0.0.0.0',port=8800)