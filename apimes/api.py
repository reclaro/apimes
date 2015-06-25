import logging
import sys
from flask import Flask

from flask_restful import Api

from apimes.resources.message import Message
from apimes.resources.subscription import Subscription

app = Flask(__name__)
api = Api(app)

api.add_resource(Message, '/<topic>')
api.add_resource(Subscription, '/<topic>/<username>')

logging.basicConfig(filename='apimes.log', level=logging.DEBUG)
if __name__ == '__main__':
    app.run(debug=True)
