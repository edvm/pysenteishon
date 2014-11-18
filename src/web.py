import os
import uuid
import webbrowser
import netifaces
from functools import wraps

from flask import Flask, render_template
from flask import jsonify as flask_jsonify
from pykeyboard import PyKeyboard
import pyqrcode


PORT = 5000  # default listen on port 5000
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
    qr_code = ""
    if local_ips:
        preferred_ip = local_ips[0]
        link = "http://%s:%s" % (preferred_ip, PORT)
        url = pyqrcode.create(link)
        filename = str(uuid.uuid4())
        path = os.path.join(
            os.path.dirname(__file__), "static/img/%s.svg" % filename)
        url.svg(path, scale=8)
        qr_code = "/static/img/%s.svg" % filename
    return render_template('index.html', local_ips=local_ips, qr_code=qr_code)


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
    k.tap_key(k.left_key)  # UX


@app.route('/btn-left/')
@jsonify
def btn_left():
    k.tap_key(k.right_key)  # UX


def run_pysenteishon(IP_ADDRESS='0.0.0.0', PORT=5000, debug=True):
    app.run(host=IP_ADDRESS, port=PORT, debug=debug)


def get_local_ip_addresses():
    local_ips = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue
        iface = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if iface is not None:
            for x in iface:
                addr = x['addr']
                if addr == '127.0.0.1':
                    continue
                local_ips.append(x['addr'])
    return local_ips


if __name__ == '__main__':
    IP_ADDRESS = '0.0.0.0'  # default listen in all interfaces
    url = 'http://{host}:{port}'.format(host=IP_ADDRESS, port=PORT)
    webbrowser.open(url)
    print(' * Opening web browser at %s, please wait ...' % url)
    run_pysenteishon(IP_ADDRESS, PORT, debug=False)