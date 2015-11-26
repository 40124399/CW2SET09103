import sqlite3
from bottle import route, run

@route('/')
def hello():
    print "hey"
    return "<h1>HEY THIS WORKS</h1>"

run(host='0.0.0.0', port=5000)
