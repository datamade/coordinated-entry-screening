from collections import namedtuple
import json

def prepare_data(cursor, query, percent_bool=True):
    colors = ['#0178BC', # blue
              '#FFD300', # yellow
              '#434348', # almost black
              '#4da0d0', # light blue
              '#FFE772', # light yellow
              '#68686C', # almost gray
              ]
    cursor.execute(query)
    data = cursor.fetchall()

    if percent_bool is True:
        total = sum(tup[1] for tup in data)
        data_for_chart = [
            {'name': tup[0], 
             'data': [ round((tup[1]/total) * 100, 2)], 
             'color': colors[idx % 6] 
            }
            for idx, tup in enumerate(data)
        ]
    else:
        data_for_chart = [
            {'name': tup[0], 
             'y': tup[1], 
             'color': colors[idx % 6] 
            } 
            for idx, tup in enumerate(data)
        ]

    mapping = {tup[0]: tup[2] for tup in data}

    return json.dumps(data_for_chart), json.dumps(mapping)
