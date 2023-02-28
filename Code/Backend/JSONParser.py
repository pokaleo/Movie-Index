import json

def dataParse(data, method):
    print("Data",data)
    res = {'queryMsg':"",
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
    res['queryMsg'] = data.get('query')
    res['by']=data.get('by')
    if method == 'GET':
        res['need_check'] = data.get('need_check',type=bool)
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
                q = item.split(",",2)
                if q[0] == '1':
                    res['andQueries'].append((q[1],q[2]))
                elif q[0] == '2':
                    res['orQueries'].append((q[1],q[2]))
                else:
                    #print(q)
                    res['notQueries'].append((q[1],q[2]))
    return res