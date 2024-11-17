import http.server
import socketserver
import json
import argparse
from urllib.parse import urlparse, parse_qs

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

            def _handle_request(self):
                """ Handle both GET/POST requests based on route """
                parsed_url = urlparse(self.path)
                path = parsed_url.path
                method = self.command

                if path in routes:
                    route_info = routes[path]
                    allowed_methods = route_info["methods"]
                    handler = route_info["handler"]

                    if method in allowed_methods:
                        try:
                            # Get query parameters
                            query_params = parse_qs(parsed_url.query)

                            # Get JSON body or form data
                            content_type = self.headers.get('Content-Type', '')
                            if 'application/json' in content_type:
                                content_length = int(self.headers.get('Content-Length', 0))
                                body = self.rfile.read(content_length).decode('utf-8')
                                data = json.loads(body)
                            elif 'application/x-www-form-urlencoded' in content_type:
                                content_length = int(self.headers.get('Content-Length', 0))
                                body = self.rfile.read(content_length).decode('utf-8')
                                data = parse_qs(body)
                            else:
                                data = None

                            # Call the route handler with request information
                            response, status_code, headers, cookies = handler(self, query_params, data)
                            self._send_response(response, status_code, headers, cookies)
                        except Exception as e:
                            self.send_error(500, f"Internal Server Error: {str(e)}")
                    else:
                        self.send_error(405, f"Method {method} Not Allowed")
                else:
                    self.send_error(404, "Route not found")

            def do_GET(self):
                self._handle_request()

            def do_POST(self):
                self._handle_request()

        return RequestHandler
