from flask import *
from flask_sqlalchemy import SQLAlchemy
import json
from ast import literal_eval as ast
app = Flask(__name__)

ch = ast(open("savedchat.dat", 'r', encoding='utf-8').read())
co = ast(open("savedcourse.dat", 'r', encoding='utf-8').read())


main = '''

<h1>Тут будет сайт, честно</h1>

'''


def savedata():
    open('savedchat.dat', 'w', encoding='utf-8').write(str(ch))
    open('savedcourse.dat', 'w', encoding='utf-8').write(str(co))


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return str(co)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return str(ch)


@app.route('/', methods=['GET', 'POST'])
def cha():
    j = request.json
    if j['func'] == 'got100':
        co[j['course']][j['module']][j['task']]['value'] = 100
    if j['func'] == 'message':
        ch.append(f'{j["name"]} {j["surname"]}({j["who"]}): {j["text"]}')
    savedata()
    return main

 
if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')        
