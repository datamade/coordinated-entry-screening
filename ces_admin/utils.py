from collections import namedtuple

def prepare_data(cursor, query):
    cursor.execute(query)
    data = cursor.fetchall()
    data_for_chart = [{'name': tup[0], 'y': tup[1]} for tup in data]
    mapping = {tup[0]: tup[2] for tup in data}

    return data_for_chart, mapping