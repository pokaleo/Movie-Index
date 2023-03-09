import json

def dataParse(data, method):
    '''
    parse the data
    Args: data: args from json, method, "GET" or "POST"

    Return : parsed_args = {'queryMsg':"",
                'by':"", # a str for search category, i.e. title, any, genres, keywords, proximity
                'need_check':False, # for debug only
                'color':"", # a str in ["all", "bw", "color"]
                'from':0, # int or None
                'to':9999, # int or None
                'additionQ':True, # a boolean value to check whether it is advanced search or not
                'moreQueries':[] # list of tuples (bool_type,by, query), i.e. ('and','title', "Vincent") bool_type in ['and','or','not']
        }

    '''
    print("Data",data)
    res = {
            'queryMsg':None, # a str or (w1, w2, d)
            'by':"", # a str for search category, i.e. title, genre, keywords, proximity, None
            'need_check':False, # for debug only
            'color':"", # a str in ["all", "bw", "color"]
            'from':0, # int or None
            'to':9999, # int or None
            'additionQ':True, # a boolean value to check whether it is advanced search or not
            'moreQueries':[] # list of tuples (bool_type,by, query), i.e. ('and','title', "Vincent") bool_type in ['and','or','not']
            }
    if data.get('pro') == 'true':
        res['by'] = 'proximity'
        msg = data.get('query')
        q = msg.split("+")
        word1 = q[0]
        word2 = q[1]
        d = q[2]
        res['queryMsg'] = d+' '+word1+' '+word2
    else:
        res['queryMsg'] = data.get('query')
        res['by']=data.get('by')
        if res['by'] == 'any':
            res['by'] = None

    if method == 'GET':
        res['need_check'] = data.get('need_check',type=bool)
        if data.get('pro') == 'true':
            res['need_check'] = False

        res['from'] = data.get('from',type=int)
        res['to'] = data.get('to',type=int)
        colorlist =  data.get('color')
        if colorlist == None or len(colorlist) == 0 or colorlist == '[]':
            res['color'] = 'all'
        else:
            colorlist = json.loads(colorlist)
            
            if isinstance(colorlist, str):
                colorlist = [colorlist]
            if len(colorlist) == 2:
                res['color'] = 'all'
            elif colorlist[0] == "Black/White":
                res['color'] = 'bw'
            else:
                res['color'] = 'color'

        print("colorlist", colorlist)

        otherQueries = data.get('additions')
        #print(otherQueries[0])
        if otherQueries == None or len(otherQueries) == 0 or otherQueries == '[]':
            res['additionQ'] = False
        else:
            res['additionQ'] = True
            otherQueries = json.loads(otherQueries)
            if isinstance(otherQueries,str):
                otherQueries = [otherQueries]
            print("other",otherQueries)
            for item in otherQueries:
                q = item.split(",")
                bool_type = q[0]
                category = q[1] # title, genres, proximity...
                bool_name =''
                if bool_type == '1':
                    bool_name = 'and'
                elif bool_type == '2':
                    bool_name='or'
                else:
                    bool_name='not'
                msg = ''
                if category == 'proximity':
                    word1 = q[2]
                    word2 = q[3]
                    d = q[4]
                    msg = '#'+d+' '+word1+' '+word2
                else:
                    if category == 'any':
                        category = None
                    msg = q[-1]
                res['moreQueries'].append((bool_name,category,msg))
    return res

def listParse(data, method):
    '''
    parse the data
    Args: data: args from json, 
          method, "GET" or "POST"
    Return : res, a list of str
    '''
    res = []
    if method == 'GET':
        res = data.get('ids')
        if res == None or res == 0 or res == '[]':
            print("Empty id list was posted by frontend!")
        else:
            res = json.loads(res)
            if isinstance(res, str):
                res = [res]
    #print(len(res))
    #print(res)
    return res