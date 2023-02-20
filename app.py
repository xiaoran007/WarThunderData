from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/indev/')
def indev():
    return render_template('indev.html')


if __name__ == '__main__':
    app.run()
