from requests.exceptions import HTTPError
import requests
import sqlite3
from pathlib import Path


COLUMNS = ['github_id', 'html_url', 'git_pull_url', 'git_push_url', 'commits_url', 'forks_url',
              'public', 'created_at', 'updated_at', 'comments', 'comments_url']
KEYS = ['id'] + COLUMNS[1:]

def import_gists_to_database(db, username, commit=True):
    """
    db : a database connection object
    username : a string corresponding to a valid github username
    """
    # load gists into list of dicts and catch a 404
    resp = requests.get('https://api.github.com/users/{}/gists'.format(username))
    if resp.status_code == 404:
        raise HTTPError
    gist_dicts = resp.json()

    # create table from schema.sql
    cursor = db.cursor()
    schema = Path('schema.sql')
    with open(schema) as fp:
        cursor.executescript(schema.read_text())
    
    # insert data into table
    query = """INSERT INTO gists (
    'github_id', 'html_url', 'git_pull_url', 'git_push_url', 'commits_url', 'forks_url',
    'public', 'created_at', 'updated_at', 'comments', 'comments_url'
     ) VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url, :forks_url,
              :public, :created_at, :updated_at, :comments, :comments_url);""" 
    for d in gist_dicts:
        values = [d[key] for key in KEYS]
        params = {column:value for column, value in zip(COLUMNS, values)}
        cursor.execute(query, params)

    return cursor

