import argparse
import cherrypy
import ipaddress
import netifaces
import os
import subprocess
import sys


ON_MACOS = sys.platform == 'darwin'

if ON_MACOS:
    MACOS_CMD = "/usr/bin/osascript -e 'tell application \"System Events\" to key code {}'"
else:
    from pykeyboard import PyKeyboard
    k = PyKeyboard()

DEFAULT_PORT = 5000


class PySenteishon(object):

    @cherrypy.expose
    def index(self):
        """Redirect to index.html"""
        raise cherrypy.HTTPRedirect("/index.html")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def press(self, key=None, *args, **kwargs):
        """Press a key endpoint.

        GET URL Example:
            http://127.0.0.1:8080/press?key=up

        Arguments:
            'up'(str)       Press the up arrow key
            'down'(str)     Press the down arrow key
            'left'(str)     Press the left arrow key
            'right'(str)    Press the right arrow key

        Returns a json response with action status.

        For example:
            {"key-pressed": true, "key": "left"}
        """
        key_to_tap = self.get_key(key)
        if key_to_tap:
            if ON_MACOS:
                subprocess.run(MACOS_CMD.format(key_to_tap), shell=True)
            else:
                k.tap_key(key_to_tap)
            return {"key-pressed": True, "key": key}
        return {"key-pressed": False, "key": None}

    @cherrypy.expose(alias='ifconfig')
    @cherrypy.tools.json_out()
    def network_information(self):
        """Return a JSON response with network information.

        GET URL Example:
            http://127.0.0.1:8080/ifconfig

        For example:
        [
            {"addresses": "192.168.0.13", "name": "wlp1s0"},
            {"addresses": "172.17.0.1", "name": "docker0"}
        ]
        """
        network_info = get_network_interface_list()
        return network_info

    def get_key(self, path):
        if ON_MACOS:
            keys = {
                'up': 126,
                'down': 125,
                'left': 123,
                'right': 124,
            }
        else:
            keys = {
                'up': k.up_key,
                'down': k.down_key,
                'left': k.left_key,
                'right': k.right_key,
            }
        return keys.get(path)


def get_network_interface_list():
    network_interfaces = []
    for ifaceName in netifaces.interfaces():
        addresses = [i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(
            netifaces.AF_INET, [{'addr': '127.0.0.1'}]) if not
            ipaddress.ip_address(i['addr']).is_loopback and i['addr'] != '']
        if not addresses:  # interface without an ip address
            continue
        network_interfaces.append({'name': ifaceName, 'addresses': addresses})
    return network_interfaces


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help="Listen on port")
    parser.add_argument('-a', '--auth', nargs=2, metavar=('user', 'password'), help="Basic auth")
    args = parser.parse_args()

    def validate_password(realm, user, password):
        return args.auth[0] == user and args.auth[1] == password

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': args.port
    })

    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        }
    }
    if args.auth is not None:
        conf['/'].update({
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'pysenteishon',
            'tools.auth_basic.checkpassword': validate_password,
        })
    cherrypy.quickstart(PySenteishon(), '/', conf)

if __name__ == '__main__':
    main()
