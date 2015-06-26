import logging
from flask import Flask

from flask_restful import Api

from apimes import utils
from apimes.resources.message import Message
from apimes.resources.subscription import Subscription

app = Flask(__name__)
api = Api(app)

api.add_resource(Message, '/<topic>')
api.add_resource(Subscription, '/<topic>/<username>')

log_file = utils.get_config_section('default', 'log_file')

logging.basicConfig(filename=log_file, level=logging.DEBUG)
if __name__ == '__main__':
    app.run(debug=True)
