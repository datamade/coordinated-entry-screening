from collections import namedtuple
import json

def prepare_data(cursor, query, percent_bool=True):
    cursor.execute(query)
    data = cursor.fetchall()

    if percent_bool is True:
        total = sum(tup[1] for tup in data)
        data_for_chart = [{'name': tup[0], 'data': [100*(tup[1]/total)]} for tup in data]
    else:
        data_for_chart = [{'name': tup[0], 'y': tup[1]} for tup in data]

    mapping = {tup[0]: tup[2] for tup in data}

    return json.dumps(data_for_chart), json.dumps(mapping)
