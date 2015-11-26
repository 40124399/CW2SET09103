from sys import argv
from flask import Flask, g, render_template, escape, Markup, request, redirect, url_for, flash
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
    #sql = "SELECT id FROM user ORDER BY id ASC"
    sql = "SELECT MAX(id) FROM user"
    holder = None
    #for row in dB.cursor().execute(sql):
    #    holder = str(row).replace('(', '').replace(',)', '')
    hold = str(dB.cursor().execute(sql).fetchone())
    holder = hold.replace('(', '').replace(',)', '')
    if holder is None:
        return "0"
    else:
        return holder

@app.route('/dbAdd/', methods=['POST', 'GET'])
def test():
    print "Adding db"
    if request.method == 'POST':
      gain = mass_ID()
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      temp = gain
      tempO = int(temp) + 1
      dB = fetch_db()
      print "inserting"
      sql = "INSERT INTO user VALUES ('" + str(tempO) + "', '" + wNAME + "', '" + wPASS + "')"
      print "String appended:"
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
