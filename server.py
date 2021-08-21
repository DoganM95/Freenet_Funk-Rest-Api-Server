from threading import currentThread
from flask import json
from funkapi import FunkAPI
import flask
from flask import request, jsonify
import os
import hashlib


# Environment vars
funk_username = os.environ.get("FUNK_USERNAME")
funk_password = os.environ.get("FUNK_PASSWORD")

password_encoding = os.environ.get("PW_ENCODING") if os.environ.get("PW_ENCODING") != None else "utf-8"
password_hashing_algorithm = (
    os.environ.get("PASSWORD_HASHING_ALGORITHM") if os.environ.get("PASSWORD_HASHING_ALGORITHM") != None else "sha512"
)

privateKey = os.environ.get("SSL_PRIVATE_KEY")
cert = os.environ.get("SSL_CERT")


# Preps

try:
    encodedFunkPassword = funk_password.encode(password_encoding)
except:
    print("Encoding " + password_encoding + "not supported.")
try:
    hashedEncodedFunkPassword = hashlib.new(password_hashing_algorithm)
    hashedEncodedFunkPassword.update(encodedFunkPassword)
    hashedEncodedFunkPassword = hashedEncodedFunkPassword.hexdigest()
except:
    print("Hashing algorithm " + password_hashing_algorithm + " not supported.")
    print("The following are supported:")
    for supportedHash in hashlib.algorithms_available:
        print(supportedHash)

print("Logging in as:")
print("Username: " + funk_username)
print("Hashed Password: " + hashedEncodedFunkPassword)

app = flask.Flask(__name__)

# Routes


@app.before_request
def before_request_callback():
    global api
    try:
        api = FunkAPI(funk_username, funk_password)
    except:
        return jsonify("Login failed. Check your credentials.")

    authErrMsg = "Client authorization failed."

    if "Authorization" not in request.headers:
        return jsonify(authErrMsg)
    if request.headers["Authorization"] != "Bearer " + hashedEncodedFunkPassword:
        return jsonify(authErrMsg)


@app.route("/", methods=["GET"])
def retrieve():
    req = request.get_json()
    if "retrieve" in req:
        requestedAction = str(req["retrieve"])
        if requestedAction == "data":
            response = api.getData()
        if requestedAction == "personalInfo":
            response = api.getPersonalInfo()
        if requestedAction == "orderedProducts":
            response = api.getOrderedProducts()
        if requestedAction == "currentPlan":
            response = api.getCurrentPlan()

        return jsonify(response)
    else:
        return "Invalid action requested. Read the docs for further information."


@app.route("/", methods=["PUT"])
def order():
    req = request.get_json()
    if "order" in req:
        requestedAction = str(req["order"])
        if requestedAction == "1gb":
            response = api.order1GBPlan()
        if requestedAction == "unlimited":
            response = api.orderUnlimitedPlan()
        if requestedAction == "pause":
            response = api.startPause()
        if requestedAction == "undo":
            response = api.stopLatestPlan()

        return jsonify(response)
    else:
        return "Invalid action requested. Read the docs for further information."


# Main

os.mkdir("./ssl")

privateKeyFile = "./ssl/privkey.pem"
open(privateKeyFile, "w+").write(privateKey)

certFile = "./ssl/cert.pem"
open(certFile, "w+").write(cert)

if privateKey != None and cert != None:
    app.run(ssl_context=(certFile, privateKeyFile), host="0.0.0.0", port=5000, debug=False)
else:
    app.run(host="0.0.0.0", port=5000, debug=False)
