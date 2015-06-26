import logging

from flask import request
from flask_restful import Resource

from apimes import utils


LOG = logging.getLogger(__name__)


class Message(Resource):
    def __init__(self):
        self.driver = utils.get_driver()

    def post(self, topic):
        if not utils.is_valid_name(topic):
            msg = "Invalid topic name. Topic name can have just digit, " \
                  "letters, hyphen, underscore, period, colon and the " \
                  "total max length is equal to 255"
            LOG.error(msg)
            return msg, 400

        # we expect the sender to put the data in the body
        # like binary data, if the data are passed with as form-data
        # the message will report details about the content-disposition
        message = request.get_data()
        LOG.debug("message to send %s" % message)
        ret_value = self.driver.publish(topic, message)
        if ret_value == 500:
            LOG.error("Server error")
            return utils.server_error()

        LOG.debug("Message sent")
        return "Publish succeeded"
