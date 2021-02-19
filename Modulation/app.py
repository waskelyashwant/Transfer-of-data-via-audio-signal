from Encoding2 import *
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['data']
      input_string(result)
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)