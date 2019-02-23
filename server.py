import logging
from uuid import uuid4 as uuid

from flask import Flask, request, jsonify, g

from intents.need_home import find_home

from db_models import db

app = Flask(__name__)
logger = logging.getLogger(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
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


    return jsonify(g.json)


@app.route('/slack-integration', methods=['POST'])
def slack_handler():
    print("slack requests")
    print(g.json)
    return jsonify(g.json)


@app.route('/dbtest',methods=['GET'])
def test_db():
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>DB works.</h1>'
    except:
        return '<h1>DB is broken.</h1>'