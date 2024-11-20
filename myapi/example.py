from miniapi import MiniAPI

app = MiniAPI()

@app.route("/hello", "GET")
def hello_world(_):
    return {"message": "Hello, World!"}

@app.route("/echo", "POST")
def echo(data):
    print(data)
    return {"received": data}

# The app will be automatically served when running the script.
if __name__ == "__main__":
    app.run()
