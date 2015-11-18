import os
import json
import argparse
import ipaddress
import netifaces
import http.server
from pykeyboard import PyKeyboard


DEFAULT_PORT = 5000
k = PyKeyboard()


class RequestHandler(http.server.BaseHTTPRequestHandler):

    def get_key(self, path):
        keys = {
            '/up': k.up_key,
            '/down': k.down_key,
            '/right': k.right_key,
            '/left': k.left_key,
        }
        return keys.get(path)

    def do_response(self, content=None, content_type=None):
        self.send_response(200)
        if content_type:
            self.send_header('Content-type', 'text/{}'.format(content_type.strip('.')))
        self.end_headers()
        if content:
            self.wfile.write(bytes(content, 'utf-8'))

    def get_static_file_content(self, staticdir='static'):
        filecontent = ''
        path, ext = os.path.splitext(self.path)
        if path == '/':
            path, ext = 'index', '.html'

        if ext in [".css", ".js", ".html"]:
            filename = path.strip('/') + ext
            filepath = os.path.join(staticdir, filename)
            with open(filepath, 'r') as fp:
                filecontent = fp.read()

        return filecontent

    def do_GET(self):
        key_to_tap = self.get_key(self.path)
        content_type = None

        if key_to_tap:
            k.tap_key(key_to_tap)
            data = json.dumps({'status': True})

        if key_to_tap is None:
            data = self.get_static_file_content()

        self.do_response(content=data, content_type=content_type)


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


def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=None):
    port = int(port) if port else DEFAULT_PORT
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    server_address, server_port = httpd.server_address
    print('Pysenteishon is running on {}:{}'.format(server_address, server_port))
    print('If you use a firewall, keep in mind to allow connections on port: {}'.format(port))
    print('On your smartphone, open the web browser using one of the following urls:')
    for iface in get_network_interface_list():
        print('\t- http://{}:{}'.format(iface['addresses'], port))
    httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    run(port=args.port)
