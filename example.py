from myapi.main import MyAPIFramework


api = MyAPIFramework()

@api.route('GET', '/hello')
def hello(request):
    response = {"message": "Hello, World!"}
    return response, 200

@api.route('POST', '/submit')
def submit(request):
    response = {"message": "Form Submitted"}
    return response, 201

if __name__ == "__main__":
    api.run()
