from sys import argv
from flask import Flask, g, render_template, escape, Markup, request, redirect, \
     url_for, flash, make_response, session
import sqlite3, os, Cookie

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
    #holder = None
    #for row in dB.cursor().execute(sql):
    #    holder = str(row).replace('(', '').replace(',)', '')
    hold = str(dB.cursor().execute(sql).fetchone())
    print hold
    print "holder"
    holder = hold.replace('(', '').replace(',)', '')
    print "working"
    if holder is None:
        print "empty 1"
        return 0
    elif "None" in holder:
        print "empty 2"
        return 0
    else:
        print holder
        return int(holder)

def checkSession():
    if 'loggedIn' in session:
      return 'logged in as ' + session['username']
    else:
      return 'please log in'
#Don't touch above+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#TESTER
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
    info = "nothing"
    return render_template('home.html')

#LOG IN
@app.route('/logIn/', methods=['POST', 'GET'])
def logUSER():
    print "Logging in."
    if request.method == 'POST':
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      dB = fetch_db()
      sql = "SELECT password FROM user WHERE username LIKE '" + wNAME + "'"
      print sql
      hold = str(dB.cursor().execute(sql).fetchone())
      hold = hold.replace("(u'", "").replace("',)", "")
      print hold
      if hold == wPASS:
        info = "logged in"
      else:
        info = "wrong password"
    else:
      info = "Please log in."
    return render_template('logIn.html', info=info)

#SIGN UP
@app.route('/newUSR/', methods=['POST', 'GET'])
def newUSER():
    print "Creating user"
    if request.method == 'POST':
      gain = mass_ID()
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      wMAIL = request.form['wMAIL']
      dB = fetch_db()
      sql = "INSERT INTO user VALUES ('" + str(gain + 1) + "', '" + wMAIL + "', '" + wNAME + "', '" + wPASS + "')"
      print sql
      dB.cursor().execute(sql)
      dB.commit()

    return render_template('newAccount.html')

#HOME
@app.route('/')
def Home():
    print "Going Home."
    dB = fetch_db()
    sql = "SELECT * FROM user"
    for row in dB.cursor().execute(sql):
        print str(row)
    return render_template('home.html')

#end stuff
app.secret_key = 'Afgiiuf&e48d JMF8Fzql!ihf,/z7894j'
if __name__ == "__main__":
    app.run(host='0.0.0.0')
