from flask import json
from funkapi import FunkAPI
import flask
from flask import Flask, request, jsonify
import json

from configuration.credentials import *

print("Logging in using:")
print("Username: " + funk_username)
print("Password: " + funk_password)

api = FunkAPI(funk_username, funk_password)
app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def retireve():
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


app.run(host = "0.0.0.0", port = 5000, debug = False)