import os
import json
import argparse
import ipaddress
import netifaces
import http.server
import cherrypy

from pykeyboard import PyKeyboard


DEFAULT_PORT = 5000
k = PyKeyboard()


class PySenteishon(object):

    @cherrypy.expose
    def index(self):
        """Redirect to index.html"""
        raise cherrypy.HTTPRedirect("/index.html")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def press(self, key=None):
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
        network_interfaces.append({'name': ifaceName, 'addresses': ','.join(addresses)})
    return network_interfaces


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()

    conf = {
        # 'server.socket_port': int(args.port) if args.port else DEFAULT_PORT,
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.abspath(os.getcwd()), "static")
        }
    }
    cherrypy.quickstart(PySenteishon(), '/', conf)
