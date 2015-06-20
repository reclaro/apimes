from ConfigParser import SafeConfigParser
from functools import wraps
from re import search
from socket import error as conn_error

from stevedore import driver

from apimes import exceptions
from amqp.exceptions import ChannelError

def can_raise_amqp_error(func):
    @wraps(func)
    def manage_exception(self, topic, q_name):
        try:
            func(self, topic, q_name)
        except ChannelError as channel_ex:
            #log error
            return exceptions.InvalidSubscription()
        except conn_error:
            return 500

    return manage_exception

def get_queue_name(topic, username):
    # we allow just digit, letters, hyphen, undrescore, period, colon for
    # max lenght of 256
    pattern = "^[\.\w:-]{1,255}$"
    queue_name = username + '_'  + topic
    if search(pattern, queue_name):
        return queue_name

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

def server_error():
    return "Sorry the server can't perform your request", 500


