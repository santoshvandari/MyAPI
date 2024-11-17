import http.server
import socketserver
import json
# import argparse

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
            print(f"Serving on {self.host}:{self.port}")
            httpd.serve_forever()

    def _create_handler(self):
        routes = self.routes

        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def _send_response(self, response_data, status_code=200):
                # Convert the response_data to JSON format
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # If the data is a dictionary, convert to JSON, else send as it is
                if isinstance(response_data, dict):
                    response_data = json.dumps(response_data)

                # Write response
                self.wfile.write(response_data.encode())

            def do_GET(self):
                if self.path in routes['GET']:
                    try:
                        # Call the registered function and expect a response and status code
                        response, status_code = routes['GET'][self.path](self)
                        self._send_response(response, status_code)
                    except Exception as e:
                        self.send_error(500, f"Internal Server Error: {str(e)}")
                else:
                    self.send_error(404, "Route not found")

            def do_POST(self):
                if self.path in routes['POST']:
                    try:
                        # Call the registered function and expect a response and status code
                        response, status_code = routes['POST'][self.path](self)
                        self._send_response(response, status_code)
                    except Exception as e:
                        self.send_error(500, f"Internal Server Error: {str(e)}")
                else:
                    self.send_error(404, "Route not found")

        return RequestHandler
