from flask import request
from flask_restful import Resource

from apimes import utils

class Message(Resource):
    def __init__(self):
        self.driver = utils.get_driver()

    def post(self, topic):
        if not utils.is_valid_name(topic):
            msg = "Invalid topic name. Topic name can have just digit, " \
                  "letters, hyphen, underscore, period, colon and the " \
                  "total max length is equal to 255"
            return msg, 400

        # we expect the sender to put the data in the body
        # like binary data, if the data are passed with as form-data
        # the message will report details about the content-disposition
        message = request.get_data()
        ret_value = self.driver.publish(topic, message)
        if ret_value == 500:
            return utils.server_error()

        return "Publish succeeded"
