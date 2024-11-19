import http.server
import socketserver
import json
import argparse
from requesthandler import handle_request

class MyAPIFramework:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.routes = {}
        self.middlewares = []

    def route(self, path, methods=['GET']):
        """ Decorator to register routes and allowed HTTP methods """
        def decorator(func):
            self.routes[path] = {"methods": methods, "handler": func}
            return func
        return decorator

    def middleware(self, middleware_func):
        """ Add middleware for request pre-processing """
        self.middlewares.append(middleware_func)

    def run(self):
        """ Start the server """
        handler = self._create_handler()
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"Serving on {self.host}:{self.port}")
            httpd.serve_forever()

    def _create_handler(self):
        """ Create request handler dynamically """
        routes = self.routes
        middlewares = self.middlewares

        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def _send_response(self, response_data, status_code=200, headers=None, cookies=None):
                """ Sends JSON response """
                self.send_response(status_code)

                # Set headers
                self.send_header('Content-type', 'application/json')
                if headers:
                    for header, value in headers.items():
                        self.send_header(header, value)
                if cookies:
                    for cookie, value in cookies.items():
                        self.send_header('Set-Cookie', f'{cookie}={value}')
                
                self.end_headers()

                # Write response data
                if isinstance(response_data, dict):
                    response_data = json.dumps(response_data)
                self.wfile.write(response_data.encode())

           

            def do_GET(self):
                handle_request(routes)

            def do_POST(self):
                handle_request(routes)

        return RequestHandler
