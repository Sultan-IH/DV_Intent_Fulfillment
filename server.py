import logging
from uuid import uuid4 as uuid

from flask import Flask, request, jsonify, g

app = Flask(__name__)
logger = logging.getLogger(__name__)


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


@app.route("/df_webhook", methods=['POST'])
def df_webhook():
    logger.info("serving request with id " + str(g.req_id))
    json = request.get_json()
    print("request json: " + str(json))

    return jsonify({"fulfillmentText": "yeet indeed"})
