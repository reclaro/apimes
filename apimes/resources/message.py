from flask import request
from flask_restful import Resource

from apimes import utils

class Message(Resource):
    def __init__(self):
        self.driver = utils.get_driver()

    def post(self, topic):
        # this is quite general we expect the sender we put the data in the body
        # like binary data, if the data are passed with as form-data the message
        # will report details about the content-disposition
        message = request.get_data()
        ret_value = self.driver.publish(topic, message)
        if ret_value == 500:
            return utils.server_error()

        return "Publish succeeded"
