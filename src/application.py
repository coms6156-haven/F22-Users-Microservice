from flask import Flask, Response, request
import json
from user_resource import UserResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.route("/api/users", methods=["GET", "POST"])
def users_route():
    # Get all users
    if request.method == "GET":
        if len(request.args) == 0:
            users = UserResource.get_all()
        else:
            users = UserResource.get_users_by_params(request.args)

        return Response(json.dumps(users), status=200, content_type="application.json")

    # Sign up a user
    elif request.method == "POST":
        email = request.json.get('email', '')
        password = request.json.get('password', '')
        first_name = request.json.get('first_name', '')
        last_name = request.json.get('last_name', '')

        if not email or not password:
            return Response("INVALID BODY", status=404, content_type="text/plain")

        try:
            UserResource.sign_up_user(email, password, first_name, last_name)
        except Exception as e:
            return Response(f"{e}", status=404, content_type="text/plain")

        return Response(json.dumps({"result": True}), status=200, content_type="application.json")


@app.route("/api/users/<uid>", methods=["GET", "DELETE", "PUT"])
def user_route(uid):
    # Get user by uid
    if request.method == "GET":
        result = UserResource.get_by_key(uid)

        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp

    # Delete user by uid
    elif request.method == "DELETE":
        try:
            UserResource.delete_user(uid)
        except Exception as e:
            return Response(f"{e}", status=404, content_type="text/plain")

        return Response(json.dumps({"result": True}), status=200, content_type="application.json")

    # Update user by uid
    elif request.method == "PUT":
        try:
            UserResource.update_user(uid, request.json)
        except Exception as e:
            return Response(f"{e}", status=404, content_type="text/plain")

        return Response(json.dumps({"result": True}), status=200, content_type="application.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
