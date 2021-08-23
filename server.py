from threading import currentThread
from flask import json
from funkapi import FunkAPI
import flask
from flask import request, jsonify
import os
import hashlib
from waitress import serve


# Environment vars
funk_username = os.environ.get("FUNK_USERNAME")
funk_password = os.environ.get("FUNK_PASSWORD")

password_encoding = os.environ.get("PW_ENCODING") if os.environ.get("PW_ENCODING") != None else "utf-8"
password_hashing_algorithm = (
    os.environ.get("PASSWORD_HASHING_ALGORITHM") if os.environ.get("PASSWORD_HASHING_ALGORITHM") != None else "sha3_512"
)

server_mode = "dev" if os.environ.get("SERVE_MODE") == None else os.environ.get("SERVE_MODE")


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
print(password_hashing_algorithm + " hashed password: " + hashedEncodedFunkPassword)

app = flask.Flask(__name__)

# Routes


@app.before_request
def before_request_callback():
    global api
    try:
        api = FunkAPI(funk_username, funk_password)
    except:
        return jsonify("Authentication (login) failed. Check your credentials."), 511

    authErrMsg = "Client authorization failed."

    if "Authorization" not in request.headers:
        return jsonify(authErrMsg), 401
    if request.headers["Authorization"] != "Bearer " + hashedEncodedFunkPassword:
        return jsonify(authErrMsg), 401


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

        return jsonify(response), 200
    else:
        return "Invalid action requested. Read the docs for further information.", 400


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

        return jsonify(response), 200
    else:
        return "Invalid action requested. Read the docs for further information.", 400


# Main


def serveApi(mode="dev", privKey=None, cert=None):
    if privKey != None and cert != None:
        if mode == "dev":
            app.run(ssl_context=(cert, privKey), host="0.0.0.0", port=5000)
        if mode == "prod":
            serve(app, ssl_context=(cert, privKey), host="0.0.0.0", port=5000)
    else:
        if mode == "dev":
            app.run(host="0.0.0.0", port=5000)
        if mode == "prod":
            serve(app, host="0.0.0.0", port=5000)


privateKeyEnvVar = os.environ.get("SSL_PRIVATE_KEY")
certEnvVar = os.environ.get("SSL_CERT")

if privateKeyEnvVar != None and certEnvVar != None:
    try:
        if not os.path.isdir("./ssl"):
            os.mkdir("./ssl")

        privateKeyFilePath = "./ssl/privkey.pem"
        open(privateKeyFilePath, "w+").write(privateKeyEnvVar)

        certFilePath = "./ssl/cert.pem"
        open(certFilePath, "w+").write(certEnvVar)

        print("SSL via docker run -e args found.")
        serveApi(mode=server_mode, cert=certFilePath, privKey=privateKeyFilePath)
    except:
        print(
            "SSL via docker run -e args skipped. Your system perhaps cripples the formatting (e.g. Synology NAS). Searching for volume mounted .pem files now."
        )

privateKeyVolumeFile = "./volume/ssl/privkey.pem"
certVolumeFile = "./volume/ssl/cert.pem"

if os.path.isfile(privateKeyVolumeFile) and os.path.isfile(certVolumeFile):
    try:
        print("Found .pem files in mounted volume.")
        serveApi(mode=server_mode, cert=certVolumeFile, privKey=privateKeyVolumeFile)
    except:
        print("Invalid .pem files in mounted volume.")

print("Starting server without encryption.")
serveApi(mode=server_mode)
