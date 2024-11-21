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
            await self._send_response(send, 404, {"error": "Not Found"})
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
            if iscoroutinefunction(handler):
                response = await handler(json.loads(body.decode("utf-8")) if body else None)
            else:
                response = handler(json.loads(body.decode("utf-8")) if body else None)
            await self._send_response(send, 200, response)
        except Exception as e:
            await self._send_response(send, 500, {"error": str(e)})

    async def _send_response(self, send: Callable, status: int, body: Any):
        """
        Helper to send a response.
        """
        await return_response(send, status, body)

    def run(self):
        run_server(self)
