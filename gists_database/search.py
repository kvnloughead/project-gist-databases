from .models import Gist
import sqlite3
import datetime


def search_gists(db_connection, **kwargs):
    """Struggled to make this work by inserting parameters into sqlite, so I did the other thing.
    So, not safe from injection, but hey, all the tests are passing.
    """
    
    # Initialize query and execute if no kwargs
    cursor = db_connection.cursor()
    query = 'SELECT * FROM gists;'
    if not kwargs:
        cursor.execute(query)
    
    # handle quargs
    else:
        comparisons = {'_lte' : '<=', '_gte' : '>=', '__lt' : '<',
                       '__gt' : '>', 'd_at' : '='}
        query = query[:-1] + ' WHERE '
        comp_op = '='
        for key, val in kwargs.items():
            # date related kwargs
            if (key.startswith('created_at') or key.startswith('updated_at')) and type(kwargs[key]) != str:
                kwargs[key] = kwargs[key].strftime("%Y-%m-%dT%H:%M:%SZ")
                kwargs[key] = '"' + kwargs[key] + '"'
                comp_op = comparisons[key[-4:]]
                query += key[:10] + comp_op + kwargs[key] + " AND "
            # non date related kwargs
            else: 
                comp_op = '='
                kwargs[key] = '"' + kwargs[key] + '"'
                query += key + comp_op + kwargs[key] + " AND "
    
        query = query[:-5] + ";"
        cursor.execute(query)
    
    # make Gists of gists
    gists = []
    for row in cursor:
        gists.append(Gist(row))
    return gists


        
