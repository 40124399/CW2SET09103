from sys import argv
from werkzeug import secure_filename
from flask import Flask, g, render_template, escape, Markup, request, redirect, \
     url_for, flash, make_response, session
import sqlite3, os, Cookie

app = Flask(__name__)
data_path = 'DataBase/data.db'
ALLOWED_EXTENSIONS = set(['mp3','jpg'])
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/'

def fetch_db():
    dB = getattr(g, 'dB', None)
    if dB is None:
        dB = sqlite3.connect(data_path)
        g.dB = dB
    return dB
######################################################################################################################################
def makeme(userID):
    dB = fetch_db()
    print "see my posts"
    userID = str(userID)
    sql = "INSERT INTO user" + userID + "list VALUES('" + userID + "')"
    print sql
    dB.cursor().execute(sql)
    dB.commit()
    return "done"



def gen_TABLE(userID):
  with app.app_context():
    dB = fetch_db()
    with app.open_resource('friends.sql', mode="r") as f:
      print "Creating friends table."
      var = f.read()
      var = str(var)
      var = var.replace("*:;", userID)
      dB.cursor().executescript(var)
    dB.commit()

def gen_COM_TABLE(postID):
  with app.app_context():
    dB = fetch_db()
    with app.open_resource('comments.sql', mode='r') as f:
      print "Creating comments table."
      var = f.read()
      var = str(var)
      var = var.replace("*:;", postID)
      dB.cursor().executescript(var)
    dB.commit()

def init_db():
    print "initDB"
    with app.app_context():
        dB = fetch_db()
        with app.open_resource('schema.sql', mode='r') as f:
            dB.cursor().executescript(f.read())
        dB.commit()

def mass_ID(table):
    dB = fetch_db()
    sql = "SELECT MAX(id) FROM " + table
    hold = str(dB.cursor().execute(sql).fetchone())
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

def checkSesh():
  if 'username' in session:
    return session
    print "active session"
  else:
    return None

def checkString(fileName):
  print "this far"
  acceptedTypes = "mp3,wav,ogg" #list of supported types from w3school
  fileName.split('.')
  if fileName[1] in acceptedTypes:
    return "ok"
  else:
    return "no"

def upLoadFile(file, wTITL):
  fileName = file.filename
  print "checking"
  if file and allowed_file(file.filename):
    fileName = secure_filename(file.filename)
    print "yay"
    ext = fileName.rsplit('.', 1)[1]
    filename = wTITL + "." + ext
    if ext == "jpg":
      filename = "pics/" + wTITL + "." + ext
    else:
      filename = "songs/" + wTITL + "." + ext
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Successfully uploaded.**" + os.path.join(app.config['UPLOAD_FOLDER'], filename)
  else:
    return "Error.**"

def checkEmpty(val):
  if val is None:
    return "empty"
  elif val == "":
    return "empty"
  elif val == None:
    return "empty"
  else:
    return "used"

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def posty(title, post):
  print "reacheed"
  title = title
  post = post
  wTITL = str(title).replace("'", "''")
  wCONT = str(post).replace("'", "''")
  seshID = str(session['id'])
  calcID = str(mass_ID("posts") + 1)
  sql = "INSERT INTO posts VALUES ('" + calcID + "', '" + seshID + "', '" + wTITL + "', '" + wCONT + "')"
  dB = fetch_db()
  dB.cursor().execute(sql)
  dB.commit()
  postID = str(calcID)
  gen_COM_TABLE(postID)
  return "done"
###################################### DONT TOUCH #####################################

#KICK FROM SESSION
@app.route('/whipeSeSH/')
def whipeSession():
  session.pop('username', None)
  session.pop('id', None)
  print "lol"
  return redirect(url_for('logUSER'))

#ADD A FRIEND PAGE
@app.route('/addFriend/', methods=['POST', 'GET'])
def addFriend():
  if checkSesh() is None:
    return redirect(url_for('logUSER'))
  else:
    if request.method == 'POST':
      print "post"
      wID = request.form['wID']
      dB = fetch_db()
      sql = "INSERT INTO user" + session['id'] + "list VALUES('" + wID + "')"
      print sql
      dB.cursor().execute(sql)
      dB.commit()
      return redirect(url_for('addFriend'))
    else:
      return render_template('addFriend.html')

