import argparse
import uvicorn


def run_server(app):
    """
    Start the ASGI server with optional host and port arguments.
    """
    parser = argparse.ArgumentParser(description="MiniAPI Development Server Running")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host IP address to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", default=8080, type=int, help="Port to run the server on (default: 8080)"
    )
    args = parser.parse_args()

    print(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
