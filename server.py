import logging
from pprint import pprint
from uuid import uuid4 as uuid

from flask import Flask, request, jsonify, g

from db_models import db
from intents.need_home import find_home

app = Flask(__name__)
logger = logging.getLogger(__name__)

peer_chatrooms = []
mentor_chatrooms = []

POSTGRES = {
    'user': 'cerber',
    'pw': 'papi',
    'db': 'paula',
    'host': 'localhost',
    'port': '5432',
}

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
        # g.sentiment = get_sentiment()

    except:
        print("can't marshall request body to json")
        g.json = False


@app.route("/ping")
def ping_route():
    logger.info("PONG for request with id " + str(g.req_id))
    return jsonify(success=True)


@app.route("/df_webhook", methods=['POST'])
def df_webhook():
    print("serving request with id " + str(g.req_id))
    if not g.json:
        return jsonify(error="unknown request format")

    query = g.json['queryResult']
    pprint(query)
    intent = query['intent']['displayName']
    if intent == 'Urgent Home - yes':
        print("finding a home for " + str(g.req_id))

        context = query['outputContexts'][0]
        params = context['parameters']

        date = params['date']
        location = params['location']['subadmin-area']

        house = find_home(location, date)
        msg = "we found a house at %s owned by %s to stay at %s" % (house['location'], house['name'], house['date'])

        return jsonify(fulfillmentText=msg)

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

        # if current chat room, connect and then clear current chat room
    if intent == "Mentorship":
        # if no current chat room, create chat room

        if len(mentor_chatrooms) == 0:
            uid = uuid()
            mentor_chatrooms.append(uid)
            url = "tlk.io/paula-" + str(uid)[:15]
            msg = "we've created a chatroom " + url + " and we are waiting for a mentor to join, please follow the link"
            return jsonify(fulfillmentText=msg)

        uid = mentor_chatrooms[-1]
        url = "tlk.io/paula-" + str(uid)[:15]
        mentor_chatrooms.remove(uid)

        msg = "we've matched you with one of our best mentors! Go to " + url
        return jsonify(fulfillmentText=msg)

    return jsonify(g.json)


@app.route('/dbtest', methods=['GET'])
def test_db():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>DB works.</h1>'
    except:
        return '<h1>DB is broken.</h1>'
