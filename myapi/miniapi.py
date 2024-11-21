import json
import argparse
import uvicorn
from typing import Callable, Dict, Any
from inspect import iscoroutinefunction
from sendresponse import return_response


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
        """
        Start the ASGI server with optional host and port arguments.
        """
        parser = argparse.ArgumentParser(description="MiniAPI Development Server")
        parser.add_argument(
            "--host", default="127.0.0.1", help="Host IP address to bind to (default: 0.0.0.0)"
        )
        parser.add_argument(
            "--port", default=8000, type=int, help="Port to run the server on (default: 8000)"
        )
        args = parser.parse_args()

        print(f"Starting server on {args.host}:{args.port}")
        uvicorn.run(self, host=args.host, port=args.port)

