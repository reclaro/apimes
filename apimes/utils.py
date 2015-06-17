from functools import wraps

from amqp.exceptions import ChannelError
from apimes import exceptions

def can_raise_channel_error(func):
    @wraps(func)
    def manage_exception(self, topic, q_name):
        try:
            func(self, topic, q_name)
        except ChannelError as channel_ex:
            #log error
            return exceptions.InvalidSubscription()
    return manage_exception

def get_queue_name(topic, username):
    #TODO validate topic and username accetta tutto lo trasformi in base alle regole di RMQ
    return username + '_' + topic

