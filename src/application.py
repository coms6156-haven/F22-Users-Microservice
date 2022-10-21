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
        users = UserResource.get_all()

        if users:
            rsp = Response(json.dumps(users), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        return rsp
    # Sign up a user
    elif request.method == "POST":
        req = request.form

        email = req['email']
        password = req['password']
        first_name = req['first_name']
        last_name = req['last_name']

        if not email or not password or not first_name or not last_name:
            return Response("INVALID BODY", status=404, content_type="text/plain")

        try:
            UserResource.sign_up_user(email, password, first_name, last_name)
        except Exception as e:
            return Response(json.dumps({"result": False, "error": f"{e}"}), status=404, content_type="application.json")

        return Response(json.dumps({"result": True}), status=200, content_type="application.json")



@app.route("/api/users/<uid>", methods=["GET"])
def get_user_by_uid(uid):
    result = UserResource.get_by_key(uid)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

