from myapi.main import MyAPIFramework


api = MyAPIFramework()



# GET and POST requests on the same route
@api.route('/user', methods=['GET', 'POST'])
def user_handler(request, query_params, data):
    if request.command == 'GET':
        response = {"message": "GET request", "query_params": query_params}
        return response, 200, None, None
    elif request.command == 'POST':
        response = {"message": "POST request", "data": data}
        return response, 201, None, {"session_id": "abc123"}

# PUT and DELETE on the same route
@api.route('/item', methods=['PUT', 'DELETE'])
def item_handler(request, query_params, data):
    if request.command == 'PUT':
        response = {"message": "PUT request", "data": data}
        return response, 200, None, None
    elif request.command == 'DELETE':
        response = {"message": "DELETE request"}
        return response, 204, None, None

if __name__ == "__main__":
    api.run()
