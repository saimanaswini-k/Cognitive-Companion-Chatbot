from flask import Flask, url_for, redirect, render_template, request
import sys
from train import chat
import datetime

app=Flask(__name__)

def chat_module(query):
    orig_stdout = sys.stdout
    sys.stdout = open('response.txt','w')

    print(chat.respond(query))

    sys.stdout.close()
    sys.stdout=orig_stdout

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin2.html')

@app.route("/submitquery", methods=["POST","GET"])
def submitquery():
    if request.method=='POST':
        query = request.form['query']
        chat_module(query)
        with open('response.txt', 'r') as f:
            res = f.read()
        # res=res.replace('\n','<br>')
        res=res.split('\n')
        res=[x.strip() for x in res if x.strip()]
        #current time
        now=datetime.datetime.now()
        now=now.strftime('%H:%M')
    return render_template("admin2.html", answer=res, query=query, time=now)

if __name__=='__main__':
    app.run(debug=True)