#BROWSE PAGE
#LOADS INFORMATION FROM FRIENDED PEOPLE AND YOURSELF
#IMP 1/ ONLY LOADS YOUR INFO
@app.route('/browse/')
def browse():
  if checkSesh() is None:
    return redirect(url_for('logUSER'))
  else:
    print session['id']
    myInfo = ""#<div id='myMusic'>"
    extInfo = ""#<div id='extMusic'>"

    dB = fetch_db()
    sql = "SELECT title, userID, id FROM songs"
    for row in dB.cursor().execute(sql):
      varR = str(row[1])
      varS = str(session['id'])
      varN = str(row[0]).replace("(u'", "").replace("',)", "")
      sql2 = "SELECT id FROM user" + varR + "list WHERE id LIKE '" + varS + "'"
      print sql2
      if varR == varS:
        print str(row[0])
        myInfo = myInfo + '''<p><a class="songs" onclick="tester(this)">''' + varN + '''</a><p>'''
      else:
        buddy = str(dB.cursor().execute(sql2).fetchone())
        buddy = buddy.replace("(", "").replace(",)", "")
        if buddy == varS:
          sql3 = "SELECT username FROM user WHERE id LIKE '" + varR + "'"
          uName = str(dB.cursor().execute(sql3).fetchone()).replace("(u'", "").replace("',)", "")
          extInfo = extInfo + '''<p>''' + uName + '''<a class="songs" onclick="tester(this)">''' + varN + '''</a><p>'''
    #myInfo = myInfo + "</div>"
    #extInfo = extInfo + "</div>"
    myInfo = Markup(myInfo)
    extInfo = Markup(extInfo)
    return render_template('browse.html', myInfo=myInfo, extInfo=extInfo)

#UPLOAD FILES HERE <<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/upLoad/', methods=['POST', 'GET'])
def upload():
  if checkSesh() is None:
    return redirect(url_for('logUSER'))
  else:
    info = session['id']
    if request.method == 'POST':
      file = request.files['file']
      wTITL = request.form['wTITL']
      wARTS = request.form['wARTS']
      wALBM = request.form['wALBM']
      wGENR = request.form['wGENR']
      sqlCheck = "SELECT title FROM songs WHERE title LIKE '" + wTITL + "'"
      print sqlCheck
      check = ""
      dB = fetch_db()
      check = dB.cursor().execute(sqlCheck).fetchone()
      check = str(check).replace("(u'", "").replace("',)", "")
      wTITL = str(wTITL)
      print check
      print wTITL
      if check != wTITL:
        info = upLoadFile(file, wTITL)
        table = "songs"
        gain = mass_ID(table)
        PATH = info.rsplit("**", 1)[1]
        sql = "INSERT INTO songs VALUES ('" + str(gain + 1) + "', '" + session['id'] + "', '" + PATH + "', '" + wTITL + "', '" + wARTS + "', '" + wALBM + "', '" + wGENR + "')"
        dB.cursor().execute(sql)
        dB.commit()
        info = info.split("**", 1)[0]
        title = str(session['username']) + " just uploaded a track."
        post = "Check it out in your browse section. It's called: " + wTITL + ". ARTIST: " + wARTS + ", ALBUM: " + wALBM + ", GENR: " + wGENR + "."
        print "worked"
        print title
        print post
        nada = posty(title, post)
      else:
        info = "Name already in use. Please choose a different one."
    else:
      info = "Please upload your file."
    return render_template('upLoad.html', info = info)

#TESTER
@app.route('/dbAdd/', methods=['POST', 'GET'])
def test():
    print "testing"
    return render_template('tester.html')

#createFriend entry
@app.route('/budMe/')
def crFr():
  if checkSesh() is None:
    return redirect(url_for('logUSER'))
  else:
    print "post"
    wID = request.args['id']
    dB = fetch_db()
    sql = "INSERT INTO user" + session['id'] + "list VALUES('" + wID + "')"
    print sql
    dB.cursor().execute(sql)
    dB.commit()
    return redirect(url_for('Home'))


