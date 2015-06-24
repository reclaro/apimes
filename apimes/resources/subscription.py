from flask_restful import Resource

from apimes import exceptions
from apimes import utils
from apimes.resources.driver import Driver

class Subscription(Resource):
    def __init__(self):
        self.driver = utils.get_driver()

    def post(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        if not q_name:
            err_msg = "Topic and username can have just digit, letters," \
                      " hyphen, underscore, period, colon and the total max" \
                      " length is equal to 255"
            return err_msg, 400

        ret_value = self.driver.subscribe(topic, q_name)

        if ret_value == 500:
            return utils.server_error()

        #TODO: Log the message
        msg = ("user %s has successfully subscribed to the %s topic" %
               (username, topic))
        return "Subscription succeeded"

    def delete(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        ret_value = self.driver.unsubscribe(topic, q_name)
        if isinstance(ret_value, exceptions.InvalidSubscription):
            return "The subscription does not exist", 404

        if ret_value == 500:
            return utils.server_error()

        #LOG "Unsubscribe succeeded"

    def get(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        ret_value = self.driver.get_message(topic, q_name)
        if not ret_value:
            #TODO LOG "There are no message available for this topic on this user"
            return None, 204

        if isinstance(ret_value, exceptions.InvalidSubscription):
            return "The subscription does not exist", 404

        if ret_value == 500:
            return utils.server_error()

        return ret_value
