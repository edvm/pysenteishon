from flask import Flask, render_template
from pykeyboard import PyKeyboard
import socket
app = Flask(__name__)
k = PyKeyboard()


@app.route('/')
def pysenteishon():
    ip_addresses = get_local_ip_addresses()
    #ip_addresses = ', '.join(('http://%s:5000' % ip for ip in ip_addresses))
    return render_template('index.html', ip_addresses=ip_addresses)


@app.route('/btn-up/')
def btn_up():
    k.tap_key(k.up_key)
    return ''


@app.route('/btn-down/')
def btn_down():
    k.tap_key(k.down_key)
    return ''


@app.route('/btn-right/')
def btn_right():
    k.tap_key(k.left_key)  # UX enduser experience
    return ''


@app.route('/btn-left/')
def btn_left():
    k.tap_key(k.right_key)  # UX enduser experience
    return ''


def run_pysenteishon():
    app.run(host='0.0.0.0', debug=True)


def get_local_ip_addresses():
    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]


if __name__ == '__main__':
    run_pysenteishon()