#LOG IN
#ALSO STARTS SESSION
@app.route('/logIn/', methods=['POST', 'GET'])
def logUSER():
    print "Logging in."
    if request.method == 'POST':
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      dB = fetch_db()
      sql = "SELECT password FROM user WHERE username LIKE '" + wNAME + "'"
      sql2 = "SELECT id FROM user WHERE username LIKE '" + wNAME + "'"
      hold = str(dB.cursor().execute(sql).fetchone())
      uID = str(dB.cursor().execute(sql2).fetchone())
      Uid = uID.replace("(", "").replace(",)", "")
      hold = hold.replace("(u'", "").replace("',)", "")
      if hold == wPASS:
        info = "logged in"
        session['username'] = wNAME
        session['id'] = Uid
        return redirect(url_for('Home'))
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
      table = "user"
      gain = mass_ID(table)
      print "hmm"
      wNAME = request.form['wNAME']
      wPASS = request.form['wPASS']
      wMAIL = request.form['wMAIL']
      print "new bug"
      file = request.files['file']
      print "or"
      dB = fetch_db()
      userID = str(gain + 1)
      sqlVer = "SELECT username FROM user WHERE username LIKE '" + wNAME + "'"
      sql = "INSERT INTO user VALUES ('" + userID + "', '" + wMAIL + "', '" + wNAME + "', '" + wPASS + "')"
      print sql
      dNAME = str(dB.cursor().execute(sqlVer).fetchone())
      if wNAME in dNAME:
        info = "Username already in use please select a different one."
        return render_template("newAccount.html", info=info)
      else:
        path = "static/pics/" + wNAME + ".png"
        state = upLoadFile(file, wNAME)
        print state
        dB.cursor().execute(sql)
        dB.commit()
        gen_TABLE(userID)
        print sql
        session.pop('username', None)
        session.pop('id', None)
        session['username'] = wNAME
        session['id'] = userID
        done = makeme(userID)
        return redirect(url_for('Home'))
    else:
      info = "Welcome to our website. Please create an account."
      return render_template('newAccount.html', info=info)


@app.route('/posting/', methods=['POST', 'GET'])
def posting():
  print "posting"
  wCOMM = request.form['wCOMM'].replace("'", "''")
  postID = str(request.args.get('postID', ''))
  table = "com" + postID + "list"
  print postID
  print table
  sql = "INSERT INTO com" + postID + "list VALUES ('" + \
        str(mass_ID(table) + 1) + "', '" + wCOMM + \
        "', '" + str(session['id']) + "')"
  print sql
  dB = fetch_db()
  dB.cursor().execute(sql)
  dB.commit()
  print "friended"
  return redirect(url_for('Home'))



#SEARCH
@app.route('/search/', methods=['POST', 'GET'])
def Search():
  print "search"
  if checkSesh() is None:
      return redirect(url_for('logUSER'))
  else:
    try:
      pos = request.args['pos']
    except:
      pos = "0"
      print "error"
    key = request.args['key']
    print key
    sql = "SELECT id, username FROM user WHERE username LIKE '%" + key + "%' ORDER BY username ASC LIMIT " + pos + ",5"
    print sql
    dB = fetch_db()
    html = ""
    for row in dB.cursor().execute(sql):
      print "this far"
      var1 = str(row[0])
      var2 = str(row[1])
      html = html + '''<p><a href="http://localhost:5000/budMe?id=''' + var1 + '''">''' + var2 + '''</a></p>'''
    previous = str(int(pos) - 1)
    print previous
    next = str(int(pos) + 1)
    buttons = '''<a href="http://localhost:5000/search/?key=''' + key + '''&pos=''' + previous + '''>previous</a><a href="http://localhost:5000/search/?key=''' + key + '''&pos=''' + next + '''>previous</a>'''
    info = buttons + html + buttons
    info = Markup(info)
    return render_template('search.html', info=info)


