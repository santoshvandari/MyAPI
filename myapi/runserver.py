import argparse

import uvicorn


def run_server(self):
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