from myapi.main import MyAPIFramework


api = MyAPIFramework()

@api.route('GET', '/hello')
def hello(request):
    request.send_response(200)
    request.end_headers()
    request.wfile.write(b"Hello, World!")

@api.route('POST', '/submit')
def submit(request):
    request.send_response(200)
    request.end_headers()
    request.wfile.write(b"Form Submitted")

if __name__ == "__main__":
    api.run()
