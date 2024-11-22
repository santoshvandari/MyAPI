import json
from typing import Callable, Dict, Any
from inspect import iscoroutinefunction
from sendresponse import return_response
from runserver import run_server


class MiniAPI:
    def __init__(self):
        self.routes = {}

    def route(self, path: str, method: str):
        """
        Decorator to register a route.
        """
        method = method.upper()
        if method not in {"GET", "POST"}:
            raise ValueError("Only GET and POST methods are supported.")

        def decorator(func: Callable):
            if path not in self.routes:
                self.routes[path] = {}
            self.routes[path][method] = func
            return func

        return decorator

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        """
        ASGI entry point.
        """
        if scope["type"] != "http":
            return

        path = scope["path"]
        method = scope["method"]
        handler = self.routes.get(path, {}).get(method)

        if handler is None:
            await return_response(send, 404, {"error": "Not Found"})
            return

        # Parse request body for POST
        body = b""
        if method == "POST":
            while True:
                event = await receive()
                if event["type"] == "http.request":
                    body += event.get("body", b"")
                    if not event.get("more_body", False):
                        break

        try:
            data = json.loads(body.decode("utf-8")) if body else None
            response = await handler(data) if iscoroutinefunction(handler) else handler(data)
            await return_response(send, 200, response)
        except Exception as e:
            await return_response(send, 500, {"error": str(e)})

    def run(self):
        """
        Starts the ASGI server using the run_server helper.
        """
        run_server(self)
