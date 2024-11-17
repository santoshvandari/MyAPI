import http.server
import socketserver
import argparse

class MyAPIFramework:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.routes = {'GET': {}, 'POST': {}}

    def route(self, method, path):
        def decorator(func):
            if method in ['GET', 'POST']:
                self.routes[method][path] = func
            return func
        return decorator

    def run(self):
        handler = self._create_handler()
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"Serving on http://{self.host}:{self.port}")
            httpd.serve_forever()

    def _create_handler(self):
        routes = self.routes
        class RequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path in routes['GET']:
                    routes['GET'][self.path](self)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")

            def do_POST(self):
                if self.path in routes['POST']:
                    routes['POST'][self.path](self)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")
        return RequestHandler
