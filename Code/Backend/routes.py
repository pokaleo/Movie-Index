from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import time
import RetrieveData
import DataPreprocessing
import Query
import Spellcheck
import JSONParser
import Util

# ../TestDataset  ../Dataset/IMDB Movie Info ../Dataset/IMDB TestData

"""
Providing possibility of export and import for the processed data
3 different modes:
normal: for one time / live data processing
import: load the pickle file for previously processed data
export: pickling the processed data and export them as files
"""
mode = "normal"
dataset_path = "../Dataset/IMDB Movie Info"

if mode == "normal":
    movies = RetrieveData.MovieInfo(dataset_path)
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
    print("Successfully processed the dataset")
elif mode == "import":
    import pickle

    movie_dict_file = open('../Dataset/movie_dict.pickle', 'rb')
    moviedict = pickle.load(movie_dict_file)
    movie_dict_file.close()
    processed_query_data_file = open('../Dataset/processed_query_data.pickle', 'rb')
    query = pickle.load(processed_query_data_file)
    processed_query_data_file.close()
    print("Successfully load the pre-saved data")
elif mode == "export":
    import pickle

    movies = RetrieveData.MovieInfo(dataset_path)
    movies.read_files()
    moviedict = movies.get_movie_info()
    movie_dict_file = open('../Dataset/movie_dict.pickle', 'wb')
    pickle.dump(moviedict, movie_dict_file)
    movie_dict_file.close()
    processed_data = DataPreprocessing.PreProcessing(movies.get_movie_info())
    processed_data.tokenise()
    processed_data.to_lowercase()
    processed_data.remove_punctuation()
    processed_data.stem_data()
    processed_data.remove_stopwords()
    processed_data.create_index()
    query = Query.Query(processed_data)
    processed_query_data_file = open('../Dataset/processed_query_data.pickle', 'wb')
    pickle.dump(query, processed_query_data_file)
    processed_query_data_file.close()
    print("Successfully exported the processed data")


def formatRes(id):
    """
    params: id: str movie id
    return: doc, a dict contain movie description
    """
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


app = Flask(__name__)
CORS(app, supports_credentials=True)


# cors = CORS(app, resources={r"/test": {"origins": "*"}})

@app.route('/')
def foo():
    return 'test!'


@app.route('/test', methods=['GET', 'POST'])
def testQuery():
    data = request.get_json()
    queryMsg = data.get('query')
    response = {
        'results': 'This is a test result! \n Your input is' + queryMsg,
        'title': [],
    }
    print('data (json): ', data)
    print('query: ', data.get('query'))
    return jsonify(response)


@app.route('/movie/<id>', methods=['GET', 'POST'])
def getMovie(id):
    print(id)
    response = moviedict[id]
    print(response)
    return jsonify(response)


@app.route('/img/<id>', methods=["GET"])
def getImg(id):
    title = moviedict[id]['title']
    print(title)
    try:
        url = Util.return_image(title)
    except Exception as e:
        url = ""
        print(e)
    print(url)
    response = {'img': url}
    return jsonify(response)


