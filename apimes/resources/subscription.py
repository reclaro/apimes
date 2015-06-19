from flask_restful import Resource

from apimes import exceptions
from apimes import utils
from apimes.resources.driver import Driver

class Subscription(Resource):
    def __init__(self):
        self.driver = utils.get_driver()

    def post(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        self.driver.subscribe(topic, q_name)
        msg = ("user %s has successfully subscribed to the %s topic" %
               (username, topic))
        #TODO: Log the message
        #TODO return the response code + the simple message
        return "Subscription succeeded"

    def delete(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        #try:
        ret_value = self.driver.unsubscribe(topic, q_name)
        if isinstance(ret_value, exceptions.InvalidSubscription):
            return "The subscription does not exist", 404

        #return "Unsubscribe succeeded"

    def get(self, topic, username):
        q_name = utils.get_queue_name(topic, username)
        #decorated = utils.can_raise_channel_error(self.driver.get_message)
        #msg = decorated(topic, q_name)
        ret_value = self.driver.get_message(topic, q_name)

        if isinstance(ret_value, exceptions.InvalidSubscription):
            return "The subscription does not exist", 404

        if not ret_value:
            # TODO check how to return just the return value without string!!
            return "", 204
            return "There are no message available for this topic on this user", 204

        return ret_value
