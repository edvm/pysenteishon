from flask import Flask, render_template
from pykeyboard import PyKeyboard
app = Flask(__name__)
k = PyKeyboard()


@app.route('/')
def pysenteishon():
    return render_template('index.html')


@app.route('/btn-up/')
def btn_up():
    k.tap_key(k.up_key)
    return render_template('index.html')


@app.route('/btn-down/')
def btn_down():
    k.tap_key(k.down_key)
    return render_template('index.html')


@app.route('/btn-right/')
def btn_right():
    k.tap_key(k.right_key)
    return render_template('index.html')


@app.route('/btn-left/')
def btn_left():
    k.tap_key(k.left_key)
    return render_template('index.html')


def run_pysenteishon():
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    run_pysenteishon()
