import logging
from uuid import uuid4 as uuid
from dashbot import google
from flask import Flask, request, jsonify, g
from intents.need_home import find_home
from credentials import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, MENTOR_DEFAULT_NUMBER, TWILIO_DEFAULT_NUMBER
from twilio.rest import Client

app = Flask(__name__)
logger = logging.getLogger(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.before_request
def preprocess():
    logger.info('endpoint: %s, url: %s, path: %s' % (
        request.endpoint,
        request.url,
        request.path))
    g.req_id = uuid()

    try:
        json = request.get_json()
        g.json = json
        # g.sentiment = get_sentiment()

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
    print("serving request with id " + str(g.req_id))
    if not g.json:
        return jsonify(error="unknown request format")

    query = g.json['queryResult']
    action = query['action']

    if action == 'UrgentHome.UrgentHome-yes':

        print("finding a home for " + str(g.req_id))
        context = query['outputContexts'][0]
        params = context['parameters']

        date = params['date']
        location = params['location']['subadmin-area']

        house = find_home(location, date)
        msg = "we found a house at %s owned by %s to stay at %s" % (house['location'], house['name'], house['date'])
        return jsonify(fulfillmentText=msg)
 	if action == 'UrgentHome.UrgentHome-yes':

        print("finding a home for " + str(g.req_id))
        context = query['outputContexts'][0]
        params = context['parameters']

        date = params['date']
        location = params['location']['subadmin-area']

        house = find_home(location, date)
        msg = "we found a house at %s owned by %s to stay at %s" % (house['location'], house['name'], house['date'])
        return jsonify(fulfillmentText=msg)

	message = client.messages.create(
	    to=MENTOR_DEFAULT_NUMBER, 
	    from_=TWILIO_DEFAULT_NUMBER,
	    body="Hello from Python!")


    return jsonify(g.json)








@app.route('/slack-integration', methods=['POST'])
def slack_handler():
    print("slack requests")
    print(g.json)
    return jsonify(g.json)
