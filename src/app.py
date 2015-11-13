import json
import codecs
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

    def do_GET(self):
        key_to_press = self.get_key(self.path)
        if key_to_press:
            k.tap_key(key_to_press)
        self.send_response(200)
        self.end_headers()
        data = json.dumps({'status': True})
        self.wfile.write(codecs.utf_8_encode(data)[0])


def run(server_class=http.server.HTTPServer, handler_class=RequestHandler):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
