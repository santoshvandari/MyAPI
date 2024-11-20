
import uvicorn
from main import MiniAPI
import argparse


app = MiniAPI()

@app.route("/hello", "GET")
async def hello_world(_):
    return {"message": "Hello, World!"}

@app.route("/echo", "POST")
async def echo(data):
    return {"received": data}


def main():
    parser = argparse.ArgumentParser(description="MiniAPI Development Server")
    parser.add_argument("dev", help="Development mode")
    parser.add_argument("main", help="Main application")
    parser.add_argument("--host", default="0.0.0.0", help="Host IP address to bind to (default is 0.0.0.0 for LAN accessibility)")
    parser.add_argument("--port", default=8000, type=int, help="Port to run the server on (default is 8000)")

    args = parser.parse_args()

    # Start the Uvicorn server
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
