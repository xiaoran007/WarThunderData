from flask import Flask, render_template
from App import aviation, railway
from gevent import pywsgi
import time

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/indev/')
def indev():
    return render_template('indev.html')


@app.route('/rocket/')
def rocket():
    TimeStr = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    content = aviation.Rocket().GetInfoNew()
    DataList = content.splitlines(keepends=False)
    return render_template('rocket2.html', Time=TimeStr, DataList=DataList)


@app.route('/search/')
def search():
    return render_template('data.html')


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
