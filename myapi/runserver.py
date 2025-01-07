import argparse
import uvicorn


def run_server(app):
    """
    Start the ASGI server with optional host and port arguments.
    """
    parser = argparse.ArgumentParser(description="MiniAPI Development Server Running")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host IP address to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        default=8080,
        type=int,
        help="Port to run the server on (default: 8080)",
    )
    parser.add_argument(
        "--reload",
        type=lambda x: str(x).lower() in {"true", "1", "yes"},
        default=True,
        help="Enable or disable auto-reload on file changes (default: True)",
    )
    args = parser.parse_args()

    print(f"Starting server on {args.host}:{args.port} (reload={'enabled' if args.reload else 'disabled'})")
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
