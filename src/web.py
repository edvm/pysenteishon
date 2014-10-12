from flask import Flask, render_template
from flask import jsonify as flask_jsonify
from functools import wraps
from pykeyboard import PyKeyboard
import netifaces
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
    local_ips = get_local_ip_addresses()
    return render_template('index.html', local_ips=local_ips)


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
    1 / 0
    k.tap_key(k.left_key)  # UX enduser experience


@app.route('/btn-left/')
@jsonify
def btn_left():
    k.tap_key(k.right_key)  # UX enduser experience


def run_pysenteishon():
    app.run(host='0.0.0.0', debug=True)


def get_local_ip_addresses():
    local_ips = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue
        iface = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if iface != None:
            for x in iface:
                local_ips.append(x['addr'])
    return local_ips


if __name__ == '__main__':
    run_pysenteishon()
