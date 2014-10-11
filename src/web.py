from flask import Flask, render_template
from flask import jsonify as flask_jsonify
from functools import wraps
from pykeyboard import PyKeyboard
import socket
app = Flask(__name__)
k = PyKeyboard()


def jsonify(f):
    @wraps(f)
    def make_response(*args, **kwargs):
        response = dict(status=None, msg='')
        try:
            f(*args, **kwargs)
            response['status'] = True
        except Exception as exc:
            response['status'] = False
            response['msg'] = str(exc)
        return flask_jsonify(**response)
    return make_response


@app.route('/')
def pysenteishon():
    ip_addresses = get_local_ip_addresses()
    return render_template('index.html', ips=ip_addresses)


@app.route('/btn-up/')
@jsonify
def btn_up():
    k.tap_key(k.up_key)


@app.route('/btn-down/')
@jsonify
def btn_down():
    k.tap_key(k.down_key)


@app.route('/btn-right/')
@jsonify
def btn_right():
    k.tap_key(k.left_key)  # UX enduser experience


@app.route('/btn-left/')
@jsonify
def btn_left():
    k.tap_key(k.right_key)  # UX enduser experience


def run_pysenteishon():
    app.run(host='0.0.0.0', debug=True)


def get_local_ip_addresses():
    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]


if __name__ == '__main__':
    run_pysenteishon()
