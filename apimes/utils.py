from ConfigParser import SafeConfigParser
from functools import wraps

from stevedore import driver

from apimes import exceptions
from amqp.exceptions import ChannelError

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

def get_driver():
    config = SafeConfigParser()
    config.read("apimes.conf")
    driver_name = config.get('default', 'driver')
    mgr = driver.DriverManager(
                namespace='apimes.plugin',
                name=driver_name,
                invoke_on_load=True,
              )
    return mgr.driver