#HOME
@app.route('/', methods=['POST', 'GET'])
def Home():
    print "home"
    if checkSesh() is None:
      return redirect(url_for('logUSER'))
    else:
      if request.method == 'POST':
        print "almost"
        bool = "false"
        try:
          comment = request.form['COMMENT']
          if comment == "Submit":
            bool = "true"
        except:
          print "error"
        if bool == "true":
          print "submitted"
          wCOMM = request.form['wCOMM']

        else:
          print "posted"
          wTITL = request.form['wTITL']
          wCONT = request.form['wCONT']
          seshID = str(session['id'])
          calcID = str(mass_ID("posts") + 1)
          sql = "INSERT INTO posts VALUES ('" + calcID + "', '" + seshID + "', '" + wTITL + "', '" + wCONT + "')"
          dB = fetch_db()
          dB.cursor().execute(sql)
          dB.commit()
          postID = str(calcID)
          gen_COM_TABLE(postID)
        return redirect(url_for('Home'))
      else:
        info = ""
        print "Going Home."
        dB = fetch_db()
        sql = "SELECT * FROM user"
        for row in dB.cursor().execute(sql):
            print str(row)
        try:
          page = request.args['start']
        except:
          page = "0"
          print "error"
        position = str(int(page) * 5)
        sql2 = "SELECT title, content, userID, id FROM posts ORDER BY id DESC LIMIT " + position + ",5"
        for row in dB.cursor().execute(sql2):
          var1 = str(row[0])
          var2 = str(row[1])
          var3 = str(row[2])
          var4 = str(session['id'])
          var5 = str(row[3])
          sql3 = "SELECT id FROM user" + var3 + "list WHERE id LIKE '" + var4 + "'"
          sqlUS = "SELECT username FROM user WHERE id LIKE '" + var3 + "'"
          buddy = str(dB.cursor().execute(sql3).fetchone()).replace("(", "").replace(",)", "")
          if buddy == var4:
            sqlUname = str(dB.cursor().execute(sqlUS).fetchone()).replace("(u'", "").replace("',)", "")
            print sqlUname
            img = '''<img src="static/pics/''' + sqlUname + '''.jpg">'''
            temp = '''<div class="Posts"><div class="postTITLE">''' + img + '''<h1>''' + sqlUname + ''': ''' + \
            var1 + '''</h1></div><div class="postBODY"><textarea type="text" readonly>''' + \
            var2 + '''</textarea></div><div class="postWRITE"><form method="POST" \
            action="posting/?postID=''' + var5 + '''"> \
            <input id="wriP" type="text" \
            name="wCOMM" placeholder="Reply. . ." required><input id="subP" type="submit" \
            name="COMMENT"></form></div><button id="toggle" \
            onclick="tester(''' + var5 + ''')">Toggle comments</button><div class="postCOMM">'''
            sql4 = "SELECT coment, userID FROM com" + var5 + "list"
            for row in dB.cursor().execute(sql4):
              var6 = str(row[0])
              var7 = str(row[1])
              sql5 = "SELECT username FROM user WHERE id LIKE '" + var7 + "'"
              for row in dB.cursor().execute(sql5):
                var8 = str(row[0])
                img = '''<img src="static/pics/''' + var8 + '''.jpg">'''
                print img
                temp = temp + '''<div class="sCom''' + var5 + '''">''' + img + '''<h3>''' + var8 + ''':</h3> \
                <textarea type="text" readonly>''' + var6 + '''</textarea></div>'''
            temp = temp + '''</div></div>'''
            info = info + temp
          else:
            print "not for user"
        previous = str(int(page) - 1)
        next = str(int(page) + 1)
        buttonsTop = '''<a id="topPrev" href="http://localhost:5000/?start=''' + previous + '''">Previous page</a><a id="topNext" href="http://localhost:5000/?start=''' + next + '''">Next page</a>'''
        buttonsBottom = '''<a id="botPrev" href="http://localhost:5000/?start=''' + previous + '''">Previous page</a><a id="botNext" href="http://localhost:5000/?start=''' + next + '''">Next page</a>'''
        info = buttonsTop + info + buttonsBottom
        info = Markup(info)
        return render_template('home.html', info=info)

@app.errorhandler(413)
def fileToLarge(error):
  return redirect(url_for('Home'))

#end stuff
app.secret_key = 'Afgiiuf&e48d JMF8Fzql!ihf,/z7894j'
if __name__ == "__main__":
    app.run(host='0.0.0.0')
