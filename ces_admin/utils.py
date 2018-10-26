from collections import namedtuple

def make_namedtuple(cursor, query):
    cursor.execute(query)
    fields = cursor.description
    nt_result = namedtuple('Session', [col[0] for col in fields])
    return [nt_result(*row) for row in cursor.fetchall()]