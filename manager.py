from sys import argv
from flask import Flask, g, render_template, escape, Markup, request, redirect, url_for
import sqlite3

app = Flask(__name__)
data_path = 'DataBase/data.db'

def fetch_db():
    dB = getattr(g, 'dB', None)
    if dB is None:
        dB = sqlite3.connect(data_path)
        g.dB = dB
    return dB

def init_db():
    print "initDB"
    with app.app_context():
        dB = fetch_db()
        with app.open_resource('schema.sql', mode='r') as f:
            dB.cursor().executescript(f.read())
        dB.commit()

def mass_ID():
    dB = fetch_db()
    sql = "SELECT id FROM user ORDER BY id ASC"
    print "lol"
    for row in dB.cursor().execute(sql):
        print str(row)
    if str(row) is None:
        return 0
    else:
        return str(row)

@app.route('/dbAdd/', methods=['POST', 'GET'])
def test():
    print "Adding db"
    gain = mass_ID()
    if request.method == 'POST':
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      print gain
      gain += 1
      print gain
      dB = fetch_db()
      print "1"
      #sql = "INSERT INTO user (username,password) VALUES ('" + wNAME +"', '" + wPass + "')"
      sql = "INSERT INTO user VALUES ('" + gain + "', '" + wNAME + "', '" + wPASS + "')"
      print "2"
      print sql
      dB.cursor().execute(sql)
      dB.commit()
    return render_template('upLoad.html')

@app.route('/')
def Home():
    dB = fetch_db()
    sql = "SELECT * FROM user"
    for row in dB.cursor().execute(sql):
        print str(row)
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
