import logging
from uuid import uuid4 as uuid
from dashbot import google
from flask import Flask, request, jsonify, g
import DASHBOT_API_KEY from credentials.py

app = Flask(__name__)
logger = logging.getLogger(__name__)
dba = google.google(DASHBOT_API_KEY)
paused_users = {}


@app.before_request
def preprocess():
    logger.info('endpoint: %s, url: %s, path: %s' % (
        request.endpoint,
        request.url,
        request.path))

    g.req_id = uuid()

    try:
        json = request.get_json()
        logger.info("request json: " + str(json))
        g.json = True

    except:
        print("can't marshall request body to json")
        g.json = False


@app.route("/ping")
def ping_route():
    logger.info("PONG for request with id " + str(g.req_id))
    return jsonify(success=True)


@app.route("/pause")
def pause_route():
    logger.info("Paused " + str(g.req_id))
    return jsonify(success=True)


@app.route("/message")
def pause_route():
    logger.info("Paused " + str(g.req_id))
    return jsonify(success=True)


@app.route("/df_webhook", methods=['POST'])
def df_webhook():
    logger.info("serving request with id " + str(g.req_id))
    json = request.get_json()
    print("request json: " + str(json))

    return jsonify({"fulfillmentText": "yeet indeed"})
