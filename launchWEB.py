from sys import argv
from flask import Flask, render_template, escape, Markup, request, redirect, url_for
app = Flask(__name__)

print "Carly says hi"

@app.route('/dbAdd/', methods=['POST', 'GET'])
def test():
    print "Adding db"
    if request.method == 'POST':
      bus = []
      empty = ""
      biggest = int(1)
      wNAME = request.form['wNAME']
      wDESC = request.form['wDESC']
      wIMAG = request.form['wIMAG']
      wTYPE = request.form['wTYPE']
      print wNAME
      if not all((wNAME, wDESC)):
          print "empty"
      else:
          book = open("static/db.txt", "r+")
          line = book.readline()
          while line:
              line = book.readline()
              bus = line.split('*')
              if not all((bus)):
                  print "empty"
              else:
                  ID = bus[0]
                  ID = int(ID)
                  if ID >= biggest:
                      biggest = int(ID) + 1

          biggest = str(biggest)
          newEntry = biggest + "*" + wNAME + "*" + wTYPE + "*" + wDESC + "*" + wIMAG + "\n"
          book.write(newEntry)
          book.close()
    action = ""
    methodType = "POST"
    return render_template('upLoad.html', action=action, methodType=methodType)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
