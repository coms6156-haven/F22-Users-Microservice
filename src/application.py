from flask import Flask, Response, request
import json
from user_resource import UserResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.route("/api/users", methods=["GET"])
def get_users():
    users = UserResource.get_all()

    if users:
        rsp = Response(json.dumps(users), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


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

