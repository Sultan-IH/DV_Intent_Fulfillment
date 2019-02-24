import logging
from uuid import uuid4 as uuid
from pprint import pprint
from flask import Flask, request, jsonify, g
from db_models import db
from intents.need_home import find_home
from sentiment import get_sentiment
from credentials import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, MENTOR_DEFAULT_NUMBER, TWILIO_DEFAULT_NUMBER, GAPP_PASSWORD
from twilio.rest import Client
import time
import smtplib



app = Flask(__name__)
logger = logging.getLogger(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

peer_chatrooms = []

POSTGRES = {
    'user': 'cerber',
    'pw': 'papi',
    'db': 'paula',
    'host': 'localhost',
    'port': '5432'
}

s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
s.login("vincnttan@gmail.com",GAPP_PASSWORD)



app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

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
        sent_text = json['queryResult']['queryText']
        sentiment = get_sentiment(sent_text, str(g.req_id))
        g.sentiment = sentiment['score']
        print("sentiment: ", g.sentiment)
        if (g.sentiment) < 0.01:
            return
        # g.sentiment = get_sentiment()

    except Exception as e:
        print("can't marshall request body to json, got e: ", e)
        g.json = False


@app.route("/ping")
def ping_route():
    logger.info("PONG for request with id " + str(g.req_id))
    return jsonify(success=True)


@app.route("/pause")
def pause_route():
    logger.info("Paused " + str(g.req_id))
    return jsonify(success=True)

'''
@app.route("/message")
def pause_route():
    logger.info("Paused " + str(g.req_id))
    return jsonify(success=True)
'''


@app.route("/df_webhook", methods=['POST'])
def df_webhook():
    print("serving request with id " + str(g.req_id))
    if not g.json:
        return jsonify(error="unknown request format")

    query = g.json['queryResult']
    pprint(query)
    intent = query['intent']['displayName']
    print("\n\n\nserving request with intent: " + intent)

    if intent == 'homeless.1 - yes - profile':
        context = query['outputContexts'][0]
        params = context['parameters']
        print("\n\n\n\n\nAAAAAAAAAAAAAAAAAAAA - "+params['age.original'])
        if int(params['age.original']) > 25:
            msg = "Sorry but we can't help people over 25."
            return jsonify(fulfillmentText=msg)
        else:
            return jsonify(g.json)

    if intent == "Companionship":
        # if no current chat room, create chat room
        if len(peer_chatrooms) == 0:
            uid = uuid()
            peer_chatrooms.append(uid)
            url = "tlk.io/paula-" + str(uid)[:15]
            msg = "we've created a chatroom " + url + " and we are waiting for someone to join!"
            return jsonify(fulfillmentText=msg)

        uid = peer_chatrooms[-1]
        url = "tlk.io/paula-" + str(uid)[:15]
        peer_chatrooms.remove(uid)

        msg = "we've matched you with someone you might like to talk to, go to " + url
        return jsonify(fulfillmentText=msg)


    if intent == "Mentorship":
        # if no current chat room, create chat room

        # if len(mentor_chatrooms) == 0:
        uid = uuid()
        url = "tlk.io/paula-" + str(uid)[:15]
        message = client.messages.create(
		    to=MENTOR_DEFAULT_NUMBER, 
		    from_=TWILIO_DEFAULT_NUMBER,
		    body="There is a person urgently in need. Please follow on to this chatroom: " + url + " !"
		    )

        msg = "we've created a chatroom " + url + " and we are waiting for a mentor to join, please follow the link"
        return jsonify(fulfillmentText=msg)


    if intent == 'homeless.1 - yes - profile.2 - reference':
        context = query['outputContexts'][-1]
        params = context['parameters']
        subject = "OMG YOU GOTTA READ THIS"
        message = "Hi %s %s, we are contacting you about %s"%(params["ref-given-name"],params["ref-last-name"],params["given-name"])
        s.sendmail("vincnttan@gmail.com",params["ref-email"], 'Subject: {}\n\n{}'.format(subject, message))
        s.quit()

    return jsonify(g.json)


@app.route('/dbtest', methods=['GET'])
def test_db():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>DB works.</h1>'
    except:
        return '<h1>DB is broken.</h1>'
