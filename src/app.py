import os
import json
import argparse
import ipaddress
import netifaces
import http.server
from pykeyboard import PyKeyboard


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

    def get_ip_address_list(self):
        local_ips = []
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if interface == 'lo':
                continue
            interface_data = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if interface_data is not None:
                for field in interface_data:
                    ip = ipaddress.ip_address(field['addr'])
                    if ip.is_loopback:
                        continue
                    local_ips.append(field['addr'])
        return local_ips

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


def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=None):
    server_address = ('', int(port) if port else 5000)
    httpd = server_class(server_address, handler_class)
    server_address, server_port = httpd.server_address
    print('Running on {}:{}'.format(server_address, server_port))
    httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    run(port=args.port)
