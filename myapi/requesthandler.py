import json
from urllib.parse import urlparse, parse_qs

def handle_request(self,routes):
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