@app.route('/search', methods=['GET', 'POST'])
def searchQuery():
    # start timer
    st = time.time()
    st_cpu = time.process_time()

    # get request
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args

    parsed_args = JSONParser.dataParse(data, request.method)
    print(parsed_args)

    # Add function for extract results
    queryMsg = parsed_args['queryMsg']
    if parsed_args['by'] == 'proximity':
        dist, w1, w2 = queryMsg.split()
        try:
            res = query.proximity_search(w1, w2, int(dist), direct_call=True,
                                         year1=parsed_args['from'], year2=parsed_args['to'],
                                         not_ranking=parsed_args['additionQ'])
        except Exception as e:
            res = []
            print(e)
        queryMsg = w1 + " " + w2  # to handle keywords in additions
        print("By proximity", res)
    else:
        try:
            print("phrase handle", queryMsg)
            res = query.phrase_search_handler(queryMsg, year1=parsed_args['from'], year2=parsed_args['to'],
                                              not_ranking=parsed_args['additionQ'], attribute=parsed_args['by'])
        except Exception as e:
            res = []
            print("phrase handle except", queryMsg)
            print(e)

    if parsed_args['additionQ']:
        total_res = []
        total_keywords = []
        current_res = res.copy()
        count = 1
        keywords = list(queryMsg.lower().split())
        for a_query in parsed_args['moreQueries']:
            bool_type = a_query[0]
            search_in = a_query[1]
            queryMsg = a_query[2]
            if bool_type == 'and':
                print("AND query", search_in, queryMsg)
                if search_in != 'proximity':
                    new_keywords = list(queryMsg.lower().split())
                    try:
                        new_res = query.phrase_search_handler(queryMsg, year1=parsed_args['from'],
                                                              year2=parsed_args['to'],
                                                              not_ranking=parsed_args['additionQ'], attribute=search_in)
                    except Exception as e:
                        new_res = []
                        print(e)
                else:  # proximity query
                    dist, w1, w2 = queryMsg.split()
                    new_keywords = [w1.lower(), w2.lower()]
                    try:
                        new_res = query.proximity_search(w1, w2, int(dist), direct_call=True,
                                                         year1=parsed_args['from'], year2=parsed_args['to'],
                                                         not_ranking=parsed_args['additionQ'])
                    except Exception as e:
                        new_res = []
                        print(e)
                keywords.extend(new_keywords)
                current_res = [mid for mid in current_res if mid in set(new_res)]
            elif bool_type == 'not':
                print("NOT query", search_in, queryMsg)
                if search_in != 'proximity':
                    try:
                        new_res = query.phrase_search_handler(queryMsg, year1=parsed_args['from'],
                                                              year2=parsed_args['to'],
                                                              not_ranking=parsed_args['additionQ'], attribute=search_in)
                    except Exception as e:
                        new_res = []
                        print(e)
                else:  # proximity query
                    dist, w1, w2 = queryMsg.split()
                    try:
                        new_res = query.proximity_search(w1, w2, int(dist), direct_call=True,
                                                         year1=parsed_args['from'], year2=parsed_args['to'],
                                                         not_ranking=parsed_args['additionQ'])
                    except Exception as e:
                        new_res = []
                        print(e)
                current_res = [mid for mid in current_res if mid not in new_res]
            elif bool_type == 'or':
                count += 1
                # store the previous result and keywords
                total_keywords.append(keywords)
                total_res.append(current_res)

                print("prev keywords", total_keywords)

                print("OR query", search_in, queryMsg)
                if search_in != 'proximity':
                    new_keywords = list(queryMsg.lower().split())
                    try:
                        new_res = query.phrase_search_handler(queryMsg, year1=parsed_args['from'],
                                                              year2=parsed_args['to'],
                                                              not_ranking=parsed_args['additionQ'], attribute=search_in)
                    except Exception as e:
                        new_res = []
                        print(e)
                else:  # proximity query
                    dist, w1, w2 = queryMsg.split()
                    new_keywords = [w1.lower(), w2.lower()]
                    try:
                        new_res = query.proximity_search(w1, w2, int(dist), direct_call=True,
                                                         year1=parsed_args['from'], year2=parsed_args['to'],
                                                         not_ranking=parsed_args['additionQ'])
                    except Exception as e:
                        new_res = []
                        print(e)
                # print(new_res)
                keywords = new_keywords.copy()
                current_res = new_res.copy()
        # after for loop, append the last query result
        total_keywords.append(keywords)
        total_res.append(current_res)

        print(total_keywords)
        print(total_res)

        docid_list = []
        bm25score_list = []
        for i in range(count):
            docid_temp, score_temp = query.bm25_ranking(total_keywords[i], total_res[i], returnScore=True)
            docid_list.extend(docid_temp)
            bm25score_list.extend(score_temp)
        res = [x for _, x in sorted(zip(bm25score_list, docid_list), reverse=True)]
        res = list(dict.fromkeys(res))

    res = list(res)
    print(res)
    reslist = []
    id_res = []
    # final_ses = []
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
        'results': reslist[:200],
        'ids': id_res,
        'wallT': round((ed - st) * 1000, 6),
        'cpuT': round((ed_cpu - st_cpu) * 1000, 6),
        'total': len(reslist)
    }
    return jsonify(response)


@app.route('/fetchmore', methods=['GET', 'POST'])
def fetchmore():
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args
    id_list = JSONParser.listParse(data, request.method)
    reslist = []
    for mid in id_list:
        reslist.append(formatRes(mid))
    response = {
        'results': reslist
    }
    return jsonify(response)


@app.route('/spellcheck', methods=['GET', 'POST'])
def spell():
    """
    #query translate and spell check
    """
    data = request.args
    msg = data.get('input')
    corrected = []
    try:
        correct = Spellcheck.spellcheck(msg)
        if isinstance(correct, str):
            corrected.append(correct)
        print("try", corrected)
    except Exception as e:
        corrected = Spellcheck.local_spellcheck(msg)
        print("except", corrected)
        print(e)
    print(corrected)
    sentences = corrected
    sentences.append(msg)
    print("test1", sentences)
    sentences = set(sentences)
    print("test2", sentences)
    translist = []

    try:
        translist = Spellcheck.deepl_trans(list(sentences))
    except Exception as e:
        for sen in sentences:
            trans = Spellcheck.trans_api(sen)
            if isinstance(trans, str):
                translist.append(trans)
        print(e)

    translist = set(translist)
    final_res = translist.union(sentences)
    final_res.remove(msg)
    response = {
        'corrected': list(final_res),
    }
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8800)
