from miniapi import MiniAPI

app = MiniAPI()

@app.route("/hello", "GET")
def hello_world(_):
    return {"message": "Hello, World!"}

@app.route("/echo", "POST")
def echo(data):
    print(data)
    return {"received": data}


@app.route("/predict", "POST")
async def predict(data):
    # Replace this with actual ML model inference
    model_result = {"prediction": "cat", "confidence": 0.95}
    return {"received_data": data, "result": model_result}

@app.route("/health", "GET")
async def health_check(_):
    return {"status": "healthy"}

# The app will be automatically served when running the script.
if __name__ == "__main__":
    app.run()
